FROM python:3.9

RUN mkdir /referral_system

WORKDIR /referral_system

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .