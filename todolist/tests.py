# Create your tests here.
from django.http import HttpRequest, HttpResponse
from django.urls import resolve
from todolist.views import home_page


# def test_bad_math():
#     assert 10 == 15, "Bad math"

def test_home_page_test():
    request = HttpRequest()
    response: HttpResponse = home_page(request)
    html = response.content.decode('utf-8')
    assert html.startswith('<html>'), "Failed to start with <html>"
    assert "<title>To-Do lists</title>" in html
    assert html.endswith("</html>")
