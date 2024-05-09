from tkinter import *
import tkintermapview
from RoutesHandler import *
from live_drones import *


def update_map(map_widget_arg):
    update_drones_on_map(map_widget_arg)
    root.after(1000, update_map, map_widget_arg)


get_addresses()

root = Tk()
root.geometry("1920x1080")

my_label = LabelFrame(root)
my_label.pack(pady=20)

map_widget = tkintermapview.TkinterMapView(my_label, width=1500, height=800)
map_widget.set_position(49.39, 8.67)
map_widget.set_zoom(15)

#placing markers (mongoDB only)
place_markers(map_widget)

#drawing routes (neo4j & saved data from mongodb to save ressources)
draw_routes(map_widget)

#placing drones on map (mongoDB & redis)
generate_data()
load_drones()
place_drones_on_map(map_widget)

update_map(map_widget)

map_widget.pack()

root.mainloop()
