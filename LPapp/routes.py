#from flask import render_template, url_for, flash, redirect
from LPapp import app
from LPapp.models import *

def debug(msg):
    print('\n\n\n'+str(msg)+'\n\n\n'+'\n\nType:\t'+str(type(msg))+'\n\n')

@app.route("/")
@app.route("/home")
def home():
    return "home"
