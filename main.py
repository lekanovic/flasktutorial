# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, views
from flask.ext.mongokit import MongoKit
from flask.ext.bootstrap import Bootstrap
import time, json, requests, urllib

app = Flask(__name__)
#mongo = MongoKit(app)
bootstrap = Bootstrap(app)

class Register(views.MethodView):

    def get(self):
        return render_template('register.html')

    def post(self):
        pass


class Main(views.MethodView):

    def get(self):
        return render_template('index.html', price=self.btstamp())

    def post(self):
        pass

    def getDollarPrice(self):
        url = "http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json"
        response = urllib.urlopen(url);
        data = json.loads(response.read())
        for i in range(0, data['list']['meta']['count']):
            if data['list']['resources'][i]['resource']['fields']['name'] == "USD/SEK":
                SEK = data['list']['resources'][i]['resource']['fields']['price']
        return SEK

    def btstamp(self):
        bitStampTick = requests.get('https://www.bitstamp.net/api/ticker/')
        bitcoinPrice = float(bitStampTick.json()['last'])
        dollarInSek = float(self.getDollarPrice())
        return "%.2f" % (bitcoinPrice * dollarInSek)


main_view = Main.as_view('index')
register_view = Register.as_view('register')

app.add_url_rule('/',
                 view_func=main_view,
                 methods=["GET", "POST"])

app.add_url_rule('/index.html',
                 view_func=main_view,
                 methods=["GET", "POST"])

app.add_url_rule('/register.html',
                 view_func=register_view,
                 methods=["GET", "POST"])

app.debug = True
app.run()