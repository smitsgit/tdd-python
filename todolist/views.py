from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .models import Item


def home_page(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text')
        Item.objects.create(text=new_item_text)
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {'list_items': items})
