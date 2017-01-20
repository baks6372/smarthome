#!/usr/bin/python
# -*- coding: cp1251 -*-

import Skype4Py
import sys, time, os
import json
from paho.mqtt import client
from paho.mqtt import publish
import sqlite3

db_path = "/home/evgeny/smarthome/smarthome.db"

def OnAttach(status):
    global skype
    print 'Attachment status: ' + skype.Convert.AttachmentStatusToText(status)
    if status == Skype4Py.apiAttachAvailable:
        skype.Attach()

def Commands(Message, Status):
    if Status == 'RECEIVED':
        message = Message.Body
        handle = Message.FromHandle
        print message
        print handle
        skype.SendMessage(handle, "done")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        form_fields = message.split('=')
        field = form_fields[0]
        field_value = form_fields[1]
        print field
        print field_value
        if field_value:
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
                print(e)
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
            
            print sensor_id
            print sensor_settings
            
            msgs.append({'topic': '/devices/value'+sensor_id, 'payload': sensor_settings})
    
            publish.multiple(msgs, hostname="localhost")

def main():
    global skype

    skype = Skype4Py.Skype()
    skype.OnAttachmentStatus = OnAttach
    skype.OnMessageStatus = Commands
    
    if not skype.Client.IsRunning:
        print 'Starting Skype..'
        skype.Client.Start()
    
    print 'Connecting to Skype process..'
    skype.Attach()
    print 'Your full name:', skype.CurrentUser.FullName
    print 'Your contacts:'
    for user in skype.Friends:
        print '    ', user.FullName
    try:
        while True:
            time.sleep(1)
    except:
       pass

if __name__ == '__main__':
  main()