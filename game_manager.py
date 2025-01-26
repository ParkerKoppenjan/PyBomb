import pygame
from game import GameState, Menu
from enum import Enum
from enums import MenuAction

class GameScreen(Enum):
    MAIN_MENU = 1
    GAME = 2
    GAME_OVER = 3

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.current_screen = GameScreen.MAIN_MENU
        self.game_state = None
        self.menu = None
        self.running = True
        self.player_count = 4 # defaults to 4

    def run(self):
        while self.running:
            if self.current_screen == GameScreen.MAIN_MENU:
                self.handle_menu()
            elif self.current_screen == GameScreen.GAME:
                self.handle_game(self.player_count)
            elif self.current_screen == GameScreen.GAME_OVER:
                self.handle_game_over()
        pygame.quit()


    def handle_menu(self):
        if self.menu is None:
            self.menu = Menu(self.screen)

        action = self.menu.run()

        if action == MenuAction.QUIT:
            self.running = False
            pygame.quit()
            return

        elif isinstance(action, list):
            if action[0] == MenuAction.START_LOCAL:
                self.player_count = action[1]
                self.current_screen = GameScreen.GAME
        elif action == MenuAction.START_MULTI:
            pass


    def handle_game(self, player_count):
        if self.game_state is None:
            self.game_state = GameState(player_count, self.screen)

        action = self.game_state.run()

        if action == MenuAction.QUIT:
            self.running = False
            pygame.quit()
            return

        if self.game_state.winner is not None:
            self.current_screen = GameScreen.GAME_OVER


    def handle_game_over(self):
        pass

def main():
    manager = GameManager()
    manager.run()
    pygame.quit()

main()



