import geocoder

def get_current_location_coordinates():
    # Use the 'ipinfo' provider to get the user's current location based on IP address.
    g = geocoder.ip('me')

    if g.latlng:
        latitude, longitude = g.latlng
        return latitude, longitude
    else:
        return None

if __name__ == "__main__":
    coordinates = get_current_location_coordinates()
    
    if coordinates:
        latitude, longitude = coordinates
        print(f"Latitude: {latitude}, Longitude: {longitude}")
    else:
        print("Unable to retrieve location coordinates.")
