# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst, Identity
from bs4 import BeautifulSoup


def code_processor(value):
    return int(value.rstrip('/').split('/')[-1])

def prix_secondaire_processor(value):
    txt = BeautifulSoup(value, "html.parser").text.strip()
    try:
        return {
            'prix': float(txt.split('$')[0].replace('ou', '').replace(',', '.').strip()),
            'qte': txt.split('$')[1].replace('/', '').strip()
        }
    except:
        return txt

def categories_processor(value):
    return value.split('/')[3:-2]

class Produit(scrapy.Item):
    nom = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    marque = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    code = Field(
        input_processor=MapCompose(code_processor),
        output_processor=TakeFirst()
    )
    categories = Field(
        input_processor=MapCompose(categories_processor),
        output_processor=Identity()
    )
    prix = Field(
        input_processor=MapCompose(float),
        output_processor=TakeFirst()
    )
    prixSecondaire = Field(
        input_processor=MapCompose(prix_secondaire_processor),
        output_processor=TakeFirst()
    )
