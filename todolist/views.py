from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .models import Item


def home_page(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world')
    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'list_items': items})
