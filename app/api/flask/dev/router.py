import json
from typing import Annotated

from fast_depends import Depends, inject
from flask import Blueprint, Response, request

from app.api.flask.dependencies import get_context
from app.core.sqlalchemy.context import Context
from app.domain.dev.commands import ItemCreateError, create_item_error_command

router = Blueprint("dev", __name__, url_prefix="/dev")


@router.get("/env")
@inject
def get_env(context: Annotated[Context, Depends(get_context)]) -> Response:
    return Response(
        json.dumps({"environment": context.environment}),
        status=200,
        content_type="application/json",
    )


@router.post("/error")
@inject
def item_error(
    context: Annotated[Context, Depends(get_context)],
) -> Response:
    error_type = request.args["error_type"]
    item_create = ItemCreateError.model_validate(request.get_json())
    item = create_item_error_command(
        context,
        item_create=item_create,
        error_type=error_type,  # ty:ignore[invalid-argument-type]
    )
    return Response(
        response=item.model_dump_json(),
        status=201,
        content_type="application/json",
    )
