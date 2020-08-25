from bs4 import BeautifulSoup
from parsers.movieparser import MovieParser, MovieDetailParser
import urllib.parse


class IMDBParser(MovieParser):
    """Parses https://www.imdb.com/search/title/"""

    def parse_movies(self):
        """Return all divs that contain movie info"""
        soup = super().get_soup()
        return soup.find_all("div", class_="lister-item")

    def parse_title(self, movie):
        return movie.find("h3").find("a").get_text(strip=True)

    def parse_year(self, movie):
        result = movie.find("span", class_="lister-item-year").get_text(strip=True)
        # Remove all non-digits
        result = "".join([i for i in result if i.isdigit()])
        return int(result)

    def parse_rating(self, movie):
        return float(movie.find("div", class_="ratings-imdb-rating").get_text(strip=True))

    def parse_url(self, movie):
        href = movie.find("h3").find("a").get("href")
        return urllib.parse.urljoin("https://www.imdb.com/", href)


class IMDBDetailParser(MovieDetailParser):
    """Parses https://www.imdb.com/title/"""

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
        details["poster_url"] = soup.select_one("div.poster img")["src"]
        details["ratings_count"] = int(soup.find("span", itemprop="ratingCount").get_text(strip=True).replace(",", ""))

        # Add time
        time = soup.select_one("div.subtext time")
        if time:
            details["time"] = time.get_text(strip=True)

        # Add genres
        # Release date may also select to genres
        details["genres"] = [i.get_text(strip=True) for i in soup.select("div.subtext a")]

        # Add release date
        # Pop release date from genres
        try:
            if not details["genres"][-1].isalpha():  # Genre can not contain digit
                details["release_date"] = details["genres"].pop()
        except IndexError:  # If release date and genres does not exist on page
            pass

        # Add credits
        credits = soup.find_all("div", class_="credit_summary_item")

        # Function to add credit info to details
        def add_credit(credit, name, details):
           details[name] = [i.get_text(strip=True) for i in credit.find_all("a") if i["href"].startswith("/name")]

        for credit in credits:
            text = credit.get_text(strip=True)
            if text.find("Director") != -1:
                add_credit(credit, "directors", details)
            elif text.find("Writer") != -1:
                add_credit(credit, "writers", details)
            elif text.find("Star") != -1:
                add_credit(credit, "stars", details)

        # Add storyline
        storyline = soup.select_one("#titleStoryLine p")
        if storyline:
            details["storyline"] = storyline.get_text(strip=True)

        txt_blocks = soup.select("div.txt-block")
        # Add budget and worldwide gross
        for block in txt_blocks:
            text = block.get_text(strip=True)
            if text.find("Budget") != -1:
                details["budget"] = "".join([i for i in text if i.isdigit()])
            if text.find("Cumulative Worldwide Gross") != -1:
                details["worldwide_gross"] = "".join([i for i in text if i.isdigit()])

        return details
