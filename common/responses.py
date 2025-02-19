from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class CustomSuccessResponse(Response):
    def __init__(self, data=None, message=None, status=200, **kwargs):
        resp = {"status": "success", "entity":data, "message":message, "success":True}
        # resp.update(data)
        super().__init__(data=resp, status=status, **kwargs)


class CustomErrorResponse(Response):
    def __init__(self, data=None, message=None, status=400, **kwargs):
        resp = {"status": "failure", "entity":data, "message":message, "success":False}
        # resp.update(data)
        super().__init__(data=resp, status=status, **kwargs)


class SerializerCustomErrorResponse(Response):
    def __init__(self, data={}, message=None, status=403, **kwargs):
        resp = {"status": "failure", "entity":data, "message":message}
        
        raise serializers.ValidationError(resp, status)

class CustomErrorResponseWithStatus(Response):
    def __init__(self, data=None, message=None, status_code=status.HTTP_400_BAD_REQUEST, **kwargs):
        resp = {"status": "failure", "entity": data, "message": message}
        super().__init__(data=resp, status=status_code, **kwargs)

class CustomErrorResponse404(CustomErrorResponseWithStatus):
    def __init__(self, data=None, message=None, **kwargs):
        super().__init__(data=data, message=message, status_code=status.HTTP_404_NOT_FOUND, **kwargs)

class CustomErrorResponse204(CustomErrorResponseWithStatus):
    def __init__(self, data=None, message=None, **kwargs):
        super().__init__(data=data, message=message, status_code=status.HTTP_204_NO_CONTENT, **kwargs)