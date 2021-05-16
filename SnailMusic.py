import pygame, sys
from pygame.locals import *
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

pygame.display.set_caption('Snail Music')

font1 = pygame.font.SysFont("pkmnrs.ttf", 24)
font2 = pygame.font.SysFont("pkmnrs.ttf", 28)

clock = pygame.time.Clock()

WIDTH = 350
HEIGHT = 600
WINDOW_SIZE = (WIDTH, HEIGHT)

DISPLAY_WIDTH = 175
DISPLAY_HEIGHT = 300
DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((DISPLAY_SIZE))

background = pygame.image.load('assets/background.png')
menu_background = pygame.image.load('assets/menu_background.png').convert()
menu_background.set_colorkey((255, 255, 255))
menu_background2 = pygame.image.load('assets/menu_background2.png').convert()
menu_background2.set_colorkey((255, 255, 255))

button1_Img = pygame.image.load('assets/button1snail.png').convert()
button1_Img.set_colorkey((255, 255, 255))
button2_Img = pygame.image.load('assets/button2snail.png').convert()
button2_Img.set_colorkey((255, 255, 255))
button3_Img = pygame.image.load('assets/button3snail.png').convert()
button3_Img.set_colorkey((255, 255, 255))
button4_Img = pygame.image.load('assets/button4snail.png').convert()
button4_Img.set_colorkey((255, 255, 255))

note1_Img = pygame.image.load('assets/nota1.png').convert()
note1_Img.set_colorkey((255, 255, 255))
note2_Img = pygame.image.load('assets/nota2.png').convert()
note2_Img.set_colorkey((255, 255, 255))
note3_Img = pygame.image.load('assets/nota3.png').convert()
note3_Img.set_colorkey((255, 255, 255))
note4_Img = pygame.image.load('assets/nota4.png').convert()
note4_Img.set_colorkey((255, 255, 255))

note_sound = pygame.mixer.Sound('assets/notas.wav')
hurt_sound = pygame.mixer.Sound('assets/hurt.wav')

