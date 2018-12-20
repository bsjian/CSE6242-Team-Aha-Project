'''
Scraping the detail information
input zpid
'''
from lxml import html
import requests
import unicodecsv as csv
import argparse
import re

def parse(zpid):
    url="https://www.zillow.com/homes/for_rent/"+zpid+"_zpid"

    headers= {
    			'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    			'accept-encoding':'gzip, deflate, sdch, br',
    			'accept-language':'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
    			'cache-control':'max-age=0',
    			'upgrade-insecure-requests':'1',
    			'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    response = requests.get(url,headers=headers)
    print(response.text)
    print(response.status_code)
    parser = html.fromstring(response.text)
    results = parser.xpath("//div[@id='search-detail-lightbox']//text()")

    raw_address = parser.xpath(
    "//div[@id='search-detail-lightbox_content']//header[@class='zsg-content-header addr']//span[@class='zsg-h2 addr_city']//text()")
    raw_price = parser.xpath(
    "//div[@id='search-detail-lightbox']//div[@class='main-row  home-summary-row']//span[@class]//text()")
    raw_title = parser.xpath(
    "//div[@id='search-detail-lightbox']//header[@class='zsg-content-header addr']//h1[@class='notranslate']//a//text()")
    raw_info = parser.xpath(
    "//div[@id='search-detail-lightbox']//header[@class='zsg-content-header addr']//h3//text()")
    raw_availability = parser.xpath(
    "//div[@id='search-detail-lightbox']//div[@class='  home-summary-row']//span[@class]//text()")
    raw_type = parser.xpath(
    "//div[@id='search-detail-lightbox']//section[@class='zsg-content-section ']//div[@class='zsg-media-bd']//div[@class='hdp-fact-ataglance-value']//text()")

    whole_addr = ' '.join(' '.join(raw_address).split()) if raw_address else None
    list = whole_addr.split(", ") if raw_address else None
    address = list[0] if raw_address else None
    city = list[1] if raw_address else None
    statezip = list[2] if raw_address else None
    sublist = statezip.split(" ") if raw_address else None
    state = sublist[0] if raw_address else None
    zipcode = sublist[1] if raw_address else None
    strprice_1 = ''.join(raw_price).strip(" ").replace("  /mo","") if raw_price else None
    strprice_2 = strprice_1.replace("$","") if raw_price else None
    price= strprice_2.replace(",","") if raw_price else None
    info = ' '.join(' '.join(raw_info).split()).replace("&nbsp",',')
    infolist = info.split(" ") if raw_info else None
    bed = infolist[0] if raw_info else None
    bath = infolist[2] if raw_info else None
    sqft = infolist[4].replace(",","") if raw_info else None
    title = ''.join(raw_title) if raw_title else None
    availability = ''.join(raw_availability).strip(" ") if raw_availability else None
    alltype = ''.join(raw_type) if raw_type else None
    type= re.findall('[A-Z][^A-Z]*',alltype)[0] if raw_type else None

    properties_list = {
                    'zpid':zpid,
    				'address':address,
    				'city':city,
    				'state':state,
    				'zipcode':zipcode,
    				'price':price,
    				'number of bedrooms':bed,
                    'number of beds':bed,
                    'number of bathrooms':bath,
                    'space':sqft,
    				'url':url,
                    'availability':availability,
    				'title':title,
                    'type':type,
    }

    return properties_list
