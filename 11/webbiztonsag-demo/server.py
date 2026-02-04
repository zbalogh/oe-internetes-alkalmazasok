#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Webbiztonság demo (XSS / CSRF / CORS) – oktatási célra

Két mini szerver indul:
  * App szerver:  http://localhost:8000
  * Evil szerver: http://127.0.0.1:8001  (más origin → CORS/CSRF szemléltetéshez)

Indítás:
  python server.py

Leállítás:
  CTRL+C
"""
from __future__ import annotations

import html
import json
import secrets
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Egyszerű (oktatási) session tároló memóriában.
# Valódi rendszernél ez adatbázis/redis/keretrendszer session.
SESSIONS: dict[str, dict] = {}

APP_HOST = "localhost"
APP_PORT = 8000
EVIL_HOST = "127.0.0.1"
EVIL_PORT = 8001


def get_cookie(header: str | None, name: str) -> str | None:
    if not header:
        return None
    parts = header.split(";")
    for p in parts:
        p = p.strip()
        if "=" in p:
            k, v = p.split("=", 1)
            if k.strip() == name:
                return v.strip()
    return None


def make_session() -> tuple[str, dict]:
    sid = secrets.token_urlsafe(16)
    SESSIONS[sid] = {}
    return sid, SESSIONS[sid]


def clamp_int(value: str, default: int, min_v: int, max_v: int) -> int:
    try:
        n = int(value)
    except Exception:
        return default
    return max(min_v, min(max_v, n))


def session_cookie_header(sid: str, mode: str) -> str:
    """
    Session cookie flag-ek demonstrációhoz.

    Megjegyzés:
      - SameSite=None esetén a modern böngészők Secure-t várnak (HTTPS).
        Mivel ez a demo HTTP-n fut, a böngésző eldobhatja / ignorálhatja a cookie-t.
    """
    mode = (mode or "lax").lower()
    if mode not in ("lax", "strict", "none"):
        mode = "lax"

    flags = "Path=/; HttpOnly; "
    if mode == "none":
        flags += "SameSite=None; Secure"
    elif mode == "strict":
        flags += "SameSite=Strict"
    else:
        flags += "SameSite=Lax"
    return f"sessionid={sid}; {flags}"


class AppHandler(BaseHTTPRequestHandler):
    server_version = "WebBiztApp/2.0"

    def _send(
        self,
        status: int,
        body: str,
        content_type: str = "text/html; charset=utf-8",
        headers: list[tuple[str, str]] | None = None,
    ):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        if headers:
            for k, v in headers:
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def _get_session(self) -> tuple[str, dict, bool]:
        cookie = self.headers.get("Cookie")
        sid = get_cookie(cookie, "sessionid")
        if sid and sid in SESSIONS:
            return sid, SESSIONS[sid], False
        sid, sess = make_session()
        return sid, sess, True

    def _html_page(self, title: str, content: str):
        return f"""<!doctype html>
