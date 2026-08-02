from fastapi import APIRouter, Request, Form
from app.log_utils import get_daily_logger
from app.client_utils import get_client_data, update_client_data, update_client_user_data
from app.auth_utils import auth_token_valid

logger = get_daily_logger()

router = APIRouter(prefix="/cgi-bin", tags=["cgi"])

# objetos.cgi
@router.get("/objetos.cgi")
async def objetos_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    #headers = dict(request.headers)
    #
    funcion = request_params.get("funcion", None)
    grupo = request_params.get("grupo", None)
    #
    auth_token = request.cookies.get("auth_token", None)
    if auth_token != None:
        system = auth_token_valid(auth_token)
        if system == None:
            return {"error": 3, "message": "Auth Token Vencido o Inválido"}
    else:
        return {"error": 3, "message": "No Auth Token"}
    #
    if funcion == "list":
        if grupo is not None:
            if system is not None:
                result = get_client_data(system, grupo)
                if result is not None:
                    return {"error": 0, "message": "Ok", "data": result}
                else:
                    return {"error": 2, "message": "No se encontraron datos"}
            else:
                return {"error": 3, "message": "Falta el parámetro System_Key"}
        else:
            return {"error": 3, "message": "Falta el parámetro grupo"}
    else:
        return {"error": 3, "message": "Parámetro funcion inválido o no especificado"}

@router.post("/dompi_cloud_notif.cgi")
async def dompi_cloud_notif_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)

    # Campos generales
    system = data.get("System_Key", None)
    estado = data.get("Estado", None)
 
    # Campos de Assign
    ass_id = data.get("ASS_Id", None)
    objeto = data.get("Objeto", None)
    tipo = data.get("Tipo", None)
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

    # Campos de usuarios
    user_id = data.get("User_Id", None)
    clave = data.get("Clave", None)
    amazon_key = data.get("Amazon_Key", None)
    google_key = data.get("Google_Key", None)
    apple_key = data.get("Apple_Key", None)
    other_key = data.get("Other_Key", None)

    if system != None:
        if ass_id != None:
            update_client_data(system, ass_id, objeto, tipo, estado, icono_apagado, icono_encendido, grupo_visual, planta, cord_x, cord_y, coeficiente, analog_mult_div, analog_mult_div_valor, flags)
        elif user_id != None and clave != None:
            update_client_user_data(user_id, clave, system, amazon_key, google_key, apple_key, other_key, estado)
        else:
            update_client_data(system)
    else:
        logger.info(f"[dompi_cloud_notif.cgi] No se pudo obtener el System_Key [{data}]")

    return {"error": 0, "message": "Ok"}

# dompi_cloud_abmuser.cgi
@router.get("/dompi_cloud_abmuser.cgi")
async def dompi_cloud_abmuser_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}

@router.post("/dompi_cloud_abmuser.cgi")
async def dompi_cloud_abmuser_post(request: Request):
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
async def dompi_cloud_alarma_post(request: Request):
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
async def dompi_cloud_amazon_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}

@router.post("/dompi_cloud_amazon.cgi")
async def dompi_cloud_amazon_post(request: Request):
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
async def dompi_cloud_mobile_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}

@router.post("/dompi_cloud_mobile.cgi")
async def dompi_cloud_mobile_post(request: Request):
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
async def dompi_cloud_status_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}

@router.post("/dompi_cloud_status.cgi")
async def dompi_cloud_status_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    return {"error": 0, "message": "Ok"}
