from lxml import html
import requests
import unicodecsv as csv
import argparse

url = "https://www.walkscore.com/score/620-glen-iris-dr-ne-atlanta-ga-30308"

headers= {
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding':'gzip, deflate',
            'accept-language':'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
            'cache-control':'max-age=0',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (X11; CrOS x86_64 11021.56.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.76 Safari/537.36'
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
print(walk_score,transit_score,bike_score)
