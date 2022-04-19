from companies import airfrance, sncf
from flask import Flask, jsonify, request
import requests
import copy

app = Flask(__name__)

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
    # Getting cookies
    response = session.post(url, data=payload, headers=headers)
    # Same call but with generated cookies, AirFrance used generated specific session cookies
    response = session.post(url, data=payload, headers=headers, cookies=session.cookies.get_dict())
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
    session = requests.Session()
    response = session.post(url, data=payload, headers=headers)
    return sncf.treat(response)


# ======== Main ======== #
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, threaded=True)