import pygame, sys, random
from pygame import Vector2
import time as t

#Make the ball faster --> Next and last step.

pygame.init()

screen_width = 700
screen_height = 600

game_font = pygame.font.Font('fonts/game-font.ttf', 20)
restart_font  = pygame.font.Font('fonts/game-font.ttf', 15) #Import the restart game font (this only change the size).
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong Game - By Feduski :)') #This is the caption of the window.
clock = pygame.time.Clock() #We create a clock object 
SCREEN_UPDATE = pygame.USEREVENT #Every time that there is an event.
pygame.time.set_timer(SCREEN_UPDATE, 90) #Each 90 miliseconds, the screen updates. 

#soccer_ball = pygame.transform.scale(pygame.image.load('graphics/ball.png').convert_alpha(),(25,25)) 

class PLAYER:
    def __init__(self, name, score_pos): #Score pos must be a pos (x,y)
        self.score = 0
        self.name = name
        self.score_pos  = score_pos

    def draw_score(self): #1 Score per player.
        score_text = 'Score ' + self.name + ": " + str(self.score) #We call the text of our score, converting it on STRING.
        score_surface = game_font.render(score_text, True, (51,0,102)) #Creates the surface of the score.
        score_rect = score_surface.get_rect(center = self.score_pos) #Creates the rect of the score, to give it a position.
        screen.blit(score_surface, score_rect) #Puts the score on the screen.

class BOARD:
    def __init__(self, x):
        self.x, self.y = x, screen_height / 2 - 35
        self.pos = Vector2(self.x, self.y) #Initialization pos. X depends if it is right or left board, the y, is the same on both.
        self.size = Vector2(10, 70) #The size of the board
        self.board = pygame.Rect(self.pos, self.size) #Creating the rect to represent the board.

    def draw_board(self):
        pygame.draw.rect(screen, (200,2,11), self.board)

    def move_up(self): #It function is called when we press the up / w key 
        if not self.board.top <= 10: #If not in the limit of the map
            self.board.top += -20 #Moving it up

    def move_down(self): #It function is called when we press the down / s key 
        if not self.board.bottom >= (screen_height - 20): #If not in the limit of the map
            self.board.bottom += 20 #Moving it down

class BALL:
    def __init__(self):
        self.size = Vector2(15,15)
        self.movement = 7
        self.spawn_ball()

    def spawn_ball(self):
        self.x = screen_width/2 - 7.5
        self.y = screen_height/2 - 7.5 
        self.pos = Vector2(self.x, self.y) #Initializes the ball in the middle of the screen
        self.ball_object = pygame.Rect(self.pos, self.size)
        random_direction = random.choice((1,-1))
        random_direction2 = random.choice((1,-1))
        self.direction = Vector2(self.movement * random_direction, self.movement * random_direction2)

    def draw_ball(self):
        pygame.draw.ellipse(screen, (22,242,22), self.ball_object)

    def move_ball(self):
        self.ball_object.center += self.direction

    def screen_collision(self): #This keeps the ball in the margins of the screen  
        if self.ball_object.top >= (screen_height - 20) or self.ball_object.bottom <= 10: 
            self.direction.y *= -1

    def goal(self):
        if self.ball_object.right >= 720: #If hits the right border
            main.player1.score += 1
            self.spawn_ball() #Re-spawn the ball
        elif self.ball_object.left <= -20: #If hits the left border
            main.player2.score += 1
            self.spawn_ball()

        if main.player1.score >= 3 or main.player2.score >= 3:
            self.winner = 'Player 1' if main.player1.score >= 3 else 'Player 2' #Defines the winner
            main.play = False #Ends the game

class MAIN:
    def __init__(self):
        self.player1 = PLAYER('Player 1', (175,20)) #Starting player 1
        self.player2 = PLAYER('Player 2', (525,20)) #Starting player 2       
        self.board1 = BOARD(15) #Starting board 1     
        self.board2 = BOARD(670) #Starting board 1     
        self.ball = BALL() #Starting ball
        self.play = True #This help us to stop/play some methods

    def update(self):
        self.draw_elements() 
        if self.play: #This prevent innecesary processes in case that the game has ended
            self.ball.screen_collision()
            self.ball.goal()
            self.ball.move_ball()
            self.check_collision()

    def check_collision(self):
        if self.ball.ball_object.colliderect(self.board1.board) or self.ball.ball_object.colliderect(self.board2.board):
            print(self.ball.direction)
            self.ball.direction.x *= -1 #Invert the direction
            self.ball.movement = self.ball.movement + (self.ball.movement * 12) / 100 #We increase the ball movement speed
            print(self.ball.direction)

    def draw_game_over(self):
        screen.fill((1, 0, 0))#We fill all the screen with a black color.
        #Sets the texts.
        go_text = 'Game Over'
        go_winner_text = f'Winner: {self.ball.winner}'
        press_r_text = 'Press R to restart'
        #Renders the texts and creates the surfaces.
        go_surface = game_font.render(go_text, True, (50,0,100))
        go_winner_surface = game_font.render(go_winner_text, True, (50,0,100)) 
        press_r_surface = restart_font.render(press_r_text, True, (255,0,100)) 
        #Creates the rect to place everything (directions) 
        go_rect = go_surface.get_rect(center = (screen_width/2, screen_height/2))
        winner_rect = go_winner_surface.get_rect(center = (screen_width/2, (screen_height/2) + 25))
        press_r_rect = press_r_surface.get_rect(center = (screen_width/2, (screen_height/2) + 45))
        #Places the texts.
        screen.blit(go_surface, go_rect)
        screen.blit(go_winner_surface, winner_rect)
        screen.blit(press_r_surface, press_r_rect)

    def draw_elements(self):
        if self.play:
            screen.fill((0, 0, 0)) #We fill all the screen with a black color.
            #Pitch lines
            pygame.draw.aaline(screen, (200,200,200), (screen_width/2,0), (screen_width/2,screen_height))
            pygame.draw.circle(screen, (200,200,200), (screen_width/2, screen_height/2), 10) 
            #All the rest of elements to draw
            self.board1.draw_board()
            self.board2.draw_board()
            self.ball.draw_ball()
            self.player1.draw_score()
            self.player2.draw_score()
        else: #Else, draw only the game over screen.
            self.draw_game_over()


main = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #If the player press the close button, it closes the windows and stops the script.
            pygame.quit() #Quit pygame.
            sys.exit() #Quit script.
        if event.type == SCREEN_UPDATE:
            main.update() #If there is an user event, update the main (check collision, etc).

        keys = pygame.key.get_pressed() #We obtain the pressed keys
        if keys[pygame.K_w]: #And depending which one is pressed, we mode the board up or down.
            main.board1.move_up()
        if keys[pygame.K_s]:
            main.board1.move_down()
        if keys[pygame.K_UP]: #Second board.
            main.board2.move_up()
        if keys[pygame.K_DOWN]:
            main.board2.move_down()
        
        if keys[pygame.K_r]:
            main.__init__() #We set all the values to default, to restart the game.
    
    main.draw_elements() #We constantly draw the elements (ball, board).
    pygame.display.update() #We constatanly update the displaying screen.
    clock.tick(60) #We set the times that the While True loop can execute in 1 second.