# -*- coding: utf-8 -*-

from types import SimpleNamespace
import requests
from bs4 import BeautifulSoup
from json import loads


class TechnolifeExtractor(object):
    PROVIDER = 'technolife'
    NOT_AVAILABLE = 'N/A'

    def extract(self, productInfo):
        req = requests.get(productInfo['url'])
        doc = BeautifulSoup(req.content, 'html.parser')
        colors = self.getColors(doc)
        results = []
        for color in colors:
            results.append(self.getResult(
                TechnolifeExtractor.PROVIDER, productInfo['product'], productInfo['ram'], productInfo['rom'], productInfo['net'], color.name, color.price))
        return results

    def getColors(self, doc):
        content = loads(doc.find(id='__NEXT_DATA__').get_text(),
                        object_hook=lambda d: SimpleNamespace(**d))
        color_items = content.props.pageProps.productPageContents.product_info.color_items
        colors = []
        for color_item in color_items:
            color = SimpleNamespace(name='', price='')
            color.name = color_item.color.value
            color.price = f'{color_item.discounted_price:,}'
            colors.append(color)
        return colors

    def getResult(self, provider, title, ram, rom, net, color, price):
        return {'provider': provider, 'product': title, 'ram': ram, 'rom': rom, 'net': net, 'color': color, 'price': price}
