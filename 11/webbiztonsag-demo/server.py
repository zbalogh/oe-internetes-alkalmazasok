#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Webbiztonság demo

Két mini szerver indul:
  * App szerver:  http://localhost:8000
  * Evil szerver: http://localhost:8001  (más origin → CORS/CSRF szemléltetéshez)

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

APP_HOST = "127.0.0.1"
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

class AppHandler(BaseHTTPRequestHandler):
    server_version = "WebBiztApp/1.0"

    def _send(self, status: int, body: str, content_type: str = "text/html; charset=utf-8", headers: list[tuple[str,str]] | None = None):
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

    def _html_page(self, title: str, content: str) -> str:
        return f"""<!doctype html>
<html lang="hu">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; line-height: 1.45; }}
    code, pre {{ background:#f4f4f4; padding:2px 4px; border-radius:4px; }}
    pre {{ padding:12px; overflow:auto; }}
    .card {{ border:1px solid #ddd; border-radius:10px; padding:16px; margin:12px 0; }}
    .row {{ display:flex; gap:12px; flex-wrap:wrap; }}
    .row .card {{ flex: 1 1 360px; }}
    a.button {{ display:inline-block; padding:8px 12px; border:1px solid #444; border-radius:8px; text-decoration:none; color:#111; }}
    .warn {{ background:#fff3cd; border:1px solid #ffeeba; padding:10px; border-radius:8px; }}
    .ok {{ background:#e6ffed; border:1px solid #b7f5c7; padding:10px; border-radius:8px; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  {content}
  <hr/>
  <p><a href="/">Vissza a főoldalra</a></p>
</body>
</html>"""

    def do_GET(self):
        sid, sess, is_new = self._get_session()
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query or "")

        set_cookie_headers = []
        if is_new:
            # Oktatási session cookie: HttpOnly + SameSite=Lax (klasszikus alap)
            set_cookie_headers.append(("Set-Cookie", f"sessionid={sid}; Path=/; HttpOnly; SameSite=Lax"))

        if path == "/":
            body = self._html_page("Webbiztonság demo – főoldal", f"""
<p>Ez a mini demo két origin-t használ:</p>
<ul>
  <li><b>App</b>: <code>http://localhost:{APP_PORT}</code></li>
  <li><b>Evil</b>: <code>http://localhost:{EVIL_PORT}</code> (külön origin a CORS/CSRF szemléltetéshez)</li>
</ul>

<div class="row">
  <div class="card">
    <h2>XSS demo</h2>
    <ul>
      <li><a href="/xss-unsafe">1) Unsafe megjelenítés (sebezhető)</a></li>
      <li><a href="/xss-safe">2) Safe megjelenítés (escape)</a></li>
    </ul>
  </div>
  <div class="card">
    <h2>Cookie flag demo</h2>
    <ul>
      <li><a href="/cookies">Cookie-k megtekintése + beállítások</a></li>
    </ul>
  </div>
  <div class="card">
    <h2>CSRF demo</h2>
    <ul>
      <li><a href="/csrf-vulnerable">CSRF-vulnerable művelet (nincs token)</a></li>
      <li><a href="/csrf-protected">CSRF-protected művelet (token)</a></li>
      <li><a href="http://localhost:{EVIL_PORT}/csrf-attack.html" target="_blank">Evil oldal (CSRF próbálkozás)</a></li>
    </ul>
  </div>
  <div class="card">
    <h2>CORS demo</h2>
    <ul>
      <li><a href="/cors-demo">CORS teszt oldal (fetch)</a></li>
      <li><a href="http://localhost:{EVIL_PORT}/cors-evil.html" target="_blank">Evil origin CORS teszt</a></li>
    </ul>
  </div>
</div>

<div class="warn">
<b>Megjegyzés:</b> A demo oktatási célú. Valódi védelmi mechanizmusok (CSP, templating, framework beállítások) itt nincsenek teljesen kidolgozva.
</div>
""")
            self._send(200, body, headers=set_cookie_headers)
            return

        if path == "/xss-unsafe":
            msg = (qs.get("msg") or [""])[0]
            body = self._html_page("XSS – Unsafe megjelenítés", f"""
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

<p class="warn"><b>Figyelem:</b> Ne futtassatok kártékony kódot. Itt elég megfigyelni, hogy a böngésző <i>értelmezni próbálja</i> a beillesztett tartalmat.</p>
""")
            self._send(200, body, headers=set_cookie_headers)
            return

        if path == "/xss-safe":
            msg = (qs.get("msg") or [""])[0]
            safe = html.escape(msg)
            body = self._html_page("XSS – Safe megjelenítés (escaping)", f"""
<p>Itt az input <b>HTML escapinggel</b> kerül vissza az oldalba (biztonságosabb minta).</p>
<div class="card">
  <form method="GET" action="/xss-safe">
    <label>Írd be az üzenetet:
      <input name="msg" style="width:320px" value="{html.escape(msg)}"/>
    </label>
    <button type="submit">Megjelenít</button>
  </form>
</div>

<div class="card">
  <h3>Eredmény (escape-elve):</h3>
  <div class="ok">{safe}</div>
</div>

<p><b>Tanulság:</b> ugyanazt a beírt szöveget a böngésző már nem HTML-ként értelmezi, hanem szövegként jeleníti meg.</p>
""")
            self._send(200, body, headers=set_cookie_headers)
            return

        if path == "/cookies":
            body = self._html_page("Cookie flag-ek megfigyelése", f"""
<p>Nyisd meg a DevTools-t: <b>F12</b> → <b>Application/Storage</b> → <b>Cookies</b>.</p>
<p>Itt állíthatsz be oktatási célú cookie-kat különböző flag-ekkel:</p>

<div class="row">
  <div class="card">
    <h3>SameSite=Lax (alap)</h3>
    <p>Jó default sok webappnál (CSRF kockázat csökkentése).</p>
    <a class="button" href="/set-cookie?mode=lax">Beállít</a>
  </div>
  <div class="card">
    <h3>SameSite=Strict</h3>
    <p>Még szigorúbb – néha UX problémát okozhat (pl. külső linkek).</p>
    <a class="button" href="/set-cookie?mode=strict">Beállít</a>
  </div>
  <div class="card">
    <h3>SameSite=None (+Secure)</h3>
    <p>Cross-site használathoz kell (pl. SSO/3rd-party). HTTPS nélkül a böngésző gyakran eldobja a cookie-t.</p>
    <a class="button" href="/set-cookie?mode=none">Beállít</a>
  </div>
</div>

<div class="warn">
<b>Megjegyzés:</b> A <code>Secure</code> flag csak HTTPS esetén értelmes igazán. Ez a demo HTTP-n fut, így a böngésző viselkedése eltérhet.
</div>
""")
            self._send(200, body, headers=set_cookie_headers)
            return

        if path == "/set-cookie":
            mode = (qs.get("mode") or ["lax"])[0].lower()
            if mode not in ("lax","strict","none"):
                mode = "lax"
            flags = "Path=/; HttpOnly; "
            if mode == "none":
                # Oktatási célból hozzáadjuk Secure-t, de HTTP-n a böngésző eldobhatja.
                flags += "SameSite=None; Secure"
            elif mode == "strict":
                flags += "SameSite=Strict"
            else:
                flags += "SameSite=Lax"

            # Egy külön demo cookie
            headers = set_cookie_headers + [("Set-Cookie", f"demo={mode}; {flags}"), ("Location", "/cookies")]
            self.send_response(302)
            for k, v in headers:
                self.send_header(k, v)
            self.end_headers()
            return

        if path == "/csrf-vulnerable":
            body = self._html_page("CSRF – sebezhető művelet (nincs token)", f"""
<p>Ez az oldal egy olyan műveletet szimulál, amit a szerver <b>csak cookie/session alapján</b> elfogad.</p>
<div class="card">
  <form method="POST" action="/do-transfer-vuln">
    <label>Összeg (Ft): <input name="amount" value="1000"/></label><br/><br/>
    <button type="submit">„Átutalás” (sebezhető)</button>
  </form>
</div>
<p class="warn"><b>Tanulság:</b> Ha a felhasználó be van jelentkezve, egy másik oldal is képes lehet ilyen POST-ot indítani a nevében.</p>
""")
            self._send(200, body, headers=set_cookie_headers)
            return

        if path == "/csrf-protected":
            # token a sessionben
            if "csrf_token" not in sess:
                sess["csrf_token"] = secrets.token_urlsafe(16)
            token = sess["csrf_token"]
            body = self._html_page("CSRF – védett művelet (token)", f"""
<p>Ez az oldal CSRF tokennel védi a műveletet.</p>
<div class="card">
  <form method="POST" action="/do-transfer-safe">
    <label>Összeg (Ft): <input name="amount" value="1000"/></label>
    <input type="hidden" name="csrf_token" value="{html.escape(token)}"/>
    <br/><br/>
    <button type="submit">„Átutalás” (védett)</button>
  </form>
</div>
<p class="ok"><b>Figyeld meg:</b> a token ott van a HTML-ben (rejtett mező). A támadó oldal tipikusan nem tudja ezt kinyerni ugyanilyen origin nélkül.</p>
""")
            self._send(200, body, headers=set_cookie_headers)
            return

        if path == "/cors-demo":
            body = self._html_page("CORS – fetch teszt", f"""
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
  out.textContent = 'blocked request... (nézd a Console-t is)';
  try {{
    const r = await fetch('http://localhost:{EVIL_PORT}/api/no-cors');
    const t = await r.text();
    out.textContent = t;
  }} catch (e) {{
    out.textContent = 'HIBA (várható): ' + e;
  }}
}}
async function testAllowed() {{
  const out = document.getElementById('out');
  out.textContent = 'allowed request...';
  try {{
    const r = await fetch('http://localhost:{EVIL_PORT}/api/with-cors');
    const j = await r.json();
    out.textContent = JSON.stringify(j, null, 2);
  }} catch (e) {{
    out.textContent = 'HIBA: ' + e;
  }}
}}
</script>
""")
            self._send(200, body, headers=set_cookie_headers)
            return

        # Not found
        self._send(404, self._html_page("404", "<p>Nem található.</p>"), headers=set_cookie_headers)

    def do_POST(self):
        sid, sess, is_new = self._get_session()
        parsed = urlparse(self.path)
        path = parsed.path
        set_cookie_headers = []
        if is_new:
            set_cookie_headers.append(("Set-Cookie", f"sessionid={sid}; Path=/; HttpOnly; SameSite=Lax"))

        length = int(self.headers.get("Content-Length") or "0")
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        form = parse_qs(raw)

        amount = (form.get("amount") or [""])[0]

        if path == "/do-transfer-vuln":
            body = self._html_page("„Átutalás” – eredmény (sebezhető)", f"""
<p class="warn">A szerver végrehajtotta a műveletet <b>CSRF ellenőrzés nélkül</b>.</p>
<div class="card">
  <p>Összeg: <b>{html.escape(amount)}</b> Ft</p>
  <p>Azonosítás: cookie/session alapján.</p>
</div>
<p><b>Beszéljétek meg:</b> hogyan tudná ezt egy másik weboldal „rákényszeríteni” a böngészőre?</p>
""")
            self._send(200, body, headers=set_cookie_headers)
            return

        if path == "/do-transfer-safe":
            token = (form.get("csrf_token") or [""])[0]
            expected = sess.get("csrf_token")
            if not expected or token != expected:
                body = self._html_page("„Átutalás” – elutasítva", f"""
<p class="warn"><b>Elutasítva:</b> hiányzó/hibás CSRF token.</p>
<div class="card">
  <p>Összeg: <b>{html.escape(amount)}</b> Ft</p>
  <p>Kapott token: <code>{html.escape(token)}</code></p>
  <p>Várt token: <code>{html.escape(str(expected))}</code></p>
</div>
<p><b>Tanulság:</b> hiába van érvényes cookie, a szerver plusz bizonyítékot kér.</p>
""")
                self._send(403, body, headers=set_cookie_headers)
                return

            body = self._html_page("„Átutalás” – siker (védett)", f"""
<p class="ok">A szerver végrehajtotta a műveletet <b>érvényes CSRF tokennel</b>.</p>
<div class="card">
  <p>Összeg: <b>{html.escape(amount)}</b> Ft</p>
</div>
""")
            self._send(200, body, headers=set_cookie_headers)
            return

        self._send(404, self._html_page("404", "<p>Nem található.</p>"), headers=set_cookie_headers)


