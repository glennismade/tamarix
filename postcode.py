class Postcode:
    def __init__(self, code, latitude, longitude, county=None):
        self.code = code
        self.latitude = latitude
        self.longitude = longitude
        self.county = county
