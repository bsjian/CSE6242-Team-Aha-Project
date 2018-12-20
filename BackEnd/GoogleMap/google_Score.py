import json
import requests

def getScore(location):
    API_Key = 'AIzaSyCo11bDlBzuFl_2BvjPElW8EKnCgk_mcsU'

    loc_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+location+'&key='+API_Key
    loc_connect = requests.get(loc_url)
    loc_content = loc_connect.json() #store json file

    place_id = loc_content['results'][0]['place_id']
    lat = loc_content['results'][0]['geometry']['location']['lat']
    lng = loc_content['results'][0]['geometry']['location']['lng']

    url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid='+place_id+'&key='+API_Key
    connect = requests.get(url)
    content = connect.json()
    if 'rating' not in content['result']:
        content['result']['rating'] = "0"
    rate = content['result']['rating']

    info = {
        'rating': rate,
        'latitude': lat,
        'longitude': lng
    }
    return(info)
