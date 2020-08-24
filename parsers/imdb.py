from bs4 import BeautifulSoup
from parsers.movieparser import MovieParser, MovieDetailParser
import urllib.parse


class IMDBParser(MovieParser):
    """Parses https://www.imdb.com/search/title/"""

    def parse_movies(self):
        """Return all divs that contain movie info"""
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


class IMDBDetailParser(MovieDetailParser):
    """Parses https://www.imdb.com/title/"""

    def parse_rank(self, soup):
        return None

    def parse_title(self, soup):
        return list(
            soup.find("h1").stripped_strings
        )[0]

    def parse_year(self, soup):
        return int(soup.find(id="titleYear").find("a").get_text(strip=True))

    def parse_rating(self, soup):
        return float(soup.find("span", itemprop="ratingValue").get_text(strip=True).replace(",", "."))

    def parse_url(self, soup):
        return self.url

    def parse_additional_info(self, soup):
        details = dict()
        details["ratings_count"] = int(soup.find("span", itemprop="ratingCount").get_text(strip=True).replace(",", ""))
        return details
