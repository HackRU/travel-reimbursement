def find_distance(event, context):
    tests = MongoClient(config.DB_URI)['tests']
    db.authenticate(config.DB_USER, config.DB_PASS)
    start_loc = db.tests.find_one({"email": event['email']}, {"address": 1, "city": 1, "state": 1, "zip": 1}) # will be called using email of pertinent user
    maps_key = 'IzaSyCvwVRp4iZXgRZrR8CJGsVkAdjc8IyQrV8'
    distancematrix_base_url = '//maps.googleapis.com/maps/api/distancematrix/json?'

    # this probably needs to be changed, not sure how to get these parameters    
    url = distancematrix_base_url + urllib.urlencode ({
	'units': "imperial",
	'origins': "%s" % origins,
	'destinations': "%s" % destinations,
	'key': maps_key,
    })
    result = requests.get(url,params=start_loc).json()
    
    if (result['status'] != 'ok':
	return ({"status":result['rows']['elements']['status'],"body":"Google api request failed."})
    
    distanceText = result['rows']['elements']['text'].split() #if we want distance in miles, it returns as a string   
    mileage = distanceText[0]
    cpm = 0.27; # cost per mile
    reimbursement = cpm * mileage; 
    
    return reimbursement 
