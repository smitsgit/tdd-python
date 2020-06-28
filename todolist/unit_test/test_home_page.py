# Create your tests here.
import pytest
from django.template.loader import render_to_string
from pytest_django.asserts import assertTemplateUsed
from todolist.models import Item


# def test_bad_math():
#     assert 10 == 15, "Bad math"

@pytest.mark.django_db
def test_home_page_test(client):
    response = client.get('/')
    assertTemplateUsed(response, "home.html")


@pytest.mark.django_db
def test_only_saves_when_necessary(client):
    client.get('/')
    assert Item.objects.count() == 0


@pytest.mark.django_db
def test_can_save_a_post(client):
    response = client.post('/', data={'item_text': 'A new item added'})
    assert Item.objects.count() == 1, "More items found than expected"
    new_item = Item.objects.first()
    assert new_item.text == 'A new item added'

    assert response.status_code == 302
    assert response['location'] == '/'


@pytest.mark.django_db
def test_redirect_after_post(client):
    response = client.post('/', data={'item_text': 'A new item added'})
    assert response.status_code == 302
    assert response['location'] == '/lists/the-only-list-in-the-world'


@pytest.mark.django_db
def test_displays_all_items_after_post(client):
    client.post('/', data={'item_text': 'Item-1'})
    client.post('/', data={'item_text': 'Item-2'})

    response = client.get('/lists/the-only-list-in-the-world')
    assert 'Item-1' in response.content.decode('utf-8')
    assert 'Item-2' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_displays_all_items(client):
    client.post('/', data={'item_text': 'Item-1'})
    client.post('/', data={'item_text': 'Item-2'})

    response = client.get('/lists/the-only-list-in-the-world/')
    assert 'Item-1' in response.content.decode('utf-8'), f"Expected 200 but Got: {response.status_code}"
    assert 'Item-2' in response.content.decode('utf-8'), f"Expected 200 but Got: {response.status_code}"


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
