import requests
import boto3
import datetime


BBC_PATH = 'https://www.bbc.com/'
CNN_PATH = 'https://edition.cnn.com/'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
BUCKET = 'news-scraping-bucket'
BUCKET_PATH = 'headlines/raw'

def handler(event, context):
    trigger_date = event['time']
    date = to_date(trigger_date)

    try:
        content = fetch_news_paper(BBC_PATH)
        file_path = set_path('BBC', date, 'BBC-HEADLINES.html')
        save_data(content, file_path)
    except:
        print('Error while scraping BBC headlines.')

    
    try:
        content = fetch_news_paper(CNN_PATH)
        file_path = set_path('CNN', date, 'CNN-HEADLINES.html')
        save_data(content, file_path)
    except:
        print('Error while scraping BBC headlines.')


def fetch_news_paper(path: str) -> bytes:
    req = requests.get(path)
    if req.ok:
        return req.content
    else:
        print(f'fetch data from {path} failed with code {req.status_code}')
        raise Exception(f'fetch data from {path} failed with code {req.status_code}')

def to_date(date_str: str) -> datetime.date:
    date_time = datetime.datetime.strptime(date_str, DATE_FORMAT)
    return date_time.date()

def set_path(newspaper: str, date: datetime.date, file_name: str) -> str:
    news_paper = f"newspaper={newspaper}"
    year = f"year={date.year}"
    month = f"month={date.month}"
    day = f"day={date.day}"

    path = f"{BUCKET_PATH}/{news_paper}/{year}/{month}/{day}/{file_name}"
    return path

def save_data(content: bytes, path) -> dict:
    s3 = boto3.resource('s3')
    s3Obj = s3.Object(BUCKET, path)
    return s3Obj.put(Body=content)


