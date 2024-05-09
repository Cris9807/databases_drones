import os
import threading
import tkinter
import tkintermapview
from PIL import Image, ImageTk

import redis
import hiredis

from pymongo import MongoClient


drones = {}
current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))

drones_markers = dict()


def get_database():
    CONNECTION_STRING = "mongodb://cris:cris@127.0.0.1/Parcel"
    client = MongoClient(CONNECTION_STRING)
    return client


def load_drones():
    dbname = get_database()
    drones_collection = dbname.Parcel.drones
    for drone in drones_collection.find():
        drones[str(drone["name"])] = drone


def generate_data():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.hset('HD-SRH1', mapping={
        'location_lat': '49.401762',
        "location_long": '8.679460',
        "battery": 99
    })
    r.hset('HD-SRH2', mapping={
        'location_lat': '49.408385',
        "location_long": '8.668200',
        "battery": 90
    })
    r.hset('HD-SRH3', mapping={
        'location_lat': '49.405208',
        "location_long": '8.676569',
        "battery": 19
    })
    r.hset('HD-SRH4', mapping={
        'location_lat': '49.404947',
        "location_long": '8.675830',
        "battery": 9
    })
    r.hset('HD-SRH5', mapping={
        'location_lat': '49.403455',
        "location_long": '8.681733',
        "battery": 55
    })
    r.hset('HD-SRH6', mapping={
        'location_lat': '49.406131',
        "location_long": '8.676970',
        "battery": 87
    })
    r.hset('HD-SRH7', mapping={
        'location_lat': '49.406087',
        "location_long": '8.686356',
        "battery": 76
    })
    r.hset('HD-SRH8', mapping={
        'location_lat': '49.398202',
        "location_long": '8.686717',
        "battery": 23
    })
    r.hset('HD-SRH9', mapping={
        'location_lat': '49.387250',
        "location_long": '8.662877',
        "battery": 99
    })


def drone_live_data(drone_id):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r.hgetall(str(drone_id))


def place_drones_on_map(map_widget):
    for drone_name in drones:
        drone_data = drone_live_data(drone_name)
        latitude = float(drone_data["location_lat"])
        longitude = float(drone_data["location_long"])

        droneIcon = ImageTk.PhotoImage(Image.open(os.path.join("./icons/drone.png")).resize((55, 55)))
        drone_marker = map_widget.set_marker(latitude, longitude, icon=droneIcon)
        drones_markers[drone_name] = drone_marker


def update_drones_on_map(map_widget):
    for drone_name in drones:
        drone_data = drone_live_data(drone_name)
        latitude = float(drone_data["location_lat"])
        longitude = float(drone_data["location_long"])

        drone_marker = drones_markers[drone_name]
        drone_marker.set_position(latitude, longitude)