use default;

show tables;

SELECT newspaper, year, month, day, category, title 
FROM news_headlines;

SELECT newspaper, year, month, day, category, title 
FROM news_headlines
WHERE newspaper='BBC';


SELECT newspaper, year, month, day, category, title 
FROM news_headlines
WHERE year = 2022 AND month = 4 AND day >= 1 AND day <= 31; 

SELECT category, count(category) as news
FROM news_headlines
GROUP BY category
ORDER BY news DESC;

SELECT newspaper, count(newspaper) as news
FROM news_headlines
GROUP BY newspaper
ORDER BY news DESC;
