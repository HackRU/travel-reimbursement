import config
import json
import googlemaps
from datetime import datetime
from pymongo import MongoClient

def find_distance(event, context):
    tests = MongoClient(config.DB_URI)['tests']
    db.authenticate(config.DB_USER, config.DB_PASS)
    start_loc = db.tests.find_one({"email": event['email']}, {"address": 1, "city": 1, "state": 1, "zip": 1}) # will be called using email of pertinent user

    start_loc = start_loc['address'] + ' ' + start_loc['city'] + ', ' + start_loc['state'] + ' ' +  start_loc['zip'] 

    gmaps = googlemaps.Client(key=config.maps_key)

    values = {
                    'bus': {}, 
                    'train': {},
                    'car': {}
             }

    rac_address = config.hackru_location['address'] + ' ' + config.hackru_location['city'] + ', ' + config.hackru_location['state'] + ' ' + config.hackru_location['zip']

    bus_values = gmaps.distance_matrix(
            origins = start_loc['address'] + ' ' + start_loc['city'] + ', ' + start_loc['state'] + ' ' + start_loc['zip'], 
            destinations = rac_address,
            units = 'imperial', 
            mode = 'transit',
            transit_mode = 'bus')
    
    values['bus'] = {'distance': bus_value['rows'][0]['elements'][0]['distance']['value'], 'reimbursement': config.bus_miles_reimburse* (bus_value['rows'][0]['elements'][0]['distance']['value'])}

    train_values = gmaps.distance_matrix(
            origins = start_loc['address'] + ' ' + start_loc['city'] + ', ' + start_loc['state'] + ' ' + start_loc['zip'], 
            destinations = rac_address,
            units = 'imperial', 
            mode = 'transit',
            transit_mode = 'train')

    values['train'] = {'distance': train_values['rows'][0]['elements'][0]['distance']['value'], 'reimbursement': config.train_values_miles_reimburse* (bus_value['rows'][0]['elements'][0]['distance']['value'])}

    car_values = gmaps.distance_matrix(
            origins = start_loc['address'] + ' ' + start_loc['city'] + ', ' + start_loc['state'] + ' ' + start_loc['zip'], 
            destinations = rac_address,
            units = 'imperial', 
            mode = 'driving', 
            traffic_model = 'best_guess')

    values['car'] = {'distance': car_values['rows']['elements']['distance']['value'], 'reimbursement': car_values['rows'][0]['elements'][0]['distance']['value'] * config.car_miles_reimburse}

    return {'statusCode': 200, 'body': json.dumps(values)}

