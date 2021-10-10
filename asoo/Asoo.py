# -*- coding: utf-8 -*-
import csv as c
import os.path
from technolife import TechnolifeExtractor
from mobile140 import Mobile140Extractor
from hamrahtel import HamrahtelExtractor
import time


def timer_func(func):

   def function_timer(*args, **kwargs):
    start = time.time()
    value = func(*args, **kwargs)
    end = time.time()
    runtime = end - start
    msg = "{func} took {time} seconds to complete its execution."
    print(msg.format(func = func.__name__,time = runtime))
    return value
   return function_timer

class Asoo(object):
    @timer_func
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
                            elif provider == TechnolifeExtractor.PROVIDER:
                                results.extend(self.execute(
                                    row, TechnolifeExtractor()))
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
