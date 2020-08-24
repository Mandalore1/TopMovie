class Movie:
    """Movie class"""
    def __init__(self, rank: int, title: str, year: int, rating: float, url: str):
        self.rank = rank
        self.title = title
        self.year = year
        self.rating = rating
        self.url = url

    def __str__(self):
        return f"{self.rank}. {self.title} ({self.year}) {self.rating}*\n{self.url}"
