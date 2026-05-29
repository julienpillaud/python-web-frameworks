from django.http import HttpRequest, JsonResponse


def custom_handler404(request: HttpRequest, exception: Exception) -> JsonResponse:
    return JsonResponse(data={"detail": "Not Found"}, status=404)