notes = []
notes_posX = [DISPLAY_WIDTH // 2 - 54, DISPLAY_WIDTH // 2 - 24, DISPLAY_WIDTH // 2 + 8, DISPLAY_WIDTH // 2 + 38]
note_Imgs = [note1_Img, note2_Img, note3_Img, note4_Img]
particles = []

timer = 0
spawnrate = 1000
global_vel = 0.1 
MAX_DIFFICULTY_SCORE = 100 #Score en el que el juego llega a su maximo spawnrate y velocidad

class Button(object):
    def __init__(self, x, image):
        self.x = x
        self.image = image
        self.y = 250

    def draw(self, display):
        display.blit(self.image, (self.x, self.y))

class Note(object):
    def __init__(self, x, y, image, vel):
        self.x = x
        self.y = y
        self.image = image
        self.vel = vel
    
    def draw(self, display):
        display.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.vel

def drawNotes():
    global lives
    for note in notes:
        note.move()
        note.draw(display)
        note.vel = global_vel + (score * (0.5 / MAX_DIFFICULTY_SCORE))
        if note.vel >= 0.5:
            note.vel = 0.5
        if note.y >= 275:
            notes.remove(note)
            hurt_sound.play()
            lives -= 1
            
def drawParticles():
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        pygame.draw.circle(display, particle[3], [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)

def drawWindow(display):
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    display.blit(background, (0, 0))
    button1.draw(display)
    button2.draw(display)
    button3.draw(display)
    button4.draw(display)
    score_text = font1.render("Score " + str(score), True, (255, 255, 255))
    display.blit(score_text, (10, 10))
    time_text = font1.render("Time " + str(int(timer)), True, (255, 255, 255))
    display.blit(time_text, (10, 30))
    lives_text = font1.render("Lives " + str(lives), True, (255, 255, 255))
    display.blit(lives_text, (10, 50))

    drawNotes()
    drawParticles()
    pygame.display.update() 

def game():
    global score
    global lives
    global time_since_spawn
    global timer
    global button1 
    global button2
    global button3
    global button4
    global survival_time
    score = 0
    lives = 50
    time_since_spawn = 0
    notes.clear()

    timer = 0

    soundtrack = pygame.mixer.music.load('assets/soundtrack1.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.050)

    pygame.time.set_timer(USEREVENT+1, 1000)

    running = True

    while running:
        button1 = Button(DISPLAY_WIDTH // 2 - 54, button1_Img)
        button2 = Button(DISPLAY_WIDTH // 2 - 24, button2_Img)
        button3 = Button(DISPLAY_WIDTH // 2 + 8, button3_Img)
        button4 = Button(DISPLAY_WIDTH // 2 + 38, button4_Img)

        dt = clock.tick(1000)
        time_since_spawn += dt 
        spawnrate = 1000 - (score * (800 / MAX_DIFFICULTY_SCORE))
        if spawnrate <= 200:
            spawnrate = 200
        if time_since_spawn >= spawnrate:
            note_index = random.randint(0, 3)
            notes.append(Note(int(notes_posX[note_index]), 10, note_Imgs[note_index], global_vel))
            time_since_spawn = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if notes:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_q:
                        if button1.x == notes[0].x and notes[0].y >= 240 and notes[0].y <= 265:
                            note_sound.play()
                            score += 1
                            for i in range(20):
                                particles.append([[button1.x + 10, button1.y + 10], [random.uniform(-1, 1), random.uniform(-1, 1)], 6, [255, 0, 0]])
                            notes.remove(notes[0])
                        else:
                            hurt_sound.play()
                            lives -= 1
                    if event.key == K_w:
                        if button2.x == notes[0].x and notes[0].y > 240 and notes[0].y < 265:
                            note_sound.play()
                            score += 1
                            for i in range(20):
                                particles.append([[button2.x + 10, button2.y + 10], [random.uniform(-1, 1), random.uniform(-1, 1)], 6, [0, 0 , 255]])
                            notes.remove(notes[0])
                        else:
                            hurt_sound.play()
                            lives -= 1
                    if event.key == K_e:
                        if button3.x == notes[0].x and notes[0].y > 240 and notes[0].y < 265:
                            note_sound.play()
                            score += 1
                            for i in range(20):
                                particles.append([[button3.x + 10, button3.y + 10], [random.uniform(-1, 1), random.uniform(-1, 1)], 6, [0, 255 , 0]])
                            notes.remove(notes[0])  
                        else:
                            hurt_sound.play() 
                            lives -= 1 
                    if event.key == K_r:
                        if button4.x == notes[0].x and notes[0].y > 240 and notes[0].y < 265:
                            note_sound.play()
                            score += 1
                            for i in range(20):
                                particles.append([[button4.x + 10, button4.y + 10], [random.uniform(-1, 1), random.uniform(-1, 1)], 6, [255, 255 , 0]])
                            notes.remove(notes[0])
                        else:
                            hurt_sound.play()
                            lives -= 1
            if event.type == USEREVENT+1:
                timer += 1

        if lives <= 0:
            pygame.mixer.music.stop()
            survival_time = int(timer)
            gameOver()
            soundtrack = pygame.mixer.music.load('assets/menu_soundtrack.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(1)
            running = False

        drawWindow(display)

            


def drawGameOver(display):
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    display.fill((0, 0, 0))
    game_over_text = font2.render("GAME OVER", True, (255, 255, 255))
    display.blit(game_over_text, (DISPLAY_WIDTH // 2 - game_over_text.get_width() // 2, 80))
    score_text = font1.render("Score " + str(score), True, (255, 255, 255))
    display.blit(score_text, (DISPLAY_WIDTH // 2 - score_text.get_width() // 2, 120))
    survival_time_text = font1.render("Time " + str(survival_time), True, (255, 255, 255))
    display.blit(survival_time_text, (DISPLAY_WIDTH // 2 - survival_time_text.get_width() // 2, 140))
    pygame.display.update()

def gameOver():
    game_over = True
    global lives
    global score
    while game_over:
        drawGameOver(display)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    game_over = False


def drawMenu(display):
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    display.fill((0, 0, 0))
    display.blit(menu_background, (0, 30))
    display.blit(menu_background2, (0, 175))
    start_text = font2.render("START GAME", True, (255, 255, 255))
    display.blit(start_text, (DISPLAY_WIDTH // 2 - start_text.get_width() // 2, 155))
    drawParticles()
    pygame.display.update()

soundtrack = pygame.mixer.music.load('assets/menu_soundtrack.mp3')
pygame.mixer.music.play(-1)
while True:

    mx, my = pygame.mouse.get_pos()
    if len(particles) < 50:
        particles.append([[mx / 2, my / 2], [random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)], 6, [255, 255, 0]])
    

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                particles.clear()
                game()
    drawMenu(display)
    