# import libs
from lxml import html
import unicodecsv as csv
import requests
from time import sleep
import re
import argparse
import time
import random
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

user_agent_list = ["Mozilla/5.0 (X11; CrOS x86_64 11021.56.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.76 Safari/537.36",
					"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
					"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15",
					"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/70.0.3588.77 Safari/537.36",
					"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14; rv:63.0) Gecko/20100101 Firefox/63.0",
					"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
					"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
					"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
					"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
					"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
					"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
					"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
					"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
					"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0",
					"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0",
					"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
					"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15",
					"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0"]

# Define a method crape every page
def scrape_page(url):
    header_agent = random.randint(0,len(user_agent_list)-1)
    headers = {'User-Agent': user_agent_list[header_agent]}
    response = requests.get(url, headers=headers, verify=False).text
    parser = html.fromstring(response)
    Listing = parser.xpath("//li[@class='regular-search-result']")
    total_results = parser.xpath("//span[@class='pagination-results-window']//text()")
    scraped_data = []
    for results in Listing:
        raw_position = results.xpath(".//span[@class='indexed-biz-name']/text()")
        raw_name = results.xpath(".//span[@class='indexed-biz-name']/a//text()")
        raw_ratings = results.xpath(".//div[contains(@class,'rating-large')]//@title")
        raw_review_count = results.xpath(".//span[contains(@class,'review-count')]//text()")
        raw_price_range = results.xpath(".//span[contains(@class,'price-range')]//text()")
        category_list = results.xpath(".//span[contains(@class,'category-str-list')]//a//text()")
        raw_address = results.xpath(".//address//text()")
        is_reservation_available = results.xpath(".//span[contains(@class,'reservation')]")
        is_accept_pickup = results.xpath(".//span[contains(@class,'order')]")
        url = "https://www.yelp.com"+results.xpath(".//span[@class='indexed-biz-name']/a/@href")[0]

        name = ''.join(raw_name).strip()
        position = ''.join(raw_position).replace('.','')
        cleaned_reviews = ''.join(raw_review_count).strip()
        reviews =  re.sub("\D+","",cleaned_reviews)
        categories = ','.join(category_list)
        cleaned_ratings = ''.join(raw_ratings).strip()
        if raw_ratings:
            ratings = re.findall("\d+[.,]?\d+",cleaned_ratings)[0]
        else:
            ratings = 0
        price_range = len(''.join(raw_price_range)) if raw_price_range else 0
        address  = ' '.join(' '.join(raw_address).split())
        reservation_available = True if is_reservation_available else False
        accept_pickup = True if is_accept_pickup else False
        data={
                'business_name':name,
                'review_count':reviews,
                'rating':ratings,
                'address':address,
                'price_range':price_range,
                'url':url
        }
        scraped_data.append(data)
    # print len(scraped_data)
    return scraped_data

def scrape_one_name(apt_name):
    apt_name_splitted = apt_name.split(' ')
    new_name = ''
    for block in apt_name_splitted:
        new_name = new_name + "%20" + block
    # url = "https://www.yelp.com/search?find_desc=Apartments&find_loc=" + str(zipcode)
    url = "https://www.yelp.com/search?find_desc=" + new_name + "&find_loc=Atlanta%2C%20GA&mapsize=412%2C675"

    header_agent = random.randint(0,len(user_agent_list)-1)
    # prepare the header
    headers = {'User-Agent': user_agent_list[header_agent]}
    scrapped_data = scrape_page(url)
    if len(scrapped_data)>0:
        print("scrape ", apt_name, " successfully")
        return scrapped_data
    else:
        print("FAILED: ", apt_name)
        return []

if __name__=="__main__":
    sysargv = sys.argv
    if sysargv[1] == '-test':
        apt_name = sysargv[2]
        scraping_result = scrape_one_name(apt_name)
        with open("real_time_scrape_test.csv","w") as fp:
            fieldnames= ['business_name','review_count','rating','address','price_range','url']
            writer = csv.DictWriter(fp,fieldnames=fieldnames)
            writer.writeheader()
            for data in scraping_result:
                writer.writerow(data)
        print("finished, result wrote to real_time_scrape_test.csv")
    if sysargv[1] == '-help':
        print("This python file is for scraping yelp real time given apartment name....")
        print("---------------------------------------")
        print("To use: call function scrape_one_name(apt_name)")
        print("To test: run")
        print("     python yelp_scrape_real_time.py -test")
        print("---------------------------------------")
        print("print FAILED: <apt_name> on failure")
        print("print scrape <apt_name> successfully on success")
