from fastapi import status

from app.domain.exceptions import (
    BadRequestError,
    ConflictError,
    DomainError,
    ForbiddenError,
    NotFoundError,
    UnprocessableContentError,
)

ERROR_MAPPING: dict[type[DomainError], int] = {
    BadRequestError: status.HTTP_400_BAD_REQUEST,
    ForbiddenError: status.HTTP_403_FORBIDDEN,
    NotFoundError: status.HTTP_404_NOT_FOUND,
    ConflictError: status.HTTP_409_CONFLICT,
    UnprocessableContentError: status.HTTP_422_UNPROCESSABLE_CONTENT,
}
