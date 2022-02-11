import pygame

from gameobjects.snake import Snake
from gameobjects.fruit import Fruit


class Game():
    red = (168, 66, 62)
    black = (0, 0, 0)
    tlo = (185, 180, 92)
    green = (64, 78, 30)

    def __init__(self, screen_width, screen_height, block_size):
        # INIT PYGAME
        pygame.init()

        self.game_over = False

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.block_size = block_size

        # FONT
        self.game_font = pygame.font.SysFont(None, 25)
        self.running = True

        # OKNO
        self.game_display = pygame.display.set_mode((self.screen_width, self.screen_height))



        # ZEGAR I FPS
        self.clock = pygame.time.Clock()
        self.fps = 15

        # SNAKE
        self.snake = Snake(self.game_display, self.block_size)

        # OWOC
        self.fruit = Fruit(self.screen_width, self.screen_height, self.block_size)

        # NAZWA OKNA
        pygame.display.set_caption("PYTONG") #ZMIENIĆ NAZWE




    def main_loop(self):
        while self.running:

            # GAME OVER
            if self.game_over:
                self.game_over_dialog()

            for event in pygame.event.get():
                # WYJSCIE PRZEZ X
                if event.type == pygame.QUIT:
                    self.running = False
                # eventy KeyDown, powinno działać na WASD i na strzałkach
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.turn_left()
                        break
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.turn_right()
                        break
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.turn_up()
                        break
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.turn_down()
                        break

                    # PAUZA PRZEZ ESC LUB P
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        self.pause_game()

            # SNAKE
            self.snake.move()
            # CHECK ZDERZENIA ZE SCIANA
            if self.check_collision():
                self.game_over = True

            # ZJEDZENIE OWOCU
            if self.check_fruit_collision():
                self.snake.add_segment()
                self.fruit.respawn(self.screen_width, self.screen_height, self.snake)

            # RYSOWANIE I ODSWIEZANIE
            self.game_display.fill(self.tlo)
            self.draw_fruit(self.fruit)
            self.draw_snake(self.snake)
            pygame.display.flip()
            # FPS
            self.clock.tick(self.fps)

    # ZDERZENIE ZE SCIANA CHECK
    def check_collision(self):
        if self.snake.segments[0].pos_x < 0 or \
                self.snake.segments[0].pos_x > self.screen_width - self.snake.block_size:
            return True
        if self.snake.segments[0].pos_y < 0 or \
                self.snake.segments[0].pos_y > self.screen_height - self.snake.block_size:
            return True

        # UROBOROS CHECK
        head_pos_x = self.snake.segments[0].pos_x
        head_pos_y = self.snake.segments[0].pos_y
        for s in self.snake.segments[1:]:
            if head_pos_x == s.pos_x and head_pos_y == s.pos_y:
                return True
        return False

    # ZJEDZENIE OWOCU CHECK
    def check_fruit_collision(self):
        if self.fruit.pos_y == self.snake.segments[0].pos_y and self.fruit.pos_x == self.snake.segments[0].pos_x:
            return True
        return False

    # METODA INPUT
    def put_message(self, message):
        pause_text = self.game_font.render(message, True, self.red)
        self.game_display.blit(pause_text, [self.screen_width / 2, self.screen_height / 2])

    def game_over_message(self):
        message = "KONIEC GRY, ENTER/SPACJA - KONTYNUUJ, ESC - WYJDŹ"
        pause_text = self.game_font.render(message, True, self.red)
        self.game_display.blit(pause_text, [self.screen_width / 5, self.screen_height / 2])

    # PAUZA I WYJSCIE Z NIEJ
    def pause_game(self):
        paused = True
        self.put_message("PAUZA, P/ESC - WRÓĆ DO GRY")
        pygame.display.update()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or pygame.K_p:
                        paused = False
            self.clock.tick(30)

    # GAME OVER
    def game_over_dialog(self):
        while self.game_over:
            self.game_display.fill(self.tlo)
            self.game_over_message()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.reset_game()
                        return
                    if event.key == pygame.K_ESCAPE:
                        self.exit_game()

    # RESET ZMIENNYCH DO NOWEJ GRY
    def reset_game(self):
        self.snake.reset_snake()
        self.game_over = False
        self.fruit.respawn(self.screen_width, self.screen_height, self.snake)
        pygame.display.flip()

    # RYSOWANIE SEGMENTOW PYTONA
    def draw_snake(self, snake):
        for s in self.snake.segments:
            self.game_display.fill(self.snake.color, rect=[s.pos_x, s.pos_y, snake.block_size, snake.block_size])

    #RYSOWANIE OWOCKOW
    def draw_fruit(self, fruit):
        self.game_display.fill(self.red, rect=[fruit.pos_x, fruit.pos_y, fruit.block_size, fruit.block_size])

    # WYJŚCIE
    def exit_game(self):
        pygame.quit()
        quit()