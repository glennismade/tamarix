class Transaction:
    def __init__(self, unique_id, price, date, postcode, property_type, old_new, duration, paon, saon, street, locality, town_city, district, county, category_type, record_status):
        self.unique_id = unique_id
        self.price = price
        self.date = date
        self.postcode = postcode
        self.property_type = property_type
        self.old_new = old_new
        self.duration = duration
        self.paon = paon
        self.saon = saon
        self.street = street
        self.locality = locality
        self.town_city = town_city
        self.district = district
        self.county = county
        self.category_type = category_type
        self.record_status = record_status

