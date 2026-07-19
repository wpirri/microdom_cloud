from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id

logger = get_daily_logger()

"""
CREATE TABLE TB_DOMCLOUD_ASSIGN (
System_Key varchar(256),
Id varchar(16),                         -- Permito Ids alfanumericos
Objeto varchar(128),
Tipo integer DEFAULT 0,                 -- 0=Output, 1=Input, 2=Analog, 3=Output Alarma, 4=Input Alarma, 5=Output Pulse/Analog_Mult_Div_Valor=Pulse Param, 6=Periferico, 1x=Automatizacion (3 estados)
Estado integer DEFAULT 0,               -- 0=Apagado, 1=Encendido, 2=Automático
Icono_Apagado varchar(32),
Icono_Encendido varchar(32),
Icono_Auto varchar(32),
Grupo_Visual integer DEFAULT 0,         -- 0=Ninguno 1=Alarma 2=Iluminación 3=Puertas 4=Climatización 5=Cámaras 6=Riego
Planta integer DEFAULT 0,
Cord_x integer DEFAULT 0,
Cord_y integer DEFAULT 0,
Coeficiente integer DEFAULT 0,
Analog_Mult_Div integer DEFAULT 0,
Analog_Mult_Div_Valor integer DEFAULT 1,
Time_Stamp bigint,
Flags integer DEFAULT 0,
PRIMARY KEY (System_Key, Id)
);
"""
def update_client_data(system, ass_id, objeto, tipo, estado, icono_apagado, icono_encendido, grupo_visual, planta, cord_x, cord_y, coeficiente, analog_mult_div, analog_mult_div_valor, flags):
    if system != None:
        if ass_id != None:
            query = f"UPDATE TB_DOMCLOUD_ASSIGN SET Time_Stamp = UNIX_TIMESTAMP(), Objeto='{objeto}', Tipo={tipo}, Estado={estado}, Icono_Apagado='{icono_apagado}', Icono_Encendido='{icono_encendido}', Grupo_Visual={grupo_visual}, Planta={planta}, Cord_x={cord_x}, Cord_y={cord_y}, Coeficiente={coeficiente}, Analog_Mult_Div={analog_mult_div}, Analog_Mult_Div_Valor={analog_mult_div_valor}, Flags={flags} WHERE System_Key='{system}' AND Id='{ass_id}'"
            if mysql_execute(query) == 0:
                query = f"INSERT INTO TB_DOMCLOUD_ASSIGN (System_Key, Id, Objeto, Tipo, Estado, Icono_Apagado, Icono_Encendido, Grupo_Visual, Planta, Cord_x, Cord_y, Coeficiente, Analog_Mult_Div, Analog_Mult_Div_Valor, Flags, Time_Stamp) VALUES ('{system}', '{ass_id}', '{objeto}', {tipo}, {estado}, '{icono_apagado}', '{icono_encendido}', {grupo_visual}, {planta}, {cord_x}, {cord_y}, {coeficiente}, {analog_mult_div}, {analog_mult_div_valor}, {flags}, UNIX_TIMESTAMP())"
                if mysql_execute(query) > 0:
                    logger.info(f"Objeto {objeto} en estado {estado} agregado al cliente {system}")
            else:
                logger.info(f"Objeto {objeto} de cliente {system} pasa a estado {estado}")
        else:
            query = f"UPDATE TB_DOMCLOUD_ASSIGN SET Time_Stamp = UNIX_TIMESTAMP()  WHERE System_Key='{system}' AND Id='0'"
            if mysql_execute(query) == 0:
                query = f"INSERT INTO TB_DOMCLOUD_ASSIGN (System_Key, Id, Time_Stamp) VALUES ('{system}', '0', UNIX_TIMESTAMP())"
                if mysql_execute(query) > 0:
                    logger.info(f"Cliente {system} agregado al sistema")
 


"""
CREATE TABLE TB_DOMCLOUD_USER (
Usuario varchar(256),
Clave varchar(256),
Id_Sistema varchar(256),
Amazon_Key varchar(256),
Google_Key varchar(256),
Apple_Key varchar(256),
Other_Key varchar(256),
Errores integer DEFAULT 0,
Ultima_Conexion bigint DEFAULT 0,
Estado integer DEFAULT 0,     -- 0 Disable, 1 Enable
Time_Stamp bigint,
PRIMARY KEY (Usuario)
);
"""
def update_client_user_data(usuario, clave, id_sistema, amazon_key, google_key, apple_key, other_key):
    if usuario != None and id_sistema != None and clave != None:
        query = f"UPDATE TB_DOMCLOUD_USER SET Time_Stamp = UNIX_TIMESTAMP(), Clave='{clave}', Id_Sistema='{id_sistema}', Amazon_Key='{amazon_key}', Google_Key='{google_key}', Apple_Key='{apple_key}', Other_Key='{other_key}' WHERE Usuario='{usuario}'"
        if mysql_execute(query) == 0:
            query = f"INSERT INTO TB_DOMCLOUD_USER (Usuario, Clave, Id_Sistema, Amazon_Key, Google_Key, Apple_Key, Other_Key, Time_Stamp) VALUES ('{usuario}', '{clave}', '{id_sistema}', '{amazon_key}', '{google_key}', '{apple_key}', '{other_key}', UNIX_TIMESTAMP())"
            if mysql_execute(query) > 0:
                logger.info(f"Usuario {usuario} de cliente {id_sistema} agregado al sistema")
        else:
            logger.info(f"Usuario {usuario} de cliente {id_sistema} actualizado")
