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
import client.menu.versus as versus
import client.menu.battle_mode as battle
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
delay =0
halt = 0
round =0
is_network_initiated = 0
score_keeper =(0,0)
while running:

    running = cur_screen.handle_events(pygame.event.get())
    cur_screen.update() 
    cur_screen.render(
        window
    ) 

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
            pygame.mixer.music.unpause()
    # 3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
    if (cur_screen.game_type != None) and (cur_screen.game_type[:6] == "versus"):
        try:
            if is_network_initiated == 0 :
                clock = pygame.time.Clock()
                n = Network()
                n.send("0")
                is_network_initiated = 1
                round =0
            game = n.send("get")

        except:
            print("Server is Down")
            cur_screen.play_sound("server_is_down")
            time.sleep(2)
            cur_screen.new_screen = versus.Versus("Server is Down")
            cur_screen = cur_screen.new_screen
            continue
        
        if cur_screen.game_type == "versus_waiting":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    n.send("DISCONNECTED")
                    n.send("DISCONNECTED")
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_DOWN):
                        print("entered stop")
                        cur_screen.new_screen = versus.Versus()
                        print("game stopped")
                        n.send("DISCONNECTED")
                        n.send("DISCONNECTED")
                        is_network_initiated = 0
                        cur_screen = cur_screen.new_screen
            
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
                cur_screen.play_sound("game_halted")
                cur_screen.new_screen = multiplayer_game_result.MultiGameResults(
                    str(score_mid1), str(score_mid2), player
                )
                cur_screen = cur_screen.new_screen
                is_network_initiated = 0

            if halt == 1:
                cur_screen.play_sound("game_halted")
                cur_screen.new_screen = multiplayer_game_result.MultiGameResults(
                    str(score_mid1), str(score_mid2), player
                )
                cur_screen = cur_screen.new_screen
                is_network_initiated = 0
                halt = 0
            
            pygame.display.flip()
            
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
                cur_screen = cur_screen.new_screen
                pygame.mixer.music.pause()
                print("both connected to server successfully and game has started running")

        if (cur_screen.game_type != None) and (cur_screen.game_type[:6] == "versus"):
            if game.bothWent():
                print("BothWent")
                move1 = game.get_player_move(0)
                move2 = game.get_player_move(1)
                cur_screen.new_screen = multiplayer_game_result.MultiGameResults(
                    move1, move2, player
                )
                pygame.mixer.music.pause()
                cur_screen = cur_screen.new_screen
                pygame.display.flip()
                is_network_initiated = 0

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
        try:
            if is_network_initiated == 0:
                clock = pygame.time.Clock()
                n = Network()
                n.send("1")
                is_network_initiated = 1
                round =0
        
            try:
                game = n.send("get")
            except Exception as e:
                game = None
                print(e)
        except Exception as e:
            print("could not connect to the server.")
            cur_screen.play_sound("server_is_down")
            time.sleep(2)
            cur_screen.new_screen = battle.Battle("Server is down")
            cur_screen = cur_screen.new_screen
            continue
        
        if cur_screen.game_type == "battle_waiting":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    n.send("DISCONNECTED")
                    n.send("DISCONNECTED")
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_DOWN):
                        print("entered stop")
                        cur_screen.new_screen = battle.Battle()
                        print("game stopped")
                        n.send("DISCONNECTED")
                        n.send("DISCONNECTED")
                        is_network_initiated = 0
                        cur_screen = cur_screen.new_screen
        
        if game!=None and cur_screen.game_type == "battle_results":
            score_t1 = game.moves[0]
            score_t2 = game.moves[1]
            time.sleep(1)
            cur_screen.play_sound("your_score_is")
            time.sleep(2)
            cur_screen.load_score(score_t1)
            time.sleep(1)
            cur_screen.play_sound("oppo_score_is")
            time.sleep(2)
            cur_screen.load_score(score_t2)
            cur_screen.new_screen = battle_game_results.BattleResults(str(score_t1), str(score_t2), player)
            cur_screen = cur_screen.new_screen
            is_network_initiated = 0
        
        if (game == None) and cur_screen.game_type != "battle_results":
            if(cur_screen.game_type == "battle_act_mult_game"):
                cur_screen.listener.stop()
            if (cur_screen.game_type == "battle_listen_mult_game"):
                cur_screen.game_screen.stop()
            time.sleep(1)
            cur_screen.play_sound("your_score_is")
            time.sleep(2)
            cur_screen.load_score(score_keeper[0])
            time.sleep(1)
            cur_screen.play_sound("oppo_score_is")
            time.sleep(2)
            cur_screen.load_score(score_keeper[1])
            cur_screen.new_screen = battle_game_results.BattleResults(str(score_keeper[0]), str(score_keeper[1]), player)
            cur_screen = cur_screen.new_screen
            is_network_initiated = 0
        
        if game !=None and cur_screen.game_type == "battle_listen_mult_game":
            score_mid1 = game.moves[0]
            score_mid2 = game.moves[1]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    n.send("DISCONNECTED")
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    halt = 1
                    cur_screen.game_screen.stop()
                    n.send("DISCONNECTED")

            if game == None:
                print("One halted")
                # score_mid1 = cur_screen.game_screen.stop()
                time.sleep(1)
                cur_screen.play_sound("your_score_is")
                time.sleep(2)
                cur_screen.load_score(score_mid1)
                time.sleep(1)
                cur_screen.play_sound("oppo_score_is")
                time.sleep(2)
                cur_screen.load_score(score_mid2)
                cur_screen.new_screen = battle_game_results.BattleResults(
                    str(score_mid1), str(score_mid2), player
                )
                cur_screen = cur_screen.new_screen
                is_network_initiated = 0

            if halt == 1:
                time.sleep(1)
                cur_screen.play_sound("your_score_is")
                time.sleep(2)
                cur_screen.load_score(score_mid1)
                time.sleep(1)
                cur_screen.play_sound("oppo_score_is")
                time.sleep(2)
                cur_screen.load_score(score_mid2)
                cur_screen.new_screen = battle_game_results.BattleResults(
                    str(score_mid1), str(score_mid2), player
                )
                cur_screen = cur_screen.new_screen
                is_network_initiated = 0
                halt = 0

        
        if game !=None and cur_screen.game_type == "battle_act_mult_game":
            score_mid1 = game.moves[0]
            score_mid2 = game.moves[1]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    n.send("DISCONNECTED")
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    halt = 1
                    cur_screen.listener.stop()
                    n.send("DISCONNECTED")

            if game == None:
                print("One halted")
                # score_mid1 = cur_screen.game_screen.stop()
                time.sleep(1)
                cur_screen.play_sound("your_score_is")
                time.sleep(2)
                cur_screen.load_score(score_mid1)
                time.sleep(1)
                cur_screen.play_sound("oppo_score_is")
                time.sleep(2)
                cur_screen.load_score(score_mid2)
                cur_screen.new_screen = battle_game_results.BattleResults(
                    str(score_mid1), str(score_mid2), player
                )
                cur_screen = cur_screen.new_screen
                is_network_initiated = 0

            if halt == 1:
                time.sleep(1)
                cur_screen.play_sound("your_score_is")
                time.sleep(2)
                cur_screen.load_score(score_mid1)
                time.sleep(1)
                cur_screen.play_sound("oppo_score_is")
                time.sleep(2)
                cur_screen.load_score(score_mid2)
                cur_screen.new_screen = battle_game_results.BattleResults(
                    str(score_mid1), str(score_mid2), player
                )
                cur_screen = cur_screen.new_screen
                is_network_initiated = 0
                halt = 0

        if game != None and cur_screen.game_type == "battle_act_mult_game":
            pygame.display.flip()
            if cur_screen.flag == 0:
                cur_screen.start_game()
            if cur_screen.listener.is_listening():
                cur_screen.listener.handle_events()

        if game != None and cur_screen.game_type == "battle_waiting":
            if game != None and game.connected():
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
                print("both connected to server successfully and server is okay")
            
        if (game !=None)and(cur_screen.game_type != None) and (
            cur_screen.game_type == "battle_listen_mult_game"
        ):
            pygame.display.flip()
            if cur_screen.flag == 0:
                cur_screen.start_game()
            if cur_screen.game_screen.is_running():
                cur_screen.game_screen.handle_events()
            if player == 0:
                if not game.p1Went:
                    if not cur_screen.game_screen.is_running():
                        score = cur_screen.game_screen.stop()
                        print("score sent by 1",score)
                        n.send(str(score))
            else:  
                if not game.p2Went:
                    if not cur_screen.game_screen.is_running():
                        score = cur_screen.game_screen.stop()
                        print("score sent by 2",score)
                        n.send(str(score))

        if game !=None and cur_screen.game_type == "battle_act_mult_game":
            if player == 0:
                if not game.p1_ready_to_go_forward:
                    if not cur_screen.listener.is_listening():
                        arr = cur_screen.listener.stop()
                        barr = pickle.dumps(arr)
                        n.send_bin(barr)
                        print(pickle.loads(barr))
            else:
                if not game.p2_ready_to_go_forward:
                    if not cur_screen.listener.is_listening():
                        arr = cur_screen.listener.stop()
                        barr = pickle.dumps(arr)
                        n.send_bin(
                            barr
                        )  
                        print(pickle.loads(barr))

        if game !=None and cur_screen.game_type == "battle_act_mult_game":
            if game.p1_ready_to_go_forward and game.p2_ready_to_go_forward:
                song_1 = game.song_array[1]  
                song_2 = game.song_array[0]  
                print(cur_screen.game_type)
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
                cur_screen.play_sound("play_to_listen")
                time.sleep(2)
                pygame.display.flip()

        if game !=None and (cur_screen.game_type != None) and (
            cur_screen.game_type == "battle_listen_mult_game"
        ):
            if game.p1Went and game.p2Went:
                try:
                    n.send("round_finished")
                except Exception as e:
                    print(e)
                round+=1
                
                if round > 1:
                    score1 = game.moves[0]
                    score2 = game.moves[1]
                    time.sleep(1)
                    cur_screen.play_sound("your_score_is")
                    time.sleep(2)
                    cur_screen.load_score(score1)
                    time.sleep(1)
                    cur_screen.play_sound("oppo_score_is")
                    time.sleep(2)
                    cur_screen.load_score(score2)
                    cur_screen.new_screen = battle_game_results.BattleResults(
                        str(score1), str(score2), player
                    )
                    cur_screen = cur_screen.new_screen
                    is_network_initiated = 0
                    delay =0
                else:
                    cur_screen.play_sound("round_over")
                    time.sleep(1.5)
                    cur_screen.new_screen = battle_play.Battle_play(player)
                    pygame.mixer.music.pause()
                    cur_screen = cur_screen.new_screen
                    n.send("reset")
                    game = n.send("get")
                    

    pygame.display.flip()

pygame.quit()
