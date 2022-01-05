import json

notfound = {
    "message": "Sorry, we couldn't find your booking details"
}

with open('bookingScheme.json') as json_file:
    booking = json.load(json_file)

def treat(response):
    if ('errors' in response.keys()):
        return notfound, 404
    reservation = response['data']['reservation']
    for (index, passenger) in enumerate(reservation['passengers']):
        booking['passengers'][index]['firstName'] = passenger['firstName']
        booking['passengers'][index]['lastName'] = passenger['lastName']
    for (index, itinerary) in enumerate(reservation['itinerary']['connections']):
        if (index > 0): booking['flights'].append(booking['flights'][0])
        flight = booking['flights'][index]
        flight['isCancelled'] = itinerary['isCancelled']
        flight['originName'] = itinerary['originName']
        flight['originCode'] = itinerary['originCode']
        flight['destinationAirportCode'] = itinerary['destinationAirportCode']
        flight['destinationCityCode'] = itinerary['destinationCityCode']
        flight['destinationCityName'] = itinerary['destinationCityName']
        flight['connectionDepartureDate'] = itinerary['connectionDepartureDate']
        flight['connectionArrivalDate'] = itinerary['connectionArrivalDate']
        flight['areAllPassengersCheckedIn'] = itinerary['checkInStatus']['areAllPassengersCheckedIn']
        flight['isCheckInOpen'] = itinerary['checkInStatus']['isCheckInOpen']
        for (indexSeg, segment) in enumerate(itinerary['segments']):
            elem = booking['flights'][index]['segments'][indexSeg]
            elem['isCancelled'] = segment['isCancelled']
            elem['origin']['cityName'] = segment['origin']['cityName']
            elem['origin']['airportName'] = segment['origin']['airportName']
            elem['origin']['airportCode'] = segment['origin']['airportCode']
            elem['destination']['cityName'] = segment['destination']['cityName']
            elem['destination']['airportName'] = segment['destination']['airportName']
            elem['destination']['airportCode'] = segment['destination']['airportCode']
            elem['flight']['carrierName'] = segment['flight']['carrierName']
            elem['flight']['duration'] = segment['flight']['duration']
            elem['flight']['flightNumber'] = segment['flight']['flightNumber']
            elem['flight']['scheduledDeparture'] = segment['flight']['scheduledDeparture']
            elem['flight']['scheduledArrival'] = segment['flight']['scheduledArrival']
            elem['flight']['departureDate'] = segment['flight']['departureDate']
            elem['flight']['arrivalDate'] = segment['flight']['arrivalDate']
    return booking
