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

    auth_token = request.cookies.get("auth_token", None)
    if auth_token != None:
        system = auth_token_valid(auth_token)
        if system != None:
            return FileResponse(file_path)

    return FileResponse(BASE_DIR / "login.html")

@app.post("/{filename}", response_class=HTMLResponse)
async def filename_post(filename: str, request: Request):
    file_path = BASE_DIR / filename
    logger.info(f"[POST] {filename}")
    # Validar existencia
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    auth_token = request.cookies.get("auth_token", None)

    if filename == "login.html":
        # Leer el POST
        form = await request.form()   # ← parsea x-www-form-urlencoded
        data = dict(form)

        if auth_token != None:
            system = auth_token_valid(auth_token)
            if system != None:
                return FileResponse(BASE_DIR / "menu.html")

        user = data.get("user", None)
        password = data.get("password", None)

        if not user or not password:
            return FileResponse(file_path)

        logger.info(f"[POST] {filename} - Usuario: {user} - Clave: {password}")

        auth_result = get_user_auth(user, password)
        if auth_result is None:
            return FileResponse(file_path)

        response = FileResponse(BASE_DIR / "menu.html")
        response.set_cookie(
            key=auth_result["key"],
            value=auth_result["value"],
            httponly=True,
            samesite="lax",
            max_age=3600
        )
        return response
    else:
        if auth_token != None:
            system = auth_token_valid(auth_token)
            if system != None:
                return FileResponse(file_path)

        return FileResponse(BASE_DIR / "login.html")


@app.get("/data/{filename}", response_class=HTMLResponse)
def root_data(filename: str):
    file_path = BASE_DIR / "data" / filename
    # Validar existencia
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(file_path)
