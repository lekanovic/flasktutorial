# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, views, redirect, url_for, session, flash
from flask.ext.mongokit import MongoKit
from flask.ext.bootstrap import Bootstrap
import time, json, requests, urllib
import functools

app = Flask(__name__)
app.secret_key = '81fa886eb7cab2a148650b25cf6c40d0fa6edebbbf2704e1b7d1f92f68b9344b'

users = {'lekanovic@gmail.com':'78celeron'}

def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'email' in session:
            return method(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return wrapper


class Userhome(views.MethodView):

    @login_required
    def get(self):
        return render_template('userhome.html',username="Radovan")

    @login_required
    def post(self):
        pass

class Signout(views.MethodView):

    def get(self):
        session.pop('email', None)
        return render_template('index.html')

    def post(self):
        pass


class Signin(views.MethodView):

    def get(self):
        return render_template('signin.html')

    def post(self):
        email = request.form['Email address']
        passwd = request.form['Password']
        require = ['Email address','Password']
        for r in require:
            if r not in request.form:
                return "Wrong password or email"
        if email in users and users[email] == passwd:
            session['email'] = email
        else:
            flash("Username doesn't exist or incorrect password")

        return redirect(url_for('userhome'))

class Register(views.MethodView):

    def get(self):
        return render_template('register.html')

    def post(self):
        username = request.form['Username']
        email = request.form['Email address']
        passwd = request.form['Password']
        print "%s %s %s" % (username,email,passwd)
        return redirect(url_for('userhome'))

class Main(views.MethodView):

    def get(self):
        return render_template('index.html', price=self.btstamp())

    def post(self):
        return "POST"

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
signin_view = Signin.as_view('signin')
signout_view = Signout.as_view('signout')
userhome_view = Userhome.as_view('userhome')

app.add_url_rule('/',
                 view_func=main_view,
                 methods=["GET", "POST"])

app.add_url_rule('/index.html',
                 view_func=main_view,
                 methods=["GET", "POST"])

app.add_url_rule('/register.html',
                 view_func=register_view,
                 methods=["GET", "POST"])

app.add_url_rule('/signin.html',
                 view_func=signin_view,
                 methods=["GET", "POST"])

app.add_url_rule('/signout.html',
                 view_func=signout_view,
                 methods=["GET", "POST"])

app.add_url_rule('/userhome.html',
                 view_func=userhome_view,
                 methods=["GET", "POST"])

app.debug = True
app.run()