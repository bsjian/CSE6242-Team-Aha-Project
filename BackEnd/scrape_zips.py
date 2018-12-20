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

def get_zips(original_zip, miles):
	print(miles)
	header_agent = 1
	url = "https://www.zip-codes.com/zip-code-radius-finder.asp?zipmileslow=0&zipmileshigh=" + str(miles) + "&zip1=" + str(original_zip) + "&submit=Search"
	headers= {
				# 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	            # 'accept-encoding':'gzip, deflate',
	            # 'accept-language':'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
	            # 'cache-control':'max-age=0',
	            # 'upgrade-insecure-requests':'1',
	            'user-agent':user_agent_list[header_agent]
	}
	response = requests.get(url,headers=headers)
	print(response.status_code)
	parser = html.fromstring(response.text)
	search_results_test = parser.xpath("//div[@id='tableview']//table//tr")
	# print(search_results_test)
	zips = []
	for i in range(1,len(search_results_test)):
	    zips.append(search_results_test[i].xpath(".//td[2]//text()"))
	    # print(search_results_test[i].xpath(".//td[2]//text()"))
	return zips
