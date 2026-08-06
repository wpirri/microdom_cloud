from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id
from app.client_utils import enqueue_action

logger = get_daily_logger()

def alexa_discover(system):
    return mysql_query(f"SELECT Id, Objeto, Tipo, Grupo_Visual, Icono_Apagado FROM TB_DOMCLOUD_ASSIGN WHERE System_Key = '{system}' AND Id > 0;")
    
def alexa_turn_on(system, objeto):
    enqueue_action(system, objeto, action="ON")
    return None

def alexa_turn_off(system, objeto):
    enqueue_action(system, objeto, action="OFF")
    return None

def alexa_turn_lock(system, objeto):
    return None

def alexa_turn_unlock(system, objeto):
    enqueue_action(system, objeto, action="PULSE")
    return None

def alexa_turn_report_state(system, objeto):
    return mysql_query(
        f"SELECT Id, Objeto, Estado, Grupo_Visual, "
        f"FROM_UNIXTIME(Time_Stamp, '%Y-%m-%d %H:%i:%s') AS Ultimo_Update "
        f"FROM TB_DOMCLOUD_ASSIGN WHERE System_Key = '{system}' AND UPPER(Objeto) = UPPER('{objeto}') AND Id > 0;"
    )