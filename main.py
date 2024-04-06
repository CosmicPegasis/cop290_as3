import pygame
from client.menu.home import Home
from client.utils.constants import WINDOW_HEIGHT, WINDOW_WIDTH
import time
import client.menu.pitch_results as pitch_results
from client.utils.network import Network
import client.menu.multiplayer_game as multiplayer_game
import client.games.multi_game as multi_game
import client.menu.multiplayer_game as multiplayer_game
import client.games.practice_results as practice_results
import client.menu.songs_results as songs_results

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Piano Master")

running = True
cur_screen = Home()

clock = 0
n = 0
player = 0

halt =0
var = 0
debugger = 0
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
            cur_screen.new_screen = pitch_results.PitchResultMenu(score,cur_screen.narrate_name,cur_screen.narrate_pitch,cur_screen.note_length)
            cur_screen = cur_screen.new_screen
            time.sleep(1)
            cur_screen.play_sound("your_score_is")
            time.sleep(2)
            cur_screen.load_score(score)
            pygame.mixer.music.unpause()

    # print(cur_screen.game_type)
    if cur_screen.game_type == "practice":
        if cur_screen.flag == 0:
            cur_screen.start_game()
            
        cur_screen.game_screen.handle_events()
        if not cur_screen.game_screen.is_running():
            score = cur_screen.game_screen.stop()
            cur_screen.new_screen = practice_results.PracticeResults(score,cur_screen.narrate_name,cur_screen.narrate_pitch,cur_screen.note_length)
            cur_screen = cur_screen.new_screen
            time.sleep(1)
            cur_screen.play_sound("your_score_is")
            time.sleep(2)
            cur_screen.load_score(score)
            pygame.mixer.music.unpause()
            
    if cur_screen.game_type == "songs":
        if cur_screen.flag ==0:
            cur_screen.start_game()
        
        cur_screen.game_screen.handle_events()
        if not cur_screen.game_screen.is_running():
            score = cur_screen.game_screen.stop()
            cur_screen.new_screen = songs_results.SongsResults(cur_screen.song,score,cur_screen.narrate_name,cur_screen.narrate_pitch,cur_screen.note_length)
            cur_screen = cur_screen.new_screen
            time.sleep(1)
            cur_screen.play_sound("your_score_is")
            time.sleep(2)
            cur_screen.load_score(score)
            pygame.mixer.music.unpause()

    if (cur_screen.game_type != None) and (cur_screen.game_type[:6] == "versus"):
        # print("hello")

        try:
            if var == 0:
                clock = pygame.time.Clock()
                n = Network()
                player = int(n.getP())  # This player is me.
                print("player : ", n.getP())
                var = 1

            
            game = n.send("get")
            # print("got game")
        except:
            # run = False
            print("Could not game. This means client is not connected to server")
            break
        
        if cur_screen.game_type == "versus_act_mult_game":
            score_mid1 =0
            score_mid2 =0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    score_mid2 = cur_screen.game_screen.stop()
                    
                    n.send("DISCONNECTED")
                    
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    print("entered stop")
                    score_mid2 = cur_screen.game_screen.stop()
                    print("game stopped")
                    halt =1
                    n.send("DISCONNECTED")
                    # cur_screen.new_screen = multiplayer_game.MultiGameResults(str(score_mid1),str(score_mid2),player)
                    # cur_screen = cur_screen.new_screen
                    # var =0
                    
            # if cur_screen.halt_flag == 1:
            #     cur_screen.game_screen.stop()
            #     n.send("DISCONNECTED")
            #     cur_screen.new_screen = multiplayer_game.MultiGameResults(str(score_mid1),str(score_mid2),player)
            #     cur_screen = cur_screen.new_screen
            #     var =0
                    
            if game == None:
                print("One halted")
                # n = Network()
                # player = int(n.getP())
                # game = n.send("get")
                score_mid1 = cur_screen.game_screen.stop()
                cur_screen.new_screen = multiplayer_game.MultiGameResults(str(score_mid1),str(score_mid2),player)
                cur_screen = cur_screen.new_screen
                var =0
            
            if halt == 1:
                cur_screen.new_screen = multiplayer_game.MultiGameResults(str(score_mid1),str(score_mid2),player)
                cur_screen = cur_screen.new_screen
                var =0
                halt =0

        if cur_screen.game_type == "versus_waiting":
            if game.connected():
                print("both connected to server successfully")
                cur_screen.new_screen = multi_game.MultiGame(int(player))
                pygame.mixer.music.pause()
                cur_screen = cur_screen.new_screen
                print("both connected to server successfully-2")

        
        if (cur_screen.game_type != None) and (cur_screen.game_type[:6] == "versus"):    
            if game.bothWent():
                print("BothWent")
            # redrawWindow(win, game, player) no need as there is already draw function
                move1 = game.get_player_move(0)
                move2 = game.get_player_move(1)
                cur_screen.new_screen = multiplayer_game.MultiGameResults(
                    move1, move2, player
                )
                cur_screen = cur_screen.new_screen
                var =0

            else:
                if cur_screen.game_type == "versus_act_mult_game":

                    if cur_screen.flag == 0:
                        cur_screen.start_game()
                    # debugger =1
                    if cur_screen.game_screen.is_running():
                        cur_screen.game_screen.handle_events()

                    if player == 0:

                        if not game.p1Went:
                        # print("current ",debugger)
                        # print(cur_screen.game_screen.is_running())
                            if not cur_screen.game_screen.is_running():
                                score = cur_screen.game_screen.stop()
                                n.send(str(score))
                                print("Score sent :", score)
                    else:

                        if not game.p2Went:
                        # print("current ",debugger)
                        # print(cur_screen.game_screen.is_running())
                            if not cur_screen.game_screen.is_running():
                                score = cur_screen.game_screen.stop()
                                n.send(str(score))
                                print("Score sent :", score)

    pygame.display.flip()

pygame.quit()
