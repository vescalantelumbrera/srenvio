import requests
import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from .convertors import inchToCm, lbToKg


def checkFedexDelaiveryService(track_id, carrier_code):

    url = "https://wsbeta.fedex.com:443/web-services/"
    pacakage_fedex_values = {
        "real_width": 0,
        "real_length": 0,
        "real_height": 0,
        "real_weight": 0,

    }
    headers = {'content-type': 'text/xml'}
    body = """<?xml version="1.0"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v16="http://fedex.com/ws/track/v16">
    <soapenv:Header/>
    <soapenv:Body>
        <v16:TrackRequest>
        <v16:WebAuthenticationDetail>
        
            <v16:UserCredential>
            <v16:Key>"""+os.environ.get("FEDEX_KEY", "")+"""</v16:Key>
            <v16:Password>"""+os.environ.get("FEDEX_PASSWORD", "")+"""</v16:Password>
            </v16:UserCredential>
        </v16:WebAuthenticationDetail>
        <v16:ClientDetail>
            <v16:AccountNumber>"""+os.environ.get("ACCOUNTNUMBER", "")+"""</v16:AccountNumber>
            <v16:MeterNumber>"""+os.environ.get("METERNUMBER", "")+"""</v16:MeterNumber>
        </v16:ClientDetail>
        <v16:TransactionDetail>
            <v16:CustomerTransactionId>Track By Number_v16</v16:CustomerTransactionId>
            <v16:Localization>
            <v16:LanguageCode>EN</v16:LanguageCode>
            <v16:LocaleCode>US</v16:LocaleCode>
            </v16:Localization>
        </v16:TransactionDetail>
        <v16:Version>
            <v16:ServiceId>trck</v16:ServiceId>
            <v16:Major>16</v16:Major>
            <v16:Intermediate>0</v16:Intermediate>
            <v16:Minor>0</v16:Minor>
        </v16:Version>
        <v16:SelectionDetails>
            <v16:CarrierCode>"""+carrier_code+"""</v16:CarrierCode>
            <v16:PackageIdentifier>
            <v16:Type>TRACKING_NUMBER_OR_DOORTAG</v16:Type>
            <v16:Value>"""+track_id+"""</v16:Value>
            </v16:PackageIdentifier>
            <v16:ShipmentAccountNumber/>
            <v16:SecureSpodAccount/>
            <v16:Destination>
            <v16:GeographicCoordinates>rates evertitque
    aequora</v16:GeographicCoordinates>
            </v16:Destination>
        </v16:SelectionDetails>
        </v16:TrackRequest>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url, data=body, headers=headers)

    soup = BeautifulSoup(response.content, 'xml')
    response_status = soup.find('TrackDetails').find(
        "Notification").find("Severity").text

    if response_status == "SUCCESS":
        pacakage_fedex_values["real_width"] = round(inchToCm(
            float(soup.find('Width').text)), 4)
        pacakage_fedex_values["real_length"] = round(inchToCm(
            float(soup.find('Length').text)), 4)
        pacakage_fedex_values["real_height"] = round(inchToCm(
            float(soup.find('Height').text)), 4)
        pacakage_fedex_values["real_weight"] = round(lbToKg(
            float(soup.find('PackageWeight').find("Value").text)), 4)

        return pacakage_fedex_values
    return None
