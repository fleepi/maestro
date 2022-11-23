from companies import airfrance, klm, condor, sncf, delta, other
from flask import Flask, jsonify, request
import json
import requests
import copy
import os
from datetime import timedelta
from requests_cache import CachedSession

app = Flask(__name__)

# ~~ MESSAGES ~~
error_500 = {"message": "Maestro Internal Server Error"}
error_400 = {"message": "Bad Request - Missing parameters"}

bookingCodeDemo = 'FLEEPI'

@app.route('/airfrance')
def get_airFrance():
    bookingCodeParam = request.args.get("bookingCode")
    lastNameParam = request.args.get("lastName")
    # Check parameters
    if bookingCodeParam is None or lastNameParam is None:
        return error_400, 400
    # Detect demo and return mock
    if (bookingCodeParam == bookingCodeDemo):
        with open('mocks/airfrance.json') as json_file:
            return json.load(json_file)
    # TODO: .env with urls
    url = "https://iran.airfrance.com/gql/v1?bookingFlow=LEISURE"
    payload='{\n\"operationName\":\"reservation\",\n\"variables\":{\"bookingCode\":\"'+bookingCodeParam+'\",\"lastName\":\"'+lastNameParam+'\"},\n\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"5862217c780db7597694b8736e2846f235c5deedcc0322e5c09b6f6ca4c8006d\"}}\n}'
    headers = {
        "language": "en",
        "country": "IR",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "PostmanRuntime/7.26.8",
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }
    session = requests.Session()
    print("INFO: Flight data requested for AirFrance company with PNR: ", bookingCodeParam)
    # Getting cookies
    session.get("https://wwws.airfrance.fr/trip", headers=headers)
    session_cached = CachedSession(
        'af_cache',
        use_cache_dir=True,
        cache_control=False,
        expire_after=timedelta(seconds=120),
        allowable_methods=['GET', 'POST'],
        allowable_codes=[200, 400, 404],
        match_headers=False,
        stale_if_error=True,
    )
    # Same call but with generated cookies, AirFrance used generated specific session cookies
    response = session_cached.post(url, data=payload, headers=headers, cookies=session.cookies.get_dict())
    return airfrance.treat(response.json())

@app.route('/klm')
def get_klm():
    bookingCodeParam = request.args.get("bookingCode")
    lastNameParam = request.args.get("lastName")
    # Check parameters
    if bookingCodeParam is None or lastNameParam is None:
        return error_400, 400
    # TODO: .env with urls
    url = "https://www.klm.fr/gql/v1?bookingFlow=LEISURE"
    payload='{\n\"operationName\":\"reservation\",\n\"variables\":{\"bookingCode\":\"'+bookingCodeParam+'\",\"lastName\":\"'+lastNameParam+'\"},\n\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"7b914f0ba09f21c67523b5fa480a86cd92dd94b0113aef156337d6715a095d91\"}}\n}'
    headers = {
        "accept-language": "en-GB",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }
    session = requests.Session()
    print("INFO: Flight data requested for KLM company with PNR: ", bookingCodeParam)
    # Getting cookies
    session.get("https://www.klm.fr/en/trip", headers=headers)
    session_cached = CachedSession(
        'klm_cache',
        use_cache_dir=True,
        cache_control=False,
        expire_after=timedelta(seconds=120),
        allowable_methods=['GET', 'POST'],
        allowable_codes=[200, 400, 404],
        match_headers=False,
        stale_if_error=True,
    )
    # Same call but with generated cookies, KLM used generated specific session cookies
    response = session_cached.post(url, data=payload, headers=headers, cookies=session.cookies.get_dict())
    return klm.treat(response.json())

