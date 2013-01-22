#!/usr/bin/env python

import os
import socket
import mimetypes
from datetime import datetime
from time import mktime
from email.utils import formatdate


def resolve_uri(uri):
    """takes a URI and returns an HTTP response"""
    path = 'web'
    for (path, dirs, files) in os.walk(path):
	for nFiles in files:
            if( uri == '/' + nFiles):
		return os.path.join(path, nFiles)
	    else:
		continue
    return 404
            
def parse_request(request, host, date):
    """takes a request and returns a URI"""
    ndata = request.split()
    if ((ndata[0] == "GET") and ((ndata[2] == "HTTP/1.1") or (ndata[2] == "HTTP/1.0"))):
    	return ndata[1]
    else:
	return client_error_response(405, ndata[0], host, date)   

def notFound_response(uri, host, date):
    """Returns 404 Not Found Error if uri not found"""
    body = getFile("404ErrorPage.html")
    type = get_mimetype("404ErrorPage.html")
    response = "HTTP/1.1 404 Not Found\r\nHost: %s\r\nDate: %s\r\nContent Type: %s\r\n\r\n"%(host, date, type)
    return (response + body)

def badRequest_response(uri, host, date):
    """Request could not be understood by the server due to malformed syntax"""
    response = "HTTP/1.1 400 Bad Request\r\nHost: %s\r\nDate: %s\r\n\r\nCould not understand request: %s"%(host, date, uri)
    return response

def methodNotAllowed_response(data, host, date):
    """The method specified in the Request line is not allowed for the resource"""
    response = "HTTP/1.1 405\r\nHost: %s\r\nDate: %s\r\nAllow: GET\r\n\r\n%s method not allowed"%(host, date, data)
    return response

def getFile(request):
    """Returns the requested file"""
    print request
    file = open(request, 'r')
    fileStuff = file.read()
    file.close()
    return fileStuff

def getImage(request):
    """Returns the requested image"""
    print request
    file = open(request, 'rb')
    imageStuff = file.read()
    file.close()
    return imageStuff

def client_error_response(error, data, host, date):
    """Returns an appropriate HTTP header based on error"""
    if(error == 400):
        response = badRequest_response(data, host, date)
    elif(error == 404):
        response = notFound_response(data, host, date)
    elif(error == 405):
        response = methodNotAllowed_response(data, host, date) 
    else:
        response = "HTTP/1.1 500 Server Error\r\nHost: %s\r\nDate: %s\r\n"%(host, date)
    return response

def gmt_datetime():
    """returns a RFC-1123 compliant timestamp"""
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return formatdate(timeval = stamp, localtime = False, usegmt = True)

def ok_response(object, host, mType, date):
    """return a positive response if we receive data"""
    response = "HTTP/1.1 200 OK\r\nHost: %s\r\nDate: %s\r\nContent-Type: %s\r\n\r\n"%(host, date, mType)
    return (response + object)

def get_mimetype(url):
    """Tries to return the Content Type based on the file name or URL"""
    type = mimetypes.guess_type(url)
    return type[0]

def get_maintype(contentType):
    """returns the main type of a "Content Type:" header"""
    result = contentType.split('/')
    return result[0]

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
        #print data
	uri = parse_request(data, serverName, date)
	#print uri
	uri_response = resolve_uri(uri)
        if uri_response != 404:
            type = get_mimetype(uri)
	    if(get_maintype(type) == "image"):
                response = getImage(uri_response)
	        newData = ok_response(response, serverName, type, date)
	    elif(get_maintype(type) == "text"):
                response = getFile(uri_response)
                newData = ok_response(response, serverName, type, date)
	else:
	    newData = client_error_response(uri_response, uri, serverName, date)

        client.send(newData) 
        client.close()
