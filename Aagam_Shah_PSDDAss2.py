import pygame
import os
import math
import time
pygame.init()


WIDTH, HEIGHT = 900, 550
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("F1 Racing Game")

FPS = 60
SPEED = 3
REVERSE_SPEED = 1.5
CAR_WIDTH, CAR_HEIGHT = 45, 18
LAPS_TO_WIN = 50
ANGLE = 180
FINISH_POSITION = 580, 460

show_title = True  # Move this outside the draw_window function

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'GrassBackground.jpg')), (WIDTH, HEIGHT))
TRACK = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Curcuit.png')), (WIDTH, HEIGHT))

BORDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Borders.png')), (WIDTH, HEIGHT))
BORDER_MASK = pygame.mask.from_surface(BORDER)

FINISHLINE_IMAGE = pygame.image.load(os.path.join('Assets', 'Finishline.png'))
FINISHLINE = pygame.transform.scale(FINISHLINE_IMAGE, (FINISHLINE_IMAGE.get_width(), FINISHLINE_IMAGE.get_height()))

TITLE = pygame.image.load(os.path.join('Assets', 'Title_Img.png'))

BLUE_CAR = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'BLUE_CAR.png')), (CAR_WIDTH, CAR_HEIGHT)), ANGLE)
BLUE_CAR_MASK = pygame.mask.from_surface(BLUE_CAR)
RED_CAR = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'RED_CAR.png')), (CAR_WIDTH, CAR_HEIGHT)), ANGLE)
RED_CAR_MASK = pygame.mask.from_surface(RED_CAR)


class FinishLineTrigger:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)


def check_lap_complete(player1, player2):
    finish_line_x = 580  # X-coordinate of the finish line
    finish_line_y = 460  # Y-coordinate of the finish line
    finish_line_width = FINISHLINE.get_width()  # Width of the finish line
    finish_line_height = FINISHLINE.get_height()  # Height of the finish line

    # Calculate the coordinates of the finish line rectangle
    FINISH_LINE_RECT = pygame.Rect(finish_line_x, finish_line_y, finish_line_width, finish_line_height)

    # Check if the player has crossed the finish line completely
    if pygame.Rect.colliderect(FINISH_LINE_RECT, player1.rect):
        player1.laps += 1
        player1.crossed_finish_line = True
    if pygame.Rect.colliderect(FINISH_LINE_RECT, player2.rect):
        player2.laps += 1
        player2.crossed_finish_line = True

    # Reset crossed_finish_line flag if player is not colliding with finish line
    if not FINISH_LINE_RECT.colliderect(player1.rect):
        player1.crossed_finish_line = False
    if not FINISH_LINE_RECT.colliderect(player2.rect):
        player2.crossed_finish_line = False


class Player:
    acceleration = 0.1
    deceleration = 0.05

    def draw(self):
        rotated_car = pygame.transform.rotate(self.color, self.angle)
        rect = rotated_car.get_rect(center=self.rect.center)
        WIN.blit(rotated_car, rect.topleft)


    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.color = color
        self.controls = controls
        self.rect = self.color.get_rect(topleft=(self.x, self.y))
        self.angle = 180
        self.speed = 0
        self.laps = -1
        self.crossed_finish_line = False


    def move(self, keys_pressed):
        if self.controls == "player1":
            if keys_pressed[pygame.K_w]:
                self.speed += self.acceleration
                if self.speed > SPEED:
                    self.speed = SPEED
            elif keys_pressed[pygame.K_s]:
                self.speed -= self.acceleration
                if self.speed < -REVERSE_SPEED:
                    self.speed = -REVERSE_SPEED
            else:
                if self.speed > 0:
                    self.speed -= self.deceleration
                    if self.speed < 0:
                        self.speed = 0
                elif self.speed < 0:
                    self.speed += self.deceleration
                    if self.speed > 0:
                        self.speed = 0

            if keys_pressed[pygame.K_a]:
                self.angle += 5
            if keys_pressed[pygame.K_d]:
                self.angle -= 5

        elif self.controls == "player2":
            if keys_pressed[pygame.K_UP]:
                self.speed += self.acceleration
                if self.speed > SPEED:
                    self.speed = SPEED
            elif keys_pressed[pygame.K_DOWN]:
                self.speed -= self.acceleration
                if self.speed < -REVERSE_SPEED:
                    self.speed = -REVERSE_SPEED
            else:
                if self.speed > 0:
                    self.speed -= self.deceleration
                    if self.speed < 0:
                        self.speed = 0
                elif self.speed < 0:
                    self.speed += self.deceleration
                    if self.speed > 0:
                        self.speed = 0

            if keys_pressed[pygame.K_LEFT]:
                self.angle += 5
            if keys_pressed[pygame.K_RIGHT]:
                self.angle -= 5

        # Convert angle to radians before using in trigonometric functions
        angle_radians = math.radians(self.angle)

        # Move the player
        new_x = self.x + self.speed * math.cos(angle_radians)
        new_y = self.y - self.speed * math.sin(angle_radians)

        # Check if the new position is within the screen boundaries
        if 0 <= new_x <= WIDTH - CAR_WIDTH and 0 <= new_y <= HEIGHT - CAR_HEIGHT:
            self.x = new_x
            self.y = new_y

        self.rect.topleft = (self.x, self.y)

    def get_pos(self):
        x = self.x
        y = self.y
        return x, y


