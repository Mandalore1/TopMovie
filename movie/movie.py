class Movie:
    """Movie class"""
    def __init__(self, rank: int, title: str, year: int):
        self.rank = rank
        self.title = title
        self.year = year

    def __str__(self):
        return f"{self.rank}. {self.title} ({self.year})"
