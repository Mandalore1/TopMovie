from bs4 import BeautifulSoup
import urllib.request


class IMDBParser:
    def __init__(self, url):
        self.url = url

    def parse(self):
        req = urllib.request.urlopen(self.url)
        html = req.read()
        soup = BeautifulSoup(html, "html.parser")
        movies = soup.find_all("h3", class_="lister-item-header")

        result = ""
        for i in movies:
            index = i.find("span", class_="lister-item-index").get_text(strip=True)
            title = i.find("a").get_text(strip=True)
            year = i.find("span", class_="lister-item-year").get_text(strip=True).strip("()")
            result += f"{index} {title} ({year})\n"

        return result
