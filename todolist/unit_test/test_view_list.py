import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_uses_list_template(client):
    response = client.get('/lists/the-only-list-in-the-world/')
    assertTemplateUsed(response, 'list.html')
