from datetime import date
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from firebase import firebase

def main():
    # Grabs the webpage.
    url = 'https://flights.ana.co.jp/en-ca/flights-from-vancouver-to-tokyo'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Grabs the "Vancouver (YVR) to Tokyo (TYO) Top Deals" section.
    orderedList = soup.find('ol', class_='clearfix')

    # Builds the values.
    codeList = []
    for routeCode in orderedList.find_all('p', class_='fare-atom-route'):
        codeList.append(routeCode.text)

    datesGoingList = []
    for datesGoing in orderedList.find_all('div', class_='d-inline-block fare-departure-info-wrapper'):
        datesGoingList.append(datesGoing.text[0:16])

    datesReturnList = []
    for datesReturn in orderedList.find_all('div', class_='fare-atom-trip-leg fare-atom-trip-leg--return'):
        datesReturnList.append(datesReturn.text)

    pricesList = []
    for prices in orderedList.find_all('span', class_='fare-atom-price-total-price'):
        priceSaved = int(prices.text.replace(',', ''))
        pricesList.append(priceSaved)

    # Creates the dictionary.
    dateToday = str(date.today())
    flightDict = {"Airports": codeList, "DepDate": datesGoingList, "ArrDate": datesReturnList,
                  "Price": pricesList, "Date": [dateToday, dateToday, dateToday, dateToday, dateToday, dateToday]}

    # Uploads Database to Firebase.
    FBConn = firebase.FirebaseApplication("https://anatopdeals-d3506.firebaseio.com/", None)
    data_to_upload = flightDict

    result = FBConn.post('/FlightData/', data_to_upload)

main()