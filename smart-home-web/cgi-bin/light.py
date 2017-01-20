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

sensor_group = "/home/light/kitchen"

config = configparser.RawConfigParser()
res = config.read("smarthome.cfg")
sections = config.sections()
have_changes = False

data = {}

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

form_fields = form.keys()

for field in form_fields:
    field_value = form.getvalue(field)
    if field_value:
        command_str = "SELECT sensor_status FROM sensors where sensor_name = \"%s\";" % (field)
        try:
            cursor.execute(command_str)
        except Exception as e:
            print(e,file=sys.stderr)
            exit(1)
            
        value_changed_check = cursor.fetchall()
        
        if(field_value != value_changed_check[0][0]):
            have_changes = True
            config.set("devices",field,field_value)
            msgs = []
            
            sensor_name = field
            sensor_status = field_value
            
            command_str = "update sensors set sensor_status = '%s' where sensor_name='%s';" % (sensor_status, sensor_name)     
            try:
                cursor.execute(command_str)
            except Exception as e:
                print(command_str)
                print(e)
                exit(1)
            
            command_str = "SELECT sensor_id, sensor_settings FROM sensors where sensor_name = \"%s\";" % (sensor_name)
            try:
                cursor.execute(command_str)
            except Exception as e:
                print(e,file=sys.stderr)
                exit(1)
                
            change_settins_str = cursor.fetchall()
            change_value_str = json.loads(change_settins_str[0][1])
            change_value_str["value"] = sensor_status
            change_value_str = json.dumps(change_value_str)
            
            command_str = "update sensors set sensor_settings = '%s' where sensor_name='%s';" % (change_value_str, sensor_name)     
            try:
                cursor.execute(command_str)
            except Exception as e:
                print(command_str)
                print(e)
                exit(1)
            conn.commit()

            sensor_id = change_settins_str[0][0]
            sensor_settings = change_value_str
            
            msgs.append({'topic': '/devices/value'+sensor_id, 'payload': sensor_settings})
    
            publish.multiple(msgs, hostname="localhost")
        
if have_changes == True:
    with open('smarthome.cfg', 'w') as configfile:
        config.write(configfile)
        
command_str = "SELECT sensor_name, sensor_status FROM sensors where sensor_group = \"%s\";" % (sensor_group)
try:
    cursor.execute(command_str)
except Exception as e:
    print(e,file=sys.stderr)
    exit(1)
    
sensors_list = cursor.fetchall()

for sensor in sensors_list:     
    data [sensor[0]] = sensor[1]
    
print ("Content-Type: application/json\n\n")
print(json.dumps(data, sort_keys=True))

