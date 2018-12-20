# import libs
from lxml import html
import unicodecsv as csv
import requests
from exceptions import ValueError
from time import sleep
import re
import argparse
import time
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# get the list of zipcodes in atlanta
def get_zipcodes():
    zipcodes = []
    with open("/media/trevor/main-storag/master_classes/CS6242/project/CS6242_backend/atlanta_zipcodes.csv") as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"):
            if line[1] == 'Standard':
                zipcodes.append(int(line[0].split(' ')[2]))
    return zipcodes


# Define a method crape every page
def scrape_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
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
    return scraped_data

def scrape_one_zip(zipcode):
    # this is an example url
    url = "https://www.yelp.com/search?find_desc=Apartments&find_loc=" + str(zipcode)

    # prepare the header
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

    # Parse the page
    response = requests.get(url, headers=headers, verify=False).text
    parser = html.fromstring(response)

    # Let's see how many pages we have...
    ## 10 listings per page
    page_row = parser.xpath("//*[@id='super-container']/div/div[2]/div[1]/div/div[4]/div[2]/div/div/div[1]/text()")
    if len(page_row)==0:
        print "failed on zip ", zipcode, ": ", url
        return []
    page_row_splitted = page_row[0].split('Page 1 of ')
    # print page_row_splitted
    page_row_splitted = page_row_splitted[1].split()[0]
    total_page = int(page_row_splitted)
    print 'total pages: ', total_page

    # Let's loop through the pages:
    scrapped_datas = []
    page_num = 0
    while page_num <= total_page:
        print "scraping pages ",page_num, "/", total_page
        time.sleep(random.randint(1, 5) * .931467298)
        scrapped_datas += scrape_page(url + '&start=' + str(page_num))
        # print url + '&start=' + str(page_num)
        page_num += 1
    return scrapped_datas

def start_scraping():
    zipcodes = get_zipcodes()
    scraping_result = []
    total_zips = len(zipcodes)
    i = 0
    for zipcode in zipcodes:
        print "======================================"
        print "scraping zipcode ", i, "/", total_zips
        i += 1
        time.sleep(random.randint(1, 10) * .931467298)
        scraping_result += scrape_one_zip(zipcode)

    # Here, we have some result ready. Let's write to a fileabs
    with open("scraped_yelp_apartments_for_Atlanta_try_2.csv","w") as fp:
        fieldnames= ['business_name','review_count','rating','address','price_range','url']
        writer = csv.DictWriter(fp,fieldnames=fieldnames)
        writer.writeheader()
        for data in scraping_result:
            writer.writerow(data)

start_scraping()
