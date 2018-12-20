import csv
from new_learning import *

failed_zips = []
reader = csv.reader(open("/media/trevor/main-storag/master_classes/CS6242/project/CS6242_backend/scraping_1_log"), delimiter=" ")
for row in reader:
    if len(row)>5:
        if row[0] == 'failed':
            failed_zips.append(row[4])
print failed_zips
total_zips = len(failed_zips)

for zipcode in failed_zips:
    print "======================================"
    print "scraping zipcode ", i, "/", total_zips
    i += 1
    time.sleep(random.randint(1, 10) * .931467298)
    scraping_result += scrape_one_zip(zipcode)

# Here, we have some result ready. Let's write to a fileabs
with open("scraped_yelp_apartments_for_Atlanta_try_3.csv","w") as fp:
    fieldnames= ['business_name','review_count','rating','address','price_range','url']
    writer = csv.DictWriter(fp,fieldnames=fieldnames)
    writer.writeheader()
    for data in scraping_result:
        writer.writerow(data)
