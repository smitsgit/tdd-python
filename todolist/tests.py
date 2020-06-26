# Create your tests here.
from django.template.loader import render_to_string
from pytest_django.asserts import assertTemplateUsed


# def test_bad_math():
#     assert 10 == 15, "Bad math"

def test_home_page_test(client):
    response = client.get('/')
    assertTemplateUsed(response, "home.html")
