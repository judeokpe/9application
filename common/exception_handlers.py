from django.http.response import Http404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import exception_handler
from .responses import CustomErrorResponse


def custom_exception_handler(exc, context):
    try:
        response = exception_handler(exc, context)
        if isinstance(exc, AuthenticationFailed):
            exc_list = str(exc).split("DETAIL: ")
            return CustomErrorResponse({"message": exc_list[-1]}, status=401)
        if response.status_code == 400:
            return CustomErrorResponse({"message": "Invalid Entry", "data": exc.detail})
        elif isinstance(exc, Http404):
            return CustomErrorResponse({"message": "Not found"}, status=404)
        else:
            return CustomErrorResponse(
                {"message": exc.detail}, status=response.status_code
            )
    except Exception as err: 
        return f"{err}"
