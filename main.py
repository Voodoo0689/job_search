import json

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def get_first_news():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.75"
    }
    url = "https://habr.com/ru/all/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("article", class_="tm-articles-list__item")
    news_dict = {}

    for article in articles_cards:

        article_title = article.find("h2", class_="tm-article-snippet__title tm-article-snippet__title_h2").text.strip()
        article_author = article.find("a", class_="tm-user-info__username").text.strip()
        article_date = datetime.strptime(article.find("time").get("datetime"), "%Y-%m-%dT%H:%M:%S.000%z")
        article_sub_title = article.find("span", class_="tm-article-snippet__hubs-item").text.strip()
        article_url = f'https://habr.com{article.find("a", class_="tm-article-snippet__title-link").get("href")}'
        article_id = article_url.split('/')[:-1][-1]
        try:
            article_desc = article.find("div", class_="article-formatted-body article-formatted-body article-formatted-body_version-2").text.strip()
            news_dict[article_id] = {
                'article_title': article_title,
                'article_sub_title': article_sub_title,
                'article_author': article_author,
                'article_date': f'{str(article_date.date())}, {str(article_date.time())}',
                'article_desc': article_desc,
                'article_url': article_url,
            }
        except AttributeError:
            news_dict[article_id] = {
                'article_title': article_title,
                'article_sub_title': article_sub_title,
                'article_author': article_author,
                'article_date': f'Date {str(article_date.date())}, Time {str(article_date.time())}',
                'article_desc': 'No description',
                'article_url': article_url,
            }

        with open("news_dict.json", "w") as file:
            json.dump(news_dict, file, indent=4, ensure_ascii=False)
    print(len(news_dict))


def check_news_update():
    with open('news_dict.json') as file:
        news_dict = json.load(file)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.75"
    }
    url = "https://habr.com/ru/all/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("article", class_="tm-articles-list__item")
    fresh_news = {

    }

    for article in articles_cards:
        article_url = f'https://habr.com{article.find("a", class_="tm-article-snippet__title-link").get("href")}'
        article_id = article_url.split('/')[:-1][-1]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("h2",
                                         class_="tm-article-snippet__title tm-article-snippet__title_h2").text.strip()
            article_author = article.find("a", class_="tm-user-info__username").text.strip()
            article_date = datetime.strptime(article.find("time").get("datetime"), "%Y-%m-%dT%H:%M:%S.000%z")
            article_sub_title = article.find("span", class_="tm-article-snippet__hubs-item").text.strip()
            try:
                article_desc = article.find("div",
                                            class_="article-formatted-body article-formatted-body article-formatted-body_version-2").text.strip()
                news_dict[article_id] = {
                    'article_title': article_title,
                    'article_sub_title': article_sub_title,
                    'article_author': article_author,
                    'article_date': f'{str(article_date.date())}, {str(article_date.time())}',
                    'article_desc': article_desc,
                    'article_url': article_url,
                }
                fresh_news[article_id] = {
                    'article_title': article_title,
                    'article_sub_title': article_sub_title,
                    'article_author': article_author,
                    'article_date': f'{str(article_date.date())}, {str(article_date.time())}',
                    'article_desc': article_desc,
                    'article_url': article_url,
                }
            except AttributeError:
                news_dict[article_id] = {
                    'article_title': article_title,
                    'article_sub_title': article_sub_title,
                    'article_author': article_author,
                    'article_date': f'Date {str(article_date.date())}, Time {str(article_date.time())}',
                    'article_desc': 'No description',
                    'article_url': article_url,
                }
                fresh_news[article_id] = {
                    'article_title': article_title,
                    'article_sub_title': article_sub_title,
                    'article_author': article_author,
                    'article_date': f'{str(article_date.date())}, {str(article_date.time())}',
                    'article_desc': 'No description',
                    'article_url': article_url,
                }
    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    # get_first_news()
    print(check_news_update())


if __name__ == '__main__':
    main()

