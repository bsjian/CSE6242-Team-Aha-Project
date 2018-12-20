import requests
import json
import math
def get_range(address, travelling, time_limit):
    time_limit = int(time_limit)
    API_Key = 'AIzaSyCo11bDlBzuFl_2BvjPElW8EKnCgk_mcsU'

    loc_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key='+API_Key
    loc_connect = requests.get(loc_url)
    print(loc_connect.status_code)
    loc_content = loc_connect.json() #store json file

    center_lat = loc_content['results'][0]['geometry']['location']['lat']
    center_lng = loc_content['results'][0]['geometry']['location']['lng']

    if travelling == 'driving':
        dis =  ( time_limit /60 * 64373.8 )  #the unit is meter
    elif travelling == 'bicycling':
        dis =  ( time_limit /60 * 22000 )
    elif travelling == 'walking':
        dis =  ( time_limit /60 * 4000 )

    lat = dis/(math.sqrt(2)*(76652.923860667727*2))#in atalanta, 1 lat = 76.652923860667727 km
    lng = dis/(math.sqrt(2)*(111000*2))# in atalanta, 1 lat = 111km

    info = {
        'lat1':center_lat + lat,
        'lng1':center_lng + lng,
        'lat2':center_lat - lat,
        'lng2':center_lng - lat,
    }
    print("exit flask helper...")
    return info
    #return(str(info['lat1']) + "," + str(info['lng1']) + "," + str(info['lat2']) + "," + str(info['lng2']))

def get_range_default(address):
    return get_range(address, 'walking', 20)