@app.route('/sncf')
def get_sncf():
    bookingCodeParam = request.args.get("bookingCode")
    lastNameParam = request.args.get("lastName")
    # Check parameters
    if bookingCodeParam is None or lastNameParam is None:
        return error_400, 400
    # TODO: .env with urls
    url = "http://www.sncf-connect.com/bff/api/v1/trips/trips-by-criteria"
    payload='{\n\"reference\":\"'+bookingCodeParam+'\",\"name\":\"'+lastNameParam+'\"\n}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
        "x-bff-key": "ah1MPO-izehIHD-QZZ9y88n-kku876",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }
    session = CachedSession(
        'sncf_cache',
        use_cache_dir=True,
        cache_control=False,
        expire_after=timedelta(seconds=180),
        allowable_methods=['GET', 'POST'],
        allowable_codes=[200, 400, 404],
        match_headers=True,
        stale_if_error=True,
    )
    print("INFO: Train data requested for SNCF company with PNR: ", bookingCodeParam)
    response = session.post(url, data=payload, headers=headers)
    return sncf.treat(response)
    with open('mocks/sncf.json') as json_file:
        return json.load(json_file)

@app.route('/delta')
def get_delta():
    bookingCodeParam = request.args.get("bookingCode")
    lastNameParam = request.args.get("lastName")
    # Check parameters
    if bookingCodeParam is None or lastNameParam is None:
        return error_400, 400
    # TODO: .env with urls
    url = "http://delta.com/api/v2/trips/"
    payload='{\n\"operationName\":\"reservation\",\n\"variables\":{\"bookingCode\":\"'+bookingCodeParam+'\",\"lastName\":\"'+lastNameParam+'\"},\n\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"5862217c780db7597694b8736e2846f235c5deedcc0322e5c09b6f6ca4c8006d\"}}\n}'
    headers = {
        "language": "en",
        "country": "FR",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "PostmanRuntime/7.26.8",
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }
    session = requests.Session()
    print("INFO: Flight data requested for DELTA company with PNR: ", bookingCodeParam)
    # Getting cookies
    response = session.post(url, headers=headers, data=payload)
    return delta.treat(response.json())

@app.route('/condor')
def get_condor():
    bookingCodeParam = request.args.get("bookingCode")
    lastNameParam = request.args.get("lastName")
    departureDateParam = request.args.get("departureDate")
    # Check parameters
    if bookingCodeParam is None or lastNameParam is None or departureDateParam is None:
        return error_400, 400
    # TODO: .env with urls
    url = "https://api.condor.com/api/booking/v0/bookings?bookingReference={}&lastName={}&departureDate={}".format(bookingCodeParam, lastNameParam, departureDateParam)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }
    session = CachedSession(
        'condor_cache',
        use_cache_dir=True,
        cache_control=False,
        expire_after=timedelta(seconds=120),
        allowable_methods=['GET', 'POST'],
        allowable_codes=[200, 400, 404],
        match_headers=True,
        stale_if_error=True,
    )
    print("INFO: Train data requested for CONDOR company with PNR: ", bookingCodeParam)
    response = session.get(url, headers=headers)
    return condor.treat(response.json())

@app.route('/other')
def get_other():
    flightNumberParam = request.args.get("flightNumber")
    departureDateParam = request.args.get("departureDate")
    # Check parameters
    if flightNumberParam is None or departureDateParam is None:
        return error_400, 400
    # TODO: .env with urls
    if "GOFLIGHT_KEY" not in os.environ:
        print("ERROR: Missing 'GOFLIGHT_KEY' env var")
        return error_500, 500
    url = "https://app.goflightlabs.com/flights?access_key={}&flight_iata={}&arr_scheduled_time_dep={}".format(os.environ['GOFLIGHT_KEY'], flightNumberParam, departureDateParam)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }
    session = CachedSession(
        'goflight_cache',
        use_cache_dir=True,
        cache_control=True,
        expire_after=timedelta(seconds=300),
        allowable_methods=['GET', 'POST'],
        allowable_codes=[200, 400, 404],
        match_headers=True,
        stale_if_error=True,
    )
    print("INFO: Flight data requested for other company with flight number: ", flightNumberParam)
    response = session.get(url, headers=headers)
    return other.treat(response)


# ======== Main ======== #
if __name__ == '__main__':
    print("--------------------------------")
    print("   MAESTRO SERVER HAS STARTED   ")
    print("--------------------------------")
    app.run(debug=True, use_reloader=True, threaded=True)