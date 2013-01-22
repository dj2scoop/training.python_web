#!/usr/bin/env python

import socket
import mimetypes
from datetime import datetime
from time import mktime
from email.utils import formatdate


def parse_request(request, host, date):
    """takes a request and returns a URI"""
    ndata = request.split()
    if ((ndata[0] == "GET") and ((ndata[2] == "HTTP/1.1") or (ndata[2] == "HTTP/1.0"))):
    	return ndata[1]
    else:
	return client_error_response(host, date)   

def client_error_response(host, date):
    """Returns an appropriate HTTP code of the validation for parse_request fails"""
    """If file does not exist on server"""
    code = "HTTP/1.1 404 Not Found\r\nHost: %s\r\nDate: %s\r\n\r\n"%(host, date)
    """If server cannot process request"""
    code = "HTTP/1.1 500 Server Error\r\nHost: %s\r\nDate: %s\r\n"%(host, date)
    return code

def gmt_datetime():
    """returns a RFC-1123 compliant timestamp"""
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return formatdate(timeval = stamp, localtime = False, usegmt = True)

def ok_response(object, mType, host, date):
    """return a positive response if we receive data"""
    response = "HTTP/1.1 200 OK\r\nHost: %s\r\nDate: %s\r\nContent-Type: %s\r\n\r\n"%(host, date, mType)
    return (response + object)

def get_mimetype(url):
    """Tries to return the Content Type based on the file name or URL"""
    type = mimetypes.guess_type(url)
    return type[0]  

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
    date = gmt_datetime()
    serverName = 'uw-python-vm:80'
    data = client.recv(size)
    if data: # if the connection was closed there would be no data
        print data
	uri = parse_request(data, serverName, date)
	print uri
	type = get_mimetype('tiny_html.html')
	html = open('tiny_html.html', 'r')
	fileStuff = html.read()
	html.close()
	newData = ok_response(fileStuff, serverName,  type, date)
        
        client.send(newData) 
        client.close()
