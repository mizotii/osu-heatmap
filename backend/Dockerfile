# syntax=docker/dockerfile:1

FROM python:3.11.3

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "server.py" ]