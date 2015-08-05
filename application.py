# -*- coding: utf-8 -*-
"""
Created on Thu May 07 23:04:36 2015

@author: ctchu
"""

#from flask import Flask
#app = Flask(__name__)
#
#@app.route('/')
#def hello_world():
#    return 'Randy!!! Hello World!'

from flask import Flask
application = Flask(__name__)

from application import application

if __name__ == '__main__':
    application.run(debug = True)       # set debug to True, so whenever the source code changes, Flask will restart the service automatically