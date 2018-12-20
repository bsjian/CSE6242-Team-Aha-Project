from flask import Flask, render_template, request, json, jsonify, abort
import re
from price_as_feature import apart_price
from zillow_scrape_real_time import apply_filters
from yelp_scrape_real_time import scrape_page, scrape_one_name
from flask_helper import *
from connectsql import *
from google_Distance import *
from google_Stores import *
from google_Score import *

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
    if 'travelling' in request.args:
        zillow_fiters['range'] = get_range(address, request.args.get('travelling'), request.args.get('time_limit'))
    else:
        zillow_fiters['range'] = get_range_default(address)
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
    if 'rate' in request.args:
        other_filters['rate'] = request.args.get('rate')
    if 'review_count' in request.args:
        other_filters['review_count'] = request.args.get('review_count')
    if 'places' in request.args:
        other_filters['places'] = request.args.get('places').split(',')

    zillow_result = apply_filters(zillow_fiters)
    return_result = {}
    for i in range(0,len(zillow_result)):
        # add yelp result
        yelp_count = 0
        yelp_result = scrape_one_name(zillow_result[i]['title'])
        if len(yelp_result) > 0:
            yelp_result = yelp_result[0]
            zillow_result[i]['review_count'] = yelp_result['review_count']
            zillow_result[i]['rating'] = yelp_result['rating']
            zillow_result[i]['yelp url'] = yelp_result['url']
        elif yelp_count < 5:
            yelp_result = scrape_one_name(zillow_result[i]['title'])
            yelp_count += 1
        else:
            zillow_result[i]['review_count'] = ""
            zillow_result[i]['rating'] = ""
            zillow_result[i]['yelp url'] = ""
        # get lat, lon, google rating
        googleScore_return = getScore(zillow_result[i]['address'])
        zillow_result[i]['google rating'] = googleScore_return['rating']
        # add criminal data
        zillow_result[i]['criminal'] = crime_info(googleScore_return['latitude'], googleScore_return['longitude']) #########################
        # add travelling times
        zillow_result[i]['travelling'] = getDistance(zillow_result[i]['address'], address)
        # get stores
        stores = []
        for keyword in other_filters['places']:
            stores.append(getStores(zillow_result[i]['address'], keyword))
        zillow_result[i]['places'] = stores
        return_result[i] = zillow_result[i]
    print("success before return...")

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
