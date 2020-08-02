from bs4 import BeautifulSoup
import requests

class SearchScrape:
    def __init__(self, url="https://www.pantarhei.sk/vsetky-produkty?q="):
        self.url = url
        self.found_items = []

    def search(self, book_name):
        arguments = book_name.split(" ")
        search_name = ""
        for arg in arguments:
            search_name += f"{arg}+"
        source = requests.get(f"{self.url}{search_name}").text
        self.__create_links(source)
        
    def __create_links(self, source):
        soup = BeautifulSoup(source, "lxml")
        items = soup.find("ul", class_="itemsListing")  # nájde vsetky knihy
        found_books = items.find_all("li")
        for book in found_books:
            div = book.find("div", class_="title")
            author = div.find("h4").find("a").get_text()
            book_info = div.find("h3").find("a")
            title = book_info["title"]
            link = book_info["href"]
            self.found_items.append(SearchInfo(title, author, link))

    def get_items(self):
        return self.found_items


# trieda pre ulozenie info
class SearchInfo:
    def __init__(self, title, author, link):
        self.info = f"{str(title)}  -  {str(author)} "
        self.link = link

    def __repr__(self):
        return self.info

class BookInfoGenerator:
    def __init__(self):
        pass