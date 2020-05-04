FROM python:3.8.2-alpine3.11

RUN apk add gcc
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 bass_bot/main.py
## IMPLEMENT log files