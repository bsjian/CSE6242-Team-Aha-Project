'''
write zpids
input specific location
'''
from zillowscraping import ZillowScraping
import xml.etree.ElementTree as ET
import csv

csvFile = open("30318house.csv", "r")
reader = csv.reader(csvFile)
for row in reader:

    object = ZillowScraping()
    object.address=row[0]
    object.zipcode="30318"
#object.address="1040 Huff Rd NW"
#object.zipcode="30318"

    object.get_content()
