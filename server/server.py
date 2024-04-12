import socket
from _thread import *
import pickle
import threading
from game_status import GameStatus
import time

DISCONNECT_SIGNAL = "DISCONNECTED"

if __name__ == "__main__":
    flag = 0
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
    waiting = []
    idCount = 0

    def send_disconnect_signal(conn):
        conn.sendall(DISCONNECT_SIGNAL.encode())

    def threaded_client(conn, p, gameId):

        global idCount
        conn.send(str.encode(str(p)))

        reply = ""
        while True:
            try:
                # data = conn.recv(4096).decode()
                data = pickle.loads(conn.recv(4096))
                print(type(data))
                if type(data) == list:
                    print("r")
                    print(list(data))
                    game.feed(p, list(data))
                    pass
                else:
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
                                idCount = idCount - 1
                                conn.close()

                            elif data == "round_finished":
                                game.round = game.round + 0.5
                            # elif data[:6] == "change":
                            #     # game.feed(
                            #     #     p, data[7:]
                            #     # )  # This info is the musical array to be recieved from client
                            elif data != "get" and data != "game_mode":
                                game.play(p, data)

                            conn.sendall(pickle.dumps(game))
                    else:
                        break
            except:
                break

        print("Lost Connection for player ", p)
        try:
            del games[gameId]
            print("Closing Game", gameId)
        except:
            pass

        idCount = idCount - 1
        conn.close()

    while True:
        conn, addr = s.accept()
        print("Connected to: ", int(addr[1]))
        idCount = idCount + 1
        flag = 0

        conn.send(str.encode(str(1)))
        game_mode = pickle.loads(conn.recv(4096))
        print("game_mode: ", game_mode)

        # for key,value in games.items():
        #     (a,b,c) = value
        #     if game_mode == c:

        for key, value in games.items():
            (a, b, c) = value
            if b == 1 and c == game_mode:

                flag = 1
                games[key] = (a, 2, game_mode)
                games[key][0].ready = True
                a.conn2 = int(addr[1])
                start_new_thread(threaded_client, (conn, 1, key))
                break

        if flag == 0:
            print("reached")
            games[idCount] = (GameStatus(idCount), 1, game_mode)
            games[idCount][0].conn1 = int(addr[1])
            start_new_thread(threaded_client, (conn, 0, idCount))
