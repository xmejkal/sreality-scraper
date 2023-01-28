import flat
import scrapy


class FlatSpider(scrapy.Spider):
    name = "sreality_spider"
    allowed_domains = ["www.sreality.cz"]
    start_urls = [
        "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page={page}&per_page=50"
        for page in range(1, 11)
    ]

    def parse(self, response):

        from scrapy.shell import inspect_response

        inspect_response(response, self)

        response_json = response.json()

        for item in response_json["_embedded"]["estates"]:
            yield scrapy.Request(
                f"https://www.sreality.cz/api${ item['_links']['self']['href']}",
                callback=self.parse_one,
            )

    def parse_one(self, flat_json):

        yield flat.Flat(
            name=flat_json["name"],
            photo_urls=flat_json["_links"]["images"]["href"],
        )
