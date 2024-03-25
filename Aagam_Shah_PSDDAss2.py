import pygame
import os
import math
import time

pygame.init()

WIDTH, HEIGHT = 900, 550
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("F1 Racing Game")

FPS = 60
SPEED = 2.5
REVERSE_SPEED = 1
CAR_WIDTH, CAR_HEIGHT = 45, 18
LAPS_TO_WIN = 3
ANGLE = 180
FINISH_POSITION = 580, 460

show_title = True 
show_count3 = True
show_count2 = True
show_count1 = True
show_count0 = True

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'GrassBackground.jpg')), (WIDTH, HEIGHT))
TRACK = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Curcuit.png')), (WIDTH, HEIGHT))

BORDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Borders.png')), (WIDTH, HEIGHT))
BORDER_MASK = pygame.mask.from_surface(BORDER)

FINISHLINE_IMAGE = pygame.image.load(os.path.join('Assets', 'Finishline.png'))
FINISHLINE = pygame.transform.scale(FINISHLINE_IMAGE, (FINISHLINE_IMAGE.get_width(), FINISHLINE_IMAGE.get_height()))

CHECKPOINT_IMAGE = pygame.image.load(os.path.join('Assets', 'Checkpoint.png'))
CHECKPOINT = pygame.transform.scale(CHECKPOINT_IMAGE, (CHECKPOINT_IMAGE.get_width(), CHECKPOINT_IMAGE.get_height()))

TITLE = pygame.image.load(os.path.join('Assets', 'Title_Img.png'))
COUNT3 = pygame.image.load(os.path.join('Assets', 'Countdown3.png'))
COUNT2 = pygame.image.load(os.path.join('Assets', 'Countdown2.png'))
COUNT1 = pygame.image.load(os.path.join('Assets', 'Countdown1.png'))
COUNT0 = pygame.image.load(os.path.join('Assets', 'CountdownGO.png'))

BLUE_CAR = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'BLUE_CAR.png')), (CAR_WIDTH, CAR_HEIGHT)), ANGLE)
BLUE_CAR_MASK = pygame.mask.from_surface(BLUE_CAR)
RED_CAR = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'RED_CAR.png')), (CAR_WIDTH, CAR_HEIGHT)), ANGLE)
RED_CAR_MASK = pygame.mask.from_surface(RED_CAR)

RED_WIN = pygame.image.load(os.path.join('Assets', 'RedVictory.png'))
BLUE_WIN = pygame.image.load(os.path.join('Assets', 'BlueVictory.png'))


# Update positions and dimensions of finish line and checkpoint rectangles
finish_line_x = 573
finish_line_y = 440
finish_line_width = FINISHLINE_IMAGE.get_width()
finish_line_height = FINISHLINE_IMAGE.get_height()

checkpoint_x = 220
checkpoint_y = 0
checkpoint_width = CHECKPOINT_IMAGE.get_width()
checkpoint_height = CHECKPOINT_IMAGE.get_height()

# Create finish line and checkpoint rectangles
FINISH_LINE_RECT = pygame.Rect(finish_line_x, finish_line_y, finish_line_width, finish_line_height)
CHECK_POINT_RECT = pygame.Rect(checkpoint_x, checkpoint_y, checkpoint_width, checkpoint_height)


class FinishLineTrigger:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)


class CheckPointTrigger:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)


