from bs4 import BeautifulSoup
import urllib.request

from movie.movie import Movie, DetailedMovie


class MovieParser:
    """
    Base class for movie parsers
    Parsers should implement parsing movie list tags and all info from that tags
    """

    def __init__(self, url):
        self.url = url

    def get_soup(self):
        """Return BeautifulSoup by url"""
        req = urllib.request.urlopen(self.url)
        html = req.read()
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def get_movie(self, movie_html, rank):
        """Return Movie"""
        title = self.parse_title(movie_html)
        year = self.parse_year(movie_html)
        rating = self.parse_rating(movie_html)
        url = self.parse_url(movie_html)
        return Movie(rank, title, year, rating, url)

    def parse(self):
        """Return Movies list"""
        # First we parse all tags that contain movie info and then convert them to Movie objects
        result = []
        for rank, movie_html in enumerate(self.parse_movies(), start=1):
            result.append(self.get_movie(movie_html, rank))

        return result

    def parse_movies(self):
        """Return tags that contain movie info"""
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
    def get_movie(self, soup, rank=None):
        """Return DetailedMovie"""
        movie = super().get_movie(soup, rank)
        details = self.parse_additional_info(soup)
        return DetailedMovie(movie, details)

    def parse(self):
        """Return DetailedMovie"""
        return self.get_movie(self.parse_movies())

    def parse_movies(self):
        """Return html that contain info about movie"""
        # Because all info about movie is on page we return soup
        return self.get_soup()

    def parse_additional_info(self, soup):
        """Return parsed movie details"""
        raise NotImplementedError
