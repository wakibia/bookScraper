# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookScrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


### you can add serializers here to serialize the data
### you can also add validators here to validate the data

#def serialize_price(value):
#    return f'£ {str(value)}'


## add a dictionary to map the star-rating to a number
## this will be used to sort the books by rating


#def serialize_rating(value):
#    rating_map = {
#        "One": 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
#    }
#    value = value.replace("star-rating ", "")
#    return rating_map[value]


class BookItem(scrapy.Item):
    book_title = scrapy.Field()
    book_availability = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    #tax = scrapy.Field(serializer=serialize_price)
    tax = scrapy.Field()
    #price_including_tax = scrapy.Field(serializer=serialize_price)
    price_including_tax = scrapy.Field()
    product_type = scrapy.Field()
    #price_excluding_tax = scrapy.Field(serializer=serialize_price)
    price_excluding_tax = scrapy.Field()
    rating = scrapy.Field()
    number_of_reviews = scrapy.Field()
