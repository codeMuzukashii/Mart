FROM python:3.7.3
LABEL maintainer='hsuehyuchieh01@gmail.com'
ENV PYTHONUNBUFFERED 1
RUN mkdir /Mart
WORKDIR /Mart
COPY . /Mart/
RUN pip install -r requirements.txt