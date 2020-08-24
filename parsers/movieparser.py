from bs4 import BeautifulSoup
import urllib.request

from movie.movie import Movie


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

    def parse(self):
        """Return Movies list"""
        result = []
        for i in self.parse_movies():
            rank = self.parse_rank(i)
            title = self.parse_title(i)
            year = self.parse_year(i)
            rating = self.parse_rating(i)
            url = self.parse_url(i)
            result.append(Movie(rank, title, year, rating, url))

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
