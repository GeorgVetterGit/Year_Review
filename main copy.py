import pygame
import numpy as np
import asyncio

HEIGHT = 720
WIDTH = 1280
AST_VEL = 10
SHIP_VEL = 12
MONTH_VEL = 4

pygame.init()
clock = pygame.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Year Review')

path_first = 'assets/'

PATH_SPACESHIP = path_first + 'pictures/spaceship.png'
IMG_SPACESHIP = pygame.image.load(PATH_SPACESHIP).convert_alpha()
IMG_SPACESHIP = pygame.transform.scale(IMG_SPACESHIP,(70,70))

PATH_ASTEROID = path_first + 'pictures/asteroid.png'
IMG_ASTEROID = pygame.image.load(PATH_ASTEROID).convert_alpha()
IMG_ASTEROID = pygame.transform.scale(IMG_ASTEROID,(70,70))
IMG_ASTEROID = pygame.transform.rotate(IMG_ASTEROID,45)
ICON_ASTEROID = pygame.transform.scale(IMG_ASTEROID,(30,30))

PATH_HIGHLIGHT = path_first + 'pictures/highlight.png'
IMG_HIGHLIGHT = pygame.image.load(PATH_HIGHLIGHT).convert_alpha()
IMG_HIGHLIGHT = pygame.transform.scale(IMG_HIGHLIGHT,(70,70))
ICON_HIGHLIGHT = pygame.transform.scale(IMG_HIGHLIGHT,(30,30))

PATH_LOWLIGHT = path_first + 'pictures/bomb.png'
IMG_LOWLIGHT = pygame.image.load(PATH_LOWLIGHT).convert_alpha()
IMG_LOWLIGHT = pygame.transform.scale(IMG_LOWLIGHT,(70,70))
ICON_LOWLIGHT = pygame.transform.scale(IMG_LOWLIGHT,(30,30))

PATH_BG = path_first + 'pictures/BG.jpg'
BG_IMG = pygame.image.load(PATH_BG)
BG_IMG = pygame.transform.scale(BG_IMG,(WIDTH,HEIGHT))

COLORS = {'BLACK': (0, 0, 0),
          'WHITE': (255, 255, 255),
          'RED': (255, 0, 0),
          'GREEN': (0, 255, 0),
          'GRAY': (100, 100, 100)}

class space_ship:

    def __init__(self, IMG_SPACESHIP):
        self.x_pos = WIDTH / 2
        self.y_pos = HEIGHT - 150
        self.rect = pygame.FRect(0, 0, 50, 50)
        self.rect.center = (self.x_pos, self.y_pos)
        pass

    def move(self, direction):
        if direction == 'up':
            self.y_pos = max(self.y_pos - SHIP_VEL, 0 + 20)
        elif direction == 'down':
            self.y_pos = min(self.y_pos + SHIP_VEL, HEIGHT - 70)
        elif direction == 'left':
            self.x_pos = max(self.x_pos - SHIP_VEL, 0)
        elif direction == 'right':
            self.x_pos = min(self.x_pos + SHIP_VEL, WIDTH - 45)
        self.rect.center = (self.x_pos, self.y_pos)
        return None

    def shoot(self):
        return None

class asteroid():

    def __init__(self):
        self.y_pos = -100
        self.x_pos = np.random.randint(0, WIDTH)
        self.ratio = np.random.random(1)
        self.rect = pygame.FRect(0, 0, 30, 30)
        self.rect.center = (self.x_pos, self.y_pos)
        self.hit_ast = False
        pass

    def move(self):
        self.y_pos += AST_VEL
        self.x_pos = self.x_pos + (self.ratio - 0.5) * 20
        self.rect.center = (self.x_pos, self.y_pos)

class star_back():

    def __init__(self):
        self.y_pos = np.random.randint(0, HEIGHT) - HEIGHT
        self.x_pos = np.random.randint(0, WIDTH)
        self.level = np.random.randint(1, 4)
        pass

    def draw(self, screen):
        pygame.draw.circle(screen,COLORS['WHITE'],(self.x_pos, self.y_pos),self.level, self.level)
        return screen
    
    def move(self):
        velocity = self.level
        self.y_pos += velocity

