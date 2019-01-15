# Rental-Recommendation-Web-System
A housing rental recommendation website for those who commutes daily, which can provide renting recommendations based on users’ personal references, such as basic information, safety anticipation, and transportation requirement.

To run our project locally:

(1)First, follow the README_BackEnd to run the backend server.

(2)Second, follow the README_FrontEnd to run the front end server.

IMPORTANT: Please make sure that the local host and port number of backend server is correctly added to line 25 and line 27 in app.js in FrontEnd directory. (i.e. Postname:127.0.0.1.  Port: 3000)

(3)Third, open your web browser and visit our website via the host and port number of your frontend program. (i.e. 127.0.0.1:3000)


## BackEnd

This project does contain scraping programs that do not respect some websites' /robots.txt. We are aware that this is not a good manner and we are not using and will never use those code other than studying. 

Notice: Execute the programs on large searching range or large number of searches in a short period of time CAN AND WILL RESULT IP BANNED from some websites!

Main scraping python files have their own testing code for testing/debugging (IP banned issue or other cases). To get specific run instruction, execute:

	$ python yelp_scrape_real_time.py -help
	$ python zillow_scrape_real_time.py -help
	$ python price_as_feature.py -help

To run the main flask app 'project_v2.py' on server for public IP address visiting, please uncomment the line 215 and comment line 216. 
List for flask reroutings: 
'/test':			return the testing test.json file; 

'/':				return index.html for server debugging purpose only (note that the index.html file is not included, it can be any file ONLY for debugging purpose);

'/apartmentprice'	return formatted prices for apartments on zillow;

'/filters'			return list of found apartments satisfy the given filters; 

[example: /filters?address='address'&type=h&beds=1&baths=1&pets=1&parking=1&laundry=1&price=500-1000&rate=3.5&review_count=10&places=xxx,yyy,zzz&travelling=driving&time_limit=20]


The backend files should be in below folder structure for successful running without modifying the code:

	/
	|__ connectsql.py
	|__ flaskhelper_revised.py
	|__ google_Distance.py
	|__ google_Score.py
	|__ price_as_feature.py
	|__ project_v2.py
	|__ scrape_zips.py
	|__ test.json
	|__ yelp_scrape_real_time.py
	|__ zillow_scrape_real_time.py
	|__ crime_data/
		|__ crime.db
		|__ crime_data_cleaning.py
		|__ crime_data.csv.zip
		|__ COBRA-2009-2017.csv.zip
		|__ cobra-2018.csv.zip


Before execute the backend, ensure you have installed following library in Python3: Flask, unicodecsv, requests, lxml, numpy

To execute the project's backend, first fill in your Google API key in line 5 of file google_Distance.py. Then execute: 
	
	$ sudo python project_v2.py



## FrontEnd

To see the app directly, go to [https://cse6242-224423.appspot.com/](https://cse6242-224423.appspot.com/)

## Features

* Responsive web design
* Customized Marker Icon in Leaflet.js map
 
## Getting Started

### Install dependencies

```sh
npm install
```
or

```sh
yarn install
```
### Start Application
```sh
npm start
```

or

```sh
node app.js
```

### Front-End Dependencies

* [ejs](http://ejs.co/)
* [Google Maps APIs](https://developers.google.com/maps/)
* [Bootstrap](https://getbootstrap.com/docs/3.3/)
* [Leaflet](https://leafletjs.com)
* [JQuery](https://jquery.com/)

## Reference
Home page's fixed/scrolling background(home.css) is based on [this tutorial](https://github.com/CodyHouse/fixed-backgrounds), which is oepn sourced on Github.