<html lang="hu">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; background: #f7f7f7; }}
    code {{ background:#eee; padding:2px 4px; border-radius:4px; }}
    a {{ color: #0b57d0; text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}
    .row {{ display:flex; gap:12px; flex-wrap:wrap; }}
    .card {{ background:white; border:1px solid #ddd; border-radius:12px; padding:16px; flex: 1 1 320px; }}
    .warn {{ background:#fff4e5; border:1px solid #ffd29e; padding:12px; border-radius:12px; }}
    .ok {{ background:#e7f6ec; border:1px solid #a9e2bb; padding:12px; border-radius:12px; }}
    .button {{ display:inline-block; padding:8px 12px; background:#0b57d0; color:white; border-radius:10px; }}
    .button:hover {{ filter: brightness(0.95); text-decoration:none; }}
    .muted {{ color:#666; }}
    input {{ padding:6px 8px; border-radius:8px; border:1px solid #ccc; }}
    button {{ padding:8px 12px; border-radius:10px; border:1px solid #ccc; cursor:pointer; }}
    hr {{ border:0; border-top:1px solid #ddd; margin: 16px 0; }}
    .kpi {{ display:flex; gap:12px; flex-wrap:wrap; }}
    .kpi > div {{ background:#fafafa; border:1px solid #eee; padding:10px 12px; border-radius:12px; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  {content}
  <hr/>
  <p><a href="/">Vissza a főoldalra</a></p>
</body>
</html>"""

    def _require_login(self, sess: dict) -> tuple[bool, str]:
        if sess.get("logged_in") is True:
            return True, ""
        return False, "Nem vagy bejelentkezve. Nyisd meg az <a href='/account'>Account</a> oldalt és jelentkezz be."

    def _ensure_defaults(self, sess: dict):
        sess.setdefault("samesite", "lax")
        # oktatási "account" állapot
        sess.setdefault("logged_in", False)
        sess.setdefault("user", "student")
        sess.setdefault("balance", 10000)
        sess.setdefault("last_action", "—")

    def do_GET(self):
        sid, sess, is_new = self._get_session()
        self._ensure_defaults(sess)

        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query or "")

        set_cookie_headers: list[tuple[str, str]] = []
        if is_new:
            set_cookie_headers.append(("Set-Cookie", session_cookie_header(sid, sess["samesite"])))

        # ---- Home ----
        if path == "/":
            body = self._html_page(
                "Webbiztonság demo – főoldal",
                f"""
<p>Ez a mini demo két origin-t használ:</p>
<ul>
  <li><b>App</b>: <code>http://{APP_HOST}:{APP_PORT}</code></li>
  <li><b>Evil</b>: <code>http://{EVIL_HOST}:{EVIL_PORT}</code> (külön origin a CORS/CSRF szemléltetéshez)</li>
</ul>

<div class="row">
  <div class="card">
    <h2>Account / CSRF környezet</h2>
    <p>Bejelentkezés + session cookie SameSite állítása.</p>
    <p><a class="button" href="/account">Account oldal</a></p>
  </div>

  <div class="card">
    <h2>XSS demo</h2>
    <ul>
      <li><a href="/xss-unsafe">1) Unsafe megjelenítés (sebezhető)</a></li>
      <li><a href="/xss-safe">2) Safe megjelenítés (escape)</a></li>
    </ul>
  </div>

  <div class="card">
    <h2>CSRF demo</h2>
    <ul>
      <li><a href="/csrf-vulnerable">CSRF-vulnerable műveletek</a></li>
      <li><a href="/csrf-protected">CSRF-protected művelet (token)</a></li>
      <li><a href="http://{EVIL_HOST}:{EVIL_PORT}/csrf-attack.html" target="_blank">Evil oldal (CSRF támadások)</a></li>
    </ul>
  </div>

  <div class="card">
    <h2>CORS demo</h2>
    <ul>
      <li><a href="/cors-demo">CORS teszt oldal (fetch)</a></li>
      <li><a href="http://{EVIL_HOST}:{EVIL_PORT}/cors-evil.html" target="_blank">Evil origin CORS teszt</a></li>
    </ul>
  </div>
</div>

<div class="warn">
<b>Megjegyzés:</b> A CSRF résznél direkt van egy “rossz gyakorlat” is: <b>GET</b>-tel állapotváltoztatás, hogy SameSite=Lax vs Strict különbség jól demonstrálható legyen.
</div>
""",
            )
            self._send(200, body, headers=set_cookie_headers)
            return

        # ---- Account ----
        if path == "/account":
            logged = "IGEN" if sess.get("logged_in") else "NEM"
            ss = html.escape(sess.get("samesite", "lax"))
            body = self._html_page(
                "Account",
                f"""
<div class="kpi">
  <div><b>User:</b> {html.escape(sess.get("user","student"))}</div>
  <div><b>Logged in:</b> {logged}</div>
  <div><b>Balance:</b> {int(sess.get("balance", 0))} Ft</div>
  <div><b>Session SameSite:</b> <code>{ss}</code></div>
</div>

<p class="muted">Last action: {html.escape(str(sess.get("last_action","—")))}</p>

<div class="row">
  <div class="card">
    <h3>1) Login state</h3>
    <form method="POST" action="/do-login">
      <button type="submit">Bejelentkezés</button>
    </form>
    <form method="POST" action="/do-logout" style="margin-top:8px">
      <button type="submit">Kijelentkezés</button>
    </form>
  </div>

  <div class="card">
    <h3>2) Session cookie SameSite beállítás</h3>
    <p>A CSRF demo ezt a <b>sessionid</b> cookie-t használja. Állítsd át és figyeld meg DevTools-ban.</p>
    <p>
      <a class="button" href="/set-session-samesite?mode=lax">SameSite=Lax</a>
      <a class="button" href="/set-session-samesite?mode=strict">SameSite=Strict</a>
      <a class="button" href="/set-session-samesite?mode=none">SameSite=None (+Secure)</a>
    </p>
    <div class="warn">
      <b>Fontos:</b> <code>SameSite=None</code> esetén a modern böngészők HTTPS+Secure-t várnak.
      Mivel a demo HTTP-n fut, lehet, hogy a böngésző <i>eldobja</i> a cookie-t.
    </div>
  </div>
</div>

<div class="card">
  <h3>3) Teszt linkek</h3>
  <ul>
    <li><a href="/csrf-vulnerable">CSRF-vulnerable műveletek (app oldalon)</a></li>
    <li><a href="/csrf-protected">CSRF-protected művelet (CSRF token)</a></li>
    <li><a href="http://{EVIL_HOST}:{EVIL_PORT}/csrf-attack.html" target="_blank">Evil oldal (CSRF támadások)</a></li>
  </ul>
</div>
""",
            )
            self._send(200, body, headers=set_cookie_headers)
            return

        if path == "/set-session-samesite":
            mode = (qs.get("mode") or ["lax"])[0].lower()
            if mode not in ("lax", "strict", "none"):
                mode = "lax"
            sess["samesite"] = mode
            # ugyanazzal a sid-del újra-kiküldjük a session cookie-t friss flag-ekkel
            headers = set_cookie_headers + [
                ("Set-Cookie", session_cookie_header(sid, mode)),
                ("Location", "/account"),
            ]
            self.send_response(302)
            for k, v in headers:
                self.send_header(k, v)
            self.end_headers()
            return

        # ---- XSS demo ----
        if path == "/xss-unsafe":
            msg = (qs.get("msg") or [""])[0]
            body = self._html_page(
                "XSS – Unsafe megjelenítés",
                f"""
<p>Itt az input <b>escape nélkül</b> kerül vissza az oldalba (sebezhető minta).</p>
<div class="card">
  <form method="GET" action="/xss-unsafe">
    <label>Írd be az üzenetet:
      <input name="msg" style="width:320px" value="{html.escape(msg)}"/>
    </label>
    <button type="submit">Megjelenít</button>
  </form>
</div>

<div class="card">
  <h3>Eredmény (veszélyes):</h3>
  <div class="warn">{msg}</div>
</div>

<p class="warn"><b>Figyeld meg:</b> próbáld ezt: <code>&lt;img src=x onerror=alert(1)&gt;</code></p>
""",
            )
            self._send(200, body, headers=set_cookie_headers)
            return

        if path == "/xss-safe":
            msg = (qs.get("msg") or [""])[0]
            body = self._html_page(
                "XSS – Safe megjelenítés (escape)",
                f"""
<p>Itt az input <b>escape-elve</b> kerül vissza az oldalba.</p>
<div class="card">
  <form method="GET" action="/xss-safe">
    <label>Írd be az üzenetet:
      <input name="msg" style="width:320px" value="{html.escape(msg)}"/>
    </label>
    <button type="submit">Megjelenít</button>
  </form>
</div>

<div class="card">
  <h3>Eredmény (biztonságosabb):</h3>
  <div class="ok">{html.escape(msg)}</div>
</div>
""",
            )
            self._send(200, body, headers=set_cookie_headers)
            return

        # ---- CSRF demo pages ----
        if path == "/csrf-vulnerable":
            ok, msg = self._require_login(sess)
            login_notice = (
                f"<div class='warn'><b>FIGYELEM:</b> {msg}</div>"
                if not ok
                else "<div class='ok'><b>OK:</b> Be vagy jelentkezve, a session cookie alapján azonosítunk.</div>"
            )
            body = self._html_page(
                "CSRF – sebezhető műveletek",
                f"""
{login_notice}

<div class="row">
  <div class="card">
    <h3>1) SEBEZHETŐ: állapotváltozás GET-tel</h3>
    <p class="warn">
      Rossz gyakorlat: <b>GET</b> kérés állapotot változtat (átutal).
      Ez kiválóan demonstrálja, hogy <b>SameSite=Lax</b> mellett egy <b>top-level link kattintás</b> gyakran viszi a cookie-t.
    </p>
    <p>
      <a class="button" href="/do-transfer-vuln-get?amount=1000">Átutalás GET-tel (sebezhető)</a>
    </p>
  </div>

  <div class="card">
    <h3>2) SEBEZHETŐ: POST token nélkül</h3>
    <p>Ez a klasszikus “nincs CSRF token” minta. (A cookie-küldés böngésző/SameSite függő.)</p>
    <form method="POST" action="/do-transfer-vuln">
      <label>Összeg (Ft): <input name="amount" value="1000"/></label><br/><br/>
      <button type="submit">Átutalás POST-tal (sebezhető)</button>
    </form>
  </div>
</div>

<div class="warn">
<b>Megjegyzés:</b>
<ol>
  <li>Menj <a href="/account">Account</a> → jelentkezz be.</li>
  <li>Állítsd a session cookie SameSite módját <b>Lax</b>-ra.</li>
  <li>Nyisd meg az <b>Evil</b> oldalt és indítsd a “GET link” támadást → tipikusan <b>sikerül</b>.</li>
  <li>Állítsd <b>Strict</b>-re → ugyanaz a támadás tipikusan <b>elbukik</b> (nincs cookie → nincs login).</li>
</ol>
</div>
""",
            )
            self._send(200, body, headers=set_cookie_headers)
            return

        if path == "/csrf-protected":
            ok, msg = self._require_login(sess)
            if not ok:
                body = self._html_page("CSRF – védett művelet (token)", f"<div class='warn'>{msg}</div>")
                self._send(401, body, headers=set_cookie_headers)
                return

            if "csrf_token" not in sess:
                sess["csrf_token"] = secrets.token_urlsafe(16)
            token = sess["csrf_token"]
            body = self._html_page(
                "CSRF – védett művelet (token)",
                f"""
<div class="ok"><b>OK:</b> Be vagy jelentkezve. A művelet CSRF tokent vár.</div>

<div class="card">
  <form method="POST" action="/do-transfer-safe">
    <label>Összeg (Ft): <input name="amount" value="1000"/></label>
    <input type="hidden" name="csrf_token" value="{html.escape(token)}"/>
    <br/><br/>
    <button type="submit">Átutalás (védett)</button>
  </form>
</div>

<p class="warn"><b>Tanulság:</b> A támadó oldal tipikusan nem tudja kiolvasni ezt a tokent (SOP miatt), ezért token nélkül elutasítjuk.</p>
""",
            )
            self._send(200, body, headers=set_cookie_headers)
            return

        # ---- CORS demo ----
        if path == "/cors-demo":
            body = self._html_page(
                "CORS – fetch teszt",
                f"""
<p>Nyisd meg a DevTools-t: <b>F12</b> → <b>Console</b>.</p>
<p>Két kérés:</p>
<ul>
  <li><b>Blocked</b>: nincs <code>Access-Control-Allow-Origin</code> fejléc</li>
  <li><b>Allowed</b>: van <code>Access-Control-Allow-Origin: *</code></li>
</ul>

<div class="card">
  <button onclick="testBlocked()">Fetch blocked (másik origin)</button>
  <button onclick="testAllowed()">Fetch allowed (CORS engedélyezett)</button>
  <pre id="out"></pre>
</div>

<script>
async function testBlocked() {{
  const out = document.getElementById('out');
  out.textContent = 'blocked... nézd a Console-t';
  try {{
    const r = await fetch('http://{EVIL_HOST}:{EVIL_PORT}/api/no-cors');
    const j = await r.json();
    out.textContent = JSON.stringify(j, null, 2);
  }} catch (e) {{
    out.textContent = 'HIBA (várható): ' + e;
  }}
}}

async function testAllowed() {{
  const out = document.getElementById('out');
  out.textContent = 'allowed...';
  try {{
    const r = await fetch('http://{EVIL_HOST}:{EVIL_PORT}/api/with-cors');
    const j = await r.json();
    out.textContent = JSON.stringify(j, null, 2);
  }} catch (e) {{
    out.textContent = 'HIBA (nem várt): ' + e;
  }}
}}
</script>
""",
            )
            self._send(200, body, headers=set_cookie_headers)
            return

        # ---- "API" endpoints for CORS demo ----
        if path == "/api/private":
            # Ez csak az app originről legyen olvasható (nincs CORS header)
            body = json.dumps({"ok": True, "secret": "TOP-SECRET (csak same-origin olvasás)"} )
            self._send(200, body, "application/json; charset=utf-8", headers=set_cookie_headers)
            return

        # ---- VULN: GET state-change endpoint (CSRF-hez) ----
        if path == "/do-transfer-vuln-get":
            ok, msg = self._require_login(sess)
            if not ok:
                body = self._html_page("Transfer (GET) – elutasítva", f"<div class='warn'>{msg}</div>")
                self._send(401, body, headers=set_cookie_headers)
                return

            amount = clamp_int((qs.get("amount") or ["1000"])[0], 1000, 1, 1000000)
            sess["balance"] = max(0, int(sess.get("balance", 0)) - amount)
            sess["last_action"] = f"VULN GET transfer: -{amount} Ft"
            body = self._html_page(
                "Transfer (GET) – sebezhető",
                f"""
<div class="warn">
<b>SEBEZHETŐ:</b> GET kérés állapotot változtatott (átutalás).
</div>
<p>Átutalva: <b>{amount} Ft</b></p>
<p>Új egyenleg: <b>{int(sess.get("balance", 0))} Ft</b></p>
<p class="muted">Próbáld ezt az evil oldalról is, és variáld a SameSite módot.</p>
""",
            )
            self._send(200, body, headers=set_cookie_headers)
            return

        # default 404
        self._send(404, self._html_page("404", "<p>Nincs ilyen oldal.</p>"), headers=set_cookie_headers)

    def do_POST(self):
        sid, sess, is_new = self._get_session()
        self._ensure_defaults(sess)

        set_cookie_headers: list[tuple[str, str]] = []
        if is_new:
            set_cookie_headers.append(("Set-Cookie", session_cookie_header(sid, sess["samesite"])))

        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        form = parse_qs(raw)

        path = urlparse(self.path).path

        if path == "/do-login":
            sess["logged_in"] = True
            sess["last_action"] = "Login"
            # CSRF token újragenerálása login után
            sess["csrf_token"] = secrets.token_urlsafe(16)
            headers = set_cookie_headers + [("Location", "/account")]
            self.send_response(302)
            for k, v in headers:
                self.send_header(k, v)
            self.end_headers()
            return

        if path == "/do-logout":
            sess["logged_in"] = False
            sess["last_action"] = "Logout"
            headers = set_cookie_headers + [("Location", "/account")]
            self.send_response(302)
            for k, v in headers:
                self.send_header(k, v)
            self.end_headers()
            return

        if path == "/do-transfer-vuln":
            ok, msg = self._require_login(sess)
            if not ok:
                body = self._html_page("Transfer (POST) – elutasítva", f"<div class='warn'>{msg}</div>")
                self._send(401, body, headers=set_cookie_headers)
                return

            amount = clamp_int((form.get("amount") or ["1000"])[0], 1000, 1, 1000000)
            sess["balance"] = max(0, int(sess.get("balance", 0)) - amount)
            sess["last_action"] = f"VULN POST transfer: -{amount} Ft (NO CSRF TOKEN)"
            body = self._html_page(
                "Transfer (POST) – sebezhető",
                f"""
<div class="warn"><b>SEBEZHETŐ:</b> Nem volt CSRF token ellenőrzés.</div>
<p>Átutalva: <b>{amount} Ft</b></p>
<p>Új egyenleg: <b>{int(sess.get("balance", 0))} Ft</b></p>
<p class="muted">Megjegyzés: hogy ezt evil originről cookie-val is elküldje a böngésző, az SameSite/HTTPS függő.</p>
""",
            )
            self._send(200, body, headers=set_cookie_headers)
            return

        if path == "/do-transfer-safe":
            ok, msg = self._require_login(sess)
            if not ok:
                body = self._html_page("Transfer (SAFE) – elutasítva", f"<div class='warn'>{msg}</div>")
                self._send(401, body, headers=set_cookie_headers)
                return

            token = (form.get("csrf_token") or [""])[0]
            if not token or token != sess.get("csrf_token"):
                body = self._html_page(
                    "Transfer (SAFE) – elutasítva",
                    """
<div class="warn">
<b>ELUTASÍTVA:</b> Hibás vagy hiányzó CSRF token.
</div>
<p>Ez a várt viselkedés: a támadó oldal nem tud érvényes tokent küldeni.</p>
""",
                )
                self._send(403, body, headers=set_cookie_headers)
                return

            amount = clamp_int((form.get("amount") or ["1000"])[0], 1000, 1, 1000000)
            sess["balance"] = max(0, int(sess.get("balance", 0)) - amount)
            sess["last_action"] = f"SAFE transfer: -{amount} Ft (CSRF token OK)"
            body = self._html_page(
                "Transfer (SAFE) – siker",
                f"""
<div class="ok"><b>Siker:</b> CSRF token ellenőrzés OK.</div>
<p>Átutalva: <b>{amount} Ft</b></p>
<p>Új egyenleg: <b>{int(sess.get("balance", 0))} Ft</b></p>
""",
            )
            self._send(200, body, headers=set_cookie_headers)
            return

        self._send(404, self._html_page("404", "<p>Nincs ilyen endpoint.</p>"), headers=set_cookie_headers)


class EvilHandler(BaseHTTPRequestHandler):
    server_version = "WebBiztEvil/2.0"

    def _send(
        self,
        status: int,
        body: str,
        content_type: str = "text/html; charset=utf-8",
        headers: list[tuple[str, str]] | None = None,
    ):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        if headers:
            for k, v in headers:
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            self._send(
                200,
                """<!doctype html><meta charset="utf-8">
<h1>Evil origin</h1>
<ul>
  <li><a href="/cors-evil.html">CORS evil oldal</a></li>
  <li><a href="/csrf-attack.html">CSRF attack oldal</a></li>
</ul>
<p><i>Megjegyzés:</i> Ez egy külön origin (8001), hogy cross-site kéréseket indítsunk.</p>
""",
            )
            return

        if path == "/cors-evil.html":
            self._send(
                200,
                f"""<!doctype html>
<html lang="hu"><head><meta charset="utf-8"><title>CORS evil</title></head>
<body style="font-family:Arial;margin:24px">
<h1>CORS – evil origin oldal</h1>
<p>Ez az oldal <b>más origin</b> ({EVIL_HOST}:{EVIL_PORT}), és megpróbál adatot olvasni az appból ({APP_HOST}:{APP_PORT}).</p>
<button onclick="tryRead()">Próbálj olvasni az app API-ból</button>
<pre id="out"></pre>
<script>
async function tryRead() {{
  const out = document.getElementById('out');
  out.textContent = 'fetch http://{APP_HOST}:{APP_PORT}/api/private ... (nézd a Console-t)';
  try {{
    const r = await fetch('http://{APP_HOST}:{APP_PORT}/api/private');
    const j = await r.json();
    out.textContent = JSON.stringify(j, null, 2);
  }} catch (e) {{
    out.textContent = 'HIBA (várható CORS): ' + e;
  }}
}}
</script>
</body></html>
""",
            )
            return

        if path == "/csrf-attack.html":
            self._send(
                200,
                f"""<!doctype html>
<html lang="hu"><head><meta charset="utf-8"><title>CSRF evil</title></head>
<body style="font-family:Arial;margin:24px">
<h1>CSRF – evil origin oldal</h1>

<p>
<b>Előfeltétel:</b> az app oldalon jelentkezz be: <a href="http://{APP_HOST}:{APP_PORT}/account" target="_blank">Account</a>.
Ott állítsd a <b>session SameSite</b> módot <b>Lax</b>-ra vagy <b>Strict</b>-re.
</p>

<div style="border:1px solid #ddd;border-radius:10px;padding:16px;margin:12px 0">
  <h3>1) CSRF “sikerül” (jellemzően) – GET link (rossz gyakorlat)</h3>
  <p>
    Ez egy <b>top-level navigáció</b> (link kattintás) az appba.
    <br/>SameSite=<b>Lax</b> esetén a cookie <i>gyakran</i> elküldésre kerül → a transfer megtörténhet.
    <br/>SameSite=<b>Strict</b> esetén a cookie tipikusan <i>nem</i> megy → a szerver “nem vagy bejelentkezve” hibát ad.
  </p>
  <p>
    <a style="display:inline-block;padding:8px 12px;background:#d93025;color:white;border-radius:10px;text-decoration:none"
       href="http://{APP_HOST}:{APP_PORT}/do-transfer-vuln-get?amount=9999">Kattints a CSRF GET támadáshoz</a>
  </p>
</div>

<div style="border:1px solid #ddd;border-radius:10px;padding:16px;margin:12px 0">
  <h3>2) POST támadás token nélküli (sebezhető) endpoint ellen</h3>
  <p>
    Ez a klasszikus CSRF minta (rejtett form submit).
    Hogy a böngésző elküldi-e a session cookie-t cross-site POST-ban,
    az <b>SameSite</b> és <b>HTTPS</b> függő (None+Secure tipikusan kell).
  </p>
  <form id="f1" method="POST" action="http://{APP_HOST}:{APP_PORT}/do-transfer-vuln">
    <input type="hidden" name="amount" value="9999">
  </form>
  <button onclick="document.getElementById('f1').submit()">Küldés (vulnerable POST)</button>
</div>

<div style="border:1px solid #ddd;border-radius:10px;padding:16px;margin:12px 0">
  <h3>3) POST támadás a védett végpontra (token nélkül) – elbukik</h3>
  <form id="f2" method="POST" action="http://{APP_HOST}:{APP_PORT}/do-transfer-safe">
    <input type="hidden" name="amount" value="9999">
    <input type="hidden" name="csrf_token" value="nincs-token">
  </form>
  <button onclick="document.getElementById('f2').submit()">Küldés (protected)</button>
</div>

</body></html>
""",
            )
            return

        if path == "/api/no-cors":
            self._send(200, json.dumps({"msg": "no CORS headers here"}), "application/json; charset=utf-8")
            return

        if path == "/api/with-cors":
            self._send(
                200,
                json.dumps({"msg": "CORS allowed (ACAO: *)"}),
                "application/json; charset=utf-8",
                headers=[("Access-Control-Allow-Origin", "*")],
            )
            return

        self._send(404, "not found", "text/plain; charset=utf-8")


def run_server(host: str, port: int, handler):
    httpd = HTTPServer((host, port), handler)
    print(f"Serving on http://{host}:{port} ({handler.__name__})")
    httpd.serve_forever()


def main():
    t1 = threading.Thread(target=run_server, args=(APP_HOST, APP_PORT, AppHandler), daemon=True)
    t2 = threading.Thread(target=run_server, args=(EVIL_HOST, EVIL_PORT, EvilHandler), daemon=True)
    t1.start()
    t2.start()

    print("\nNyisd meg:")
    print(f"  App:  http://{APP_HOST}:{APP_PORT}/")
    print(f"  Evil: http://{EVIL_HOST}:{EVIL_PORT}/\n")

    # main thread idle
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\nBye.")


if __name__ == "__main__":
    main()