class month_line():

    def __init__(self, month_name):
        self.month_name = month_name
        self.y_pos = -50
        pass
    
    def move(self):
        self.y_pos += MONTH_VEL

    def draw(self, screen):
        pygame.draw.line(screen, COLORS['WHITE'],(0, self.y_pos), (WIDTH, self.y_pos), width=5)
        Month_txt = my_font.render(str(self.month_name), False, COLORS['WHITE'])
        screen.blit(Month_txt, (50, self.y_pos - 50))
        return screen

class highlight():

    def __init__(self, highlight_name):
        self.name = highlight_name
        self.y_pos = -50
        self.x_pos = np.random.randint(0 + 100, WIDTH - 100)
        self.rect = pygame.FRect(0, 0, 30, 30)
        self.rect.center = (self.x_pos, self.y_pos)
    
    def move(self):
        self.y_pos += MONTH_VEL
        self.rect.center = (self.x_pos, self.y_pos)
        pass

    def draw(self, screen, IMG_HIGHLIGHT):
        screen.blit(IMG_HIGHLIGHT, self.rect)
        rows = self.name.count('\n')
        High_txt = small_font.render(str(self.name), False, COLORS['WHITE'])
        text_rect = High_txt.get_rect(center=(self.x_pos + 20, self.y_pos + 80 + (rows * 10)))
        screen.blit(High_txt, text_rect)
        return screen

class lowlight():

    def __init__(self, lowlight_name):
        self.name = lowlight_name
        self.y_pos = -50
        self.x_pos = np.random.randint(0 + 100, WIDTH - 100)
        self.rect = pygame.FRect(0, 0, 30, 30)
        self.rect.center = (self.x_pos, self.y_pos)
    
    def move(self):
        self.y_pos += MONTH_VEL
        self.rect.center = (self.x_pos, self.y_pos)
        pass

    def draw(self, screen, IMG_LOWLIGHT):
        screen.blit(IMG_LOWLIGHT, self.rect)
        High_txt = small_font.render(str(self.name), False, COLORS['WHITE'])
        text_rect = High_txt.get_rect(center=(self.rect.centerx, self.y_pos - 80))
        screen.blit(High_txt, text_rect)
        return screen

player = space_ship(IMG_SPACESHIP)
score = 0

stars = [star_back() for i in range(30)]
asteroids = [asteroid()]

my_font = pygame.font.SysFont('Consolas', 45)
small_font = pygame.font.SysFont('Consolas', 20)
title_font = pygame.font.SysFont('Consolas', 70)

time = 0
hit_time = 0
high_time = 0
low_time = 0
hit_low = False
hit_high = False

title_y_pos = HEIGHT + 100

cool_down = 50
health = 100

MONTH_STEPS = 500
TIME_LIST = list(range(MONTH_STEPS, 13 * MONTH_STEPS, MONTH_STEPS))
MONTH_LIST = ['January',
              'February',
              'March',
              'April',
              'May',
              'June',
              'July',
              'August',
              'September',
              'October',
              'November',
              'December']

highlight_dict = {str(int(MONTH_STEPS * 4.5)): 'Highlight 1',
                  str(int(MONTH_STEPS * 2.5)): 'Highlight\n2',
                  str(int(MONTH_STEPS * 9.8)): 'Highlight 3',
                  str(int(MONTH_STEPS * 10.4)): 'Highlight 4',
                  str(int(MONTH_STEPS * 10.8)): 'Highlight 5',
                  str(int(MONTH_STEPS * 6.3)): 'Highlight 6',
                  str(int(MONTH_STEPS * 9.3)): 'Highlight 7',
                  str(int(MONTH_STEPS * 10.1)): 'Highlight 8'}

lowlight_dict = {str(int(MONTH_STEPS * 6.8)): 'Lowlight 1',
                 str(int(MONTH_STEPS * 11.5)): 'Lowlight 2',
                 str(int(MONTH_STEPS * 1.5)): 'Lowlight 3'}

month_dict = {str(key): value for key, value in zip(TIME_LIST, MONTH_LIST)}

def text(screen, text: str, size,x ,y):
    my_font = pygame.font.SysFont('Consolas', size)
    Title_txt = my_font.render(text, False, COLORS['WHITE'])
    text_rect = Title_txt.get_rect(center=(x, y))
    screen.blit(Title_txt, text_rect)
    return screen

def text_2(screen, text: str, size,x ,y, color):
    my_font = pygame.font.SysFont('Consolas', size)
    Title_txt = my_font.render(text, False, color)
    text_rect = Title_txt.get_rect(topleft=(x, y))
    screen.blit(Title_txt, text_rect)
    return screen

