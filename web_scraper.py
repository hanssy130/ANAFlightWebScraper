from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv

url = 'https://flights.ana.co.jp/en-ca/flights-from-vancouver-to-tokyo'

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# csvFile = open("flightinfo.csv", "wt", newline='')
# writer = csv.writer(csvFile)

orderedList = soup.find('ol', class_='clearfix')

codeList = []
for routeCode in orderedList.find_all('p', class_='fare-atom-route'):
    codeList.append(routeCode.text)
    # print(routeCode.text)

datesGoingList = []
for datesGoing in orderedList.find_all('div', class_='d-inline-block fare-departure-info-wrapper'):
    datesGoingList.append(datesGoing.text[0:16])
    # print(datesGoing.text[0:16])

datesReturnList = []
for datesReturn in orderedList.find_all('div', class_='fare-atom-trip-leg fare-atom-trip-leg--return'):
    datesReturnList.append(datesReturn.text)
    # print(datesReturn.text)

pricesList = []
for prices in orderedList.find_all('span', class_='fare-atom-price-total-price'):
    priceSaved = int(prices.text.replace(',', ''))
    pricesList.append(priceSaved)
    # print(priceSaved)

flightDict = {"Airports": codeList, "Departure Date": datesGoingList, "Arrival Date": datesReturnList,
              "Price": pricesList}
# print(flightDict)

flightDict_df = pd.DataFrame.from_dict(flightDict, orient='index').T

flightDict_df.to_csv('flightinfo.csv')



# writer.writerow(codeList)
# writer.writerow(datesGoingList)
# writer.writerow(datesReturnList)
# writer.writerow(pricesList)
#
# csvFile.close()