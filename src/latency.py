from threading import Thread
import threading
import requests
import time
import logging


class Latency(Thread):
    latency_list = []
    latency_avg = 0
    log = logging.getLogger(__name__)
    def __init__(self,target):
        self.latency = 0
        Thread.__init__(self)
        self.url = "http://"+target.host+":"+str(target.port)

    def run(self):
        # try:
        response = requests.get(self.url).elapsed.total_seconds()
        self.latency_list.append(response)
        self.log.info("[Latency] -- {}".format(response))
            # time.sleep(20)

        # except (KeyboardInterrupt, SystemExit):
            # self.latency_avg = sum(self.latency_list) / len(self.latency_list)
            # print("Average latency = {}".format(self.latency_list))
            
    def get_average(self):
        self.latency_avg = sum(self.latency_list) / len(self.latency_list)
        return self.latency_avg