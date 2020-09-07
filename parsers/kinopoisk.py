from bs4 import BeautifulSoup
from parsers.movieparser import MovieParser, MovieDetailParser
import urllib.parse
import re


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
        return re.search(r"\([1, 2].*\)",
                         list(movie.select_one("div.name >span").stripped_strings)[0]).group(0)

    def parse_rating(self, movie):
        return float(list(movie.select_one("div.numVote > span").stripped_strings)[0])

    def parse_url(self, movie):
        href = movie.select_one("div.name >a")["href"]
        return urllib.parse.urljoin("https://www.kinopoisk.ru/", href)


class KinopoiskDetailParser(MovieDetailParser):
    """Parses https://www.kinopoisk.ru/film/"""

    @staticmethod
    def _search_link_href_startswith(soup, strings):
        """Return first <a> whose href starts with given strings"""
        links = soup.select("a")
        result = None
        for link in links:
            href = link["href"]
            if href.startswith(strings):
                result = link.get_text(strip=True)
                break
        return result

    def parse_title(self, soup):
        # Title is in h1
        return soup.select_one("h1 > span").get_text(strip=True)

    def parse_year(self, soup):
        # Year href starts with /lists/navigator/2 or lists/navigator/1
        return self._search_link_href_startswith(soup, ("/lists/navigator/2", "lists/navigator/1"))

    def parse_rating(self, soup):
        return float(soup.select_one("span.film-rating-value").get_text(strip=True))

    def parse_url(self, soup):
        return self.url

    def parse_additional_info(self, soup):
        details = dict()
        details["poster_url"] = soup.select_one("img.film-poster")["src"]
        details["ratings_count"] = int(soup
                                       .select_one(".styles_ratingContainer__24Wyy span.styles_count__3hSWL")
                                       .get_text(strip=True).replace(",", "").replace(" ", ""))

        # Details are in div.styles_row__2ee6F
        details_html = soup.select("div.styles_row__2ee6F")

        def search_detail(string, details_html):
            """Get details from html"""
            for detail in details_html:
                if detail.div.get_text(strip=True) == string:
                    return detail
            return None

        # Add time
        time = search_detail("Время", details_html)
        if time:
            details["time"] = time.select_one(".styles_value__2F1uj").get_text(strip=True)

        # Add genres
        genres = search_detail("Жанр", details_html)
        if genres:
            details["genres"] = [i.get_text(strip=True)
                                 for i in genres.select("a") if i["href"].startswith("/lists/")]

        # Add release date
        release_date = search_detail("Премьера в мире", details_html)
        if release_date:
            details["release_date"] = release_date.find("a", attrs={"data-tid": True}).get_text(strip=True)

        # Add directors
        directors = search_detail("Режиссер", details_html)
        if directors:
            details["directors"] = [i.get_text(strip=True)
                                    for i in directors.select("a") if i["href"].startswith("/name/")]

        # Add writers
        writers = search_detail("Сценарий", details_html)
        if directors:
            details["writers"] = [i.get_text(strip=True)
                                  for i in writers.select("a") if i["href"].startswith("/name/")]

        # Add stars
        stars = soup.select_one(".styles_actors__2zt1j").select("li > a")
        details["stars"] = [i.get_text(strip=True) for i in stars]

        # Add storyline
        storyline = soup.select_one(".styles_filmSynopsis__zLClu > p")
        if storyline:
            details["storyline"] = storyline.get_text(strip=True)

        # Add budget and worldwide gross
        budget = search_detail("Бюджет", details_html)
        if budget:
            details["budget"] = budget.select_one(".styles_value__2F1uj").get_text(strip=True).replace("\xa0", "")

        worldwide_gross = search_detail("Сборы в мире", details_html)
        if worldwide_gross:
            # Remove everything before =
            s = worldwide_gross.select_one(".styles_value__2F1uj > a").get_text(strip=True).replace("\xa0", "")
            i = s.index("=")
            details["worldwide_gross"] = s[i + 2:]

        return details
