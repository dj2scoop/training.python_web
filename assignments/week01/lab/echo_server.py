import socket
import sys

def add(num1, num2):
    return num1 + num2

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
HOST = ''

# Bind the socket to the port
server_address = (HOST, 50000)
server.bind(server_address)

# Listen for incoming connections
server.listen(5)

while True:
    # Wait for a connection
    con, addr = server.accept()
   
    try:
    # Receive the data and send it back
	data = con.recv(1024)
	print 'Received: ', repr(data)
	con.sendall("Good connection.")
    
    except KeyboardInterrupt:
	server.close()

    finally:
    # Clean up the connection
        con.close()
