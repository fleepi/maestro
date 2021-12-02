from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

incomes = [
    { 'description': 'salary', 'amount': 5000 }
]

@app.route('/airfrance')
def get_airFrance():
    data = {
        "operationName": "reservation",
        "variables": {"bookingCode":"NBJ154","lastName":"ZONA"},
        "extensions": {"persistedQuery":{"version":1,"sha256Hash":"51076196b41d2ffe39204365bfd2bf5416f16cc9e1c6e3b5f12ecd7ea6c13d6b"}}
    }
    response = requests.post("https://iran.airfrance.com/gql/v1?bookingFlow=LEISURE", data = data, headers = {"language": "en", "country": "IR"})
    print(response.json())
    return response.json


@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204

# ======== Main ======== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=8000)