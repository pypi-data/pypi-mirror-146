from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from firebrick.exceptions.api import BadRequest


ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']


class Endpoint:
    def __init_subclass__(cls):
        cls.methods = {}
        # Registering all the methods in the endpoint so we can quickly check if the endpoint has a method handler
        for method in ALLOWED_METHODS:
            if method in cls.__dict__:
                cls.methods[method] = cls.__dict__[method]

    @classmethod
    @csrf_exempt
    def handler(cls, request, *args, **kwargs):
        # Check if the method is in the endpoint and if not return a not allowed method msg
        if request.method in cls.methods:
            try:
                response = cls.methods[request.method](cls, request, *args, **kwargs)
            except BadRequest as e:
                # Return a function so if the user wants to they can override the function to give custom functionliaty
                return cls.badrequesthandler(e)
            # Check what type the return of the endpoint 
            if type(response) == dict:
                return JsonResponse(response)
            elif type(response) == tuple:
                return JsonResponse(response[0], status=response[1])
            else:
                return response
        else:
            # Return a function so if the user wants a custom response they can override the functions in the endpoint class
            return cls.not_allowed(request, *args, **kwargs)
    
    @classmethod
    def not_allowed(cls, request, *args, **kwargs):
        return JsonResponse({'success': False, 'error_message': 'Method is not allowed.'}, status=405)
    
    @classmethod
    def badrequesthandler(cls, error_msg):
        if type(error_msg) == tuple:
            return JsonResponse({'success': False, 'error_message': str(error_msg[0])}, status=int(error_msg[1]))
        else:
            return JsonResponse({'success': False, 'error_message': str(error_msg)}, status=400)