def handle_input(event):
    global selected_option

    if event.type:
        selected_option = ""


# The Draw the background
def draw_window(player1, player2):
    global show_title  # Add this line to access the global variable
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(TRACK, (0, 0))
    WIN.blit(BORDER, (0, 0))
    WIN.blit(FINISHLINE, (580, 460))

    # start_time = pygame.time.get_ticks()  # Get the current time

    # if show_title:  
    #     WIN.blit(TITLE, (0, 0))
    #     pygame.display.update()  # Update the display to show the title

    #     if pygame.time.get_ticks() - start_time <= 5000:  # Check if 5 seconds have elapsed
    #         return
    #     else:
    #         show_title = False  # Stop showing the title after 5 seconds

    # pygame.draw.line(WIN, (255, 255, 255), (600, 459), (610, 550), 1)  # Finish line
    player1.draw()
    player2.draw()

    # Display laps completed for player 1 in the top left corner
    font = pygame.font.Font(None, 36)
    text = font.render(f"Player 1: {player1.laps} laps", True, (0, 80, 189))
    WIN.blit(text, (10, 10))

    # Display laps completed for player 2 in the top right corner
    text = font.render(f"Player 2: {player2.laps} laps", True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.right = WIDTH - 10
    text_rect.top = 10
    WIN.blit(text, text_rect)

    pygame.display.update()


# Main code for my Game
def main():
    clock = pygame.time.Clock()
    player1 = Player(610, 480, BLUE_CAR, "player1")
    player2 = Player(610, 520, RED_CAR, "player2")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            else:
                handle_input(event)

        keys_pressed = pygame.key.get_pressed()

        # Check for collisions and apply penalties
        posB = player1.get_pos()  # Get location of the Blue Car at any given point in time
        posR = player2.get_pos()  # Get location of the Red Car at any given point in time
        if BORDER_MASK.overlap(BLUE_CAR_MASK, (posB[0], posB[1])):
            print("Blue Collision")
            if player1.speed > 0:  # If car is moving forward
                player1.speed -= SPEED
                time.sleep(1)
            else:
                player1.speed -= REVERSE_SPEED
                time.sleep(1)
            player1 -= 5  # Move the car slightly away from the border

        if BORDER_MASK.overlap(RED_CAR_MASK, (posR[0], posR[1])):
            print("Red Collision")
            if player2.speed > 0:  # If car is moving forward
                player2.speed -= SPEED
                time.sleep(1)
            else:
                player2.speed -= REVERSE_SPEED
                time.sleep(1)
            

        player1.move(keys_pressed)
        player2.move(keys_pressed)

        # Call check_lap_complete function for both players
        check_lap_complete(player1, player2)

        player1.crossed_finish_line = False  # Reset finish line flag for player 1
        player2.crossed_finish_line = False  # Reset finish line flag for player 2

        draw_window(player1, player2)

        clock.tick(FPS)

        # Check for game completion based on laps
        if player1.laps >= LAPS_TO_WIN:
            print("Player 1 wins!")
            print(f"Player 1 completed {player1.laps} laps.")
            main
            return
        elif player2.laps >= LAPS_TO_WIN:
            print("Player 2 wins!")
            print(f"Player 2 completed {player2.laps} laps.")
            main
            return


# Start the game
if __name__ == "__main__":
    main()
