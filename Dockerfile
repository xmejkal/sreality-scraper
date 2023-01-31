FROM --platform=linux/amd64 python:3.10-alpine
COPY ./requirements.txt /scraper/requirements.txt
WORKDIR /scraper
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt
COPY . /scraper
CMD [ "scrapy", "crawl", "flats" ]

