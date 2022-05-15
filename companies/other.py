import json

notfound = {
    "message": "Sorry, we couldn't find your booking details"
}

def treat(response):
    with open('bookingFlightScheme.json') as json_file:
        booking = json.load(json_file)
    if ('success' in response.json()):
        return notfound, 404
    reservation = response.json()[0]
    booking['type'] = "flight"
    flight = booking['trips'][0]
    flight['isCancelled'] = True if reservation['flight_status'] == 'cancelled' else False
    flight['originName'] = reservation['departure']['airport']
    flight['originCode'] = reservation['departure']['iata']
    flight['destinationAirportCode'] = reservation['arrival']['iata']
    flight['destinationCityCode'] = reservation['arrival']['iata']
    flight['destinationCityName'] = reservation['arrival']['airport']
    flight['departureDateTime'] = reservation['departure']['scheduled']
    flight['arrivalDateTime'] = reservation['arrival']['scheduled']
    segment = flight['segments'][0]
    segment['isCancelled'] = flight['isCancelled']
    segment['origin']['cityName'] = flight['originName']
    segment['origin']['airportName'] = flight['originName']
    segment['origin']['airportCode'] = flight['originCode']
    segment['destination']['cityName'] = flight['destinationCityName']
    segment['destination']['airportName'] = flight['destinationCityName']
    segment['destination']['airportCode'] = flight['destinationCityCode']
    segment['flight']['carrierName'] = reservation['airline']['name']
    # segment['flight']['duration'] = segment['flight']['duration']
    segment['flight']['flightNumber'] = reservation['flight']['iata']
    segment['flight']['scheduledDeparture'] = reservation['departure']['scheduled']
    segment['flight']['scheduledArrival'] = reservation['arrival']['scheduled']
    segment['flight']['departureDate'] = reservation['departure']['scheduled']
    segment['flight']['arrivalDate'] = reservation['arrival']['scheduled']
    return booking
