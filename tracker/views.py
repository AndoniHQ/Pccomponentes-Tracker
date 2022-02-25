from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect 
import requests
from bs4 import BeautifulSoup
from .models import Item
from .forms import AddNewItemForm

def tracker_view(request):
    items = Item.objects.order_by('-id')
    form = AddNewItemForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            url = form.cleaned_data.get('url')
            crawled_data = crawl_data(url)
            Item.objects.create(
            url = url,
            title = crawled_data['title'],
            average_price= crawled_data['last_price'],
            last_price=crawled_data['last_price'],
            no_iva=crawled_data['last_price'] * 0.8264,
            discount_price='No dispone de descuento',
            )
            return HttpResponseRedirect('/')
        else:
            form = AddNewItemForm()
    context = {
        'items':items,
        'form':form,
    }
    return render(request, 'tracker.html', context)

def crawl_data(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find('h1').get_text()
    price = soup.find(id='precio-main').get_text()
    clean_price = float(price[0:-1].replace(',','.'))
    return {'title': title, 'last_price':clean_price }