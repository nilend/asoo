# -*- coding: utf-8 -*-
import csv as c
import os.path
from mobile140 import Mobile140Extractor
from hamrahtel import HamrahtelExtractor


class Asoo(object):
    def extract(self, csv="urls.csv"):
        if os.path.exists(csv):
            with open(csv, encoding='utf8') as reader:
                with open('results.csv', 'w', newline='', encoding='utf8') as writer:
                    csv_reader = c.DictReader(
                        reader, fieldnames=('provider', 'product', 'ram', 'rom', 'net', 'url'))
                    csv_writer = c.DictWriter(
                        writer, fieldnames=('provider', 'product', 'ram', 'rom', 'net', 'color', 'price'), quoting=c.QUOTE_NONNUMERIC)
                    csv_writer.writeheader()
                    results = []
                    for row in csv_reader:
                        if row['url'] and row['provider']:
                            provider = row['provider'].lower()
                            if provider == Mobile140Extractor.PROVIDER:
                                results.extend(self.execute(
                                    row, Mobile140Extractor()))
                            elif provider == HamrahtelExtractor.PROVIDER:
                                results.extend(self.execute(
                                    row, HamrahtelExtractor()))
                        else:
                            print('URL or provider is not available.', row)
                    csv_writer.writerows(results)
        else:
            print("File %s not exist" % csv)

    def execute(self, row, provider):
        try:
            return provider.extract(row)
        except Exception as e:
            print(e, row)
