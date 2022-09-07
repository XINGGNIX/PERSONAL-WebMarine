from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime
from random import randint
from lxml import etree
import pandas as pd
import json
import time
import re

class webmarine:
    # ===================================
    # Default parameters
    # ===================================
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "eager"
    base_url = 'https://www.carsales.com.au/cars'
    current_url = 'https://www.carsales.com.au/cars/?q=Service.carsales.&offset=0&sort=LastUpdated'
    webmarine = None
    webmarine_buffer = None
    features = {"brand": None,
                "model": None,
                "state": None,
                "bodystyle": None,
                "price_min": None,
                "price_max": None,
                "sort": '?sort=LastUpdated'}

    def __init__(self):
        # set driver profile
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument("--disable-blink-features=AutomationControlled")

        # initiate driver object
        self.webmarine = webdriver.Chrome("./webmarine/chromedriver", options = options)

        # change driver appearance
        with open('./webmarine/stealth.min.js') as f:
            js = f.read()
        self.webmarine.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
        self.webmarine.implicitly_wait(2)
        self.webmarine.maximize_window()

    def xfind(self, path):
        element = self.webmarine.find_element_by_xpath(path)
        return element

    def click(self, path):
        element = self.webmarine.find_element_by_xpath(path)
        self.webmarine.execute_script("arguments[0].click()", element)

    def get_content(self, url):
        try:
            self.webmarine.get(url)
            return self.webmarine.page_source
        except Exception as error:
            print("WebMarine(): fail get content from webpage ... ")
            return None

    # =======================================
    # features -> DICT: set filter features
    # =======================================
    def set_features(self, features):
        for key_item in features:
            if (key_item in self.features):
                self.features[key_item] = features[key_item]
        self.set_url()

    # =======================================
    # show_url -> BOOL: Build searching url
    # =======================================
    def set_url(self, show_url = False):
        current_url = 'https://www.carsales.com.au/cars'

        if (self.features['brand'] != None):
            brand = re.sub(' ', '-', self.features['brand'])
            current_url = current_url + '/' + brand

        if (self.features['brand'] != None and self.features['model'] != None):
            current_url = current_url + '/' + self.features['model']

        if (self.features['state'] != None):
            current_url = current_url + '/' + self.features['state'] + '-state'

        if (self.features['bodystyle'] != None):
            current_url = current_url + '/' + self.features['bodystyle'] + '-bodystyle'

        if (self.features['price_min'] != None and self.features['price_max'] != None):
            current_url = current_url + '/' + "between-" + str(self.features['price_min']) + "-" + str(
                self.features['price_max'])

        if (self.features['sort'] != None):
            current_url = current_url + '/' + self.features['sort']

        self.current_url = current_url

        if (show_url):
            print("Searching url: " + self.current_url)

    def load_cookies(self):
        with open("./webmarine/cookies.json", 'r') as f:
            data = json.loads(f.read())
            for cookie in data:
                self.webmarine.add_cookie(cookie)

    def run_webmarine(self):
        # get page content to fill cookies
        self.get_content(self.current_url)
        self.load_cookies()

        buffer = []
        page_counter = 1
        next_page_url = True
        while next_page_url:
            time.sleep(randint(5, 10))

            # extract car features
            page_text = self.webmarine.page_source
            html = etree.HTML(page_text)
            title_list = html.xpath('//h3/a/text()')
            url_list = html.xpath('//h3/a/@href')
            price_list = html.xpath('//div[@class="price"]/a/text()')
            km_list = html.xpath('//ul[@class="key-details"]/li[1]/text()')
            body_type_list = html.xpath('//ul[@class="key-details"]/li[2]/text()')
            matic_list = html.xpath('//ul[@class="key-details"]/li[3]/text()')
            petrol_list = html.xpath('//ul[@class="key-details"]/li[4]/text()')
            location_list = html.xpath('//div[@class="seller-location d-flex"]/text()')
            time.sleep(randint(5, 10))

            # get next page html
            next_page_url = html.xpath('//ul[@class="pagination"]/li[7]/a/@href')

            # save current extraction
            tmp_matrix = zip(title_list, url_list, price_list, km_list, body_type_list, matic_list, petrol_list, location_list)
            for title, url, price, km, body_type, matic, petrol ,location in tmp_matrix:
                buffer.append([title, url, price, km, body_type, matic, petrol, location])

            buffer_df = pd.DataFrame(buffer, columns=['title', 'url', 'price', 'km', 'body_type', 'matic', 'petrol', 'location'])
            buffer_df.to_csv('./webmarine/buffer_result.csv')

            if next_page_url:
                self.current_url = 'https://www.carsales.com.au' + next_page_url[0]
                print('webmarine(): processed at page -> ' + str(page_counter))
                self.get_content(self.current_url)
                page_counter = page_counter + 1
            else:
                # Website requires mannual slide action
                user_action = input('webmarine(): requires human action ... (quit|.*): \n')
                if(user_action == 'q' or user_action == 'quit'):
                    print("webmarine(): break with ->" + str(next_page_url))
                    break
                else:
                    self.get_content(self.current_url)

        buffer_df = pd.DataFrame(buffer, columns=['title', 'url', 'price', 'km', 'body_type', 'matic', 'petrol', 'location'])
        buffer_df.to_csv('./webmarine/buffer_result.csv')
        self.current_url = 'https://www.carsales.com.au/cars/?q=Service.carsales.&offset=0&sort=LastUpdated'
        self.webmarine.quit()

    def end_webmarine(self):
        self.webmarine.quit()









