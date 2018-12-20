#!/usr/bin/python3
'''
Use API to get zpids of a specific location
'''
import csv
import sys
import pandas
from xml.etree import cElementTree as ElementTree
import requests
import urllib
import json

class ZillowScraping(object):

    def __init__(object):
        object.api_id = 'X1-ZWz18a64m9g6bv_38l6u'
        object.address= None
        object.zipcode= None
    #for each department
    def get_content(object):
        '''
        Get basic information
        input object/address/zipcode
        make a get_data call
        '''
        #url example
        #   http://www.zillow.com/webservice/GetSearchResults.htm?
        #   zws-id=X1-ZWz18a64m9g6bv_38l6u
        #   &address=2114+Bigelow+Ave
        #   &citystatezip=Seattle%2C+WA
        url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm'

        parameters = {
            'zws-id': object.api_id,
            'address': object.address,
            'citystatezip': object.zipcode
        }
        return(object.get_data(url,parameters))

#    def get_property(object):
#
#        #Get detail properties
#
#        url = 'https://www.zillow.com/webservice/GetZestimate.htm'
#
#        parameters = {
#            'zws-id': object.api_id,
#            'zpid':object.zpid
#
#        }
#        return(object.get_data(url,parameters))


    def get_data(object, url, parameters):
        '''
        make url calls
        return the data
        '''
        try:
            response = requests.get(url=url, params=parameters)
            print(response.url)
        except:
            print("Can't make api call (get_data)")

        try:
            tree = ElementTree.fromstring(response.content)
            #tree = ElementTree.parse(connect.text)
            '''
            parse the XML
            write the zpids
            '''
            subtrees = tree.findall("response/results/result")

            for subtree in subtrees:
                zpid = subtree.find("zpid").text
                lat = subtree.find("address/latitude").text
                long = subtree.find("address/longitude").text
                try:
                    yearBuilt = subtree.find("yearBuilt").text
                except:
                    yearBuilt = None

                parameters = {
                    "zpid":zpid,
                    "latitude":lat,
                    "longitude":long,
                    "yearBuilt":yearBuilt
                }

                print ("Writing data to output file")
                print(parameters)
                with open("zpids.csv",'a+')as csvfile:
                    fieldnames = ['zpid','latitude','longitude','yearBuilt']
                    writer = csv.DictWriter(csvfile,fieldnames)
                    writer.writerow(parameters)

            return(tree)
        except ElementTree.ParseError:
            print("Zillow response is not XML")
