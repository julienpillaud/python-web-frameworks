from typing import Annotated, Any, Literal

from fastapi import APIRouter, Depends, status

from app.api.fastapi.dependencies import get_context
from app.core.settings import AppEnvironment
from app.core.sqlalchemy.context import Context
from app.domain.dev.commands import ItemCreateError, create_item_error_command
from app.domain.items.entities import Item

router = APIRouter(prefix="/dev")


@router.get("/env")
def get_env(
    context: Annotated[Context, Depends(get_context)],
) -> dict[str, AppEnvironment]:
    return {"environment": context.environment}


@router.post("/error", response_model=Item, status_code=status.HTTP_201_CREATED)
def item_error(
    item_create: ItemCreateError,
    context: Annotated[Context, Depends(get_context)],
    error_type: Literal["domain", "unexpected"] | None = None,
) -> Any:
    return create_item_error_command(
        context,
        item_create=item_create,
        error_type=error_type,
    )
