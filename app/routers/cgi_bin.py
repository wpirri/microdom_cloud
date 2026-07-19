from fastapi import APIRouter, Request, Form
from app.log_utils import get_daily_logger
from app.client_utils import update_client_data

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

    #logger.info("POST /cgi-bin/dompi_cloud_notif.cgi")
    #logger.info(f"    Headers: {headers}")
    #logger.info(f"    Query Params: {request_params}")
    #logger.info(f"    Form Data: {data}")

    #    'ASS_Id': '18', 'Objeto': 'Luz Pasillo', 'Tipo': '0', 'Estado': '0', 'Icono_Apagado': 'lamp0.png', 'Icono_Encendido': 'lamp1.png', 'Grupo_Visual': '2', 'Planta': '1', 'Cord_x': '525', 'Cord_y': '245', 'Coeficiente': '0', 'Analog_Mult_Div': '0', 'Analog_Mult_Div_Valor': '1', 'Flags': '0', 'System_Key': 'D3S4RR0LL0-0001'}
    #   update_client_data(system, ass_id, objeto, tipo, estado, icono_apagado, icono_encendido, grupo_visual, planta, cord_x, cord_y, coeficiente, analog_mult_div, analog_mult_div_valor, flags):
    system = data.get("System_Key", None)
    ass_id = data.get("ASS_Id", None)
    objeto = data.get("Objeto", None)
    tipo = data.get("Tipo", None)
    estado = data.get("Estado", None)
    icono_apagado = data.get("Icono_Apagado", None)
    icono_encendido = data.get("Icono_Encendido", None)
    grupo_visual = data.get("Grupo_Visual", None)
    planta = data.get("Planta", None)
    cord_x = data.get("Cord_x", None)
    cord_y = data.get("Cord_y", None)
    coeficiente = data.get("Coeficiente", None)
    analog_mult_div = data.get("Analog_Mult_Div", None)
    analog_mult_div_valor = data.get("Analog_Mult_Div_Valor", None)
    flags = data.get("Flags", None)

    update_client_data(system, ass_id, objeto, tipo, estado, icono_apagado, icono_encendido, grupo_visual, planta, cord_x, cord_y, coeficiente, analog_mult_div, analog_mult_div_valor, flags)

    return {"error": 0, "message": "Ok"}

# dompi_cloud_abmuser.cgi
@router.get("/dompi_cloud_abmuser.cgi")
async def abmsys_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}

@router.post("/dompi_cloud_abmuser.cgi")
async def abmsys_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}

# dompi_cloud_alarma.cgi
@router.get("/dompi_cloud_alarma.cgi")
async def abmsys_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}

@router.post("/dompi_cloud_alarma.cgi")
async def abmsys_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}

# dompi_cloud_amazon.cgi
@router.get("/dompi_cloud_amazon.cgi")
async def abmsys_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}

@router.post("/dompi_cloud_amazon.cgi")
async def abmsys_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}

# dompi_cloud_mobile.cgi
@router.get("/dompi_cloud_mobile.cgi")
async def abmsys_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}

@router.post("/dompi_cloud_mobile.cgi")
async def abmsys_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}

# dompi_cloud_status.cgi
@router.get("/dompi_cloud_status.cgi")
async def abmsys_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}

@router.post("/dompi_cloud_status.cgi")
async def abmsys_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}
