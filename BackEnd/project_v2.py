from flask import Flask, render_template, request, json, jsonify, abort
import re
from price_as_feature import apart_price
from zillow_scrape_real_time import apply_filters, parse
from yelp_scrape_real_time import scrape_page, scrape_one_name
from flaskhelper_revised import *
from connectsql import *
from google_Distance import *
from google_Stores import *
from google_Score import *
from scrape_zips import get_zips
import sys



app = Flask(__name__)

# Reroute for maps download
@app.route('/filters')
def http_filters():
    """
    address, type, beds, baths, pets, parking, laundry, price, rate, review count, places, travelling, time_limit
    html request should be
    /filters?address='address'&type=h&beds=1&baths=1&pets=1&parking=1&laundry=1&price=500-1000&rate=3.5&review_count=10&places=xxx,yyy,zzz&travelling=driving&time_limit=20
    return a json object
    {
        name, address, rate, review count, price, yelp url, zillow url, scores,
        criminal data, travelling times{driving,walking,biking}, closest stores{}
    }
    """
    zillow_fiters = {}
    other_filters = {}
    address = request.args.get('address')
    print(address)
    zillow_fiters['address'] = address
    zillow_fiters['zipcode'] = address.split(' ')[-1] #last one must be zipcode, must be seperated by ' '
    if 'travelling' in request.args:
        zillow_fiters['range'] = get_range(address, request.args.get('travelling'), request.args.get('time_limit'))
        transit_r = get_distance(request.args.get('travelling'), request.args.get('time_limit'))
    else:
        zillow_fiters['range'] = get_range_default(address)
        transit_r = get_distance_default()
    if 'type' in request.args:
        zillow_fiters['type'] = request.args.get('type')
    if 'beds' in request.args:
        zillow_fiters['beds'] = request.args.get('beds')
    if 'baths'in request.args:
        zillow_fiters['baths'] = request.args.get('baths')
    if 'pets' in request.args:
        zillow_fiters['pets'] = request.args.get('pets')
    if 'parking' in request.args:
        zillow_fiters['parking'] = request.args.get('parking')
    if 'laundry' in request.args:
        zillow_fiters['laundry'] = request.args.get('laundry')
    if 'price' in request.args:
        zillow_fiters['price'] = request.args.get('price')
    if 'rate' in request.args:
        other_filters['rate'] = request.args.get('rate')
    if 'review_count' in request.args:
        other_filters['review_count'] = request.args.get('review_count')
    if 'places' in request.args:
        other_filters['places'] = request.args.get('places').split(',')

    # get the zipcode list:
    zip_list = get_zips(zillow_fiters['zipcode'], transit_r)
    print("within ", transit_r, " miles", len(zip_list), "zipcodes")

    return_result = {}
    return_apart_list = []
    return_result['type'] = "FeatureCollection"
    return_result['features'] = return_apart_list
    min_crime = sys.maxsize
    max_crime = 0

    for zipcode in zip_list:
        zillow_fiters['zipcode'] = zipcode[0]
        zillow_result = apply_filters(zillow_fiters)

        for i in range(0,len(zillow_result)):
            one_apart_result = {}
            one_apart_result['type'] = "Feature"
            # get lat, lon, google rating
            googleScore_return = getScore(zillow_result[i]['address'])
            zillow_result[i]['google rating'] = googleScore_return['rating']
            try:
                flag = ((float(zillow_fiters['range']['lat2']) <= float(googleScore_return['latitude']) <= float(zillow_fiters['range']['lat1'])) and \
                (float(zillow_fiters['range']['lng2']) <= float(googleScore_return['longitude']) <= float(zillow_fiters['range']['lng1'])))
            except ValueError:
                print("ValueError, continue")
                continue
            else:
                if not ((float(zillow_fiters['range']['lat2']) <= float(googleScore_return['latitude']) <= float(zillow_fiters['range']['lat1'])) and \
                (float(zillow_fiters['range']['lng2']) <= float(googleScore_return['longitude']) <= float(zillow_fiters['range']['lng1']))):
                    continue
                # add coord
                zillow_result[i]['coord'] = str(googleScore_return['latitude']) + "," + str(googleScore_return['longitude'])
                one_apart_geometry = {}
                one_apart_geometry['type'] = "Point"
                one_apart_geometry['coordinates'] = [googleScore_return['latitude'], googleScore_return['longitude']]
                # add criminal data
                crime_dict = json.loads(crime_info(googleScore_return['latitude'], googleScore_return['longitude']))
                zillow_result[i]['criminal'] = crime_dict
                if(min_crime>crime_dict['total_crime']):
                    min_crime = crime_dict['total_crime']

                if(max_crime<crime_dict['total_crime']):
                    max_crime = crime_dict['total_crime']
                # add travelling times
                zillow_result[i]['travelling'] = getDistance(zillow_result[i]['address'], address)
                # get stores
                stores = []
                for keyword in other_filters['places']:
                    stores.append(getStores(zillow_result[i]['address'], keyword))
                zillow_result[i]['places'] = stores

                # add yelp result
                if not zillow_result[i]['price'] is None or zillow_result[i]['title'] == "For Rent":
                    print("this is a house")
                    zillow_result[i]['review_count'] = ""
                    zillow_result[i]['rating'] = ""
                    zillow_result[i]['yelp url'] = ""
                else:
                    yelp_count = 0
                    yelp_result = scrape_one_name(zillow_result[i]['title'])
                    while len(yelp_result) == 0 and yelp_count < 3:
                        yelp_result = scrape_one_name(zillow_result[i]['title'])
                        yelp_count += 1
                    if len(yelp_result) > 0:
                        yelp_result = yelp_result[0]
                        zillow_result[i]['review_count'] = yelp_result['review_count']
                        zillow_result[i]['rating'] = yelp_result['rating']
                        zillow_result[i]['yelp url'] = yelp_result['url']
                    else:
                        zillow_result[i]['review_count'] = ""
                        zillow_result[i]['rating'] = ""
                        zillow_result[i]['yelp url'] = ""

            one_apart_properties = {}
            one_apart_properties['address'] = zillow_result[i]['address']
            one_apart_properties['bike score'] = zillow_result[i]['bike score']
            one_apart_location = {}
            one_apart_location['lat'] = googleScore_return['latitude']
            one_apart_location['lon'] = googleScore_return['longitude']
            one_apart_properties['location'] = one_apart_location
            one_apart_properties['criminal'] = zillow_result[i]['criminal']
            one_apart_properties['facts and features'] = zillow_result[i]['facts and features']
            one_apart_properties['google rating'] = zillow_result[i]['google rating']
            one_apart_properties['places'] = zillow_result[i]['places']
            one_apart_properties['price'] = zillow_result[i]['price']
            one_apart_properties['rating'] = zillow_result[i]['rating']
            one_apart_properties['review_count'] = zillow_result[i]['review_count']
            one_apart_properties['title'] = zillow_result[i]['title']
            one_apart_properties['transit score'] = zillow_result[i]['transit score']
            one_apart_properties['travelling'] = zillow_result[i]['travelling']
            one_apart_properties['url'] = zillow_result[i]['url']
            one_apart_properties['walk score'] = zillow_result[i]['walk score']
            one_apart_properties['yelp url'] = zillow_result[i]['yelp url']

            one_apart_result['geometry'] = one_apart_geometry
            one_apart_result['properties'] = one_apart_properties
            return_apart_list.append(one_apart_result)

    print("success before return...")

    for i in range(0, len(return_apart_list)):
        print(min_crime, max_crime)
        print(return_apart_list[i]['properties']['criminal']['total_crime'])
        return_apart_list[i]['properties']['criminal']['crime_score'] = \
        100*(return_apart_list[i]['properties']['criminal']['total_crime'] - min_crime)/(max_crime-min_crime)

        print(return_apart_list[i]['properties']['criminal']['crime_score'])
    #write test json
    file_name = 'test.json'
    with open(file_name,'w') as file_object:
        json.dump(return_result,file_object)
    return jsonify(return_result)


@app.route('/apartmentprice')
def clean_price():
    """
        http request should be /apartmentprice?string=string
    """
    price_string = request.args.get('string')
    return apply_filters(price_string)

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username']
    password = request.form['password']
    error = check_password(password)

    if(len(error)>0):
        response = jsonify({'status':'BAD','user':user,'pass':error})
        response.status_code = 400
        return response

    else:
        return json.dumps({'status':'OK','user':user,'pass':password})


@app.route('/test')
def test():
    with open('test.json','r') as file_object:
        contents = json.load(file_object)
    return jsonify(contents)


if __name__=="__main__":
    # app.run(host='0.0.0.0',port=80)
    # app.run(host='136.59.238.149',port=80)
    app.run()
