# FastAPI REST Lab (MVC + REST alapok)

## Előfeltételek
- Python 3.11+ (ajánlott)
- venv (virtuális környezet)

## Telepítés (Windows / Linux / macOS)
A projekt gyökérkönyvtárában:

### 1) Virtuális környezet létrehozása
**Windows (PowerShell):**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS (bash):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Függőségek telepítése
```bash
pip install -r requirements.txt
```

## Futtatás
```bash
uvicorn app.main:app --reload --port 8000
```

## Swagger UI / OpenAPI
- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

## API végpontok
- GET    http://localhost:8000/api/v1/users
- GET    http://localhost:8000/api/v1/users/{id}
- POST   http://localhost:8000/api/v1/users
- PUT    http://localhost:8000/api/v1/users/{id}
- DELETE http://localhost:8000/api/v1/users/{id}
