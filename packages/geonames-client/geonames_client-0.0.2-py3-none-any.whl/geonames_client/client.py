'''
All client code for interacting with the API goes here
'''
import requests


def get_coordinates_from_suburb(suburb, state='NSW'):
    url = 'http://v0.postcodeapi.com.au/suburbs.json?name=%s&state=%s' % (suburb, state)
    response = requests.request("GET", url)
    return response.json()


def surrounding_suburbs_from_coordinates(latitude, longitude, distance=4000):
    url = 'http://v0.postcodeapi.com.au/radius.json?latitude=%s&longitude=%s&distance=%s' % (latitude, longitude, distance)
    response = requests.request("GET", url)
    return response.json()


def filter_response(surrounding_list):
    filter_dict = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
    return [filter_dict(x, ('name', 'postcode', 'state')) for x in surrounding_list]


def get_surrounding_results(suburb, distance=4000):
    coordinate_response = get_coordinates_from_suburb(suburb)[0]
    return(filter_response(surrounding_suburbs_from_coordinates(coordinate_response['latitude'], coordinate_response['longitude'], distance)))
