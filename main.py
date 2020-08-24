from parsers.imdb import IMDBParser

URL = "https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&sort=user_rating,desc"

parser = IMDBParser(URL)

movies = parser.parse()

for movie in movies:
    print(movie)

# print(movies[0])
