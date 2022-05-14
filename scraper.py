import requests
from bs4 import BeautifulSoup

from bot import BotMaker


class ProductScraper:
    """Scrapes product based on ISBN number"""
    def __init__(self):
        self.__bot = BotMaker(browser="Chrome", remote=True)
        self.URL = "https://www.amazon.in/dp/{isbn}"
        self.soup = None

    def __get_product_title(self):
        title = self.soup.find("span", {"id":"productTitle"}).text.strip()
        return title

    def __get_product_price(self):
        price_temp = self.soup.find("span", {"class":"a-price-whole"}).text.strip()
        # Add only the numeric chars
        price = ""
        for char in price_temp:
            if char.isnumeric():
                price += char
        price = int(price)
        return price

    def __get_ratings(self):
        # customer ratings is present in the format of 3 out of 5 starts \n total_reviews,
        # for now we don't want the number of total_reviews, so we split it.        
        customer_rating = self.soup.find("div", {"id":"averageCustomerReviews"})        
        num_of_ratings = ""
        if customer_rating == None:
            customer_rating = ""
        else:
            customer_rating, num_of_ratings = customer_rating.text.strip().split("\n")
            customer_rating = customer_rating.strip()
            num_of_ratings = num_of_ratings.strip()
        return customer_rating, num_of_ratings

    def __get_image_url(self):
        # Image list for product is present as a key value pair in data-a-dynamic-image attribute
        # We will get that attribute data and evaluate it to make it a python dict
        # then we create a list from the keys of that dict, the dict contains image url and their resolution
        # we just need the image url which is present in key. We will only select 1st image.
        img_li = self.soup.find("li", {"class":"image"})
        if img_li == None:
            img_li = self.soup.find("div", {"id":"img-canvas"})
        disp_img_attr_str = img_li.find("img")['data-a-dynamic-image']
        disp_img_attr = eval(disp_img_attr_str)
        disp_img_list = list(disp_img_attr.keys())
        product_image_url = disp_img_list[0]
        return product_image_url

    def scrape(self, isbn):
        self.product_url = self.URL.format(isbn=isbn)
        self.__bot.move(self.product_url)
        self.soup = self.__prepare_soup()

        title = self.__get_product_title()
        price = self.__get_product_price()
        rating, n_of_rating = self.__get_ratings()
        image_url = self.__get_image_url()

        return {
            "title":title,
            "price":price,
            "customer_ratings":rating,
            "number_of_ratings": n_of_rating,
            "image_url": image_url
        }

    def __prepare_soup(self):
        return BeautifulSoup(self.__bot.get_source(), 'lxml')

