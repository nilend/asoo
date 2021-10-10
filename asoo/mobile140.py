# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from types import SimpleNamespace
from unidecode import unidecode


class Mobile140Extractor(object):
    PROVIDER = 'mobile140'
    NOT_AVAILABLE = 'N/A'

    def extract(self, productInfo):
        req = requests.get(productInfo['url'])
        doc = BeautifulSoup(req.content, 'html.parser')
        product = self.getProduct(doc)
        price = self.getPrice(doc)
        colors = self.getColors(doc)
        results = []
        for color in colors:
            if color.checked:
                results.append(self.getResult(
                    Mobile140Extractor.PROVIDER, productInfo['product'], productInfo['ram'], productInfo['rom'], productInfo['net'], color.name, price))
            else:
                url = f"https://www.mobile140.com/fa/price_show.html&priceid=&colorid={color.id}&productid={product.id}&ajax=ok"
                coloredDoc = BeautifulSoup(
                    requests.get(url).content, 'html.parser')
                results.append(self.getResult(
                    Mobile140Extractor.PROVIDER, productInfo['product'], productInfo['ram'], productInfo['rom'], productInfo['net'], color.name, self.getPrice(coloredDoc)))
        return results

    def getProduct(self, doc):
        pid = doc.select_one('#productid').get('value')
        return SimpleNamespace(id=pid)

    def getPrice(self, doc):
        span = doc.select_one('span.single__desc__price--new span')
        if span:
            price = unidecode(span.get_text())
            return price
        return self.NOT_AVAILABLE

    def getColors(self, doc):
        inputs = doc.select('label.select_color__label input[name=color]')
        colors = []
        for input in inputs:
            color = SimpleNamespace(checked=False, name='', id='')
            if input.has_attr('checked'):
                color.checked = True
            color.id = input.get('data-val')
            color.name = input.get('data-title')
            colors.append(color)
        return colors

    def getResult(self, provider, title, ram, rom, net, color, price):
        return {'provider': provider, 'product': title, 'ram': ram, 'rom': rom, 'net': net, 'color': color, 'price': price}
