from parsers.imdb import IMDBParser, IMDBDetailParser
from parsers.kinopoisk import KinopoiskParser

# LIST_URL = "https://www.imdb.com/search/title/?title_type=feature&sort=user_rating,desc"
LIST_URL = "https://www.kinopoisk.ru/top/navigator/m_act[years]/1900%3A2020/order/rating/"
DETAIL_URL = "https://www.imdb.com/title/tt0252487/?ref_=adv_li_tt"

parser = KinopoiskParser(LIST_URL)
# parser = IMDBParser(LIST_URL)

movies = parser.parse()

for movie in movies:
    print(movie, "\n")

# parser = IMDBDetailParser(DETAIL_URL)
#
# movie = parser.parse()
#
# print(movie, "\n", movie.details)
