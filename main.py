
import pygame
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from home import Home

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Piano Master")

running = True
cur_screen = Home()

while running:
    running = cur_screen.handle_events(pygame.event.get())
    cur_screen.update() # This line changes the current state of game window but its effects are not visible. 
    cur_screen.render(window) # This line will bring the current state onto the game_window
    if cur_screen.switch_screen:
        cur_screen = cur_screen.new_screen
    pygame.display.flip()

pygame.quit()
