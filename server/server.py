import socket
from _thread import *
import pickle
from game_status import GameStatus
import random
DISCONNECT_SIGNAL = "DISCONNECTED"

if __name__ == "__main__":
    server = "localhost"
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        print(str(e))

    s.listen()
    print("Waiting for a connection, Server Started")

    connected = set()
    games = {}
    waiting =[]
    idCount = 0
    
    def send_disconnect_signal(conn):
        conn.sendall(DISCONNECT_SIGNAL.encode())

    def threaded_client(conn, p, gameId):
        global idCount
        conn.send(str.encode(str(p)))

        reply = ""
        while True:
            try:
                data = conn.recv(4096).decode()

                if gameId in games:
                    game = games[gameId][0]

                    if not data:
                        break
                    else:
                        if data == "reset":
                            game.resetWent()
                        elif data == "DISCONNECTED":
                            del games[gameId]
                            print("Closing Game", gameId)
                            idCount = idCount-1
                            conn.close()
                        elif data != "get":
                            game.play(p, data)

                        conn.sendall(pickle.dumps(game))
                else:
                    break
            except:
                break

        print("Lost Connection for player ",p)
        try:
            del games[gameId]
            print("Closing Game", gameId)
        except:
            pass

        idCount = idCount - 1
        conn.close()

    while True:
        conn, addr = s.accept()

        print("Connected to: ", addr)
        idCount = idCount+1
        p = 0
        # gameId = (idCount - 1) // 2
        
        # if idCount % 2 == 1:
        #     games[gameId] = GameStatus(gameId)
        #     print("Creating a new game...")
        # else:    
        #     print(gameId)
        #     print(games)
        #     games[gameId].ready = True
        #     p = 1
        
        flag =0
            
        for key,value in games.items():
            (a,b) = value
            if b ==1:
                flag =1
                games[key] = (a,2)
                games[key][0].ready = True
                
                start_new_thread(threaded_client, (conn, 1, key))
                break
        
         
        if flag == 0:
            
            games[idCount] = (GameStatus(idCount),1)
            start_new_thread(threaded_client, (conn, 0, idCount))
            
        
        

        # start_new_thread(threaded_client, (conn, p, gameId))
