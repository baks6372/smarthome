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
kitchen_backlight_relay = form.getvalue('kitchen_backlight_relay')
kitchen_chandelier_relay = form.getvalue('kitchen_chandelier_relay')
config = configparser.RawConfigParser()
res = config.read("light.cfg")
sections = config.sections()

have_changes = False
if kitchen_backlight_relay:
    if(kitchen_backlight_relay != config['kitchen']['kitchen_backlight_relay']):
        have_changes = True
        config.set("kitchen","kitchen_backlight_relay",kitchen_backlight_relay)
        msgs = []
        
        sensor_name = "kitchen_backlight_relay"
        sensor_status = kitchen_backlight_relay
        
        command_str = "update sensors set sensor_status = '%s' where sensor_name='%s';" % (sensor_status, sensor_name)     
        try:
            cursor.execute(command_str)
        except Exception as e:
            print(command_str)
            print(e)
            exit(1)
        conn.commit()
        
        command_str = "SELECT sensor_settings FROM sensors where sensor_name = \"%s\";" % (sensor_name)
        try:
            cursor.execute(command_str)
        except Exception as e:
            print(e,file=sys.stderr)
            exit(1)
            
        change_settins_str = cursor.fetchall()
        change_value_str = json.loads(change_settins_str[0][0])
        change_value_str["value"] = sensor_status
        change_value_str = json.dumps(change_value_str)
        #print(change_value_str)
        
        command_str = "update sensors set sensor_settings = '%s' where sensor_name='%s';" % (change_value_str, sensor_name)     
        try:
            cursor.execute(command_str)
        except Exception as e:
            print(command_str)
            print(e)
            exit(1)
        conn.commit()
        
        command_str = "SELECT sensor_id, sensor_settings FROM sensors where sensor_name = \"%s\";" % (sensor_name)
        try:
            cursor.execute(command_str)
        except Exception as e:
            print(e,file=sys.stderr)
            exit(1)
    
        result_str = cursor.fetchall()
        sensor_id = result_str[0][0]
        sensor_settings = result_str[0][1]
        
        msgs.append({'topic': sensor_id, 'payload': sensor_settings})

        publish.multiple(msgs, hostname="localhost")
if kitchen_chandelier_relay:
    if(kitchen_chandelier_relay != config['kitchen']['kitchen_chandelier_relay']):
        have_changes = True
        config.set("kitchen","kitchen_chandelier_relay",kitchen_chandelier_relay)
        msgs = []
        
        sensor_name = "kitchen_chandelier_relay"
        sensor_status = kitchen_chandelier_relay
        
        command_str = "update sensors set sensor_status = '%s' where sensor_name='%s';" % (sensor_status, sensor_name)     
        try:
            cursor.execute(command_str)
        except Exception as e:
            print(command_str)
            print(e)
            exit(1)
        conn.commit()
        
        command_str = "SELECT sensor_settings FROM sensors where sensor_name = \"%s\";" % (sensor_name)
        try:
            cursor.execute(command_str)
        except Exception as e:
            print(e,file=sys.stderr)
            exit(1)
            
        change_settins_str = cursor.fetchall()
        change_value_str = json.loads(change_settins_str[0][0])
        change_value_str["value"] = sensor_status
        change_value_str = json.dumps(change_value_str)
        #print(change_value_str)
        
        command_str = "update sensors set sensor_settings = '%s' where sensor_name='%s';" % (change_value_str, sensor_name)     
        try:
            cursor.execute(command_str)
        except Exception as e:
            print(command_str)
            print(e)
            exit(1)
        conn.commit()
        
        command_str = "SELECT sensor_id, sensor_settings FROM sensors where sensor_name = \"%s\";" % (sensor_name)
        try:
            cursor.execute(command_str)
        except Exception as e:
            print(e,file=sys.stderr)
            exit(1)
    
        result_str = cursor.fetchall()
        sensor_id = result_str[0][0]
        sensor_settings = result_str[0][1]
        
        #print ("sensor_id = %s , sensor_settings = %s" % (sensor_id,sensor_settings))
        
        msgs.append({'topic': sensor_id, 'payload': sensor_settings})

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
