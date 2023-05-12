import os
import requests
from dotenv import load_dotenv
from flight_data import FlightData

load_dotenv()

endpoint_tequila = "https://api.tequila.kiwi.com/"
header_tequila = {"apikey": os.environ.get("TEQUILA_API_KEY")}


# Class FlightSearch: This class is responsible for talking to the Flight Search API.
class FlightSearch:
    """# Class FlightSearch: This class is responsible for talking to the Flight Search API.
    method : get_code_city, search_fly
    """

    # Method to get IATACODE
    def get_code_city(self, city):
        """# Method to get IATACODE
        accept:
        city -> str
        
        return:
        code_city["code"] -> str IATACODE
        """
        tequila_param = {"term": city, "location_types": "city"}
        tequila_response = requests.get(
            url=f"{endpoint_tequila}locations/query",
            headers=header_tequila,
            params=tequila_param
        )
        tequila_json = tequila_response.json()
        code_city = tequila_json["locations"][0]
        
        return code_city["code"]
        
    # Method to search fly
    def search_fly(self, fly_from, fly_to, date_from, date_to):
        """
        # Method to search fly
        accept:
        fly_from -> str IATACODE
        fly_to -> str IATACODE
        date_from -> str date gg/mm/yyyy
        date_to -> str date gg/mm/yyyy
        
        return:
        flight_data -> object
        """
        tequila_search_param = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        tequila_search_response = requests.get(
            url=f"{endpoint_tequila}v2/search",
            headers=header_tequila,
            params=tequila_search_param
        )
        try:
            tequila_search_json = tequila_search_response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {fly_to}.")
            return None
        
        date_to_fly = tequila_search_json["route"][0]["local_departure"].split("T")[0].split("-")
        date_to_fly = f"{date_to_fly[2]}/{date_to_fly[1]}/{date_to_fly[0]}"
        
        date_to_return = tequila_search_json["route"][1]["local_departure"].split("T")[0].split("-")
        date_to_return = f"{date_to_return[2]}/{date_to_return[1]}/{date_to_return[0]}"
        
        flight_data = FlightData(
            price=tequila_search_json["price"],
            origin_city=tequila_search_json["route"][0]["cityFrom"],
            origin_airport=tequila_search_json["route"][0]["flyFrom"],
            destination_city=tequila_search_json["route"][0]["cityTo"],
            destination_airport=tequila_search_json["route"][0]["flyTo"],
            out_date=date_to_fly,
            return_date=date_to_return
        )
        return flight_data
