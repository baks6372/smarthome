#! /usr/bin/python3
#

# Import modules for CGI handling 
import cgi, cgitb 
import json

#print ("Content-Type: text/html\n\n")
#print ("<html><head><meta content=\"text/html; charset=UTF-8\" />")
#print ("<title>Raspberry Pi</title><p>")

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
backlight_status = form.getvalue('backlight_status')
chandelier_status = form.getvalue('chandelier_status')
#backlight_status = 1
data = {}
if backlight_status:
    data ["backlight_status"] = backlight_status
if chandelier_status:
    data ["chandelier_status"] = chandelier_status

#if backlight_status:
#    print ("backlight-status = %s" % backlight_status)
#else:
#    for count in range(1,100): 
#        print ("ERROR")
print ("Content-Type: application/json\n\n")
print(json.dumps(data, sort_keys=True))
#print ("</p></body></html>")
