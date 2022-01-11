FROM python:3.8-slim-buster

RUN mkdir -p /App

WORKDIR /App

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python3", "maestro.py"]