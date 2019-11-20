# Simple pong using python 3 and pygame
# Added start screen and game over/continue screen

import pygame
import random

# For using vectors
vec = pygame.math.Vector2

TITLE = 'Simple Pong with Python 3 and Pygame'
WIDTH = 800
HEIGHT = 600
FPS = 120
FONT_NAME = 'arial'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = xpos # Used to place paddle left or right
        self.image = pygame.Surface((20,100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect() 
        
        # Position vector (x,y)
        self.pos = vec(xpos,300)
         
    def update(self):
       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and self.xpos > 700: # Player 2
            self.pos.y += 50
        if keys[pygame.K_UP] and self.xpos > 700:
            self.pos.y -= 50

        if keys[pygame.K_s] and self.xpos < 100: # Player 1
            self.pos.y += 50
        if keys[pygame.K_w] and self.xpos < 100:
            self.pos.y -= 50

        if self.pos.y <100:
            self.pos.y = 50
        if self.pos.y >500:
            self.pos.y = 550
            
        self.rect.center = self.pos


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score1 = 0
        self.score2 = 0
        
        ball_image = pygame.Surface((20, 20)) # radius x2
        pygame.draw.circle(ball_image, WHITE, (10,10), 10) # surface, color, (x,y), radius
        
        self.image = ball_image
        self.rect = self.image.get_rect() 
        
        # Position vector (x,y)
        self.pos = vec(400,300)
        self.vel = vec(20,20)
        
    def update(self):
        self.pos += self.vel
        
        # Score player2
        if self.pos.x <= 10:
            self.pos.x = 400
            self.pos.y = 300
            self.vel = vec(20,20) # resets speed if it was sped up (see game update)
            #self.vel.x *= -1
            self.score2 += 1
            
        # Score Player 1
        if self.pos.x >= 790:
            self.pos.x = 400
            self.pos.y = 300
            self.vel = vec(20,20) # Resets initial speed if sped up
            self.vel.x *= -1
            self.score1 += 1
            
        if self.pos.y <= 10 or self.pos.y >= 590:
            self.vel.y *= -1
            
        self.rect.center = self.pos
    

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)


    def new(self):
        # Start new game
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        
        self.ball = Ball()
        self.player1 = Player(50)
        self.player2 = Player(750)
        
        self.all_sprites.add(self.ball)
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)
        
        self.players.add(self.player1)
        self.players.add(self.player2)
        
        # Run new game
        self.run()


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                
                
    def update(self):
        self.all_sprites.update()

        # Paddle check and accelerate
        # Paddle 1
        hit_paddle = pygame.sprite.spritecollide(self.ball, self.players, False)
        if hit_paddle and self.ball.pos.x < 100 and self.ball.vel.x < 0: # Paddle1
            self.ball.pos.x = 70  # Does not go into paddle
            self.ball.vel.x *= -1
            # Speed up the ball
            #if self.ball.vel.x >0:
                #self.ball.vel.x += 2
            #else:
                #self.ball.vel.x -= 2

        # Paddle 2
        if hit_paddle and self.ball.pos.x > 700 and self.ball.vel.x > 0:  # Paddle2
            self.ball.pos.x = 730 # Does not go into paddle
            self.ball.vel.x *= -1
            # Speed up the ball
            #if self.ball.vel.x >0:
                #self.ball.vel.x += 2
            #else:
                #self.ball.vel.x -= 2

        # Game over if player gets to 5 points
        if self.ball.score1 ==5 or self.ball.score2 == 5:
            self.playing = False


    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text('Player A   '+str(self.ball.score1)+'  Player B   '+str(self.ball.score2),
                       36, RED, WIDTH/2, 50)
        
        pygame.display.flip()
        
    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text('Pong with Python3 and Pygame', 36, RED, WIDTH/2, HEIGHT/3)
        self.draw_text('Press any key to begin', 24, WHITE, WIDTH/2, HEIGHT/2)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text('Player A   '+str(self.ball.score1)+'  Player B   '+str(self.ball.score2),
                       36, RED, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play again", 26, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()


    def wait_for_key(self): # Wait for key press in start/game over screen
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False


    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
  
    
game = Game()
game.show_start_screen()

while game.running:
    game.new()
    game.show_go_screen()


pygame.quit()



