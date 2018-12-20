'''
write details
input zpid.csv
'''
import time
from lxml import html
import requests
import unicodecsv as csv
import argparse
from getProperties import parse
import csv

csvFile = open("zpids.csv", "r")
reader = csv.reader(csvFile)

for zpid in reader:
    print ("Fetching data for %s")
    scraped_data = parse(zpid[0])
    print ("Writing data to output file")
    print(scraped_data)
    with open("properties.csv",'a+')as csvfile:
        fieldnames = ['zpid','title','address','city','state','zipcode','price','availability','type','number of beds','number of bedrooms','number of bathrooms','space','url']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writerow(scraped_data)
    time.sleep(60)
