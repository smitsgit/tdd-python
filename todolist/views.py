from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Create your views here.

def home_page(request: HttpRequest) -> HttpResponse:
    temp_resp = "<html><title>To-Do lists</title></html>"
    response = HttpResponse(temp_resp)
    return response



