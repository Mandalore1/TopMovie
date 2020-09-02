"""Main file used for debugging"""
from parsers.imdb import IMDBParser, IMDBDetailParser
from parsers.kinopoisk import KinopoiskParser, KinopoiskDetailParser

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


def print_top_movies(parser):
    movies = parser.parse()

    for movie in movies:
        print(movie, "\n")


def print_detailed_movie(parser):
    movie = parser.parse()

    print(movie, "\n", movie.details)


choices = []
get_choice("Where to search movies from? 1 - IMDB, 2 - Kiopoisk", choices, (1, 2))
get_choice("What to search? 1 - top movies 2 - movie detail?", choices, (1, 2))

parsers = {
    (1, 1): IMDBParser(LIST_URL_IMDB),
    (1, 2): IMDBDetailParser(DETAIL_URL_IMDB),
    (2, 1): KinopoiskParser(LIST_URL_KINOPOISK),
    (2, 2): KinopoiskDetailParser(DETAIL_URL_KINOPOISK),
}

parser = parsers[tuple(choices)]

if choices[1] == 1:
    print_top_movies(parser)
elif choices[1] == 2:
    print_detailed_movie(parser)
