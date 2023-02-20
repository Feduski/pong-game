import pygame, sys, random
from pygame import Vector2
import time as t

#New Feduski 2023: 
#Make the ball faster
#Endgame // finished 02/20/23
#Restart // finished 02/20/23
#Player wons // finished 02/20/23


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

    def draw_score(self):
        score_text = 'Score ' + self.name + ": " + str(self.score) #We call the text of our score, converting it on STRING.
        score_surface = game_font.render(score_text, True, (51,0,102)) #Creates the surface of the score.
        #score_x = int(cell_size * cell_number - 60) #Puts an X coord, -60 to place it far from the border.
        #score_y = int(cell_size * cell_number - 610) #Puts and Y coord, -40 to place it far from the border.
        score_rect = score_surface.get_rect(center = self.score_pos) #Creates the rect of the score, to give it a position.
        screen.blit(score_surface, score_rect) #Puts the score on the screen.

class BOARD:
    def __init__(self, x):
        self.x, self.y = x, screen_height / 2 - 35
        self.pos = Vector2(self.x, self.y)
        self.size = Vector2(10, 70)
        self.board = pygame.Rect(self.pos, self.size)

    def draw_board(self):
        pygame.draw.rect(screen, (200,2,11), self.board)

    def move_up(self):
        if not self.board.top <= 10:
            self.board.top += -20

    def move_down(self):
        if not self.board.bottom >= (screen_height - 20):
            self.board.bottom += 20

class BALL:
    def __init__(self):
        self.size = Vector2(15,15)
        self.x_movement = 30
        self.y_movement = 30
        self.spawn_ball()

    def spawn_ball(self):
        self.x = screen_width/2 - 7.5
        self.y = screen_height/2 - 7.5
        self.pos = Vector2(self.x, self.y)
        self.ball = pygame.Rect(self.pos, self.size)
        random_direction = random.choice((1,-1))
        self.direction = Vector2(self.x_movement * random_direction,self.y_movement* random_direction)

    def draw_ball(self):
        pygame.draw.ellipse(screen, (22,242,22), self.ball)

    def move_ball(self):
        self.ball.center += self.direction

    def screen_collision(self):
        if self.ball.top >= (screen_height - 20) or self.ball.bottom <= 10: #use the first part estructure (more flexible)
            self.direction.y *= -1

    def goal(self):
        if self.ball.right >= 720:
            main.player1.score += 1
            self.x_movement = 30
            self.y_movement = 30
            self.spawn_ball()
        elif self.ball.left <= -20:
            main.player2.score += 1
            self.x_movement = 30
            self.y_movement = 30
            self.spawn_ball()

        if main.player1.score >= 1 or main.player2.score >= 1:
            self.winner = 'Player 1' if main.player1.score >= 1 else 'Player 2'
            print('Game Over')
            main.play = False


class MAIN:
    def __init__(self):
        self.player1 = PLAYER('Player 1', (175,20))
        self.player2 = PLAYER('Player 2', (525,20))        
        self.board1 = BOARD(15)
        self.board2 = BOARD(670)
        self.ball = BALL()
        self.play = True

    def update(self):
        self.draw_elements()
        if self.play:
            self.ball.screen_collision()
            self.ball.goal()
            self.ball.move_ball()
            self.check_collision()

    def check_collision(self):
        if self.ball.ball.colliderect(self.board1.board) or self.ball.ball.colliderect(self.board2.board):
            print(self.ball.direction)
            self.ball.direction.x *= -1
            self.ball.y_movement += (self.ball.y_movement * 12) / 100
            self.ball.x_movement += (self.ball.x_movement * 12) / 100
            print(self.ball.direction)

    def draw_game_over(self):
        #Sets the texts.
        screen.fill((1, 0, 0))#We fill all the screen with a light green color.

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
            screen.fill((0, 0, 0))#We fill all the screen with a light black color.
            pygame.draw.aaline(screen, (200,200,200), (screen_width/2,0), (screen_width/2,screen_height))
            pygame.draw.circle(screen, (200,200,200), (screen_width/2, screen_height/2), 10) #Pitch lines
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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            main.board1.move_up()
        if keys[pygame.K_s]:
            main.board1.move_down()
        if keys[pygame.K_UP]:
            main.board2.move_up()
        if keys[pygame.K_DOWN]:
            main.board2.move_down()
        
        if keys[pygame.K_r]:
            main.__init__() #We set all the values to default, to restart the game.
    
    main.draw_elements() #We constantly draw the elements (ball, board).
    pygame.display.update() #We constatanly update the displaying screen.
    clock.tick(60) #We set the times that the While True loop can execute in 1 second.