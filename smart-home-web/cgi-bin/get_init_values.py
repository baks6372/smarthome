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
res = config.read("smarthome.cfg")
sections = config.sections()

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

init_values_str = form.getvalue('init_values')
init_values = init_values_str.split(',')

for init_value in init_values:
    #data[init_value] = config['devices'][init_value]
    command_str = "SELECT sensor_status FROM sensors where sensor_name = \"%s\";" % (init_value)
    try:
        cursor.execute(command_str)
    except Exception as e:
        print(e,file=sys.stderr)
        exit(1)
    value_changed_check = cursor.fetchall()
    data[init_value]= value_changed_check[0][0]
    

    
print ("Content-Type: application/json\n\n")
print(json.dumps(data, sort_keys=True))
