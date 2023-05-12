from datetime import datetime, timedelta
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager

my_data_manager = DataManager()
my_flight_search = FlightSearch()
my_notification_manager = NotificationManager()

sheet_json = my_data_manager.get_sheet()

# Cycle for to read all row in excel sheet
for code in sheet_json:
    # if condition to check IATACODE is empty
    if code["iataCode"] == "":
        iata_code = my_flight_search.get_code_city(code["city"])
        my_data_manager.update_sheet(code["id"], iata_code)

tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
six_month = (datetime.now() + timedelta(days=(6*30))).strftime("%d/%m/%Y")

# Cycle for to read all row in excel sheet
for search in sheet_json:
    # call search_fly method
    flight_find = my_flight_search.search_fly(
        fly_from="LON",
        fly_to=search["iataCode"],
        date_from=tomorrow,
        date_to=six_month
    )
    # "if" condition to check is lower price of my budget
    if flight_find is not None and flight_find.price < search["lowestPrice"]:
        fly_text = f"Low price alert! Only £{flight_find.price} to fly from {flight_find.origin_city}-{flight_find.origin_airport} to {flight_find.destination_city}-{flight_find.destination_airport}, from {flight_find.out_date} to {flight_find.return_date}."
        # Call sent_text method
        my_notification_manager.send_text(fly_text)
