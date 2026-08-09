import json
from fastapi import APIRouter, Request, Form
from app.log_utils import get_daily_logger
from app.client_utils import dequeue_action, enqueue_action, get_client_data, update_client_data, update_client_user_data
from app.auth_utils import auth_token_valid, get_client_system_by_amazon_key
from app.amazon_alexa import alexa_discover, alexa_turn_on, alexa_turn_off, alexa_lock, alexa_unlock, alexa_report_state

logger = get_daily_logger()

router = APIRouter(prefix="/cgi-bin", tags=["cgi"])

"""
**** Discovery ****
REMOTE_ADDR=54.160.178.88 
REQUEST_URI=/cgi-bin/dompi_cloud_amazon.cgi/?funcion=Discover 
REQUEST_METHOD=POST 
CONTENT_LENGTH=855 
POST={"data": {"directive": {"header": {"namespace": "Alexa.Discovery", "name": "Discover", "payloadVersion": "3", "messageId": "5e90b8b4-f1fd-4011-a7e1-54211be03d98"}, "payload": {"scope": {"type": "BearerToken", "token": "Atza|gQBNhvYwAwEBAC2OWyqW9Ox02W_qRyEHcLQ1ooOkaoJQYDvT7UG1_UVf5jgZOH7WKZVZssNOwzaCD3dG2B9lEUEKMWi8AiRQWb-udZq1gtqI--LRUchOH0-gRjbA8QrMWYW4-1ZKguR-XY6Yy11GgRgb67zs9osJwyuEcSPKbE9SCVOODDXWBw9t7dufwKwQPUHk7lMrBpuCsIcBphd1z6iodSD0B7YqtXiMwnoMveOrdYKlMQT7PA3yP1spoNN4R8sMQGHWM28W5sIzvdm3q7_M9br0TRncqeURpoZ3zU7iT0EJffb1qsd6_Op5Qao_JnXN3sWZBF_UJJP6WTTE7tFAcKHslbSF3mgCuE_QX_pcYhCUhfvWG-f-e9zHS9VabyeE2gQvEiyEHCazX1HOD8owaBLb8gWj6ueFt6bplu-t38stSvQUtApASl2QtAy_aziB4vekAlgr9Y304AjNU49XWRXmawWruDqFpCsrcbDNWB60LzXPTuf4Kf9gxeuvfArb8VlqpZB1FA"}}}}, "user": {"user_id": "amzn1.account.AHR7ZDWLFNCUWTJOA76CM4M3627Q", "email": "camila@pirri.com.ar"}}

**** TurnOff ****
REMOTE_ADDR=3.236.120.227 
REQUEST_URI=/cgi-bin/dompi_cloud_amazon.cgi/?funcion=TurnOff 
REQUEST_METHOD=POST 
CONTENT_LENGTH=1175 
POST={"data": {"directive": {"header": {"messageId": "d5445bdf-cc7a-493d-bd46-e5482eba5a11", "namespace": "Alexa.PowerController", "name": "TurnOff", "payloadVersion": "3", "correlationToken": "SUdTVEs6AAE6AAg6eyJpZCI6IjUzNmE3Nzg5LTJkNjktNDA3Ni05ZTc4LTNmMjE5ODk4MGQ4MSIsInVyaSI6Imh0dHBzOi8vZC1hY3JzLW5hLXAtN2U1LWZkNDIyOTYxLnVzLWVhc3QtMS5hbWF6b24uY29tOjk0NDQiLCJzZXNzaW9uSWQiOiJiZTIyMTRmOS0xM2NhLTQzMTUtOTRjNC0wMzBhZDI5MTVjYzkifQ=="}, "endpoint": {"scope": {"type": "BearerToken", "token": "Atza|gQDBgAV4AwEBACYyO93xZamRG8YDeR_NZf4PEB8cEp-2kYyuXTHD8jbygWqlgEQNkRbSwnR0gg7QXs3GTfzm2ZSM4UKUeCwz9Ude5pWfMPMGJOze3ASGSsboVnr02z0TUTYjSwxoNrjOBXqoCqSvkOyC_Sjtj4wH_AHob5QBqabr6t2Ragf2RNegcWboLqWAMEjDQCRQKk7kLARLrB-1TnUGBPK-iNR6r4eatNLdvpe8TzHfcAfAJN2exxjB2MkbvP5nGC8wBCEQnq7yiqauvYxm9o4NkcLpnvSs5UCq-wm2G7Ts_IAKomlnTJ72-oD7-fhfggkHXf4aTiTcPNiAlUz2g8Clb1ibGtQvof3PSyuSLhNO_wD6KmL4sC2g6Lr9676u--5lb7TKInOOt9cU8GEr5UvsPo_FQzrZ4sMXemKuDOLKyh9A28PdlLuP5uJILE6joxaZovtYem4TAgT_BvJa3GwxX9O-i7vS9gse-YVieXlICvoJYTqDukYQ9VeHJpmQQhqsMg"}, "endpointId": "Luz-Pasillo", "cookie": {}}, "payload": {}}}, "user": {"user_id": "amzn1.account.AFJBR7A4TM7ST4ZICQ2DD4JAW2RQ", "email": "walter@pirri.com.ar"}}
Resp [{ "response": {"resp_code": "0", "resp_msg": "Ok", "Objeto": "Luz Pasillo", "Estado": "0", "Ultimo_Update": "2026-08-09 03:21:27" } }]


**** TurnOn ****
REMOTE_ADDR=34.231.70.165 
REQUEST_URI=/cgi-bin/dompi_cloud_amazon.cgi/?funcion=TurnOn 
REQUEST_METHOD=POST 
CONTENT_LENGTH=1174 
POST={"data": {"directive": {"header": {"messageId": "32f1292a-4776-4855-b275-f59fc38e7b95", "namespace": "Alexa.PowerController", "name": "TurnOn", "payloadVersion": "3", "correlationToken": "SUdTVEs6AAE6AAg6eyJpZCI6IjdiMWYwNmQzLWNjNzMtNDVlNS1iZjUxLWU1OWE1MGRkMzNiNCIsInVyaSI6Imh0dHBzOi8vZC1hY3JzLW5hLXAtN2I0LWQ4ZjllODY3LnVzLWVhc3QtMS5hbWF6b24uY29tOjk0NDQiLCJzZXNzaW9uSWQiOiI0ODNmM2ZjZC01OGE0LTRkN2ItOGIwYS01NDYyMzE5NjE2YmEifQ=="}, "endpoint": {"scope": {"type": "BearerToken", "token": "Atza|gQB9IQ5iAwEBAM2lLKqWvIfidbJQZR8wTgVto9ioOrxS9viYgmEffdHL6VJvbVmgAgHboSg_gg-OxrSTte8wGuF9B5Tj9ImHYQRuz5767WhEGus_mqA3dseYc9tT1VSIIfbHWPjVRveF9kVvTEHLh1mC4mWOMC1YhQckNvn6-40ubmqnf8FApmW6ahhZrCrJjZG2tQzTDmdtWJldTc_6Zbm2KldfaFckvXUSPAqo5_5fxjpIoQQ8YUraIBsGJ8CAPBrEUU8ojhezt7lhv3PfQWuEvL1yDMZnnZDFbsC5MxGIsoN70O798xkQ963PJomfY6IGX-tBTnUT9UsN8B5nFcBD3BoTpdAz90IzTUwPXO9A8C-IUgltETFx_WviGgq1dgNj1H_sgrCl7MNl1K1UjizQeO7PoFRmFSkf6-eLPKyU_OI-Pv9gQJn6NDMpQPeW1H7dO_CKL-CzbWf4pryh1i-BdHy9D1prcU_V3dELFpm8o_WESmnkZZT5qmSfKOs3_dQBB5Y2jP4"}, "endpointId": "Luz-Taller", "cookie": {}}, "payload": {}}}, "user": {"user_id": "amzn1.account.AFJBR7A4TM7ST4ZICQ2DD4JAW2RQ", "email": "walter@pirri.com.ar"}}
Resp [{ "response": {"resp_code": "0", "resp_msg": "Ok", "Objeto": "Luz Taller", "Estado": "1", "Ultimo_Update": "2026-08-07 18:13:37" } }]

**** ReportState **** 
REMOTE_ADDR=44.201.22.78 
REQUEST_URI=/cgi-bin/dompi_cloud_amazon.cgi/?funcion=ReportState 
REQUEST_METHOD=POST 
CONTENT_LENGTH=1253 
POST={"data": {"directive": {"header": {"messageId": "8fda64e8-af18-4724-8318-0274d63deb00", "namespace": "Alexa", "name": "ReportState", "payloadVersion": "3", "correlationToken": "SUdTVEs6AAE6AAs6eyJ0aW1lc3RhbXAiOiIxNzg1NzEzMDgzNjY3IiwiY2xpZW50SWRlbnRpdHkiOm51bGwsImRldmljZSI6bnVsbCwiY2hyRW5kcG9pbnRJZCI6ImFtem4xLmFsZXhhLmVuZHBvaW50LjYzMDI3ZmJmLTkxYjktNGNlMy05MmE2LTc5ZTM5NjU0MTY1NCIsImN1c3RvbWVySWQiOiJBRjc2VEw1TkdBNU5QIiwibGlmZUN5Y2xlIjoiUE9MTElOR19TVEFSVEVEIiwiY29ycmVsYXRpb25Ub2tlbiI6bnVsbH0="}, "endpoint": {"scope": {"type": "BearerToken", "token": "Atza|gQAZoMG5AwEBAEmtP2QdzbG0dYSZux6JpxqSso5w6pZGt-KcjG91n3DmH7SsPqFx9ioekTqCEAr4YcZd4XbLGnYf8BNBlzw3PwxMHwFdWu4iecB5N8tHaugUuVFCBQyxUOp_88ZHcCixOtMi6A15zeYc08EdbstKCs9UuWzdOGSn78ETDt-s_1-NIUZgZCf-BNDBAdGgQd7sH8e9dmwoCz7FX6MS7xCA51A7uyuL-eAsOoA8KIiGzhIgZI1ZbWfmp4-Cz07eUke1w7z_mlZl2I31z7KB8uWXOXJGadTh3PeiI9WaiF5e5yyGqtpH6xIf75eiiuK8AkS8ArNSRjaD1bmjn2Pf9dbPPKwOVlzneyCXzQLWa8YQlLQMNwDK-d64rRqnabX8okClaeJacupWgF9bsbNkuvXfR3ng8BRxud3vEg3qPzPEQNwvDwvvyrggSj-IbP5YFT477YYGYwFPrGp1P34jLYDpldGMvb2JJxpjFkFOZhskqgdjNhlDCuLRdm17HHWO084"}, "endpointId": "Luz-Pasillo-Exterior", "cookie": {}}, "payload": {}}}, "user": {"user_id": "amzn1.account.AFJBR7A4TM7ST4ZICQ2DD4JAW2RQ", "email": "walter@pirri.com.ar"}}

"""

