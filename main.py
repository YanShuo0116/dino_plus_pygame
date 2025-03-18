import pygame
import os
import random
import image

pygame.init()

# 全域常數
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

birdY = [265, 225, 325]
scoreboard = []

color_light = (170,170,170)
color_dark = (100,100,100) 
white = (255, 255, 255)
black = (0, 0, 0)

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]
           
           
#音效
start_sound = pygame.mixer.Sound(os.path.join("Assets/Sound", "start.wav"))
bgm_sound = pygame.mixer.Sound(os.path.join("Assets/Sound", "fast.mp3"))
ROAR_SOUND = pygame.mixer.Sound(os.path.join("Assets/Sound", "roar.mp3"))
TANK_MOVE_SOUND = pygame.mixer.Sound(os.path.join("Assets/Sound", "tankmove.mp3"))
JUMP_SOUND = pygame.mixer.Sound(os.path.join("Assets/Sound", "jump.mp3"))
HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets/Sound", "hit.mp3"))

# 新增迅猛龍 NPC 圖片載入
NPC_RUNNING = [pygame.image.load(os.path.join("Assets/NPC", f"npc{i}.png")) for i in range(6)]


# 載入坦克圖資
TANK = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Tank", f"tank_{i}.png")), (243, 180)) for i in range(8)]


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):

        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.in_tank = False  # 判斷是否在坦克中

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.collision_rect = pygame.Rect(self.dino_rect.x, self.dino_rect.y, self.dino_rect.width - 35, self.dino_rect.height - 20)

    def update(self, userInput):
        if self.in_tank:
            self.drive_tank()
        else:
            if self.dino_duck:
                self.duck()
            if self.dino_run:
                self.run()
            if self.dino_jump:
                self.jump()

            if self.step_index >= 10:
                self.step_index = 0

            if userInput[pygame.K_UP] and not self.dino_jump:
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
                JUMP_SOUND.play()
            elif userInput[pygame.K_DOWN] and not self.dino_jump:
                self.dino_duck = True
                self.dino_run = False
                self.dino_jump = False
            elif not (self.dino_jump or userInput[pygame.K_DOWN]):
                self.dino_duck = False
                self.dino_run = True
                self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1
        self.collision_rect = pygame.Rect(self.dino_rect.x, self.dino_rect.y, self.dino_rect.width - 35, self.dino_rect.height - 20)

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1
        self.collision_rect = pygame.Rect(self.dino_rect.x, self.dino_rect.y, self.dino_rect.width - 35, self.dino_rect.height - 20)

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
        self.collision_rect = pygame.Rect(self.dino_rect.x, self.dino_rect.y, self.dino_rect.width - 35, self.dino_rect.height - 20)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def drive_tank(self):
        # 確保 step_index 不會超出範圍
        if self.step_index < 30:
            self.image = TANK[min(self.step_index // 5, len(TANK) - 1)]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS - 70  # 調整Y座標以適應縮放後的坦克圖像
            self.step_index += 1
        else:
            self.image = TANK[6 + (self.step_index // 5) % 2]  # 6和7為坦克行走
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS - 70  # 調整Y座標以適應縮放後的坦克圖像
            self.step_index += 1

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.inflate_ip(-20, -20)
        self.rect.x = SCREEN_WIDTH
        

    def update(self):
        self.rect.x -= game_speed
        self.collision_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width - 20, self.rect.height - 20)
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
        self.collision_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width - 20, self.rect.height - 20)

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300
        self.collision_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width - 20, self.rect.height - 20)


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = birdY[random.randint(0, 2)]
        self.index = 0
        self.collision_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width - 20, self.rect.height - 20)

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1
        
