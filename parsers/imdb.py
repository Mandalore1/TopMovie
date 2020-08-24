from bs4 import BeautifulSoup
from parsers.movieparser import MovieParser
import urllib.parse


class IMDBParser(MovieParser):
    """Parses https://www.imdb.com/search/title/"""

    def parse_movies(self):
        soup = super().get_soup()
        return soup.find_all("div", class_="lister-item")

    def parse_rank(self, movie):
        return int(movie.find("span", class_="lister-item-index").get_text(strip=True).strip("."))

    def parse_title(self, movie):
        return movie.find("h3").find("a").get_text(strip=True)

    def parse_year(self, movie):
        return int(movie.find("span", class_="lister-item-year").get_text(strip=True).strip("()"))

    def parse_rating(self, movie):
        return float(movie.find("div", class_="ratings-imdb-rating").get_text(strip=True))

    def parse_url(self, movie):
        href = movie.find("h3").find("a").get("href")
        return urllib.parse.urljoin("https://www.imdb.com/", href)
