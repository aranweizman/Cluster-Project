import folium
import numpy
import pandas as pd
import requests
from bs4 import BeautifulSoup


def line_to_trip_id(line_id):
    date = "20230123"
    website_prefix = "https://transitfeeds.com"
    operator_url = website_prefix + "/p/ministry-of-transport-and-road-safety/820/latest/routes?agency=18"

    # get route link
    source = requests.get(operator_url).content
    soup = BeautifulSoup(source, 'html.parser')
    td_tags = soup.select("td")
    a = None  # link label with route link

    for td in td_tags:
        div = td.find("div")
        if div is None:
            continue

        small = div.find("small")
        if small is None:
            continue

        if small.text == line_id:
            a = td.find("a")

    route_link_postfix = a["href"] + "/"

    # get trip id
    trip_source = requests.get(website_prefix + route_link_postfix + date).content
    soup = BeautifulSoup(trip_source, 'html.parser')
    code = soup.select_one("td:has(code)").select_one('code')
    return code.string


def trip_id_to_shape(trip_id):
    print(trip_id)
    trips = pd.read_csv("all_routes_data/trips.csv")
    shape_id = trips.query(f"trip_id == '{trip_id}'")["shape_id"].iloc[0]
    shape_id_s = str(numpy.int32(shape_id))
    shapes = pd.read_csv("all_routes_data/shapes.csv")
    shape = shapes.query(f"shape_id == {shape_id_s}")
    shape = shape[["shape_pt_lat", "shape_pt_lon"]].values.tolist()
    return shape


def draw_shape_on_map(shape):
    _map = folium.Map(location=shape[0], zoom_start=12)

    # add the path to the map
    folium.PolyLine(shape, color="red", weight=2.5, opacity=1).add_to(_map)

    _map.show_in_browser()


draw_shape_on_map(trip_id_to_shape(line_to_trip_id("10889-2-0")))
