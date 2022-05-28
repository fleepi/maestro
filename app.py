from companies import airfrance, sncf, other
from flask import Flask, jsonify, request
import requests
import copy
import os
from datetime import timedelta
from requests_cache import CachedSession

app = Flask(__name__)

# ~~ MESSAGES ~~
error_500 = {"message": "Maestro Internal Server Error"}

@app.route('/airfrance')
def get_airFrance():
    # TODO: .env with urls
    url = "https://iran.airfrance.com/gql/v1?bookingFlow=LEISURE"
    payload='{\n\"operationName\":\"reservation\",\n\"variables\":{\"bookingCode\":\"'+request.args.get('bookingCode')+'\",\"lastName\":\"'+request.args.get('lastName')+'\"},\n\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"5862217c780db7597694b8736e2846f235c5deedcc0322e5c09b6f6ca4c8006d\"}}\n}'
    headers = {
        "language": "en",
        "country": "IR",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "PostmanRuntime/7.26.8",
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }
    session = requests.Session()
    print("INFO: Flight data requested for AirFrance company with PNR: ", request.args.get('bookingCode'))
    # Getting cookies
    session.post(url, data=payload, headers=headers)
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

@app.route('/sncf')
def get_sncf():
    # TODO: .env with urls
    url = "https://www.sncf-connect.com/bff/api/v1/trips/trips-by-criteria"
    payload='{\n\"reference\":\"'+request.args.get('bookingCode')+'\",\"name\":\"'+request.args.get('lastName')+'\"\n}'
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
    print("INFO: Train data requested for SNCF company with PNR: ", request.args.get('bookingCode'))
    response = session.post(url, data=payload, headers=headers)
    return sncf.treat(response)

@app.route('/other')
def get_other():
    # TODO: .env with urls
    if "GOFLIGHT_KEY" not in os.environ:
        print("ERROR: Missing 'GOFLIGHT_KEY' env var")
        return error_500, 500
    url = "https://app.goflightlabs.com/flights?access_key={}&flight_iata={}&arr_scheduled_time_dep={}".format(os.environ['GOFLIGHT_KEY'], request.args.get('flightNumber'), request.args.get('departureDate'))
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
    print("INFO: Flight data requested for other company with flight number: ", request.args.get('flightNumber'))
    response = session.get(url, headers=headers)
    return other.treat(response)


# ======== Main ======== #
if __name__ == '__main__':
    print("--------------------------------")
    print("   MAESTRO SERVER HAS STARTED   ")
    print("--------------------------------")
    app.run(debug=True, use_reloader=True, threaded=True)