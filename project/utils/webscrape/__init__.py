from bs4 import BeautifulSoup
import requests
from project.users.admin.forms import NewBookForm
import unicodedata
from flask import flash

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
        self.info = f"{str(title)}  ---  {str(author)} "
        self.link = link
        
    def __repr__(self):
        return self.info

class BookInfoGenerator:
    def __init__(self):
        self.info_holder = None
        self.pages_num = 666
        self.isbn = 1234567890
        self.language = "Slovenský"
        self.publisher = "Neuvedený"


    def generate_data(self, link):
        source = requests.get(link).text
        soup = BeautifulSoup(source, "lxml")

        main = soup.find("div", id="mainContent")
        section = main.find("section")

        header = section.find("header")
        self.title = header.find("h1").get_text()
        self.author = header.find("h2").find("a").get_text()

        found_price = section.find("div", class_="sale-price").get_text()
        clean_text = unicodedata.normalize("NFKD", found_price)
        self.price = clean_text.strip().split(":")[1][-7:-1]

        self.info = section.find("div", class_="about nlabout").find("span").next_sibling

        book_info = section.find("div", class_="bookInfo")
        s = book_info.find_all("span", class_="highlight")
        
        #hardcoded shit
        for el in s:
            if el.get_text() == "Počet strán:":
                self.pages_num = el.next_sibling
            elif el.get_text() == "Jazyk:":
                self.language = el.next_sibling
            elif el.get_text() == "ISBN:":
                self.isbn = el.next_sibling
            elif el.get_text() == "Dátum vydania:":
                self.date_published = el.next_sibling.strip()[-4:]
           

        self.publisher = book_info.find("a").get_text()


    def fill_in_form(self, form):
        if isinstance(form, NewBookForm) == False:
            return

        form.title.data = self.title
        form.author.data = self.author
        form.price.data = self.price.replace(",", ".")
        form.genre.data = "Neuvedené"
        form.isbn.data = self.isbn
        form.pages_num.data = self.pages_num
        form.year_published.data = self.date_published
        form.publisher.data = self.publisher
        form.language.data = self.language
        form.info.data = self.info

