FROM --platform=linux/amd64 python:3.10-alpine
COPY ./requirements.txt /app/requirements.txt
WORKDIR /scraper
RUN pip install -r requirements.txt
COPY . /scraper
ENTRYPOINT [ "scrapy" ]
CMD [ "crawl", "flats" ]

