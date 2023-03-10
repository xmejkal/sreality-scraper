import scrapy

from flats.items import Flat

FLAT_IMAGE_DEFAULT_HEIGHT = 300
FLAT_IMAGE_DEFAULT_WIDTH = 400


class FlatsSpider(scrapy.Spider):
    name = "flats"
    allowed_domains = ["www.sreality.cz"]
    pages = 1
    start_urls = [
        f"https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page={page}&per_page=50"
        for page in range(1, 1 + pages)
    ]

    # parse a list of flats
    def parse(self, response):
        response_json = response.json()
        for item in response_json["_embedded"]["estates"]:
            yield scrapy.Request(
                f"https://www.sreality.cz/api{ item['_links']['self']['href']}",
                callback=self.parse_one,
            )

    # parse a single flat response
    def parse_one(self, response):
        # breakpoint()
        # from scrapy.shell import open_in_browser
        # open_in_browser(response)

        response_json = response.json()

        flat_title = response_json.get("name").get("value")
        flat_address = response_json.get("locality").get("value")

        flat_description = f"{flat_title}: {flat_address}"
        flat = Flat(flat_description, [])

        image = response_json["_embedded"]["images"][0]
        image_link_dynamic_down = image["_links"]["dynamicDown"]
        if image_link_dynamic_down:
            url = (
                image_link_dynamic_down["href"]
                .replace("{width}", str(FLAT_IMAGE_DEFAULT_WIDTH))
                .replace("{height}", str(FLAT_IMAGE_DEFAULT_HEIGHT))
            )

            flat.photo_url = url
        yield flat
