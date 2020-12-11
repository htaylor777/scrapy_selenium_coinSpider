# ================================================================
# NICE WORKS WELL
# ================================================================
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy_splash.request import SplashRequest, SplashFormRequest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class CoinSpiderSelenium(scrapy.Spider):
    name = "coinselenium"
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ["https://www.livecoin.net/en"]

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get("https://www.livecoin.net/en")
        my_tab = driver.find_elements_by_class_name("filterPanelItem___2z5Gb")
        my_tab[5].click()
        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        for currency in resp.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS')]"):
            yield {
                'currency pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get()

            }
        # print(response.body)
