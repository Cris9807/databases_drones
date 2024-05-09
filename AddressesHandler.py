from pymongo import MongoClient

def get_database():
    CONNECTION_STRING = "mongodb://cris:cris@127.0.0.1/Parcel"
    client = MongoClient(CONNECTION_STRING)
    return client

def get_addresses():
    dbname = get_database()
    addressesCollection = dbname.Parcel.addresses
    addresses = addressesCollection.find()
    for address in addresses:
        address_ids = address["location"]["ids"]
        for address_id in address_ids:
            locationId = address_id["locationId"]


def get_address_by_id(address_id):
    dbname = get_database()
    addresses_collection = dbname.Parcel.addresses
    return addresses_collection.find_one({"location.ids.locationId": str(address_id)}, {"location.ids.locationId": 1, "place.geo": 1})


def place_markers(map_widget):
    dbname = get_database()
    addresses_collection = dbname.Parcel.addresses

    for address in addresses_collection.find({}, {"location.ids.locationId": 1, "place.geo": 1}):
        latitude = address['place']['geo']['latitude']
        longitude = address['place']['geo']['longitude']

        map_widget.set_marker(latitude, longitude)
