from bs4 import BeautifulSoup
import urllib.request

from movie.movie import Movie


class MovieParser:
    def __init__(self, url):
        self.url = url

    def get_soup(self):
        req = urllib.request.urlopen(self.url)
        html = req.read()
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def parse(self):
        result = []
        for i in self.parse_movies():
            rank = self.parse_rank(i)
            title = self.parse_title(i)
            year = self.parse_year(i)
            rating = self.parse_rating(i)
            result.append(Movie(rank, title, year, rating))

        return result

    def parse_movies(self):
        raise NotImplementedError

    def parse_rank(self, movie):
        raise NotImplementedError

    def parse_title(self, movie):
        raise NotImplementedError

    def parse_year(self, movie):
        raise NotImplementedError

    def parse_rating(self, movie):
        raise NotImplementedError
