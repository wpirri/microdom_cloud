from fastapi import APIRouter, Request, Form
from app.log_utils import get_daily_logger
from app.client_utils import dequeue_action, enqueue_action, get_client_data, update_client_data, update_client_user_data
from app.auth_utils import auth_token_valid, get_client_system_by_amazon_key
from app.amazon_alexa import alexa_discover, alexa_turn_on, alexa_turn_off, alexa_turn_lock, alexa_turn_unlock, alexa_turn_report_state

logger = get_daily_logger()

router = APIRouter(prefix="/cgi-bin", tags=["cgi"])

##############################################################################
# dompi_cloud_amazon.cgi
# "CONTENT_LENGTH":"1170","REMOTE_ADDR":"18.234.120.118","REQUEST_METHOD":"POST","REQUEST_URI":"/cgi-bin/dompi_cloud_amazon.cgi/?funcion=TurnOn"
# "request":{"data":{"directive":{"header":{"messageId":"06531875-50b2-4be6-89fe-2f80cdd4361c","namespace":"Alexa.PowerController","name":"TurnOn","payloadVersion":"3","correlationToken":"SUdTVEs6AAE6AAg6eyJpZCI6IjZhYmIxMzQxLWI3ZGUtNDE0Yi05Yjk3LTY2NmZjYjRmNmY3MyIsInVyaSI6Imh0dHBzOi8vZC1hY3JzLW5hLXAtN2UtMjdkMjdhNGIudXMtZWFzdC0xLmFtYXpvbi5jb206OTQ0NCIsInNlc3Npb25JZCI6IjNhODEwYmI4LTRlNWEtNDkyNy1iMjc4LTI2ZTNmOTdhZmIwNSJ9"},"endpoint":{"scope":{"type":"BearerToken","token":"Atza|gQAZoMG5AwEBAEmtP2QdzbG0dYSZux6JpxqSso5w6pZGt-KcjG91n3DmH7SsPqFx9ioekTqCEAr4YcZd4XbLGnYf8BNBlzw3PwxMHwFdWu4iecB5N8tHaugUuVFCBQyxUOp_88ZHcCixOtMi6A15zeYc08EdbstKCs9UuWzdOGSn78ETDt-s_1-NIUZgZCf-BNDBAdGgQd7sH8e9dmwoCz7FX6MS7xCA51A7uyuL-eAsOoA8KIiGzhIgZI1ZbWfmp4-Cz07eUke1w7z_mlZl2I31z7KB8uWXOXJGadTh3PeiI9WaiF5e5yyGqtpH6xIf75eiiuK8AkS8ArNSRjaD1bmjn2Pf9dbPPKwOVlzneyCXzQLWa8YQlLQMNwDK-d64rRqnabX8okClaeJacupWgF9bsbNkuvXfR3ng8BRxud3vEg3qPzPEQNwvDwvvyrggSj-IbP5YFT477YYGYwFPrGp1P34jLYDpldGMvb2JJxpjFkFOZhskqgdjNhlDCuLRdm17HHWO084"},"endpointId":"Luz-Taller","cookie":{}},"payload":{}}},"user":{"user_id":"amzn1.account.AFJBR7A4TM7ST4ZICQ2DD4JAW2RQ","email":"walter@pirri.com.ar"}}
@router.post("/dompi_cloud_amazon.cgi")
async def alexa_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)
    #
    funcion = request_params.get("funcion", None)
    user = data.get("user", None)
    email = data.get("email", None)
    directive = data.get("directive", None)

    if funcion is None or user is None or email is None or directive is None:
        return {"error": 1, "message": "Faltan parámetros"}

    system = get_client_system_by_amazon_key(email)
    if system is None:
        return {"error": 2, "message": "Usuario no registrado"}

    if funcion == "Discover":
        return {"error": 0, "message": "Ok", "response": alexa_discover(system)}
    elif funcion == "TurnOn":

        return {"error": 0, "message": "Ok"}
    elif funcion == "TurnOff":

        return {"error": 0, "message": "Ok"}
    elif funcion == "ReportState":

        return {"error": 0, "message": "Ok"}
    elif funcion == "Lock":

        return {"error": 0, "message": "Ok"}
    elif funcion == "Unlock":

        return {"error": 0, "message": "Ok"}



    return {"error": 2, "message": "Funcion desconocida o no especificada"}

# objetos.cgi
@router.get("/touch.cgi")
async def touch_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    objeto = request_params.get("objeto", None)
    #
    auth_token = request.cookies.get("auth_token", None)
    if auth_token != None:
        system = auth_token_valid(auth_token)
        if system == None:
            return {"error": 3, "message": "Auth Token Vencido o Inválido"}
    else:
        return {"error": 3, "message": "No Auth Token"}
    #
    enqueue_action(system, objeto)
    return {"error": 0, "message": "Ok"}


# objetos.cgi
@router.get("/objetos.cgi")
async def objetos_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
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

    return dequeue_action(system)

# dompi_cloud_abmuser.cgi
@router.get("/dompi_cloud_abmuser.cgi")
async def dompi_cloud_abmuser_get(request: Request):

    return {"error": 0, "message": "Ok"}

@router.post("/dompi_cloud_abmuser.cgi")
async def dompi_cloud_abmuser_post(request: Request):

    return {"error": 0, "message": "Ok"}

# dompi_cloud_alarma.cgi
@router.get("/dompi_cloud_alarma.cgi")
async def abmsys_get(request: Request):

    return {"error": 0, "message": "Ok"}

@router.post("/dompi_cloud_alarma.cgi")
async def dompi_cloud_alarma_post(request: Request):

    return {"error": 0, "message": "Ok"}