class EvilHandler(BaseHTTPRequestHandler):
    server_version = "WebBiztEvil/1.0"

    def _send(self, status: int, body: str, content_type: str = "text/html; charset=utf-8", headers: list[tuple[str,str]] | None = None):
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
            self._send(200, f"""<!doctype html><meta charset="utf-8">
<h1>Evil origin</h1>
<ul>
  <li><a href="/cors-evil.html">CORS evil oldal</a></li>
  <li><a href="/csrf-attack.html">CSRF attack oldal</a></li>
</ul>
""")
            return

        if path == "/cors-evil.html":
            self._send(200, f"""<!doctype html>
<html lang="hu"><head><meta charset="utf-8"><title>CORS evil</title></head>
<body style="font-family:Arial;margin:24px">
<h1>CORS – evil origin oldal</h1>
<p>Ez az oldal <b>más origin</b> (<code>localhost:{EVIL_PORT}</code>), és megpróbál adatot olvasni az appból (<code>localhost:{APP_PORT}</code>).</p>
<button onclick="tryRead()">Próbálj olvasni az app API-ból</button>
<pre id="out"></pre>
<script>
async function tryRead() {{
  const out = document.getElementById('out');
  out.textContent = 'fetch http://localhost:{APP_PORT}/api/private ... (nézd a Console-t)';
  try {{
    const r = await fetch('http://localhost:{APP_PORT}/api/private');
    const j = await r.json();
    out.textContent = JSON.stringify(j, null, 2);
  }} catch (e) {{
    out.textContent = 'HIBA (várható CORS): ' + e;
  }}
}}
</script>
<p><b>Tanulság:</b> a böngésző blokkolja az adatolvasást, ha az app nem engedélyezi CORS-szal.</p>
</body></html>
""")
            return

        if path == "/csrf-attack.html":
            self._send(200, f"""<!doctype html>
<html lang="hu"><head><meta charset="utf-8"><title>CSRF evil</title></head>
<body style="font-family:Arial;margin:24px">
<h1>CSRF – evil origin oldal</h1>
<p>Ez az oldal megpróbál POST-ot küldeni az appnak a felhasználó nevében.</p>

<div style="border:1px solid #ddd;border-radius:10px;padding:16px;margin:12px 0">
  <h3>1) Támadás a sebezhető végpontra</h3>
  <form id="f1" method="POST" action="http://localhost:{APP_PORT}/do-transfer-vuln">
    <input type="hidden" name="amount" value="9999">
  </form>
  <button onclick="document.getElementById('f1').submit()">Küldés (vulnerable)</button>
</div>

<div style="border:1px solid #ddd;border-radius:10px;padding:16px;margin:12px 0">
  <h3>2) Támadás a védett végpontra (token nélkül)</h3>
  <form id="f2" method="POST" action="http://localhost:{APP_PORT}/do-transfer-safe">
    <input type="hidden" name="amount" value="9999">
    <input type="hidden" name="csrf_token" value="nincs-token">
  </form>
  <button onclick="document.getElementById('f2').submit()">Küldés (protected)</button>
</div>

<p><b>Mit figyelj meg?</b></p>
<ul>
  <li>Az 1) valószínűleg „sikerül”, ha van session cookie.</li>
  <li>A 2) elutasításra kerül, mert a token hibás/hiányzik.</li>
</ul>
</body></html>
""")
            return

        if path == "/api/no-cors":
            self._send(200, json.dumps({"msg":"no CORS headers here"}), "application/json; charset=utf-8")
            return

        if path == "/api/with-cors":
            self._send(200, json.dumps({"msg":"CORS allowed (ACAO: *)"}), "application/json; charset=utf-8",
                       headers=[("Access-Control-Allow-Origin", "*")])
            return

        self._send(404, "not found", "text/plain; charset=utf-8")

