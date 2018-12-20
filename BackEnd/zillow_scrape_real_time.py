from lxml import html
import requests
import unicodecsv as csv
import argparse
import random
import sys

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

def parse_ws(address, header_agent):
	url = "https://www.walkscore.com/score/"
	for char in address:
		if char == ' ':
			url += "+"
		elif char != ',':
			url += char
	headers= {
	            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	            'accept-encoding':'gzip, deflate',
	            'accept-language':'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
	            'cache-control':'max-age=0',
	            'upgrade-insecure-requests':'1',
	            'user-agent': user_agent_list[header_agent]
	            }

	response = requests.get(url,headers=headers)
	print(response.status_code)
	parser = html.fromstring(response.text)
	search_results = parser.xpath("//div[contains(@data-eventsrc,'score page')]")
	walk_score = 0
	transit_score = 0
	bike_score = 0
	for result in search_results:
	    if walk_score != 0 and transit_score !=0 and bike_score !=0:
	        break
	    scores = result.xpath("//img[contains(@src,'score')]/@src")
	    for score in scores:
	        if 'walk/score' in score:
	            walk_score = int(score.split('/')[-1].split('.')[0])
	        if 'transit/score' in score:
	            transit_score = int(score.split('/')[-1].split('.')[0])
	        if 'bike/score' in score:
	            bike_score = int(score.split('/')[-1].split('.')[0])
	return walk_score,transit_score,bike_score

def parse(url):
	print(url)

	header_agent = random.randint(0,len(user_agent_list)-1)
	# url = "https://www.zillow.com/homes/for_rent/1-_beds/500-5000_price/33.787084,-84.372103,33.754692,-84.404418_rect/14_zm/"
	# url = "https://www.zillow.com/homes/for_rent/30308_rb/1-_beds/500-1000_price"
	# url = "https://www.zillow.com/homes/for_rent/30308_rb/33.784399,-84.381996,33.768204,-84.404376_rect/"

	for i in range(5):
		# try:
		headers= {
					'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		            'accept-encoding':'gzip, deflate',
		            'accept-language':'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
		            'cache-control':'max-age=0',
		            'upgrade-insecure-requests':'1',
		            'user-agent':user_agent_list[header_agent]
		}
		response = requests.get(url,headers=headers)
		print(response.status_code)
		parser = html.fromstring(response.text)
		# search_results_test = parser.xpath("//*[@id='search-results']")
		# print(search_results_test)
		search_results = parser.xpath("//div[@id='search-results']//article")
		properties_list = []
		print("len of search_results: ",len(search_results))

		for properties in search_results:
			new_raw_address = properties.xpath(".//span[@class='zsg-photo-card-address']//text()")[0]
			raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
			raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
			raw_state= properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
			raw_postal_code= properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
			raw_price = properties.xpath(".//span[@class='zsg-photo-card-price']//text()")
			raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
			raw_broker_name = properties.xpath(".//span[@class='zsg-photo-card-broker-name']//text()")
			url = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")
			raw_title = properties.xpath(".//h4//text()")

			address = ' '.join(' '.join(raw_address).split()) if raw_address else None
			city = ''.join(raw_city).strip() if raw_city else None
			state = ''.join(raw_state).strip() if raw_state else None
			postal_code = ''.join(raw_postal_code).strip() if raw_postal_code else None
			price = ''.join(raw_price).strip() if raw_price else None
			info = ' '.join(' '.join(raw_info).split()).replace(u"\xb7",',')
			title = ''.join(raw_title) if raw_title else None
			property_url = "https://www.zillow.com"+url[0] if url else None
			wk_score, tran_score, bike_score = parse_ws(new_raw_address, header_agent)
			is_forrent = properties.xpath('.//span[@class="zsg-icon-for-rent"]')
			properties = {
							'address':new_raw_address,
							'price':price,
							'facts and features':info,
							'url':property_url,
							'title':title,
							'walk score': wk_score,
							'transit score': tran_score,
							'bike score': bike_score
			}
			if is_forrent:
				properties_list.append(properties)
		return properties_list


