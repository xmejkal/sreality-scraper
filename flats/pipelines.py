# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os

import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class FlatsPipeline:
    def process_item(self, item, spider):
        self.cur.execute(
            """ insert into flats (name,photo_url) values (%s,%s)""",
            (item.name, item.photo_url),
        )
        self.connection.commit()
        return item

    def __init__(self):

        database_name = os.environ.get("POSTGRES_DB")
        hostname = os.environ.get("POSTGRES_HOST")
        username = os.environ.get("POSTGRES_USER")
        password = os.environ.get("POSTGRES_PASSWORD")
        database = database_name

        ## Create/Connect to database
        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password, dbname=database
        )

        self.cur = self.connection.cursor()
        self.cur.execute(f"DROP TABLE IF EXISTS {database_name}")
        self.cur.execute(
            f"""
        CREATE TABLE IF NOT EXISTS {database_name}(
            id serial PRIMARY KEY, 
            name VARCHAR(255),
            photo_url VARCHAR(255)
        )
        """
        )

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
