from bs4 import BeautifulSoup
import urllib.request

from movie.movie import Movie, DetailedMovie


class MovieParser:
    """Base class for movie parsers"""

    def __init__(self, url):
        self.url = url

    def get_soup(self):
        """Return BeautifulSoup by url"""
        req = urllib.request.urlopen(self.url)
        html = req.read()
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def get_movie(self, movie_html):
        """Return Movie"""
        rank = self.parse_rank(movie_html)
        title = self.parse_title(movie_html)
        year = self.parse_year(movie_html)
        rating = self.parse_rating(movie_html)
        url = self.parse_url(movie_html)
        return Movie(rank, title, year, rating, url)

    def parse(self):
        """Return Movies list"""
        result = []
        for movie_html in self.parse_movies():
            result.append(self.get_movie(movie_html))

        return result

    def parse_movies(self):
        """Return parsed movies"""
        raise NotImplementedError

    def parse_rank(self, movie):
        """Return parsed rank"""
        raise NotImplementedError

    def parse_title(self, movie):
        """Return parsed title"""
        raise NotImplementedError

    def parse_year(self, movie):
        """Return parsed year"""
        raise NotImplementedError

    def parse_rating(self, movie):
        """Return parsed rating"""
        raise NotImplementedError

    def parse_url(self, movie):
        """Return parsed url"""
        raise NotImplementedError


class MovieDetailParser(MovieParser):
    """Base class for detailed movie parsers"""
    def get_movie(self, soup):
        """Return DetailedMovie"""
        movie = super().get_movie(soup)
        details = self.parse_additional_info(soup)
        return DetailedMovie(movie, details)

    def parse(self):
        """Return DetailedMovie"""
        return self.get_movie(self.parse_movies())

    def parse_movies(self):
        """Return soup"""
        return self.get_soup()

    def parse_additional_info(self, soup):
        """Return parsed movie details"""
        raise NotImplementedError
