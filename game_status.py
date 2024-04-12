import random


class GameStatus:
    def __init__(self, id):
        self.p1Went = (
            False  # this will be used to check if game is over for both players
        )
        self.round = 0
        self.conn1 = 0
        self.conn2 = 0
        self.p1_listened = False
        self.p2_listened = False
        self.p2Went = False  # That means that game.stop() has been done for player-1
        self.ready = False  # To see if they are connected
        self.id = id
        self.moves = [0, 0]  # here move is an int(This is score)

        self.wins = [0, 0]
        self.song_array = [None, None]
        self.ties = 0
        self.restart = False
        self.song_number = random.randint(0, 1)
        self.p1_ready_to_go_forward = False
        self.p2_ready_to_go_forward = False

    def get_player_move(self, p):
        return self.moves[p]

    def feed(self, player, data):
        self.song_array[player] = data
        if player == 0:
            self.p1_ready_to_go_forward = True
        else:
            self.p2_ready_to_go_forward = True

    def play(self, player, move):
        res = self.moves[player]
        self.moves[player] = int(move) + res
        print("res : ", res)
        print("move: ", move)
        if player == 0:
            self.p1Went = move
        else:
            self.p2Went = move

    def connected(self):
        return self.ready

    def feed_addr(self, p, conn):
        if p == 0:
            self.conn1 = conn
        else:
            self.conn2 = conn

    def bothWent(self):
        # print("reached in both went")
        return (self.p1Went) and (self.p2Went)

    def winner(self):
        score1 = int(self.moves[0])
        score2 = int(self.moves[1])

        winner = -1

        if score1 > score2:
            winner = 0
        elif score1 < score2:
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
        self.p1_ready_to_go_forward = False
        self.p2_ready_to_go_forward = False

    def restart(self):
        self.restart = True
