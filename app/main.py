from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.log_utils import get_daily_logger
from app.auth_utils import get_user_auth, auth_token_valid, new_auth_token

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
    #logger.info(f"[GET] {filename}")
    # Validar existencia
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    auth_token = request.cookies.get("auth_token", None)
    if auth_token != None:
        system = auth_token_valid(auth_token)
        if system != None:
            #logger.info(f"[GET] {filename} - Usuario autenticado para sistema: {system}")
            # Genero un token nuevo para el usuario autenticado
            auth_result = new_auth_token(system)
            response = FileResponse(file_path)
            response.set_cookie(
                key=auth_result["key"],
                value=auth_result["value"],
                httponly=True,
                samesite="lax",
                max_age=600
            )
            # Ok
            return response
    # Si no tiene cookie de autenticación válida, lo devuelvo al login
    logger.info(f"[GET] {filename} - No autenticado. Dvolviendo login")
    return FileResponse(BASE_DIR / "login.html")

@app.post("/{filename}", response_class=HTMLResponse)
async def filename_post(filename: str, request: Request):
    file_path = BASE_DIR / filename
    #logger.info(f"[POST] {filename}")
    # Validar existencia
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    auth_token = request.cookies.get("auth_token", None)

    # Páfina de login, se procesa el POST para validar usuario y contraseña
    if filename == "login.html":
        # Leer el POST
        form = await request.form()   # ← parsea x-www-form-urlencoded
        data = dict(form)
        # Tomo los datos de usuario y contraseña
        user = data.get("user", None)
        password = data.get("password", None)
        if not user or not password:
            # Lo devuelvo al login sin decirle nada
            return FileResponse(file_path)
        # Valido al usuario y contraseña
        auth_result = get_user_auth(user, password)
        if auth_result is None:
            # Lo devuelvo al login sin decirle nada para que no sepa si el usuario existe o no
            return FileResponse(file_path)
        # Si es correcto, le devuelvo el menu.html y le pongo la cookie de autenticación
        response = FileResponse(BASE_DIR / "menu.html")
        response.set_cookie(
            key=auth_result["key"],
            value=auth_result["value"],
            httponly=True,
            samesite="lax",
            max_age=600
        )
        return response
    else:
        # Para cualquier otro POST, valido la cookie de autenticación
        if auth_token != None:
            system = auth_token_valid(auth_token)
            if system != None:
                #logger.info(f"[POST] {filename} - Usuario autenticado para sistema: {system}")
                # Genero un token nuevo para el usuario autenticado
                auth_result = new_auth_token(system)
                response = FileResponse(file_path)
                response.set_cookie(
                    key=auth_result["key"],
                    value=auth_result["value"],
                    httponly=True,
                    samesite="lax",
                    max_age=600
                )
                # Ok
                return response
        # Si no es login.html y no tiene cookie de autenticación válida, lo devuelvo al login
        logger.info(f"[POST] {filename} - No autenticado. Dvolviendo login")
        return FileResponse(BASE_DIR / "login.html")


@app.get("/data/{filename}", response_class=HTMLResponse)
def root_data(filename: str):
    file_path = BASE_DIR / "data" / filename
    # Validar existencia
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(file_path)
