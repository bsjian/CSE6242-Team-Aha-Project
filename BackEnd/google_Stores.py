import json
import requests
from google_Distance import getDistance

def getStores(location , keywords):
    API_Key = 'AIzaSyCo11bDlBzuFl_2BvjPElW8EKnCgk_mcsU'

    location_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+location+'&key='+API_Key

    loc_connect = requests.get(location_url)
    loc_content= loc_connect.json() #store json file
    if len(loc_content['results']):
        latitude = str(loc_content['results'][0]['geometry']['location']['lat'])
        longitude = str(loc_content['results'][0]['geometry']['location']['lng'])

        cloest_url ='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+latitude+','+longitude+'&rankby=distance&keyword='+keywords+'&key='+API_Key

        cloest_connect = requests.get(cloest_url)
        cloest_content = cloest_connect.json()
        if 'results' not in cloest_content or len(cloest_content['results']) < 1:
            nearby = {'cloest_store_name':"",
                'cloest_store_lng':"",
                'cloest_store_lat':"",
                'number_of_stores':0,
                'walk_distance':"",
                'walk_duration':"",
                'bicycl_distance':"",
                'bicycl_duration':"",
                'drive_distance':"",
                'drive_duration':""}
            return nearby
        cloest_name = cloest_content['results'][0]['name']
        cloest_id = 'place_id:'+str(cloest_content['results'][0]['place_id'])
        cloest_store_lng = cloest_content['results'][0]['geometry']['location']['lng']
        cloest_store_lat = cloest_content['results'][0]['geometry']['location']['lat']

        distance = getDistance(location, cloest_id)
        list = distance['walk_distance'].split(" ")
        dis = str(list[0]*3)

        stores_url ='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+latitude+','+longitude+'&radius='+dis+'&keyword='+keywords+'&key='+API_Key
        stores_connect = requests.get(stores_url)
        stores_content = stores_connect.json()
        stores_list = stores_content['results']
        num_stores = len(stores_list)

        nearby = {'cloest_store_name':cloest_name,
            'cloest_store_lng': cloest_store_lng,
            'cloest_store_lat': cloest_store_lat,
            'number_of_stores':num_stores,
            'walk_distance':distance['walk_distance'],
            'walk_duration':distance['walk_duration'],
            'bicycl_distance':distance['bicycl_distance'],
            'bicycl_duration':distance['bicycl_duration'],
            'drive_distance':distance['drive_distance'],
            'drive_duration':distance['drive_duration']}
    else:
        nearby = {'cloest_store_name':"",
            'cloest_store_lng':"",
            'cloest_store_lat':"",
            'number_of_stores':"",
            'walk_distance':"",
            'walk_duration':"",
            'bicycl_distance':"",
            'bicycl_duration':"",
            'drive_distance':"",
            'drive_duration':""}
    return(nearby)

    #print( json.dumps(stores_content, indent=4, sort_keys=True) )
