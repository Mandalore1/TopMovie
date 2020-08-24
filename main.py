from parsers.imdb import IMDBParser, IMDBDetailParser

LIST_URL = "https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&sort=user_rating,desc"
DETAIL_URL = "https://www.imdb.com/title/tt0111161/"

parser = IMDBParser(LIST_URL)

movies = parser.parse()

for movie in movies:
    print(movie, "\n")

# parser = IMDBDetailParser(DETAIL_URL)
#
# movie = parser.parse()
#
# print(movie, "\n", movie.details)
