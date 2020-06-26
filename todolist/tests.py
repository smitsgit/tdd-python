# Create your tests here.
from django.template.loader import render_to_string
from pytest_django.asserts import assertTemplateUsed
from todolist.models import Item


# def test_bad_math():
#     assert 10 == 15, "Bad math"

def test_home_page_test(client):
    response = client.get('/')
    assertTemplateUsed(response, "home.html")


def test_can_save_a_post(client):
    response = client.post('/', data={'item_text': 'A new item added'})
    assert 'A new item added' in response.content.decode('utf-8')


def test_save_and_retrieve_item(db):
    first_item = Item()
    first_item.text = "Hello Der how are you ?"
    first_item.save()

    second_item = Item()
    second_item.text = "What the fuck is happening ?"
    second_item.save()

    items = Item.objects.all()
    assert items.count() == 2

    first_saved_item = items[0]
    second_saved_item = items[1]
    assert first_saved_item.text == 'Hello Der how are you ?'
    assert second_saved_item.text == 'What the fuck is happening ?'




