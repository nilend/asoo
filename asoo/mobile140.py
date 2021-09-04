# -*- coding: utf-8 -*-

from lxml.html import parse, HTMLParser
from urllib.request import urlopen
from urllib.parse import quote
from types import SimpleNamespace


class Mobile140Extractor(object):
    PROVIDER = 'mobile140'
    NOT_AVAILABLE = 'ناموجود'

    def extract(self, productInfo):
        parser = HTMLParser(encoding='utf8')
        doc = parse(
            urlopen(quote(productInfo['url'], safe='/:')), parser=parser).getroot()
        product = self.getProduct(doc)
        price = self.getPrice(doc)
        colors = self.getColors(doc)
        results = []
        for color in colors:
            if color.checked:
                results.append(self.getResult(
                    Mobile140Extractor.PROVIDER, product.name, color.name, price))
            else:
                url = f"https://www.mobile140.com/fa/price_show.html&priceid=&colorid={color.id}&productid={product.id}&ajax=ok"
                coloredDoc = parse(urlopen(url)).getroot()
                results.append(self.getResult(
                    Mobile140Extractor.PROVIDER, product.name, color.name, self.getPrice(coloredDoc)))

        return results

    def getProduct(self, doc):
        pid = doc.cssselect('input#productid')[0].get('value')
        name = self.getTitle(doc)
        return SimpleNamespace(id=pid, name=name)

    def getTitle(self, doc):
        h1s = doc.cssselect('h1.innerPageTitle')
        if len(h1s) > 0:
            return h1s[0].text

    def getPrice(self, doc):
        spans = doc.cssselect('span.single__desc__price--new')
        if len(spans) > 0:
            return spans[0].text_content().split(' ')[0] if spans[0].text_content() is not None else self.NOT_AVAILABLE
        return self.NOT_AVAILABLE

    def getColors(self, doc):
        labels = doc.cssselect('label.select_color__label')
        colors = []
        for label in labels:
            color = SimpleNamespace(checked=False, name='', id='')
            input = label.cssselect('input[name=color]')[0]
            if input.checked:
                color.checked = True
            color.name = input.get('data-title')
            color.id = input.get('data-val')
            colors.append(color)
        return colors

    def getResult(self, provider, title, color, price):
        return {'provider': provider, 'product': title, 'color': color, 'price': price}
