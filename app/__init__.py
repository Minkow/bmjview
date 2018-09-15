#!/usr/bin/env python3
# encoding: utf-8

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
Bootstrap(app)

from app.views import *
from app.models import *