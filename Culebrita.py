import pygame
from pygame.math import Vector2
import random

WIDTH = 800
HEIGHT = 600




BLACK = (0, 0, 0)

pygame.init()
pygame.font.init()
pygame.mixer.init()

SCORE_TEXT = pygame.font.SysFont("serif",15)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DogSnaky")
clock = pygame.time.Clock()

background_image = pygame.image.load("assets/fondo.jpg")  # Asegúrate de tener la imagen "background.jpg" en tu directorio
pygame.mixer.music.load("assets/musica.mp3")
pygame.mixer.music.set_volume(0.2)

eat_sound = pygame.mixer.Sound("assets/morder.mp3")

def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, (255, 255, 255))
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def show_game_over():
    draw_text(screen, "DogSnaky",60, WIDTH//2, HEIGHT//5)
    draw_text(screen, "Instrucciones",27, WIDTH//2, HEIGHT//3)
    draw_text(screen, "Press A Key",20, WIDTH//2, HEIGHT//2)
    pygame.display.flip()
    waitting = True
    clock.tick(60)
    while waitting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waitting = False

class Snake:
    def __init__(self):
        self.body = [Vector2(200, 200), Vector2(200, 220), Vector2(200, 240)]
        self.direction = Vector2(0, -20)
        self.image = pygame.image.load("assets/cabeza.png").convert()
        self.image.set_colorkey(BLACK)
        self.add = False

    def draw(self):
        for bloque in self.body:
            screen.blit(self.image, (bloque.x, bloque.y))
            
    def move(self):
        
        if self.add == True:
            body_copy = self.body
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body = body_copy[:]
            self.add = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body = body_copy[:]
        
        
    def move_up(self):
        self.direction = Vector2(0, -20)
        
    def move_down(self):
        self.direction = Vector2(0, 20)
        
    def move_right(self):
        self.direction = Vector2(20, 0)
        
    def move_left(self):
        self.direction = Vector2(-20, 0)
        
    def die(self):
        if self.body[0].x >= WIDTH-80 or self.body[0].y >= HEIGHT-80 or self.body[0].x < 80 or self.body[0].y < 80:
            return True
        
        for i in self.body[1:]:
            if self.body[0] == i:
                return True
            
            
class Food:
    def __init__(self):
        self.generate()
        self.image = pygame.image.load("assets/rana.png").convert()
        self.image.set_colorkey(BLACK)
    
    
    def generate(self):
        self.x = random.randrange(100/20,(WIDTH-100)/20)
        self.y = random.randrange(100/20,(HEIGHT-100)/20)
        self.pos = Vector2(self.x*20,self.y*20)
        
    def draw(self):
        screen.blit(self.image, (self.pos.x, self.pos.y))
        
    def checkColition(self,snake):
        if snake.body[0] == self.pos:
            eat_sound.play()
            self.generate()
            snake.add = True
            return True
        
        for block in snake.body[1:]:
            if block == self.pos:
                self.generate()
        
        return False
            
            
        
def main():
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.05)

    game_over = True
    running = True
    fps = 3
    
    while running:
        if game_over:
            show_game_over()
            game_over = False
            snake = Snake()
            food = Food()
            score = 0   
            
        
        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    fps=5
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    fps=10
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    fps=15
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_4:
                    fps=20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_5:
                    fps=25
            
            if event.type == pygame.KEYDOWN and snake.direction.y != 20:
                if event.key == pygame.K_UP:
                    snake.move_up()
            if event.type == pygame.KEYDOWN and snake.direction.y != -20:
                if event.key == pygame.K_DOWN:
                    snake.move_down()
            if event.type == pygame.KEYDOWN and snake.direction.x != -20:
                if event.key == pygame.K_RIGHT:
                    snake.move_right()
            if event.type == pygame.KEYDOWN and snake.direction.x != 20:
                if event.key == pygame.K_LEFT:
                    snake.move_left()
            
            
            

        clock.tick(fps)
        
        screen.blit(background_image, (0, 0))
        snake.draw()
        food.draw()
        snake.move()
        
        if snake.die():
            game_over = True

            
        if food.checkColition(snake):
            score =+ 1
        
        text = SCORE_TEXT.render("Score: {}".format(score),1,(255,255,255))
        screen.blit(text, (400 - text.get_width()/2,30))
        
        pygame.display.flip()

main()
