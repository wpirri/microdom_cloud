from fastapi import APIRouter, Request, Form
from app.log_utils import get_daily_logger

logger = get_daily_logger()

router = APIRouter(prefix="/cgi-bin", tags=["cgi"])

# dompi_cloud_notif.cgi
@router.get("/dompi_cloud_notif.cgi")
async def abmsys_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error=0&message=Ok"}

@router.post("/dompi_cloud_notif.cgi")
async def abmsys_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    logger.info("POST /cgi-bin/dompi_cloud_notif.cgi")
    logger.info(f"    Headers: {headers}")
    logger.info(f"    Query Params: {request_params}")
    logger.info(f"    Form Data: {data}")
    logger.info(f"    Request Body: {await request.body()}")

    return {"error=0&message=Ok"}

# dompi_cloud_abmuser.cgi
@router.get("/dompi_cloud_abmuser.cgi")
async def abmsys_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error=0&message=Ok"}

@router.post("/dompi_cloud_abmuser.cgi")
async def abmsys_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error=0&message=Ok"}

# dompi_cloud_alarma.cgi
@router.get("/dompi_cloud_alarma.cgi")
async def abmsys_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error=0&message=Ok"}

@router.post("/dompi_cloud_alarma.cgi")
async def abmsys_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error=0&message=Ok"}

# dompi_cloud_amazon.cgi
@router.get("/dompi_cloud_amazon.cgi")
async def abmsys_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error=0&message=Ok"}

@router.post("/dompi_cloud_amazon.cgi")
async def abmsys_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error=0&message=Ok"}

# dompi_cloud_mobile.cgi
@router.get("/dompi_cloud_mobile.cgi")
async def abmsys_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error=0&message=Ok"}

@router.post("/dompi_cloud_mobile.cgi")
async def abmsys_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error=0&message=Ok"}

# dompi_cloud_status.cgi
@router.get("/dompi_cloud_status.cgi")
async def abmsys_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error=0&message=Ok"}

@router.post("/dompi_cloud_status.cgi")
async def abmsys_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error=0&message=Ok"}
