from typing import Annotated

from fast_depends import Depends

from app.api.dependencies import get_settings
from app.core.django.context import Context
from app.core.settings import Settings


def get_context(settings: Annotated[Settings, Depends(get_settings)]) -> Context:
    return Context(settings=settings)
