# -*- coding: utf-8 -*-
from re import findall
from json import loads
from types import SimpleNamespace
from requests import post
from base64 import b64encode, b64decode


class HamrahtelExtractor(object):
    PROVIDER = 'hamrahtel'
    NOT_AVAILABLE = 'N/A'
    API_URL = 'https://hamrahtel.com/panel/api.php'

    def extract(self, productInfo):
        productId = self.getProductId(productInfo['url'])
        message = f'{{"task": "getXProductDetails","params": {{"productId": "{productId}"}}}}'
        response = post(self.API_URL, data={
            'service_worker': b64encode(message.encode('ascii'))})
        s = b64decode(response.text)
        doc = loads(s.decode('utf8'))
        colors = self.getColors(doc)
        results = []
        for color in colors:
            results.append(self.getResult(
                HamrahtelExtractor.PROVIDER, productInfo['product'], productInfo['ram'], productInfo['rom'], productInfo['net'], color.name, color.price))
        return results

    def getProductId(self, url):
        return findall('\d+', url)[0]

    def getColors(self, doc):
        colors = []
        for item in doc['item']['subProducts']:
            if item['quantity'] > 0:
                color = SimpleNamespace(name='', price='')
                color.name = item['colorTitle']
                price = item['price']
                color.price = f'{price:,}'
                colors.append(color)
        return colors

    def getResult(self, provider, title, ram, rom, net, color, price):
        return {'provider': provider, 'product': title, 'ram': ram, 'rom': rom, 'net': net, 'color': color, 'price': price}
