CREATE EXTERNAL TABLE news_headlines(
    title string,
    url string,
    category string
)
PARTITIONED BY (newspaper string, year int, month int, day int)
ROW FORMAT DELIMITED
    fields terminated by ","
    escaped by "\\"
    lines terminated by "\n"
LOCATION
    "s3://news-scraping-bucket/news/final/"
TBLPROPERTIES ("skip.header.line.count"="1");
