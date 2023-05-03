import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep



headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0', 'Accept-Language': 'en-US, en;q=0.5' }

search_query= 'laptops'.replace(' ','+')
base_url = f'https://www.amazon.com/s?k={search_query}'

items=[]
for i in range (1, 5):
    print(f'Processing{i}...'+ base_url + f'&page={i}')
    response= requests.get(base_url + '&page={0}'.format(i),headers=headers)
    soup= BeautifulSoup (response.content, 'html.parser')

    results= soup.find_all ('div',{'class': 's-resukt-item','data-component-type': 's_search_result'})

    for result in results:
        product_name=result.h2.text

        try:
            rating=result.find('i',{'class': 'a-icon'}).text
            rating_count=result.find_all('span',{'aria-label': True})[1].text
        except ArithmeticError:
            continue

        try:
            price1= result.find('span',{'class': 'a-price-whole'}.text)
            price2= result.find('span',{'class': 'a-price-fraction'}.text)
            price=price1+price2
            product_url='https://amzon.com'+result.h2.a['href']
            #print(rating_count, product_url)
            items.append([product_name, rating, rating_count, price, product_url])
        except AttributeError:
            continue
        sleep(1.5)

df=pd.DataFrame(items, columns=['product','rating','rating count', 'price', 'product url'])
print(df)
df.to_excel(f'{search_query}.xlsx')