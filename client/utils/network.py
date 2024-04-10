import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server = "localhost"
                        
        self.port = 5555
        self.addr = (self.server,self.port)
        self.p = self.connect()
        
    def connect(self):
        try:
            
            self.client.connect(self.addr)
            
            ans = self.client.recv(2048).decode()
            # print("connected successfully")
            return ans  # this conatins the overall data of the game
        except Exception as e:
            print(e)
            print("error in the connect function in network.py")
        
    def send(self,data):
        try:
            self.client.send(str.encode(data))
           # print("sent successfully")
            ans = pickle.loads(self.client.recv(2048*2))
            return ans # this sends the overall data of the game
        except Exception as e:
            print(e)
           # print("error in the send function in network.py")
            
    def getP(self):
        return self.p