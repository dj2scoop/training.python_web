import socket
import sys

# Create a TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)

# Connect the socket to the port where the server is listening
HOST = 'block647045-6ca.blueboxgrid.com'
server_address = (HOST, 50000)
client.connect(server_address)

try:	
    # Send data
    client.sendall('Hello...computer')

    # print the response
    data = client.recv(1024)
    print 'Recieved: ', repr(data)

finally:
    # close the socket to clean up
    client.close()
