# maestro beta
Maestro is a Python Flask API which can retrieve a booking data from any flight or train company in the world.

* Currently supporting Air France for planes
* Currently supporting SNCF for trains
* Possibility to get real time data with flight number thanks to Goflight API

## How start Maestro?

### Docker

Simply use the Dockerfile!

### Python3

* Install required modules
`pip install -r requirements.txt`

* Set up your GOFLIGHT_KEY env var

* Launch Maestro `python3 app.py`

## How to use it?

* http://{HOST}:{PORT}/{COMPANY}?bookingCode={PNR}&lastName={LASTNAME}
