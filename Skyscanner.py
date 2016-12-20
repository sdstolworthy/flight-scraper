import requests
import json


r = requests.get("http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/US/USD/en-US/BNA-iata/anywhere/anytime/anytime?apiKey=sp489739188182394334205070918236")

j = json.loads(r.content.decode('utf-8'))

flight_quotes = []

flight_places = {}


for x in j["Quotes"]:
    flight_quotes.append(x)

for p in j["Places"]:
    flight_places[p["PlaceId"]] = p
flight_quotes = sorted(flight_quotes, key=lambda k: k['MinPrice'])
for f in flight_quotes:
    if 'CountryName' in flight_places[f["OutboundLeg"]["DestinationId"]]:

    print(f['MinPrice'],flight_places[f["OutboundLeg"]["DestinationId"]]['Name'])
