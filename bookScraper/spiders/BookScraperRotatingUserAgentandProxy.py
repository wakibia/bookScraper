##### Part 5: Pipeline #####

import scrapy
from bookScraper.items import BookItem


class BooksSpider(scrapy.Spider):
    name = "BookScraperwithRotatingUserAgentandProxy"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    ## export the data by customizing the FEEDS setting in settings.py
    ##    custom_settings = {
    ##        'FEEDS': {
    ##            'booksDataFromFeed.csv': {
    ##                'format': 'csv',
    ##                'encoding': 'utf8',
    ##                'overwrite': True
    ##            }
    ##        }
    ##    }

    def parse(self, response):
        ## extract all the book links from the page
        books = response.xpath('//article[@class="product_pod"]')
        book_links = books.xpath('.//h3/a/@href').getall()
        abs_links = [response.urljoin(link) for link in book_links]

        for link in abs_links:
            yield response.follow(link, callback=self.parse_book_items)

        ## extract the next page link
        next_page = response.xpath('//a[contains(text(), "next")]/@href').get()
        next_page_link = response.urljoin(next_page)

        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)

    def parse_book_items(self, response):

        book_item = BookItem()

        table_details = response.xpath('//table[@class="table table-striped"]/tr/td/text()').getall()

        book_item["book_title"] = response.xpath('//div/h1/text()').get(),
        book_item["book_availability"] = response.xpath('//p[@class="instock availability"]/text()[2]').get().strip(),
        book_item['link'] = response.url,
        book_item['category'] = response.xpath('(//ul[@class="breadcrumb"]/li/a/text())[3]').get(),
        book_item['description'] = response.xpath('//article[@class="product_page"]/p/text()').get(),
        book_item['tax'] = table_details[4],
        book_item['price_including_tax'] = table_details[3],
        book_item['product_type'] = table_details[1],
        book_item['price_excluding_tax'] = table_details[2],
        book_item['rating'] = response.xpath('//p[@class="star-rating Three"]/@class').get(),
        book_item['number_of_reviews'] = table_details[6]

        yield book_item
