# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.loader import ItemLoader
from epicerie.items import Produit

class MetrospiderSpider(scrapy.Spider):
    name = "metroSpider"
    allowed_domains = ["www.metro.ca"]
    start_urls = ["https://www.metro.ca/epicerie-en-ligne/recherche"]

    def parse(self, response):
        produits = response.css('.pt__content')
        for produit in produits:
            l = ItemLoader(item=Produit(), selector=produit)
            l.add_css('nom', '.head__title::text')
            l.add_css('marque', '.head__brand::text')
            l.add_css('code', '.product-details-link::attr(href)')
            l.add_css('categories', '.product-details-link::attr(href)')
            l.add_css('prix', '.content__pricing div::attr(data-main-price)')
            l.add_css('prixSecondaire', '.pricing__secondary-price span')
            yield l.load_item()

            page_suivante = response.css('.img-arrow-right').xpath('../@href').get()
            if page_suivante is not None:
                url_page_suivante = 'https://www.metro.ca' + page_suivante
                yield response.follow(url_page_suivante, callback=self.parse)