start = False
end_screen = False
game_over = False

num_hit_ast = 0
num_missed_ast = 0
high_list = []
low_list = []

running = True

async def main():
    global running, time, screen, start, end_screen, game_over, title_y_pos, health, score, IMG_SPACESHIP, IMG_ASTEROID, ICON_ASTEROID, IMG_HIGHLIGHT, ICON_HIGHLIGHT, IMG_LOWLIGHT, ICON_LOWLIGHT, BG_IMG, COLORS, player, stars, asteroids, my_font, small_font, title_font, hit_time, high_time, low_time, hit_low, hit_high, cool_down, MONTH_STEPS, highlight_dict, lowlight_dict, month_dict, num_hit_ast, num_missed_ast, high_list, low_list
    while running:
        clock.tick(60)
        time += 1

        if time > MONTH_STEPS * 13:
            end_screen = True
            start = False

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move('up')
        if keys[pygame.K_DOWN]:
            player.move('down')
        if keys[pygame.K_LEFT]:
            player.move('left')
        if keys[pygame.K_RIGHT]:
            player.move('right')
        if keys[pygame.K_SPACE]:
            start = True
            time = 0
        if keys[pygame.K_r]:
            if end_screen or game_over:
                #restart
                start = False
                end_screen = False
                game_over = False
                num_hit_ast = 0
                num_missed_ast = 0
                high_list = []
                low_list = []
                time = 0
                health = 100
                hit_time = 0
                high_time = 0
                low_time = 0
                hit_low = False
                hit_high = False
                title_y_pos = HEIGHT + 100
                score = 0

        # draw the game
        screen.fill(COLORS['BLACK'])
        screen.blit(BG_IMG, (0, 0))

        for idx, star in enumerate(stars):
            screen = star.draw(screen)
            star.move()
            if star.y_pos > HEIGHT:
                stars.pop(idx)
                stars.append(star_back())

        if not start and not end_screen and not game_over:
            title_y_pos -= MONTH_VEL

            Title_txt = title_font.render(str('YEAR REVIEW'), False, COLORS['WHITE'])
            text_rect = Title_txt.get_rect(center=(WIDTH/2, max(title_y_pos, 100)))
            screen.blit(Title_txt, text_rect)

            screen = text(screen, 'Game Control', 50, WIDTH/2, max(title_y_pos + 800, 200))

            screen = text(screen, str('Use the arrow keys and collect all the highlights.\nDodge lowlights and asteroids.\n\n\n\n\n\nPress spacebar to start.'), 30, WIDTH/2, max(title_y_pos + 1100, 500))

            icon_rect = IMG_HIGHLIGHT.get_rect(center=((WIDTH / 3) * 1 - (WIDTH / 6) + 50, max(title_y_pos + 1100, 500)))
            screen.blit(IMG_HIGHLIGHT, icon_rect)
            screen = text(screen, 'Highlight', 30, (WIDTH / 3) * 1 - (WIDTH / 6) + 50, max(title_y_pos + 1150, 550))

            icon_rect = IMG_LOWLIGHT.get_rect(center=((WIDTH / 3) * 2 - (WIDTH / 6), max(title_y_pos + 1100, 500)))
            screen.blit(IMG_LOWLIGHT, icon_rect) 
            screen = text(screen, 'Lowlight', 30, (WIDTH / 3) * 2 - (WIDTH / 6), max(title_y_pos + 1150, 550))

            icon_rect = IMG_ASTEROID.get_rect(center=((WIDTH / 3) * 3 - (WIDTH / 6) - 50, max(title_y_pos + 1100, 500)))
            screen.blit(IMG_ASTEROID, icon_rect) 
            screen = text(screen, 'Asteroid', 30, (WIDTH / 3) * 3 - (WIDTH / 6) - 50, max(title_y_pos + 1150, 550))

        if start and not end_screen and not game_over:

            #Countdown
            lower_bound = MONTH_STEPS / 2
            if time > lower_bound / 2 and time < MONTH_STEPS:
                screen = text(screen, 'Year review starts in ...', 25, WIDTH / 2, 200)
            if time > lower_bound and time < lower_bound + (MONTH_STEPS / 6):
                screen = text(screen, '3', 85, WIDTH / 2, 300)           
            if time > lower_bound + (MONTH_STEPS / 6) and time < 2 * (MONTH_STEPS / 6) + lower_bound:
                screen = text(screen, '2', 85, WIDTH / 2, 300)
            if time > lower_bound + 2 * (MONTH_STEPS / 6) and time < 3 * (MONTH_STEPS / 6) + lower_bound:
                screen = text(screen, '1', 85, WIDTH / 2, 300)

            first_month_time = min([int(k) for k in month_dict.keys()])

            if month_dict.get(str(time),'') != '':
                month_obj = month_line(month_dict.get(str(time)))
            if time >= first_month_time:
                month_obj.move()
                month_obj.draw(screen)

            if time > MONTH_STEPS:
                for idx, ast in enumerate(asteroids):
                    ast.move()
                    if ast.y_pos > HEIGHT:
                        asteroids.pop(idx)
                        score += 1
                        num_missed_ast += 1
                    if ast.rect.colliderect(player.rect):
                        if hit_time <= time:
                            health -= 10
                            hit_time = time + cool_down
                            score -= 1
                            ast.hit_ast = True
                            num_hit_ast += 1
                    if not ast.hit_ast:
                        screen.blit(IMG_ASTEROID, ast.rect)
                
                new_ast = np.random.random() < 0.03
                if new_ast:
                    asteroids.append(asteroid())

            pygame.draw.line(screen,COLORS['WHITE'],(50,110),(50 + health, 110),width = 10)
            if health < 100:
                pygame.draw.line(screen,COLORS['RED'],(50 + health + 1,110),(150, 110),width = 10)       

            first_highlight_time = min([int(k) for k in highlight_dict.keys()])

            if highlight_dict.get(str(time),'') != '':
                highlight_obj = highlight(highlight_dict.get(str(time)))
                hit_high = False
            if time >= first_highlight_time:
                highlight_obj.move()
                if highlight_obj.rect.colliderect(player.rect):
                    if high_time <= time:
                        high_time = time + cool_down
                        health = min(health + 20, 100)
                        score += 100
                        hit_high = True
                        high_list.append(highlight_obj.name)
                if not hit_high:
                    highlight_obj.draw(screen, IMG_HIGHLIGHT)


            first_lowlight_time = min([int(k) for k in lowlight_dict.keys()])

            if lowlight_dict.get(str(time),'') != '':
                lowlight_obj = highlight(lowlight_dict.get(str(time)))
                hit_low = False
            if time >= first_lowlight_time:
                lowlight_obj.move()
                if lowlight_obj.rect.colliderect(player.rect):
                    if low_time <= time:
                        low_time = time + cool_down
                        health = max(health - 20, 0)
                        score -= 100
                        hit_low = True
                        low_list.append(lowlight_obj.name)
                if not hit_low:
                    lowlight_obj.draw(screen, IMG_LOWLIGHT)


            Health_txt = small_font.render('Health: ' + str(health), False, COLORS['WHITE'])
            screen.blit(Health_txt, (50, 120))

            screen.blit(IMG_SPACESHIP, player.rect)

            Score = my_font.render('Score: ' + str(score), False, COLORS['WHITE'])
            screen.blit(Score, (50, 50))

            if health <= 0:
                game_over = True
                start = False

            title_y_pos = HEIGHT + 100

        if (end_screen or game_over) and not start:
            title_y_pos -= MONTH_VEL

            if end_screen:
                text_title = 'Year done!'
            else:
                text_title = 'GAME OVER!'

            screen = text(screen, text_title, 45, WIDTH/2 ,max(title_y_pos, 100))

            # table 1 header
            col_width = int((WIDTH - 200) / 4)
            screen = text(screen, 'Dodged', 25, 2 * col_width - (col_width / 2), max(title_y_pos + 200, 200))
            screen = text(screen, 'Collisions', 25, 3 * col_width - (col_width / 2), max(title_y_pos + 200, 200))
            screen = text(screen, 'Points', 25, 4 * col_width - (col_width / 2), max(title_y_pos + 200, 200))

            # table 1 content
            screen = text(screen, 'Asteroids', 25, col_width - (col_width / 2), max(title_y_pos + 230, 230))        
            screen = text(screen, str(num_missed_ast), 20, 2 * col_width - (col_width / 2), max(title_y_pos + 230, 230))
            screen = text(screen, str(num_hit_ast), 20, 3 * col_width - (col_width / 2), max(title_y_pos + 230, 230))
            if (num_missed_ast - num_hit_ast) > 0:
                color = 'GREEN'
                txt = '+' + str(num_missed_ast - num_hit_ast)
            else:
                color = 'RED'
                txt = '-' + str(num_missed_ast - num_hit_ast)
            screen = text_2(screen, txt, 20, 4 * col_width - (col_width / 2), max(title_y_pos + 230, 230),COLORS[color])  

            # table 2 header
            col_width = int((WIDTH - 200) / 2)
            screen = text(screen, 'HIGHLIGHTS', 25, col_width - (col_width / 2), max(title_y_pos + 300, 300))
            screen = text(screen, 'LOWLIGHTS', 25, 2 * col_width - (col_width / 2), max(title_y_pos + 300, 300))

            # table 3 content
            col_width = int((WIDTH - 200) / 4)
            dist = 30
            # highlights
            high_list = list(set(high_list))
            high_list.sort()
            for idx, hl in enumerate(high_list):
                hl = hl.replace('\n',' ')
                screen = text_2(screen, str(hl), 18, 100, max(title_y_pos + 350 + (dist * idx), 350 + (dist * idx)),COLORS['WHITE'])
                screen = text_2(screen, '+ 100', 18, 2 * col_width - (col_width / 2) + 100, max(title_y_pos + 350 + (dist * idx), 350 + (dist * idx)),COLORS['GREEN'])
            idx = -1
            for hl in highlight_dict.values():
                if not hl in high_list:
                    hl = hl.replace('\n',' ')
                    idx += 1
                    screen = text_2(screen, str(hl), 18, 100, max(title_y_pos + 350 + (dist * idx) + (dist * len(high_list)), 350 + (dist * idx) + (dist * len(high_list))), COLORS['GRAY'])
                    screen = text_2(screen, '0', 18, 2 * col_width - (col_width / 2) + 100, max(title_y_pos + 350 + (dist * idx) + (dist * len(high_list)), 350 + (dist * idx) + (dist * len(high_list))), COLORS['GRAY'])

            # lowlights
            low_list = list(set(low_list))
            low_list.sort()
            for idx, hl in enumerate(low_list):
                hl = hl.replace('\n',' ')
                screen = text_2(screen, str(hl), 18, 2 * col_width + 100, max(title_y_pos + 350 + (dist * idx), 350 + (dist * idx)),COLORS['WHITE'])
                screen = text_2(screen, '- 100', 18, 2 * col_width + 2 * col_width - (col_width / 2) + 100, max(title_y_pos + 350 + (dist * idx), 350 + (dist * idx)),COLORS['RED'])
            idx = -1
            for hl in lowlight_dict.values():
                if not hl in low_list:
                    hl = hl.replace('\n',' ')
                    idx += 1
                    screen = text_2(screen, str(hl), 18, 2 * col_width + 100, max(title_y_pos + 350 + (dist * idx) + (dist * len(low_list)), 350 + (dist * idx) + (dist * len(low_list))), COLORS['GRAY'])
                    screen = text_2(screen, '0', 18, 2 * col_width + 2 * col_width - (col_width / 2) + 100, max(title_y_pos + 350 + (dist * idx) + (dist * len(low_list)), 350 + (dist * idx) + (dist * len(low_list))), COLORS['GRAY'])

            pygame.draw.line(screen, COLORS['WHITE'], (100, max(title_y_pos + 590, 590)), (WIDTH - 100, max(title_y_pos + 590, 590)))

            final_score = f'Score = ({(num_missed_ast - num_hit_ast)} (Asteroids) + {len(high_list) * 100} (Highlights) - {len(low_list) * 100} (Lowlights)) * {health} (Health)'
            screen = text(screen, final_score, 20, WIDTH / 2,  max(title_y_pos + 620, 620))
            points = ((num_missed_ast - num_hit_ast) + len(high_list) - len(low_list)) * health

            if points > 0:
                color = 'GREEN'
            else:
                color = 'RED'
            
            screen = text_2(screen, str(points), 45, WIDTH / 2,  max(title_y_pos + 650, 650),COLORS[color])

            screen = text(screen, 'press (r) for restart', 15, 100, max(title_y_pos + 700, 700))

        pygame.display.update()

        await asyncio.sleep(0)

asyncio.run(main())