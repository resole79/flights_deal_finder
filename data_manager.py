import os
import requests
from dotenv import load_dotenv

load_dotenv()

projectName = os.environ.get("SHEETY_PROJECT_NAME")
sheetName = os.environ.get("SHEETY_SHEET_NAME")
username = os.environ.get("SHEETY_USERNAME")
bearer_headers = {"Authorization": f"Basic {os.environ.get('SHEETY_BEARER_HEADERS')}"}

sheety_url = f"https://api.sheety.co/{username}/{projectName}/{sheetName}"

# Class DataManager: This class is responsible for talking to the Google Sheet.
class DataManager:
    """
    # Class DataManager: This class is responsible for talking to the Google Sheet.
    instance: sheety_json
    method:get_sheet, update_sheet
    """
    def __init__(self):
        self.sheety_json = {}

    # Method to get excel sheet by sheety API
    def get_sheet(self):
        """# Method to get sheet by sheety API
        return:
        sheety_json -> dict
        """
        sheety_response = requests.get(sheety_url, headers=bearer_headers)
        self.sheety_json = sheety_response.json()["prices"]
        return self.sheety_json
    
    # Method to update excel sheet by sheety API
    def update_sheet(self, id, iata):
        """
        # Method to update excel sheet by sheety API
        accept:
        id -> int
        iata -> str IATACODE
        """
        new_sheety_json = {
            "price": {
                "iataCode": iata,
            },
        }
        response = requests.put(url=f"{sheety_url}/{id}", json=new_sheety_json, headers=bearer_headers)
        print(response.text)
