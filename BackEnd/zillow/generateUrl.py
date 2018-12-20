import csv

csvFile = open("zpids.csv", "r")
reader = csv.reader(csvFile)
for row in reader:
    zpid = row[0].strip(" ")

    url = "https://www.zillow.com/homes/for_rent/"+zpid+"_zpid"
    parameters={
        'url': url,
    }

    with open("url3018.csv",'a+')as csvfile:
        fieldnames = ['url']
        writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
        writer.writerow(parameters)
