from flask import Blueprint, Response, request

from app.api.flask.dependencies import get_context
from app.domain.dev.commands import ItemCreateError, create_item_error_command

router = Blueprint("dev", __name__, url_prefix="/dev")


@router.post("/error")
def item_error() -> Response:
    error_type = request.args["error_type"]
    context = get_context()
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
