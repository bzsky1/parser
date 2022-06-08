import requests
import csv
from bs4 import BeautifulSoup as BS
from time import sleep

CSV = 'posts.csv'
HOST = 'https://scrapingclub.com'
URL = 'https://scrapingclub.com/exercise/list_basic/?page=1'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BS(html, 'lxml')
    items = soup.find_all('div', class_='col-lg-4 col-md-6 mb-4')
    posts = []

    for item in items:
        posts.append(
            {
                'title': item.find('h4', class_='card-title').text.replace('\n', ''),
                'price': item.find('h5').text,
                'link': HOST + item.find('a').get('href'),
                'image': HOST + item.find('img', class_='card-img-top img-fluid').get('src')
            }
        )
    return posts

def save_in_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Title', 'Price', 'Link', 'Image'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['link'], item['image']])

def how_many_pages_parser():
    PAGINATION = input("How many pages You want me to pars?: ")
    PAGINATION = int(PAGINATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        posts = []
        for page in range(1, PAGINATION + 1):

            sleep(4) # Slowing down the process to hide that it is not a human

            print(f'Parsing of page № {page}')
            html = get_html(URL, params={'page': page})
            posts.extend(get_content(html.text))
            save_in_doc(posts, CSV)
    else:
        print('Error :(')

how_many_pages_parser()