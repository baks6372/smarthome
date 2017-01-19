#! /usr/bin/python3
#

# Import modules for CGI handling 
import cgi, cgitb 
import json
import configparser 
import sys
import sqlite3
import os

try:
    from paho.mqtt import client
    from paho.mqtt import publish
except Exception as e:
    print ("error here: " + str(e))

# print ("Content-Type: text/html\n\n")
# print ("<html><head><meta content=\"text/html; charset=UTF-8\" />")
# print ("<title>Raspberry Pi</title><p>")

db_path = "/home/evgeny/smarthome/smarthome.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

data = {}

config = configparser.RawConfigParser()
res = config.read("light.cfg")
sections = config.sections()

data ['kitchen_backlight_relay'] = config['kitchen']['kitchen_backlight_relay']
data ['kitchen_chandelier_relay'] = config['kitchen']['kitchen_chandelier_relay']
    
print ("Content-Type: application/json\n\n")
print(json.dumps(data, sort_keys=True))
