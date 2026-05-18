from django.http import HttpRequest
from pydantic import BaseModel


class EnhancedHttpRequest[T: BaseModel](HttpRequest):
    validated_data: T
