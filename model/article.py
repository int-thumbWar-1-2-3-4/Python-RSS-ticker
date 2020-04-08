from datetime import datetime

class Article:
    # TODO: Split Article class into its own file
    # A single rss item, i.e. a single news article.py

    def __init__(self, title: str, link: str, published_date: datetime):
        self.title = title
        self.link = link
        self.published_date = published_date
