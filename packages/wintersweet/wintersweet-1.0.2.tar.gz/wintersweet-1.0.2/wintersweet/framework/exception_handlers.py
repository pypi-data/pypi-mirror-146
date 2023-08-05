from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

from wintersweet.framework.response import Response, ErrResponse
from wintersweet.utils.base import Utils


async def http_exception_handler(
        request: Request, exc: HTTPException
) -> Response:

    headers = getattr(exc, r'headers', None)

    Utils.log.error(exc.detail)

    if headers:
        return ErrResponse(
            code=-1,
            status_code=exc.status_code,
            headers=headers
        )
    else:
        return ErrResponse(
            code=-1,
            status_code=exc.status_code
        )


async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
) -> Response:

    return ErrResponse(
        code=-1,
        data=jsonable_encoder(exc.errors()),
        status_code=HTTP_400_BAD_REQUEST,
    )