#!venv/bin/python
from bs4 import BeautifulSoup, Comment


class HTMLParser:
    def __init__(self):
        print("HTMLParser init")

    def parse(self, html_doc):
        soup = BeautifulSoup(html_doc, 'lxml')
        # Remove scripts and styles
        for x in soup.findAll('script', 'style', 'href'):
            x.extract()
        # Avoid commets
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()
        return soup.get_text()
