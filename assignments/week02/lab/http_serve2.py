#!/usr/bin/env python

import socket
from datetime import datetime
from time import mktime
from email.utils import formatdate

def gmt_datetime():
    """returns a RFC-1123 compliant timestamp"""
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return formatdate(timeval = stamp, localtime = False, usegmt = True)

def ok_response(body):
    """return a positive response if we receive data"""
    response = "HTTP/1.0 200 OK\r\nDate: %s\r\nContent-Type: text/html\r\n\r\n"%date
    return (response + body)  

host = '' # listen on all connections (WiFi, etc) 
port = 50000 
backlog = 5 # how many connections can we stack up
size = 1024 # number of bytes to receive at once

## create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# set an option to tell the OS to re-use the socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# the bind makes it a server
s.bind( (host,port) ) 
s.listen(backlog) 

while True: # keep looking for new connections forever
    client, address = s.accept() # look for a connection
    data = client.recv(size)
    if data: # if the connection was closed there would be no data
        print "received: %s"%data
	html = open('tiny_html.html', 'r')
	fileStuff = html.read()
	html.close()
	date = gmt_datetime()
	newData = ok_response(fileStuff)
        
        client.send(newData) 
        client.close()
