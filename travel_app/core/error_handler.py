import logging
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import httpx


def handle_error(e: Exception, logger: logging.Logger, endpoint: str) -> HTTPException:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_type = type(e).__name__
    error_msg = str(e)

    if isinstance(e, HTTPException):
        status_code = e.status_code
        client_detail = e.detail
    elif isinstance(e, OperationalError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        client_detail = f"Database connection error ({endpoint})."
    elif isinstance(e, SQLAlchemyError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        client_detail = f"Database error ({endpoint})."
    elif isinstance(e, (ValueError, KeyError)):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        client_detail = f"Invalid data input ({endpoint}):\n {e}."
    elif isinstance(e, httpx.RequestError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        client_detail = f"External API connection error ({endpoint}):\n {e}."
    elif isinstance(e, httpx.HTTPStatusError):
        status_code = status.HTTP_502_BAD_GATEWAY
        client_detail = f"External API returned error ({endpoint}:\n {e})."
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        client_detail = f"Internal server error ({endpoint})."

    log_line = f"[{now}] - {endpoint} - {status_code} - {error_type}: {error_msg}"

    logger.error(log_line)

    return HTTPException(status_code=status_code, detail=client_detail)
