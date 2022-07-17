import json

notfound = {
    "message": "Sorry, we couldn't find your booking details"
}

def treat(response):
    with open('bookingTrainScheme.json') as json_file:
        booking = json.load(json_file)
    if (response.status_code == 404):
        print("WARNING: SNCF return a non-found response")
        return notfound, 404
    if (response.status_code == 409):
        print("WARNING: SNCF return that the booking has been cancelled")
        return notfound, 409
    print(response.status_code)
    reservation = response.json()['response']
    booking['type'] = "train"
    for (index, itinerary) in enumerate(reservation['trips']):
        if (index > 0): booking['trips'].append(booking['trips'][0].copy())
        train = booking['trips'][index]
        train['arrivalTime'] = itinerary['trip']['arrivalTimeLabel']
        train['departureTime'] = itinerary['trip']['departureTimeLabel']
        train['duration'] = itinerary['trip']['duration']
        train['originName'] = itinerary['trip']['originLabel']
        train['destinationCityName'] = itinerary['trip']['destinationLabel']
        train['departureDateTime'] = itinerary['trip']['tripDetails']['outwardJourney']['departureDate']
        train['arrivalDateTime'] = itinerary['trip']['tripDetails']['outwardJourney']['arrivalDate']
        train['isRoundTrip'] = itinerary['trip']['isRoundTrip']
        train['routeLabel'] = itinerary['trip']['routeLabel']
        for (indexT, traveller) in enumerate(itinerary['trip']['tripDetails']['outwardJourney']['travelersIdentity']):
            train['travellers'].append(traveller)
    return booking
