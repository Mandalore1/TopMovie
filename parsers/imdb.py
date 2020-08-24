from bs4 import BeautifulSoup
import urllib.request
from movie.movie import Movie


class IMDBParser:
    """Parses https://www.imdb.com/search/title/"""
    def __init__(self, url):
        self.url = url

    def parse(self):
        """Returns parsed Movie objects"""
        req = urllib.request.urlopen(self.url)
        html = req.read()
        soup = BeautifulSoup(html, "html.parser")
        movies = soup.find_all("h3", class_="lister-item-header")

        result = []
        for i in movies:
            rank = int(i.find("span", class_="lister-item-index").get_text(strip=True).strip("."))
            title = i.find("a").get_text(strip=True)
            year = int(i.find("span", class_="lister-item-year").get_text(strip=True).strip("()"))
            result.append(Movie(rank, title, year))

        return result
