import pygame
from game import GameState, Menu, GameOverScreen
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
        self.game_over = None
        self.running = True
        self.player_count = None
        self.winner = None


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
            elif action == MenuAction.JOIN_MULTI:
                pass


    def handle_game(self, player_count=None):
        if player_count is None:
            player_count = self.player_count
        self.player_count = player_count
        if self.game_state is None:
            self.game_state = GameState(player_count, self.screen)

        action = self.game_state.run()

        if action == MenuAction.QUIT:
            self.running = False
            return

        elif action == MenuAction.TO_GAME_OVER:
            self.winner = self.game_state.winner
            self.current_screen = GameScreen.GAME_OVER
            self.game_state = None
            return


    def handle_game_over(self):
        if self.game_over is None:
            self.game_over = GameOverScreen(self.screen, self.winner)

        action = self.game_over.run()

        if action == MenuAction.QUIT:
            self.running = False
            pygame.quit()
            return
        elif action == MenuAction.START_LOCAL:
            self.current_screen = GameScreen.GAME
            self.game_state = None
            self.game_over = None
        elif action == MenuAction.TO_MENU:
            self.current_screen = GameScreen.MAIN_MENU
            self.menu = None
            self.game_over = None




def main():
    manager = GameManager()
    manager.run()
    pygame.quit()

main()



