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

sensor_group = "light/kitchen"

command_str = "SELECT sensor_name, sensor_status FROM sensors where sensor_group = \"%s\";" % (sensor_group)
try:
    cursor.execute(command_str)
except Exception as e:
    print(e,file=sys.stderr)
    exit(1)
    
sensors_list = cursor.fetchall()
#print (sensors_list)

data = {}

# Create instance of FieldStorage 
form = cgi.FieldStorage() 
   
# Get data from fields
backlight_switch_status = form.getvalue('backlight_switch_status')
chandelier_switch_status = form.getvalue('chandelier_switch_status')
config = configparser.RawConfigParser()
res = config.read("light.cfg")
sections = config.sections()

have_changes = False
if backlight_switch_status:
    if(backlight_switch_status != config['kitchen']['backlight_switch_status']):
        have_changes = True
        config.set("kitchen","backlight_switch_status",backlight_switch_status)
        msgs = []
        msgs.append({'topic': sensor_group, 'payload': "backlight_switch_status="+backlight_switch_status})
        publish.multiple(msgs, hostname="localhost")
if chandelier_switch_status:
    if(chandelier_switch_status != config['kitchen']['chandelier_switch_status']):
        have_changes = True 
        config.set("kitchen","chandelier_switch_status",chandelier_switch_status)
        msgs = []
        msgs.append({'topic': sensor_group, 'payload': "chandelier_switch_status="+chandelier_switch_status})
        publish.multiple(msgs, hostname="localhost")  
#
if have_changes == True:
    with open('light.cfg', 'w') as configfile:
        config.write(configfile)

for sensor in sensors_list:     
    data [sensor[0]] = sensor[1]
    #data ["chandelier_status"] = config['kitchen']['chandelier_status']
    
print ("Content-Type: application/json\n\n")
print(json.dumps(data, sort_keys=True))
#print ("</p></body></html>")

# try:
#     print(os.environ.get("HTTP_USER_AGENT"))
#     data ["QUERY_STRING_OK"] = os.environ.get("HTTP_USER_AGENT")
# except Exception as e:
#     print ("error here: " + str(e))
#     data ["QUERY_STRING_ERR"] = str(e)
