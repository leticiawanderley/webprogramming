from rest_framework.views import exception_handler
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None and not response.status_code:
    	if response.data[0] == "It's not possible to update actors in this state.":
    		response.status_code= status.HTTP_406_NOT_ACCEPTABLE
    	elif response.data[0] == "It's not possible to update the director in this state.":
    		response.status_code= status.HTTP_406_NOT_ACCEPTABLE
    return response