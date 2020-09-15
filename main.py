"""Main file used for debugging"""
import sqlite3
from parsers.imdb import IMDBParser, IMDBDetailParser
from parsers.kinopoisk import KinopoiskParser, KinopoiskDetailParser
from movie.movie import Movie

LIST_URL_IMDB = "https://www.imdb.com/search/title/?sort=user_rating,desc&title_type=feature&num_votes=25000,"
LIST_URL_KINOPOISK = "https://www.kinopoisk.ru/top/navigator/m_act[years]/1900%3A2020/order/rating/"
DETAIL_URL_IMDB = "https://www.imdb.com/title/tt0111161/?ref_=adv_li_tt"
DETAIL_URL_KINOPOISK = "https://www.kinopoisk.ru/film/535341/?from_block=main_recommend"


def get_choice(message, choices, options):
    """
    Get user choice from given choices
    choices is a list of user choices
    options is a tuple of int that contain possible choices
    """
    print(message)
    while True:
        try:
            choice = int(input())
        except ValueError:
            # if user entered non-digits
            print(f"Enter your choice from {options}")
            continue

        if choice in options:
            choices.append(choice)
            break
        else:
            # if user entered number not from options
            print(f"Enter your choice from {options}")


def get_website_id_from_database(website, cursor):
    """Get website id by given string name"""
    cursor.execute(f"SELECT id FROM Websites WHERE name = '{website}'")
    website_id = cursor.fetchone()
    website_id = website_id[0]
    return website_id


def insert_movies_to_database(movies, website):
    """First delete old database records then insert new ones"""
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()

    website_id = get_website_id_from_database(website, cursor)

    q = f"DELETE FROM Movies WHERE website = {website_id}"
    cursor.execute(q)

    for movie in movies:
        title = movie.title.replace("'", "''")
        cursor.execute(
            f"INSERT INTO Movies (rank, title, year, rating, url, website) "
            f"VALUES({movie.rank}, '{title}', '{movie.year}', {movie.rating}, '{movie.url}', {website_id})")

    connection.commit()
    connection.close()


def get_movies_from_database(website):
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()

    website_id = get_website_id_from_database(website, cursor)

    movies_raw = cursor.execute(f"SELECT rank, title, year, rating, url FROM Movies WHERE website = {website_id}")
    movies = []
    for movie in movies_raw:
        movies.append(Movie(*movie))

    return movies


def print_top_movies(parser, website, from_db=True):
    if from_db:
        movies = get_movies_from_database(website)
    else:
        movies = parser.parse()

    for movie in movies:
        print(movie, "\n")

    if not from_db:
        insert_movies_to_database(movies, website)


def print_detailed_movie(parser):
    movie = parser.parse()

    print(movie, "\n", movie.details)


choices = []
get_choice("Where to search movies from? 1 - IMDB, 2 - Kinopoisk", choices, (1, 2))
get_choice("What to search? 1 - top movies 2 - movie detail?", choices, (1, 2))

parsers = {
    (1, 1): IMDBParser(LIST_URL_IMDB),
    (1, 2): IMDBDetailParser(DETAIL_URL_IMDB),
    (2, 1): KinopoiskParser(LIST_URL_KINOPOISK),
    (2, 2): KinopoiskDetailParser(DETAIL_URL_KINOPOISK),
}

parser = parsers[tuple(choices)]

website = "IMDB" if choices[0] == 1 else "Kinopoisk"

if choices[1] == 1:
    print_top_movies(parser, website, from_db=True)
elif choices[1] == 2:
    print_detailed_movie(parser)
