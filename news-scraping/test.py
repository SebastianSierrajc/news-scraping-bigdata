import unittest
import datetime
from scraping import fetch_newspaper, to_date, set_path

BBC_PATH = 'https://www.bbc.com/'
CNN_PATH = 'https://edition.cnn.com/'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
BUCKET_PATH = 'headlines/raw'

class TestScrapingMethods(unittest.TestCase):

    def test_fetch_newspaper(self):
        bbc_content = fetch_newspaper(BBC_PATH)
        self.assertEqual(type(bbc_content), bytes)

        cnn_content = fetch_newspaper(CNN_PATH)
        self.assertEqual(type(cnn_content), bytes)

    def test_to_date(self):
        date_str = '2022-04-15T18:25:43Z'
        date = to_date(date_str)

        self.assertEqual(type(date), datetime.date)
        self.assertEqual(date.isoformat(), '2022-04-15')
        self.assertEqual(date.year, 2022)
        self.assertEqual(date.month, 4)
        self.assertEqual(date.day, 15)

    def test_set_path(self):
        date = datetime.date(2022, 4, 15)
        bbc_path = 'headlines/raw/newspaper=BBC/year=2022/month=4/day=15/BBC-headlines.html'
        cnn_path = 'headlines/raw/newspaper=CNN/year=2022/month=4/day=15/BBC-headlines.html'
        
        path = set_path('BBC', date, 'BBC-headlines.html')

        self.assertEqual(path, bbc_path);
        self.assertNotEqual(path, cnn_path)


if __name__ == '__main__':
    unittest.main()
