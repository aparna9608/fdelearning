import logging
import time
import uuid

from fastapi import Request

from request_context import request_id_context

logger = logging.getLogger(__name__)


async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())

    request_id_context.set(request_id)

    start_time = time.perf_counter()

    logger.info(
        "%s | %s %s | started",
        request_id,
        request.method,
        request.url.path
    )

    try:
        response = await call_next(request)

        duration = time.perf_counter() - start_time
        duration_ms = round(duration * 1000, 2)

        logger.info(
            "%s | %s %s | status=%s | duration=%sms",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms
        )

        response.headers["X-Request-ID"] = request_id

        return response

    except Exception:
        duration = time.perf_counter() - start_time
        duration_ms = round(duration * 1000, 2)

        logger.exception(
            "%s | %s %s | failed | duration=%sms",
            request_id,
            request.method,
            request.url.path,
            duration_ms
        )

        raise