@router.post("/dompi_cloud_amazon.cgi")
async def alexa_post(request: Request):
    body = await request.json()

    try:
        namespace = body['data']['directive']['header']['namespace']
    except KeyError:
        namespace = None

    try:
        name = body['data']['directive']['header']['name']
    except KeyError:
        name = None

    if namespace == "Alexa.Discovery" and name == "Discover":
        try:
            email = body['data']['user']['email']
        except KeyError:
            email = None
    else:
        try:
            email = body['user']['email']
        except KeyError:
            email = None

    if email is None or namespace is None or name is None:
        logger.info(f"[POST:dompi_cloud_amazon.cgi] Falta algun datos clave en el mensaje recibido: namespace={namespace}, name={name}, email={email}")
        return "response: " + json.dumps({"error": 1, "message": "Faltan parámetros"})

    system = get_client_system_by_amazon_key(email)
    if system is None:
        logger.info(f"[POST:dompi_cloud_amazon.cgi] No se pudo obtener el sistema para el email={email}")
        return "response: " + json.dumps({"error": 2, "message": "Usuario no registrado"})

    logger.info(f"[POST:dompi_cloud_amazon.cgi] namespace: {namespace} - name: {name} - email: {email} - system: {system}")

    if namespace == "Alexa.Discovery" and name == "Discover":
        # 
        response_data = alexa_discover(system)
        return "response: " + json.dumps(response_data)
    elif namespace == "Alexa.PowerController" and name == "TurnOn":
        objeto = body['data']['directive']['endpoint']['endpointId']
        objeto_real = objeto.replace("-", " ")
        # { "response": {"resp_code": "0", "resp_msg": "Ok", "Objeto": "Luz Taller", "Estado": "1", "Ultimo_Update": "2026-08-07 18:13:37" } }
        response_data = alexa_turn_on(system, objeto_real)
        return "response: " + json.dumps(response_data)
    elif namespace == "Alexa.PowerController" and name == "TurnOff":
        objeto = body['data']['directive']['endpoint']['endpointId']
        objeto_real = objeto.replace("-", " ")
        # { "response": {"resp_code": "0", "resp_msg": "Ok", "Objeto": "Luz Pasillo", "Estado": "0", "Ultimo_Update": "2026-08-09 03:21:27" } }
        response_data = alexa_turn_off(system, objeto_real)
        return "response: " + json.dumps(response_data)
    elif namespace == "Alexa.SecurityPanelController" and name == "Lock":
        objeto = body['data']['directive']['endpoint']['endpointId']
        objeto_real = objeto.replace("-", " ")
        # 
        response_data = alexa_lock(system, objeto_real)
        return "response: " + json.dumps(response_data)
    elif namespace == "Alexa.SecurityPanelController" and name == "Unlock":
        objeto = body['data']['directive']['endpoint']['endpointId']
        objeto_real = objeto.replace("-", " ")
        # 
        response_data = alexa_unlock(system, objeto_real)
        return "response: " + json.dumps(response_data)
    elif namespace == "Alexa" and name == "ReportState":
        objeto = body['data']['directive']['endpoint']['endpointId']
        objeto_real = objeto.replace("-", " ")
        # 
        response_data = alexa_report_state(system, objeto_real)
        return "response: " + json.dumps(response_data)

    return "response: " + json.dumps({"error": 2, "message": "Funcion desconocida o no especificada"})

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
