class Article:
    # TODO: Split Article class into its own file
    # A single rss item, i.e. a single news article.py

    def __init__(self, title: str, link: str, datetime):
        self.title = title
        self.link = link
        self.datetime = datetime    # time.struct_time object
