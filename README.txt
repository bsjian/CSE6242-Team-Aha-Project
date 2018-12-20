# CSE 6242 Team Aha Project

To run our project locally:

(1)First, follow the README_BackEnd to run the backend server.

(2)Second, follow the README_FrontEnd to run the front end server.
## IMPORTANT: Please make sure that the local host and port number of backend server is correctly added to line 25 and line 27 in app.js in FrontEnd directory. (i.e. Postname:127.0.0.1.  Port: 3000)

(3)Third, open your web browser and visit our website via the host and port number of your frontend program. (i.e. 127.0.0.1:3000)





*****************************************************************
**********************README_BackEnd*****************************
* This is the Readme for Fall 2018 CSE6242 Team Aha backend files

************NOTICE***************
This project does contain scraping programs
that do not respect some websites' /robots.txt
We are aware that this is not a good manner and 
we are not using and will never use those code 
other than this class project. 

***************IMPORTANT INFORMATION**************
Execute the programs on large searching range or 
large number of searches in a short period of time 
CAN AND WILL RESULT IP BANNED from some websites!
**************************************************

There are 11 python files: 
connectsql.py:				For querying the sqlite storing crime data;
flaskhelper_revised.py:		Helper functions for main flask app;
google_Distance.py: 		For getting distance between locations using Google Map API; [fill in your API key at '# fill in your API key' before running]
google_Score.py:			For getting place's rating on Google Map using Google Places API; [fill in your API key at '# fill in your API key' before running]
google_Stores.py:			For getting nearby store information using Google Places API; [fill in your API key at '# fill in your API key' before running]
price_as_feature.py:		For handling special price information format for apartments on Zillow;
project_v2.py:				Main flask app; 
scrape_zips.py:				For scraping zip codes within distance from a website; 
yelp_scrape_real_time.py 	For scraping real time yelp data;
zillow_scrape_real_time.py 	For scraping real time zillow data;
crime_data_cleaning.py 		For cleaning the crime dataset; 

There is also a folder 'crime_data' containing sqlite dataset storing crime data, original dataset and python file for cleaning the dataset. 

There is also a file 'test.json' containing a example/testing json file returned by backend. 

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








*****************************************************************
**********************README_frontEnd*****************************
* This is the Readme for Fall 2018 CSE6242 Team Aha frontend files
## Live Demo

To see the app, go to [https://cse6242-224423.appspot.com/](https://cse6242-224423.appspot.com/)

## Features

* Responsive web design
* Customized Marker Icon in Leaflet.js map
 
## Getting Started

### Clone or download this repository

```sh
git clone https://github.gatech.edu/bjian3/CSE6242-Front-End.git
```

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


## Built with

### Front-end

* [ejs](http://ejs.co/)
* [Google Maps APIs](https://developers.google.com/maps/)
* [Bootstrap](https://getbootstrap.com/docs/3.3/)
* [Leaflet](https://leafletjs.com)
* [JQuery](https://jquery.com/)




