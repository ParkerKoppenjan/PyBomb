from english_words import get_english_words_set
import pygame
from enums import MenuAction
import math
import syllables as syl
from tweener import *

class GameState:
    def __init__(self, player_count, screen=pygame.display.set_mode((1280, 720))):
        pygame.init() # THIS IS ONLY FOR TESTING. GAME_MANAGER WILL HANDLE INIT
        # creates list of players
        self.players = []
        for i in range(player_count):
            name = f"Player {i+1}"
            new_player = Player(name)
            self.players.append(new_player)

        self.valid_words = get_english_words_set(sources=['web2'], lower=True, alpha=True) # preload valid English words
        self.used_words = set()
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]
        self.current_diff = syl.easy_syllables # start with easy difficulty
        self.current_syl = self.current_diff.random_key() # get initial random syllable
        self.input_buffer = "" # player input while its being typed
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.turn_time = 20 # initial turn duration
        self.current_turn_time = self.turn_time
        self.turn_count = 0
        self.winner = None

        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((74, 64, 57))  # gray background color
        self.arrow = Arrow(self.screen, 640, 376)

        # images
        self.image = pygame.image.load("assets/bomb.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))


    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000  # calculates delta time, elapsed time between each frame
            self.handle_events()
            self.logic()
            self.render()
        return MenuAction.QUIT

    def handle_events(self):
        """Handles local player actions; keyboard inputs and quitting"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.input_buffer = self.input_buffer[:-1] # remove last character
                elif event.key == pygame.K_RETURN:
                    if self.validate_word(self.input_buffer.lower()):
                        self.next_turn(True)
                else:
                    self.input_buffer += event.unicode

    def logic(self):
        self.current_turn_time -= self.dt
        if self.current_turn_time <= 0:
            self.current_player.lives -= 1 # player loses a life for timing out
            self.next_turn(False)

        if self.current_player.lives <= 0:
            self.players.pop(self.current_player_index) # remove player with no lives

            if len(self.players) == 1:
                self.winner = self.players[0]
                self.running = False
                return


        # increase difficulty as game progresses
        if self.turn_count // len(self.players) == 6 and self.turn_time != 15:
            self.current_diff = syl.medium_syllables
            self.turn_time = 15
            self.current_turn_time = self.turn_time
        elif self.turn_count // len(self.players) == 12 and self.turn_time != 10:
            self.current_diff = syl.hard_syllables
            self.turn_time = 10
            self.current_turn_time = self.turn_time

    def render(self):
        """Draws everything to the screen."""
        self.screen.blit(self.background, (0, 0))  # draw the background
        self.arrow.update()
        self.arrow.render()
        self.screen.blit(self.image, (565, 285))  # draw the bomb at its center


        font = pygame.font.Font("assets/Poppins.ttf", 26)

        # calculate text position to center it on the bomb
        bomb_center_x = 565 + self.image.get_width() // 2
        bomb_center_y = 16 + 285 + self.image.get_height() // 2 # 16 is an eyeball adjustment for the bomb text
        text_width, text_height = font.size(self.current_syl)
        text_x_pos = bomb_center_x - text_width // 2
        text_y_pos = (bomb_center_y - text_height // 2)

        self.screen.blit(font.render(self.current_syl, True, (255, 255, 255)), (text_x_pos, text_y_pos))

        self.screen.blit(font.render(f"Time Left: {int(self.current_turn_time)}", True, (255, 255, 255)), (50, 100))
        self.screen.blit(font.render(f"Input: {self.input_buffer}", True, (255, 255, 255)), (50, 150))

        active_players = [p for p in self.players if p.lives > 0] # removes 0 life players from visual rendering

        player_angles = {} # dict to store the angle at which player names are from the center, for arrow pointing
        for i, player in enumerate(active_players):
            # calculate player's position on a circle around the bomb
            angle = (2 * math.pi * i) / len(active_players)
            player_angles[player] = angle
            player_x = bomb_center_x + 200 * math.cos(angle)
            player_y = bomb_center_y - 200 * math.sin(angle)

            # render player name and lives
            text_surface = font.render(f"{player.name}: {player.lives}", True, (255, 255, 255))
            text_width, text_height = text_surface.get_size()

            # adjust text positioning to look less wonky
            text_x = player_x - text_width / 2
            text_y = player_y - text_height / 2

            self.screen.blit(text_surface, (text_x, text_y))

        if player_angles[self.current_player] != self.arrow.start_angle:
            self.arrow.rotate(player_angles[self.current_player], 20)


        pygame.display.flip()  # updates the display

    def validate_word(self, buffer) -> bool:
        """ Validates input to ensure it includes the syllable, in order and without characters in between."""
        if len(buffer) == len(self.current_syl): # prevent exact syllable match
            return False
        if buffer not in self.valid_words: # check if word exists
            return False
        if buffer in self.used_words: # prevent repeating words
            return False
        syl_pointer = 0
        for char in buffer:
            if char == self.current_syl[syl_pointer]:
                syl_pointer += 1
                if syl_pointer == len(self.current_syl):
                    self.used_words.add(buffer)
                    return True
            else:
                syl_pointer = 0 # reset pointer if sequence breaks
        return False

    def next_turn(self, success): # success is bool that bases on if the player got a valid word in time
        self.turn_count += 1
        self.current_turn_time = self.turn_time
        self.input_buffer = ""
        # cycle to next player, wrapping around the list
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]
        if success:
            self.current_syl = self.current_diff.random_key() # get new syllable on successful word


class Player:
    def __init__(self, name = "player"):
        self.name = name
        self.lives = 2 # each player starts with 2 lives


class Menu:
    def __init__(self, screen=pygame.display.set_mode((1280, 720))):
        self.input_buffer = ""
        self.running = True
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size())

        self.background.fill((74, 64, 57))
        self.MOUSE_POS = None
        self.buttons = {
            'local': Button(440, 335, 400, 50, "START LOCAL", (59, 89, 182), (32, 49, 102)),
            'multiplayer': Button(440, 415, 400, 50, "HOST MULTIPLAYER", (59, 89, 182), (32, 49, 102)),
            'join': Button(440, 495, 400, 50, "JOIN GAME", (59, 89, 182), (32, 49, 102))
        }

    def run(self):
        while self.running:
            self.MOUSE_POS = pygame.mouse.get_pos()
            action = self.handle_events()
            if action is not None:
                return action

            self.render()

            # update button hover state
            for button in self.buttons.values():
                button.is_hovered = button.is_mouse_over(self.MOUSE_POS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return MenuAction.QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons['local'].handle_click(self.MOUSE_POS):
                    store = self.input_render() # get number of players
                    self.running = False
                    return store
                elif self.buttons['multiplayer'].handle_click(self.MOUSE_POS):
                    return MenuAction.START_MULTI
                elif self.buttons['join'].handle_click(self.MOUSE_POS):
                    return MenuAction.JOIN_MULTI


    def render(self):
        self.screen.blit(self.background, (0, 0))

        font = pygame.font.Font("assets/Retro.ttf", 80)
        self.screen.blit(font.render("PYBOMB", True, (255, 255, 255)), (400, 100))

        for button in self.buttons.values():
            button.draw(self.screen)
        pygame.display.flip()

    def input_render(self):
        while True:
            self.screen.blit(self.background, (0, 0)) # clear screen
            font = pygame.font.Font("assets/Poppins.ttf", 30)
            self.screen.blit(font.render(f"How many players? (2-8): {self.input_buffer}", True, (255, 255, 255)), (50, 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            player_count = int(self.input_buffer)
                            # validate player count
                            if 2 <= player_count <= 8:
                                return [MenuAction.START_LOCAL, int(self.input_buffer)]
                        except ValueError:
                            pass
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_buffer = self.input_buffer[:-1] # remove last character
                    elif event.unicode.isdigit() and len(self.input_buffer) < 1:
                       self.input_buffer += event.unicode

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color = None):
        # store button properties and rectangle
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.current_color = color
        self.hover_color = hover_color # defaults to None


    def is_mouse_over(self, mouse_pos):
        # check if mouse is hovering over button
        is_over = self.rect.collidepoint(mouse_pos)
        if self.hover_color:
            if is_over:
                self.current_color = self.hover_color
            else:
                self.current_color = self.color
        return is_over

    def handle_click(self, mouse_pos):
        # detect left mouse button click on the button
        return self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2) # white outline
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))

        # center the text on the button
        text_rect = text_surface.get_rect(center=self.rect.center)

        # draw the text
        screen.blit(text_surface, text_rect)

class Arrow:
    def __init__(self, screen, x_pos, y_pos, start_angle=0):
        self.screen = screen
        self.image = pygame.image.load("assets/arrow.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] / 1.2 , self.image.get_size()[1] / 2))
        self.arrow_rect = self.image.get_rect(center=(x_pos, y_pos))
        self.start_angle = start_angle
        self.angle = start_angle
        self.rotation_tween = None

    def render(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.arrow_rect.center)
        self.screen.blit(rotated_image, rotated_rect.topleft)

    def rotate(self, target_angle_radians, duration):
        # convert the target angle from radians to degrees
        target_angle_degrees = math.degrees(target_angle_radians)

        # keep both angles in range [0, 360)
        current_angle = self.start_angle % 360
        target_angle = target_angle_degrees % 360

        # if the target angle is behind the current angle, add 360 to go counterclockwise
        if target_angle < current_angle:
            target_angle += 360

        # tween set up !!!
        self.rotation_tween = Tween(
            begin=current_angle,
            end=target_angle,
            duration=duration,
            easing=Easing.QUAD,
            easing_mode=EasingMode.IN,
            boomerang=False,
            loop=False,
            reps=1,
        )
        self.rotation_tween.start()

    def update(self):
        if self.rotation_tween:
            self.rotation_tween.update()
            self.angle = self.rotation_tween.value
        self.start_angle = self.angle



















# tester, to be removed
def main():
    game = GameState(3)
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()