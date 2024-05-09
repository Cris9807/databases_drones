import neo4j
from neo4j import GraphDatabase
from AddressesHandler import *

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4jneo4j")


def draw_routes(map_widget):

    with (GraphDatabase.driver(URI, auth=AUTH) as driver):
        driver.verify_connectivity()

        records, summary, keys = driver.execute_query(
            "MATCH (s:Location)-->(e:Location) RETURN s.location_id as start, e.location_id as end"
        )

        for result in records:
            start_location = get_address_by_id(result["start"])["place"]["geo"]
            end_location = get_address_by_id(result["end"])["place"]["geo"]

            start_position = (start_location["latitude"] , start_location["longitude"])
            end_position = (end_location["latitude"] , end_location["longitude"])

            map_widget.set_path([start_position, end_position])
