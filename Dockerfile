FROM python:3.11-alpine

WORKDIR /

RUN mkdir out
COPY ./req.txt .
RUN ["pip", "install", "-r", "req.txt"]


COPY . .

ENTRYPOINT ["python", "main.py"]