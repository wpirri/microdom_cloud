from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id

logger = get_daily_logger()

def get_user_auth(user, password):
    if user is None or password is None:
        return None
    logger.info(f"[get_user_auth] User: {user} Password: {password}")

    return {"key":"auth_token", "value": "uHvt5rOP"}

def auth_token_valid(auth_token):
    logger.info(f"[auth_token_valid] Token: {auth_token}")

    if auth_token == "uHvt5rOP":
        return "D3S4RR0LL0-0001"
    else:
        return None
    