import pygame
from client.menu.home import Home
from client.utils.constants import WINDOW_HEIGHT, WINDOW_WIDTH
import time
import client.menu.pitch_results as pitch_results
from client.utils.network import Network
import client.menu.multiplayer_game_result as multiplayer_game_result
import client.games.multi_game as multi_game
import client.menu.multiplayer_game_result as multiplayer_game_result
import client.games.practice_results as practice_results
import client.menu.songs_results as songs_results
import client.games.battle_game_play as battle_play
import client.menu.battle_game_results as battle_game_results
import client.games.battle_game_listen as battle_listen
import socket
import pickle

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Piano Master")

running = True
cur_screen = Home()

clock = 0
n = 0
player = 0

halt = 0
var = 0
debugger = 0
debugger2 = 0
while running:

    running = cur_screen.handle_events(pygame.event.get())
    cur_screen.update()  # This line changes the current state of game window but its effects are not visible.
    cur_screen.render(
        window
    )  # This line will bring the current state onto the game_window

    if cur_screen.switch_screen:
        cur_screen = cur_screen.new_screen

    if cur_screen.game_type == "pitch":

        if cur_screen.flag == 0:
            cur_screen.start_game()

        cur_screen.game_screen.handle_events()
        if not cur_screen.game_screen.is_running():
            score = cur_screen.game_screen.stop()
            cur_screen.new_screen = pitch_results.PitchResultMenu(
                score,
                cur_screen.narrate_name,
                cur_screen.narrate_pitch,
                cur_screen.note_length,
            )
            cur_screen = cur_screen.new_screen
            time.sleep(1)
            cur_screen.play_sound("your_score_is")
            time.sleep(2)
            cur_screen.load_score(score)
            pygame.mixer.music.unpause()

    if cur_screen.game_type == "practice":
        if cur_screen.flag == 0:
            cur_screen.start_game()

        cur_screen.game_screen.handle_events()
        if not cur_screen.game_screen.is_running():
            score = cur_screen.game_screen.stop()
            cur_screen.new_screen = practice_results.PracticeResults(
                score,
                cur_screen.narrate_name,
                cur_screen.narrate_pitch,
                cur_screen.note_length,
            )
            cur_screen = cur_screen.new_screen
            time.sleep(1)
            cur_screen.play_sound("your_score_is")
            time.sleep(2)
            cur_screen.load_score(score)
            pygame.mixer.music.unpause()

    if cur_screen.game_type == "songs":
        if cur_screen.flag == 0:
            cur_screen.start_game()

        cur_screen.game_screen.handle_events()
        if not cur_screen.game_screen.is_running():
            score = cur_screen.game_screen.stop()
            cur_screen.new_screen = songs_results.SongsResults(
                cur_screen.song,
                score,
                cur_screen.narrate_name,
                cur_screen.narrate_pitch,
                cur_screen.note_length,
            )
            cur_screen = cur_screen.new_screen
            time.sleep(1)
            cur_screen.play_sound("your_score_is")
            time.sleep(2)
            cur_screen.load_score(score)
            pygame.mixer.music.unpause()
    # 3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
    if (cur_screen.game_type != None) and (cur_screen.game_type[:6] == "versus"):
        try:
            if var == 0:
                clock = pygame.time.Clock()
                n = Network(0)
                n.send("0")
                player = int(n.getP())  # This player is me.
                # print("player : ", n.getP())
                var = 1

            game = n.send("get")

        except:
            print("Could not game. This means client is not connected to server")
            break

        if cur_screen.game_type == "versus_act_mult_game":
            score_mid1 = 0
            score_mid2 = 0  # This is disconnection logic
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    score_mid2 = cur_screen.game_screen.stop()
                    n.send("DISCONNECTED")
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    print("entered stop")
                    score_mid2 = cur_screen.game_screen.stop()
                    print("game stopped")
                    halt = 1
                    n.send("DISCONNECTED")

            if game == None:
                print("One halted")
                score_mid1 = cur_screen.game_screen.stop()
                cur_screen.new_screen = multiplayer_game_result.MultiGameResults(
                    str(score_mid1), str(score_mid2), player
                )
                cur_screen = cur_screen.new_screen
                var = 0

            if halt == 1:
                cur_screen.new_screen = multiplayer_game_result.MultiGameResults(
                    str(score_mid1), str(score_mid2), player
                )
                cur_screen = cur_screen.new_screen
                var = 0
                halt = 0
            # 3333333333333333333333333333333333333333333333333333333333333
        if cur_screen.game_type == "versus_waiting":
            if game.connected():

                if game.conn1 == n.client_number:
                    player = 0
                else:
                    player = 1

                print("player: ", player)
                print("both connected to server successfully")
                cur_screen.asset_man.sounds["waiting"].stop()
                cur_screen.play_sound("connected")
                time.sleep(2)
                cur_screen.new_screen = multi_game.MultiGame(
                    int(player), game.song_number
                )
                pygame.mixer.music.pause()
                cur_screen = cur_screen.new_screen
                print("both connected to server successfully-2")

        if (cur_screen.game_type != None) and (cur_screen.game_type[:6] == "versus"):
            if game.bothWent():
                print("BothWent")
                move1 = game.get_player_move(0)
                move2 = game.get_player_move(1)
                cur_screen.new_screen = multiplayer_game_result.MultiGameResults(
                    move1, move2, player
                )
                cur_screen = cur_screen.new_screen
                var = 0

            else:
                if cur_screen.game_type == "versus_act_mult_game":

                    if cur_screen.flag == 0:
                        cur_screen.start_game()
                    if cur_screen.game_screen.is_running():
                        cur_screen.game_screen.handle_events()

                    if player == 0:
                        if not game.p1Went:
                            if not cur_screen.game_screen.is_running():
                                score = cur_screen.game_screen.stop()
                                n.send(str(score))
                                print("Score sent :", score)
                    else:
                        if not game.p2Went:  # add stopper
                            if not cur_screen.game_screen.is_running():
                                score = cur_screen.game_screen.stop()
                                n.send(str(score))
                                print("Score sent :", score)
    #################################################################################################
    if (cur_screen.game_type != None) and (cur_screen.game_type[:6] == "battle"):
        # try:
        if var == 0:
            clock = pygame.time.Clock()
            n = Network(1)
            n.send("1")
            player = int(n.getP())  # This player is me.
            # print("player : ", n.getP())
            var = 1

        game = n.send("get")
        # n.send("match_players")
        # print("game: ",game)

        # except:
        #     print("Could not game. This means client is not connected to server")
        #     break

        if cur_screen.game_type == "battle_act_mult_game":
            # print("recahed here")
            score_mid1 = game.moves[0]
            score_mid2 = game.moves[1]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # score_mid2 = cur_screen.game_screen.stop()
                    n.send("DISCONNECTED")
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    print("entered stop")
                    # score_mid2 = cur_screen.game_screen.stop()
                    print("game stopped")
                    halt = 1
                    n.send("DISCONNECTED")

            if game == None:
                print("One halted")
                # score_mid1 = cur_screen.game_screen.stop()
                cur_screen.new_screen = battle_game_results.BattleResults(
                    str(score_mid1), str(score_mid2), player
                )
                cur_screen = cur_screen.new_screen
                var = 0

            if halt == 1:
                cur_screen.new_screen = battle_game_results.BattleResults(
                    str(score_mid1), str(score_mid2), player
                )
                cur_screen = cur_screen.new_screen
                var = 0
                halt = 0

        if cur_screen.game_type == "battle_act_mult_game":
            pygame.display.flip()
            if cur_screen.flag == 0:
                cur_screen.start_game()
            if cur_screen.listener.is_listening():
                cur_screen.listener.handle_events()

                # start playing mode here

        if cur_screen.game_type == "battle_waiting":
            if game.connected():

                if game.conn1 == n.client_number:
                    player = 0
                else:
                    player = 1

                print("player: ", player)
                print("both connected to server successfully")
                cur_screen.asset_man.sounds["waiting"].stop()
                cur_screen.play_sound("connected")
                time.sleep(2)
                cur_screen.new_screen = battle_play.Battle_play(int(player))
                pygame.mixer.music.pause()
                cur_screen = cur_screen.new_screen
                print("both connected to server successfully-2")

        if (cur_screen.game_type != None) and (
            cur_screen.game_type == "battle_listen_mult_game"
        ):
            # print("here")
            # print("song_array1: ",game.song_array[0])
            # print("song_array2: ",game.song_array[1])
            pygame.display.flip()
            # print(cur_screen.flag)
            if cur_screen.flag == 0:
                cur_screen.start_game()
            if cur_screen.game_screen.is_running():
                cur_screen.game_screen.handle_events()
            if player == 0:
                if not game.p1Went:
                    if not cur_screen.game_screen.is_running():
                        score = cur_screen.game_screen.stop()
                        print(score)
                        n.send(str(score))
                        # n.send(str(99))
            else:  # Game stop of listening mode and sending score to the server
                if not game.p2Went:
                    if not cur_screen.game_screen.is_running():
                        score = cur_screen.game_screen.stop()
                        print(score)
                        n.send(str(score))

        if cur_screen.game_type == "battle_act_mult_game":
            # print("came here")
            if player == 0:
                if not game.p1_ready_to_go_forward:
                    if not cur_screen.listener.is_listening():
                        arr = cur_screen.listener.stop()
                        print(arr)
                        barr = pickle.dumps(arr)
                        n.send_bin(
                            barr
                        )  # send array of array of playing mode to server
                        print(pickle.loads(barr))
            else:
                if not game.p2_ready_to_go_forward:
                    if not cur_screen.listener.is_listening():
                        arr = cur_screen.listener.stop()
                        print(arr)
                        barr = pickle.dumps(arr)
                        n.send_bin(
                            barr
                        )  # send array of array of playing mode to server
                        print(pickle.loads(barr))

        if cur_screen.game_type == "battle_act_mult_game":
            if game.p1_ready_to_go_forward and game.p2_ready_to_go_forward:
                song_1 = game.song_array[1]  ## loading array from server
                song_2 = game.song_array[0]  ## in the listening mode
                print(song_1)
                print(song_2)
                if player == 0:
                    cur_screen.new_screen = battle_listen.Battle_listen(
                        int(player), song_1
                    )
                else:
                    cur_screen.new_screen = battle_listen.Battle_listen(
                        int(player), song_2
                    )
                pygame.mixer.music.pause()
                cur_screen = cur_screen.new_screen
                pygame.display.flip()

        if (cur_screen.game_type != None) and (
            cur_screen.game_type == "battle_listen_mult_game"
        ):
            if game.p1Went and game.p2Went:
                n.send("round_finished")

                if game.round >= 0:
                    score1 = game.moves[0]
                    score2 = game.moves[1]
                    cur_screen.new_screen = battle_game_results.BattleResults(
                        str(score1), str(score2), player
                    )
                    cur_screen = cur_screen.new_screen
                    n.send("DISCONNECTED")
                    var = 0
                else:
                    cur_screen.new_screen = battle_play.Battle_play(player)
                    pygame.mixer.music.pause()
                    cur_screen = cur_screen.new_screen
                    n.send("reset")
                    debugger = 0
                    debugger2 = 0

    pygame.display.flip()

pygame.quit()