def check_lap_complete(player1, player2):
    if CHECK_POINT_RECT.colliderect(player1.rect) and not player1.crossed_checkpoint:
        player1.crossed_checkpoint = True 
    if CHECK_POINT_RECT.colliderect(player2.rect) and not player2.crossed_checkpoint:
        player2.crossed_checkpoint = True 

    if player1.crossed_checkpoint == True and FINISH_LINE_RECT.colliderect(player1.rect):
        player1.laps += 1
        player1.crossed_finish_line = False
        player1.crossed_checkpoint = False  # Reset checkpoint flag
        # print("Player 1 completed a lap")
    if player2.crossed_checkpoint == True and FINISH_LINE_RECT.colliderect(player2.rect):
        player2.laps += 1
        player2.crossed_finish_line = False
        player2.crossed_checkpoint = False  # Reset checkpoint flag
        # print("Player 2 completed a lap")


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
        self.laps = 0
        self.crossed_finish_line = False
        self.crossed_checkpoint = False
        # Initialize mask attribute with the mask of the car image
        self.mask = pygame.mask.from_surface(self.color)


    def move(self, keys_pressed):
        if keys_pressed[pygame.K_ESCAPE]:
            pygame.quit()
            os._exit()

        # Ensure the player stays within the screen boundaries
        if self.x < 0:  # Left boundary
            self.x = 0
        elif self.x > WIDTH - CAR_WIDTH:  # Right boundary
            self.x = WIDTH - CAR_WIDTH
        if self.y < 0:  # Top boundary
            self.y = 0
        elif self.y > HEIGHT - CAR_HEIGHT:  # Bottom boundary
            self.y = HEIGHT - CAR_HEIGHT

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
        self.x += self.speed * math.cos(angle_radians)
        self.y -= self.speed * math.sin(angle_radians)

        # Update the rect attribute with new position
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
    global show_title
    global show_count3
    global show_count2
    global show_count1
    global show_count0
    
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(TRACK, (0, 0))
    WIN.blit(BORDER, (0, 0))
    WIN.blit(FINISHLINE, (580, 460))
    WIN.blit(CHECKPOINT, (checkpoint_x, checkpoint_y))

    if show_title:  # Start showing the title for 5 seconds
        WIN.blit(TITLE, (0, 0))
        pygame.display.update()  # Update the display to show the title
        time.sleep(5)
        show_title = False  # Stop showing the title after 5 seconds
    elif show_count3:  
        WIN.blit(COUNT3, (0, 0))
        pygame.display.update()  
        time.sleep(1)
        show_count3 = False
    elif show_count2:  
        WIN.blit(COUNT2, (0, 0))
        pygame.display.update()  
        time.sleep(1)
        show_count2 = False  
    elif show_count1:  
        WIN.blit(COUNT1, (0, 0))
        pygame.display.update()  
        time.sleep(1)
        show_count1 = False  
    elif show_count0:  
        WIN.blit(COUNT0, (0, 0))
        pygame.display.update()  
        time.sleep(1)
        show_count0 = False  

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
            # print("Blue Collision")
            if player1.speed > 0:  # If car is moving forward
                player1.speed -= SPEED*2
                #time.sleep(1)
            else:
                player1.speed += SPEED*1.5
                #time.sleep(1)

        if BORDER_MASK.overlap(RED_CAR_MASK, (posR[0], posR[1])):
            # print("Red Collision")
            if player2.speed > 0:  # If car is moving forward
                player2.speed -= SPEED*2
                #time.sleep(1)
            else:
                player2.speed += SPEED*1.5
                #time.sleep(1)

        if BLUE_CAR_MASK.overlap(RED_CAR_MASK, (posR[0] - posB[0], posR[1] - posB[1])):
            # print("Red car collision")
            if player2.speed > 0:  # If car is moving forward
                player2.speed -= SPEED
                #time.sleep(1)
            else:
                player2.speed += REVERSE_SPEED
                #time.sleep(1)
            if BLUE_CAR_MASK.overlap(BORDER_MASK, (posB[0], posB[1])):
                # print("Blue Collision")
                if player1.speed > 0:  # If car is moving forward
                    player1.speed -= SPEED*3
                    #time.sleep(1)
                else:
                    player1.speed += SPEED*2.5
                    #time.sleep(1)

        if RED_CAR_MASK.overlap(BLUE_CAR_MASK, (posB[0] - posR[0], posB[1] - posR[1])):
            # print("Blue car collision")
            if player1.speed > 0:  # If car is moving forward
                player1.speed -= SPEED
                #time.sleep(1)
            else:
                player1.speed += REVERSE_SPEED
                #time.sleep(1)
            if RED_CAR_MASK.overlap(BORDER_MASK, (posR[0], posR[1])):
                # print("Red Collision")
                if player2.speed > 0:  # If car is moving forward
                    player2.speed -= SPEED*3
                    #time.sleep(1)
                else:
                    player2.speed += SPEED*2.5
                    # time.sleep(1)

        player1.move(keys_pressed)
        player2.move(keys_pressed)

        # Call check_lap_complete function for both players
        check_lap_complete(player1, player2)

        draw_window(player1, player2)

        clock.tick(FPS)

        # Check for game completion based on laps
        if player1.laps >= LAPS_TO_WIN:
            WIN.blit(BLUE_WIN, (0, 0))
            pygame.display.update()
            time.sleep(7)
            return
        if player2.laps >= LAPS_TO_WIN:
            WIN.blit(RED_WIN, (0, 0))
            pygame.display.update()  
            time.sleep(7)
            return

if __name__ == '__main__':
    main()
