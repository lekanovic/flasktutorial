# -*- coding: utf-8 -*-
import json, requests, urllib

class BTCPrice:

    def __init__(self, currency="sek"):
        self.currency = currency.upper()

    def __getCurrency(self):
        url = "http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json"
        response = urllib.urlopen(url);
        data = json.loads(response.read())
        for i in range(0, data['list']['meta']['count']):
            if data['list']['resources'][i]['resource']['fields']['name'] == "USD/" + self.currency:
                return data['list']['resources'][i]['resource']['fields']['price']

    def getPrice(self):
        bitStampTick = requests.get('https://www.bitstamp.net/api/ticker/')
        bitcoinPrice = float(bitStampTick.json()['last'])
        if self.currency == "USD":
            return bitcoinPrice
        else:
            return "%.2f" % (bitcoinPrice * float(self.__getCurrency()))


#print BTCPrice('HRK').getPrice()
#print BTCPrice('RSD').getPrice()
#print BTCPrice('SEK').getPrice()
