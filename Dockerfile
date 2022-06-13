# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8-appservice
FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

RUN apt-get update && apt-get install -y \
    autoconf automake build-essential curl git libsnappy-dev libtool pkg-config


WORKDIR /libpostal
RUN git clone https://github.com/openvenues/libpostal .
COPY --chmod=775 build_libpostal.sh .
RUN ./build_libpostal.sh

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot

