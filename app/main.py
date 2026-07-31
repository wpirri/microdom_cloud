import base64
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.log_utils import get_daily_logger
from app.auth_utils import get_user_auth, auth_token_valid

from app.routers import cgi_bin, download

app = FastAPI(
    title="Administración remota de sistemas de domótica",
    version="1.0.0"
)

logger = get_daily_logger()

# Routers existentes
app.include_router(cgi_bin.router)
app.include_router(download.router)

# Archivos estáticos específicos
app.mount("/css", StaticFiles(directory="/app/html/css"), name="css")
app.mount("/js", StaticFiles(directory="/app/html/js"), name="js")
app.mount("/images", StaticFiles(directory="/app/html/images"), name="images")

BASE_DIR = Path("/app/html")  # Cambialo según tu mapeo real

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def root():
    return FileResponse(BASE_DIR / "login.html")

@app.get("/{filename}", response_class=HTMLResponse)
def filename_get(filename: str, request: Request):
    file_path = BASE_DIR / filename

    logger.info(f"[GET] {filename}")

    # Validar existencia
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    auth_header = request.headers.get("authorization")
    if not auth_header:
        logger.info(f"[GET] {filename} - No auth header")
        return FileResponse(BASE_DIR / "login.html")

    scheme, _, credentials = auth_header.partition(" ")
    if scheme.lower() != "basic" or not credentials:
        logger.info(f"[GET] {filename} - No Basic auth")
        return FileResponse(BASE_DIR / "login.html")

    try:
        decoded = base64.b64decode(credentials).decode("utf-8")
        user, password = decoded.split(":", 1)
    except Exception:
        return FileResponse(BASE_DIR / "login.html")

    if user == "token_auth":
        logger.info(f"[GET] {filename} - Identificado Token Auth")
        if not auth_token_valid(password):
            logger.info(f"[GET] {filename} - Token Auth no valido")
            return FileResponse(BASE_DIR / "login.html")
    else:
        user_auth = get_user_auth(user, password)
        logger.info(f"[GET] {filename} - User Auth: {user_auth}")
        if not user_auth:
            return FileResponse(BASE_DIR / "login.html")

    return FileResponse(file_path)

@app.post("/{filename}", response_class=HTMLResponse)
def filename_post(filename: str, request: Request):
    file_path = BASE_DIR / filename

    logger.info(f"[POST] {filename}")

    # Validar existencia
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    auth_header = request.headers.get("authorization")
    if not auth_header:
        logger.info(f"[POST] {filename} - No auth header")
        return FileResponse(BASE_DIR / "login.html")

    scheme, _, credentials = auth_header.partition(" ")
    if scheme.lower() != "basic" or not credentials:
        logger.info(f"[POST] {filename} - No Basic auth")
        return FileResponse(BASE_DIR / "login.html")

    try:
        decoded = base64.b64decode(credentials).decode("utf-8")
        user, password = decoded.split(":", 1)
    except Exception:
        return FileResponse(BASE_DIR / "login.html")

    if user == "token_auth":
        logger.info(f"[POST] {filename} - Identificado Token Auth")
        if not auth_token_valid(password):
            logger.info(f"[POST] {filename} - Token Auth no valido")
            return FileResponse(BASE_DIR / "login.html")
    else:
        user_auth = get_user_auth(user, password)
        logger.info(f"[POST] {filename} - User Auth: {user_auth}")
        if not user_auth:
            return FileResponse(BASE_DIR / "login.html")

    return FileResponse(file_path)


@app.get("/data/{filename}", response_class=HTMLResponse)
def root_data(filename: str):
    file_path = BASE_DIR / "data" / filename
    # Validar existencia
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(file_path)
