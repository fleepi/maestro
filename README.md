# maestro beta
Maestro is a Python Flask API which can retrieve a booking data from any flight company in the world.

* Currently supporting only Air France

## What you need?

### Docker

Simply use the Dockerfile!

### Python3

* Install required modules
`pip install -r requirements.txt`

* Launch Maestro `python3 app.py`

## How to use it?

* http://{HOST}:{PORT}/{COMPANY}?bookingCode={PNR}&lastName={LASTNAME}
