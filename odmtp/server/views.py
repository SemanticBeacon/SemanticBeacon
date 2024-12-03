from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods, require_http_methods

# Default endpoint
@require_http_methods(["GET"])
def hello_world(request):
    response = HttpResponse("You need to choose a different endpoint :)", content_type="text/plain; charset=utf-8")
    response["Access-Control-Allow-Origin"] = "*"
    return response
