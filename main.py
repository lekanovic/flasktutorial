# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask.ext.mongokit import MongoKit
from flask.ext.bootstrap import Bootstrap


app = Flask(__name__)
#mongo = MongoKit(app)
bootstrap = Bootstrap(app)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/register.html')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)