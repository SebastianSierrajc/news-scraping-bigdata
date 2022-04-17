import datetime
import re
import boto3
import pandas
import json
from urllib.parse import unquote
from bs4 import BeautifulSoup


BBC_PATH = 'https://www.bbc.com'
CNN_PATH = 'https://edition.cnn.com'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
BUCKET = 'news-scraping-bucket'
BUCKET_PATH = 'news/final'

def handler(event, context):
    event_data = event['Records'][0]
    trigger_date = event_data['eventTime']
    date = to_date(trigger_date)

    try:
        key = event_data["s3"]["object"]["key"]
        key = unquote(key)
        newspaper = set_newspaper(key)
        data = get_data(BUCKET, key)
        soup = soup_data(data)
        news = process_soup(newspaper, soup)
        path = set_path(newspaper, date, f'{newspaper}-news.csv')
        save_data(news, path)
    except Exception as e:
        print(e)
        print('Error processing data')

def to_date(date_str: str) -> datetime.date:
    date_time = datetime.datetime.strptime(date_str, DATE_FORMAT)
    return date_time.date()


def set_newspaper(key: str) -> str:
    a = re.search("newspaper=(\w+)/", key)
    return a.group(1)

def set_path(newspaper: str, date: datetime.date, file_name: str) -> str:
    news_paper = f"newspaper={newspaper}"
    year = f"year={date.year}"
    month = f"month={date.month}"
    day = f"day={date.day}"

    path = f"{BUCKET_PATH}/{news_paper}/{year}/{month}/{day}/{file_name}"
    return path

def get_data(bucket: str, key: str):
    s3 = boto3.resource('s3')
    s3Obj = s3.Object(bucket, key)
    res = s3Obj.get()
    return res['Body']

def soup_data(data: bytes):
    soup = BeautifulSoup(data, 'html.parser')
    return soup

def process_soup(newspaper, soup):
    if newspaper == 'BBC':
        return process_soup_bbc(soup)
    
    if newspaper == 'CNN':
        return process_soup_cnn(soup)

def process_soup_bbc(soup):
    news = []
    medias = soup.find_all('div', class_='media')
    for media in medias:
        link = media.find('a', class_='media__link')
        if link:
            tag = media.find('a', class_='media__tag').string.strip()
            url = link.get('href')
            url = format_url(BBC_PATH, url)
            title = link.string.strip()
            news.append({'title': title, 'url': url, 'category': tag})
    return news

def process_soup_cnn(soup):
    news = []
    scripts = soup.find_all("script")
    for script in scripts:
        s = script.get_text()
        se = re.search('"articleList":(\[.+?\])', s)
        if se:
            articles = se.group(1)
            articles = json.loads(articles)
            for article in articles:
                cat_search = re.search("\/\d+\/\d+\/\d+\/(\w+)\/", article['uri'])
                category = cat_search.group(1) if cat_search else 'news'
                news.append({
                    'title': article['headline'],
                    'url': format_url(CNN_PATH, article['uri']),
                    'category': category
                })
    return news

def save_data(data, path):
    s3 = boto3.resource('s3')
    s3Obj = s3.Object(BUCKET, path)
    df = pandas.DataFrame.from_dict(data)
    body = bytes(df.to_csv(index=False), encoding='utf-8')
    return s3Obj.put(Body=body)

format_url = lambda path, url: url if re.match(path, url) else path + url


