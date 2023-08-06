import requests
from bs4 import BeautifulSoup

GOODREADS_BASE_URL = "https://www.goodreads.com"


class Reader:

    def __init__(self, user_id):
        self.user_id = user_id

    def get_books_list(self):
        self.go_through_pages(5)

    def get_all_books(self, document):
        book_list = []

        for book_div in document.find_all('img'):
            print(book_div.get('alt'))

        return book_list

    def go_through_pages(self, page_limit):
        for i in range(1, page_limit + 1):
            URL = GOODREADS_BASE_URL + "/review/list/93917322?ref=nav_mybooks&view=covers&page=" + str(i)

            page = requests.get(URL)

            soup = BeautifulSoup(page.content, 'html.parser')
            books_body = soup.find(id="booksBody")

            self.get_all_books(books_body)
            if len(books_body.contents) == 0:
                return




'''

class Book:

    def __init__(self, name, image):
        self.book_name = name
        self.book_img = image

    def set(self, key, value):
        if key == "name":
            self.book_name = value
        elif key == "image":
            self.book_img = value
        return

    def get(self, key):
        if key == "name":
            return self.book_name
        else:
            return self.book_img

def get_larger_image(book_url):
    page = requests.get(GOODREADS_BASE_URL + book_url)
    soup = BeautifulSoup(page.content, 'html.parser')

def print_list(input_list):
    return
    for b in input_list:
        print(b.get('name'))
        print(b.get('image'))
'''
