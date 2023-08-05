from rest_framework.request import Request
from rest_framework.views import APIView
from pgs_backend.ws_cache.middleware import send_set_path_dirty
from functools import wraps
from inspect import signature



class DependentRoutesMixin(APIView):

    cls_dependent_routes = []

    def finalize_response(self, request, response, *args, **kwargs):
        finalized_response = super().finalize_response(request, response, *args, **kwargs)
        if (request.method != "GET" and not request.user.is_anonymous):
            for route in self.cls_dependent_routes:
                send_set_path_dirty(request.user.id, route)
        return finalized_response

def dependent_routes(routes=[], keys=[]):
    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            req_pos = 0
            if isinstance(args[0], Request):
                request = args[0]
            elif isinstance(args[0], Request):
                req_pos = 1
                request = args[1]
            else:
                request = args[0].request
            response = func(*args, **kwargs)
            if request.method != "GET" and not request.user.is_anonymous:
                for route in routes:
                    effective_route = None
                    if callable(route):
                        try:
                            effective_route = route(*args[req_pos+1:])
                        except:
                            pass
                        try:
                            new_args = []
                            for k in keys:
                                new_args.append(kwargs[k])
                            effective_route = route(*new_args)
                        except:
                            pass
                    else:
                        effective_route = route
                    if effective_route:
                        send_set_path_dirty(request.user.id, effective_route)
            return response
        return wrapped_func
    return decorator