class NPC:
    def __init__(self):
        self.image = NPC_RUNNING[0]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = 240
        self.speed = 35
        self.step_index = 0
        self.collision_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width - 20, self.rect.height - 20)
        ROAR_SOUND.play()

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            npcs.remove(self)

        # 更新動畫圖片
        self.step_index += 1
        if self.step_index >= len(NPC_RUNNING) * 5:
            self.step_index = 0
        self.image = NPC_RUNNING[self.step_index // 5]

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        

def readScore():
    file_path = './Assets/scoreLog.txt'
    try:
        with open(file_path, 'r') as file:
            for line in file:
                number = int(line.strip())  # 讀取每行並轉換為整數
                scoreboard.append(number)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except ValueError:
        print("Error: Non-numeric data found in the file")
    return scoreboard

def writeScore(numbers):
    file_path = './Assets/scoreLog.txt'
    try:
        with open(file_path, 'w') as file:
            for number in numbers:
                file.write(f"{number}\n")  # 將每個數字寫入文件中
    except IOError:
        print(f"Error: Could not write to file at {file_path}")
        
def ranking(death_count, scoreboard):
    run = True
    font = pygame.font.Font('freesansbold.ttf', 30)
    while run:
        SCREEN.fill((255, 255, 255))
        for i in range(10):
            rect = pygame.Rect(SCREEN_WIDTH//2-200, i*SCREEN_HEIGHT/10, 400, SCREEN_HEIGHT/10)
            pygame.draw.rect(SCREEN, black, rect, 5)
            top = font.render(f'top {i+1}: ', True, black)
            score = font.render(f'{scoreboard[i]}', True, black)
            SCREEN.blit(top, (SCREEN_WIDTH//2-150, i*SCREEN_HEIGHT/10+10))
            SCREEN.blit(score, (SCREEN_WIDTH//2+100, i*SCREEN_HEIGHT/10+10))
        back = font.render('menu', True, (0, 0, 0))
        mouse = pygame.mouse.get_pos()
        if 100 <= mouse[0] <= 250 and 50 <= mouse[1] <= 100: 
            pygame.draw.rect(SCREEN,color_light,[100,50,150,50])   
        else: 
            pygame.draw.rect(SCREEN,color_dark,[100,50,150,50])
        SCREEN.blit(back, (130, 60))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 100 <= mouse[0] <= 250 and 50 <= mouse[1] <= 100:
                    start_sound.stop()
                    menu(death_count, start=False)
            if event.type == pygame.QUIT:
                writeScore(scoreboard)
                pygame.quit()
                run = False


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, energy, tank_mode, last_energy_update, npcs
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    npcs = []  # 新增一個列表來保存 NPC
    death_count = 0
    energy = 0
    max_energy = 10
    energy_increase_interval = 1000
    last_energy_update = 0
    tank_mode = False
    tank_mode_duration = 3000
    tank_mode_start_time = 0
    last_energy_decrease = 0
    last_npc_spawn_time = 0  # 新增一個變數來追蹤 NPC 的產生時間

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        if points >=1800:
            start_sound.stop()
            bgm_sound.play(loops=-1)
            
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def draw_energy_bar(energy, max_energy):
        for i in range(max_energy):
            color = (0, 255, 0) if i < energy else (255, 0, 0)
            pygame.draw.rect(SCREEN, color, (50 + i * 12, 50, 10, 10))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        # 新增 NPC 的生成邏輯
        current_time = pygame.time.get_ticks()
        if points % 1000 == 0 and points > 0 and current_time - last_npc_spawn_time > 5000:
            npcs.append(NPC())
            last_npc_spawn_time = current_time

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if not tank_mode:
                if player.collision_rect.colliderect(obstacle.rect):
                    HIT_SOUND.play()
                    pygame.time.delay(500)
                    death_count += 1
                    start_sound.stop()
                    bgm_sound.stop()
                    menu(death_count, start=False)

        # 更新和繪製 NPC
        for npc in npcs:
            npc.draw(SCREEN)
            npc.update()
            if player.collision_rect.colliderect(npc.rect):
                if not tank_mode:
                    HIT_SOUND.play()
                    pygame.time.delay(500)
                    death_count += 1
                    start_sound.stop()
                    bgm_sound.stop()
                    menu(death_count, start=False)

        background()
        
        player.draw(SCREEN)
        player.update(userInput)

        cloud.draw(SCREEN)
        cloud.update()

        score()

        # 更新能量條
        if current_time - last_energy_update >= energy_increase_interval:
            if energy < max_energy:
                if not tank_mode:
                    energy += 1
            last_energy_update = current_time

        # 畫能量條
        draw_energy_bar(energy, max_energy)

        # 檢查是否按下空白鍵並且能量條滿了
        if userInput[pygame.K_SPACE] and energy == max_energy and not tank_mode:
            player.in_tank = True
            tank_mode = True
            tank_mode_start_time = pygame.time.get_ticks()
            TANK_MOVE_SOUND.play(-1)

        # 檢查坦克模式時間
        if tank_mode:
            if current_time - tank_mode_start_time > tank_mode_duration:
                tank_mode = False
                player.in_tank = False
                player.step_index = 0 #重置 step_index
                TANK_MOVE_SOUND.stop()
                
            if current_time - last_energy_decrease >= 300:
                if energy > 0:
                    energy -= 1
                last_energy_decrease = current_time
            
            if current_time - tank_mode_start_time > 1000 and userInput[pygame.K_SPACE]:
                tank_mode = False
                player.in_tank = False
                player.step_index = 0
                TANK_MOVE_SOUND.stop()
                
                

        clock.tick(30)
        pygame.display.update()

def menu(death_count, start):
    global points, scoreboard
    run = True
    overwrite = False
    #readFile = True
    start_sound.play(loops=-1)
    
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            if start:
                scoreboard = readScore()
                start = False
                #readFile = False
            text = font.render("Press any Key to Start", True, (0, 0, 0))
            
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            
            if not overwrite:
                scoreboard.insert(0, points)
                scoreboard.sort(reverse=True)
                overwrite = True
            # 如果插入了新的分數且分數板長度超過10，移除最後一個元素
            if overwrite and len(scoreboard) > 10:
                scoreboard.pop()
            # 如果新分數不大於分數板上的任何分數，且分數板長度小於10，則添加到末尾
            if not overwrite and len(scoreboard) < 10:
                scoreboard.append(score)
                
            for i in range(len(scoreboard)):
                print(f'{i}: {scoreboard[i]}')
            
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 140))
        rk = font.render('Ranking', True, (0, 0, 0))
        mouse = pygame.mouse.get_pos()
        if SCREEN_WIDTH // 2-70 <= mouse[0] <= SCREEN_WIDTH // 2+70 and SCREEN_HEIGHT // 2+100 <= mouse[1] <= SCREEN_HEIGHT // 2 + 140: 
            pygame.draw.rect(SCREEN,color_light,[SCREEN_WIDTH // 2-70,SCREEN_HEIGHT // 2 + 100,140,40])   
        else: 
            pygame.draw.rect(SCREEN,color_dark,[SCREEN_WIDTH // 2-70,SCREEN_HEIGHT // 2 + 100,140,40])
        SCREEN.blit(rk, (SCREEN_WIDTH // 2 - 61, SCREEN_HEIGHT // 2+105))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                writeScore(scoreboard)
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SCREEN_WIDTH // 2-70 <= mouse[0] <= SCREEN_WIDTH // 2+70 and SCREEN_HEIGHT // 2+100 <= mouse[1] <= SCREEN_HEIGHT // 2 + 140:
                    ranking(death_count, scoreboard)

menu(death_count=0, start=True)