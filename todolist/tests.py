# Create your tests here.
from django.urls import resolve
from todolist.views import home_page


# def test_bad_math():
#     assert 10 == 15, "Bad math"

def test_home_page_test():
    found = resolve('/')
    print(found.func)
    assert found.func is home_page
