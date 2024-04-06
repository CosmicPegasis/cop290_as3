class GameStatus:
    def __init__(self, id):
        self.p1Went = (
            False  # this will be used to check if game is over for both players
        )
        self.p2Went = False  # That means that game.stop() has been done for player-1
        self.ready = False  # To see if they are connected
        self.id = id
        self.moves = [None, None]  # here move is an int(This is score)
        self.wins = [0, 0]
        self.ties = 0
        self.restart = False

    def get_player_move(self, p):
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = move
        else:
            self.p2Went = move

    def connected(self):
        return self.ready

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
        
    def restart(self):
        self.restart = True