# -*- coding: utf-8 -*-
import csv as c
import os.path
from mobile140 import Mobile140Extractor


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
                    for row in csv_reader:
                        if row['provider'].lower() == 'mobile140':
                            rows = Mobile140Extractor().extract(row)
                            csv_writer.writerows(rows)
        else:
            print("File %s not exist" % csv)