# Extra: app API endpoint to show CORS from evil origin
def app_api_private(handler: AppHandler):
    # Nincs CORS header → evil origin nem olvashatja
    handler._send(200, json.dumps({"secret":"TOP-SECRET"}), "application/json; charset=utf-8")

# Monkey patch: route inside AppHandler by extending do_GET a bit via composition is overkill;
# we'll implement by subclassing quickly by checking the path in a wrapper server.
# Instead, we add a small hack: intercept in a custom HTTPServer with a handler factory.


class AppHandlerWithAPI(AppHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/private":
            return app_api_private(self)
        return super().do_GET()


def run_server(host: str, port: int, handler_cls):
    httpd = HTTPServer((host, port), handler_cls)
    print(f"Listening on http://{host}:{port}")
    httpd.serve_forever()

def main():
    t1 = threading.Thread(target=run_server, args=(APP_HOST, APP_PORT, AppHandlerWithAPI), daemon=True)
    t2 = threading.Thread(target=run_server, args=(EVIL_HOST, EVIL_PORT, EvilHandler), daemon=True)
    t1.start(); t2.start()
    print("\nDemo running.")
    print(f"  App : http://localhost:{APP_PORT}")
    print(f"  Evil: http://localhost:{EVIL_PORT}")
    print("Press CTRL+C to stop.\n")
    try:
        while True:
            t1.join(1)
            t2.join(1)
    except KeyboardInterrupt:
        print("\nStopping...")

if __name__ == "__main__":
    main()
