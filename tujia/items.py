# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class TujiaItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    checkInDate = Field()
    commentDetailc = Field()
    customerAvatarUrl = Field()
    customerName = Field()
    name = Field()
    pictureList = Field()
    replyContent = Field()
    replyDate = Field()
    totalScore = Field()
    unitDetail = Field()
    unitId = Field()
    unitName = Field()
