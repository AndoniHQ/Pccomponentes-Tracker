from django.core.management.base import BaseCommand
from tracker.models import Item
import requests
from bs4 import BeautifulSoup
import smtplib, ssl

def crawl_data(url):

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find('h1').get_text()
        price = soup.find(id='precio-main').get_text()
        clean_price = float(price[0:-1].replace(',','.'))
        return {'title': title, 'last_price':clean_price }

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        items = Item.objects.all()
        for item in items:
            data = crawl_data(item.url)
            if data['last_price'] < item.average_price:
                print(f'Discount for {data["title"]}')
                item_discount = Item.objects.get(id=item.id)
                item_discount.no_iva = data['last_price'] * 0.8264
                item_discount.discount_price = f'DESCUENTO! El precio es {data["last_price"]}'
                item_discount.save()

                gmail_user = ''
                gmail_password = ''

                sent_from = gmail_user
                to = ['']
                subject = 'BAJADA DE PRECIO - ' + item.title
                body = 'PRECIO: ' + str(item.last_price) + '\n' + 'Link: ' + item.url + '\n'

                
                msg = f"Subject: {subject}\n\n{body}"

                try:
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.ehlo()
                    server.login(gmail_user, gmail_password)
                    server.sendmail(sent_from, to, msg.encode("utf8"))
                    server.close()

                    print('Email sent!')
                except: 
                    print('Something went wrong...')

            elif data['last_price'] >= item.average_price:
                item_discount = Item.objects.get(id=item.id)
                item_discount.no_iva = data['last_price'] * 0.8264
                item_discount.discount_price = "No dispone de descuento"
                item_discount.save()
                


    