def apply_filters(filters):
	url = "https://www.zillow.com/homes/for_rent/"
	if 'zipcode' in filters:
		url += (filters['zipcode'] + "_rb/")
	# if 'range' in filters:
	# 	url += (filters['range'] + "_rect/")
	if 'type' in filters:
		type_url = "mobile,land_type"
		splitted = list(filters['type'])
		if len(splitted) < 4:
			for char in splitted:
				if char == 'h':
					type_url += ",house"
				if char == 'a':
					type_url += ",apartment_duplex"
				if char == 'c':
					type_url += ",condo"
				if char == 't':
					type_url += ",townhouse_type"
			url += (type_url + "/")
	if 'beds' in filters:
		url += (filters['beds'] + "-_beds/")
	if 'baths' in filters:
		url += (filters['baths'] + "_baths/")
	if 'pets' in filters:
		if filters['pets'] == 1:
			url += "1_pets/"
	if 'parking' in filters:
		if filters['parking'] == 1:
			url += "1_parking/"
	if 'laundry' in filters:
		if filters['laundry'] == 1:
			url += "1_laundry/"
	if 'price' in filters:
		url += (filters['price'] + "_price/")
	scraped_data = parse(url)
	print("successfully")
	return scraped_data

if __name__ == "__main__":
	"""
	sample url: https://www.zillow.com/homes/for_rent/Georgia-Tech-Atlanta-GA/
	house,condo,apartment_duplex,mobile,land_type/399508_rid/2-_beds/1-_baths/
	119550-239100_price/500-1000_mp/1_pets/1_parking/1_laundry/33.792611,
	-84.376503,33.760221,-84.421263_rect/14_zm/
	"""
	sysargv = sys.argv

	if sysargv[1] == "-help":
		print("This python file is for scraping zillow real time given filters ....")
		print("---------------------------------------")
		print("To use: call function apply_filters(filters)")
		print("To test: run")
		print("     python zillow_scrape_real_time.py")
		print("Allow filters: ")
		print("		-search : main search key words (address, neighborhoods, zip codes), example input: 30309")
		print("		-type : home type, please input using single letter (h: houses, a: apartment, c: condos, t: townhouses), example input: hac")
		print("		-beds : bedroom numbers, example input: 1")
		print("		-baths : baths numbers, example input:1, 1.5, 2...")
		print("		-price : price lower and upper bound, example input: 500-1000")
		print("		-parking : onside parking, 1 for yes, 0 for no")
		print("		-pets : allow pet, same as parking")
		print("		-laundry : have in-Unit laundry, same as parking")
		print("---------------------------------------")
		print("print successfully on success")

	else:
		url = "https://www.zillow.com/homes/for_rent/"
		i = 1
		while i<len(sysargv):
			if sysargv[i] == '-search':
				url += (sysargv[i+1] + "_rb/")
			if sysargv[i] == "-type":
				type_url = "mobile,land_type"
				splitted = list(sysargv[i+1])
				if len(splitted) < 4:
					for char in splitted:
						if char == 'h':
							type_url += ",house"
						if char == 'a':
							type_url += ",apartment_duplex"
						if char == 'c':
							type_url += ",condo"
						if char == 't':
							type_url += ",townhouse_type"
					url += (type_url + "/")
			if sysargv[i] == '-beds':
				url += (sysargv[i+1] + "-_beds/")
			if sysargv[i] == '-baths':
				url += (sysargv[i+1] + "-_baths/")
			if sysargv[i] == '-pets':
				if sysargv[i+1] == 1:
					url += "1_pets/"
			if sysargv[i] == '-parking':
				if sysargv[i+1] == 1:
					url += "1_parking/"
			if sysargv[i] == '-laundry':
				if sysargv[i+1] == 1:
					url += "1_laundry/"
			if sysargv[i] == '-price':
				url += (sysargv[i+1] + "_price/")
			i += 2
		scraped_data = parse(url)
		print("Writing data to output file")
		with open("zillow_result.csv",'wb')as csvfile:
			fieldnames = ['title','address','price','walk score','transit score','bike score','facts and features','url']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for row in  scraped_data:
				writer.writerow(row)
		print("successfully")
