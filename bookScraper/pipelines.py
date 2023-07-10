# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter


class BookscraperPipeline:

    def process_item(self, item, spider):

        ## this creates an instance of the ItemAdapter class
        adapter = ItemAdapter(item)

        ## get the variable/field names
        ##field_names = adapter.field_names()

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                if value[0] is not None:
                    adapter[field_name] = value[0].strip()
            else:
                value = adapter.get(field_name)[0]
        ## lowercase the category and product_type
        lowercase_fields = ['category', 'product_type']
        for lowercase_field in lowercase_fields:
            value = adapter.get(lowercase_field)
            adapter[lowercase_field] = value.lower()

        ## remove the pound sign from the price fields
        price_fields = ['tax', 'price_including_tax', 'price_excluding_tax']
        for price_field in price_fields:
            value = adapter.get(price_field)
            adapter[price_field] = value.replace('£', '')

        ## remove the star-rating from the rating field
        book_rated = adapter.get('rating')
        if 'star-rating ' not in book_rated:
            adapter['rating'] = 'No rating'
        else:
            adapter['rating'] = book_rated.replace('star-rating ', '')
        adapter['rating'] = adapter['rating'].lower()

        ## rating is a string, convert it to an integer by mapping it to a dictionary
        rating_map = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'no rating': 0}
        bk_rating = adapter.get('rating')
        adapter['rating'] = rating_map[bk_rating]

        ## book availability -> number of books in stock
        ## use regular expressions to extract the number of books in stock
        ## from the book availability field
        import re
        availability = adapter.get('book_availability')
        pattern = r'(\d+)'
        match = re.search(pattern, availability)
        if match:
            adapter['book_availability'] = int(match.group(1))
        else:
            adapter['book_availability'] = 0

        ## number of reviews -> number of reviews
        num_reviews = adapter.get('number_of_reviews')
        adapter['number_of_reviews'] = int(num_reviews)

        return item


## store the data to database

import mysql.connector


class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Wakibia',
            database='books'
        )

        ## create a cursor, used to execute commands
        self.cur = self.conn.cursor()

        ## create a table to store the data
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment,
                book_title TEXT,
                book_availability INTEGER,
                link TEXT,
                category TEXT,
                description TEXT,
                tax FLOAT,
                price_including_tax FLOAT,
                product_type TEXT,
                price_excluding_tax FLOAT,
                rating INTEGER,
                number_of_reviews INTEGER,
                PRIMARY KEY (id)
            )
        ''')

    def process_item(self, item, spider):
        ## define the query - for inserting data into the table

        self.cur.execute(''' insert into books(
            book_title,
            book_availability,
            link,
            category,
            description,
            tax,
            price_including_tax,
            product_type,
            price_excluding_tax,
            rating,
            number_of_reviews
        ) values (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
        )''', (
            item['book_title'],
            item['book_availability'],
            item['link'],
            item['category'],
            str(item['description'][0]),
            item['tax'],
            item['price_including_tax'],
            item['product_type'],
            item['price_excluding_tax'],
            item['rating'],
            item['number_of_reviews']
        ))

        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
