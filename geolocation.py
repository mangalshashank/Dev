import geocoder
from geopy.distance import geodesic

def get_current_location_coordinates():
    # Use the 'ipinfo' provider to get the user's current location based on IP address.
    g = geocoder.ip('me')

    if g.latlng:
        latitude, longitude = g.latlng
        return latitude, longitude
    else:
        return None
    
authorized_locations = []

def verifyLocation():
    coordinates = get_current_location_coordinates()
    authorized_locations.append(coordinates)
    for auth_location in authorized_locations:
        distance = geodesic(coordinates, auth_location).meters
        if distance < 100:
            return True
    return False
