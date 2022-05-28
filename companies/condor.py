import json
import airportsdata

# Load IATA to Name
airports = airportsdata.load('IATA')  # key is IATA code

notfound = {
    "message": "Sorry, we couldn't find your booking details"
}

def treat(response):
    with open('bookingFlightScheme.json') as json_file:
        booking = json.load(json_file)
    if (response['code'] == 'RT_1001' or response == notfound):
        print("WARNING: Condor return a non-success response")
        return notfound, 404
    reservation = response['data'][0]
    booking['type'] = "flight"
    for (index, passenger) in enumerate(reservation['paxes']):
        booking['passengers'][index]['firstName'] = passenger['firstName']
        booking['passengers'][index]['lastName'] = passenger['lastName']
    for (index, itinerary) in enumerate(reservation['items'][0]['flightJourneys']):
        if (index > 0): booking['trips'].append(booking['trips'][0].copy())
        flight = booking['trips'][index]
        flight['originName'] = airports[itinerary['origin']]['city']
        flight['originCode'] = itinerary['origin']
        flight['destinationAirportCode'] = itinerary['destination']
        flight['destinationCityCode'] = itinerary['destination']
        flight['destinationCityName'] = airports[itinerary['destination']]['city']
        flight['departureDateTime'] = itinerary['departure']
        flight['arrivalDateTime'] = itinerary['arrival']
        for (indexSeg, segment) in enumerate(itinerary['segments']):
            elem = flight['segments'][indexSeg]
            elem['origin']['cityName'] = airports[segment['origin']]['city']
            elem['origin']['airportName'] = airports[segment['origin']]['name']
            elem['origin']['airportCode'] = segment['origin']
            elem['destination']['cityName'] = airports[segment['destination']]['city']
            elem['destination']['airportName'] = airports[segment['destination']]['name']
            elem['destination']['airportCode'] = segment['destination']
            elem['flight']['carrierName'] = segment['operatingCarrier']
            elem['flight']['duration'] = segment['flightDuration']
            elem['flight']['flightNumber'] = segment['flightNumber']
            elem['flight']['scheduledDeparture'] = segment['departure']
            elem['flight']['scheduledArrival'] = segment['arrival']
            elem['flight']['departureDate'] = segment['departure']
            elem['flight']['arrivalDate'] = segment['arrival']
    return booking
