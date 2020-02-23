class Target:
    latency = None
    def __init__(self,host,port,sockets_number):
        self.host = host
        self.port = port
        self.sockets_number = sockets_number
        self.connections = []