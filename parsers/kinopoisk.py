from bs4 import BeautifulSoup
from parsers.movieparser import MovieParser, MovieDetailParser
import urllib.parse


class KinopoiskParser(MovieParser):
    """Parses https://www.kinopoisk.ru/top/navigator/"""

    def parse_movies(self):
        """Return all divs that contain movie info"""
        soup = super().get_soup()
        result = soup.select("#itemList > div")
        return result

    def parse_title(self, movie):
        return movie.select_one("div.name >a").get_text(strip=True)

    def parse_year(self, movie):
        return list(movie.select_one("div.name >span").stripped_strings)[0]

    def parse_rating(self, movie):
        return float(list(movie.select_one("div.numVote > span").stripped_strings)[0])

    def parse_url(self, movie):
        href = movie.select_one("div.name >a")["href"]
        return urllib.parse.urljoin("https://www.imdb.com/", href)
