import pygame
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from main_menu import MainMenu

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Piano Master")

running = True
cur_screen = MainMenu()
while running:
    running = cur_screen.handle_events(pygame.event.get())
    cur_screen.update()
    cur_screen.render(window)
    if cur_screen.switch_screen:
        cur_screen = cur_screen.new_screen
    pygame.display.flip()

pygame.quit()
