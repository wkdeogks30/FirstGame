import pygame
import random
import time

WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen_height = 600
screen_width = 500



#오브젝트 출력
def drawObj(obj, x, y):
    global screen
    screen.blit(obj, (x, y))

def ShotSound():
    pygame.mixer.music.load('Shot.mp3')
    pygame.mixer.music.play()

def showText(txt, size, x, y, color):
    font = pygame.font.Font('DOSMyungjo.ttf', size)
    text = font.render(txt, True, color)
    screen.blit(text, (x, y))
def EnemyMake(enemy_type):
    enemy = list()
    for i in range(5):
        enemy_fake = pygame.image.load('enemy' + enemy_type + '.png')
        enemy.append(pygame.transform.scale(enemy_fake, (30, 30)))
    return enemy

def RunGame():

    #적 관련 정보    
    enemy_loc = list()
    speed = 0.2
    enemy_locY = 102
    enemy_count = 0
    enemy_type = -1

    #점수
    score = 0

    #플레이어 좌표
    player_x = 230
    player_y = 530

    #배경 좌표
    background_y = 0
    background2_y = -600

    #기본 설정
    finish = False
    initGame()
    clock.tick(60)

    #총 발사 여부 및 총알 좌표 모음(순서대로 생성, 순서대로 삭제)
    shooted = list()
    bullet = list()
    for i in range(5):
        shooted.append(False)
        bullet.append([1000, 1000])
    print(len(bullet))
    Press = False
    while not finish:
        #방향키 입력            
        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_a]:
            player_x -= 2
        elif key_event[pygame.K_d]:
            player_x += 2
        #사용자 입력(종료 및 발사) get_pressed() -> Tuple
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for i, xshootedx in enumerate(shooted):
                        if xshootedx != True:
                            shooted[i] = True
                            bullet[i] = [player_x + 10.5, player_y]
                            ShotSound()
                            break # Q. 어디 루프 탈출?
        #배경 출력
        background_y += 0.3
        background2_y += 0.3
        if background_y >= 600:
            background_y = 0
            background2_y = -600
            drawObj(background2, 0, background2_y)
            drawObj(background, 0, background_y)
        else:
            drawObj(background2, 0, background2_y)
            drawObj(background,0, background_y)
        
        #총알 출력
        for i, xshootedx in enumerate(shooted):
            if xshootedx == True:
                bullet[i][1] -= 2
                drawObj(player_bullet, bullet[i][0], bullet[i][1])
            if bullet[i][1] <= 0:
                shooted[i] = False

        #플레이어 출력
        drawObj(player, player_x, player_y)

        #적 출력
        for i in range(5):
            if enemy_count == 0:
                enemy_loc.append(random.randrange(0, 460))
            elif enemy_count < 5:
                enemy_loc.append(random.randrange(0, 460))
                enemy_count += 1
        for i,enemy in enumerate(EnemyMake('1')):
            enemy_locY += speed
            drawObj(enemy, enemy_loc[i], enemy_locY)

        #총알이 적에게 맞을 경우
        for i in range(5):
            for x in range(5):
                if enemy_locY <= bullet[i][1] and enemy_locY + 30 >= bullet[i][1]:
                    if bullet[i][0] >= enemy_loc[x] and bullet[i][0] <= enemy_loc[x] + 30:
                        enemy_count -= 1
                        drawObj(boom, enemy_loc[x], enemy_locY)
                        enemy_loc[x] = 10000
                        score += 5
        #적과 자신이 충돌했을경우
        for i in range(5):
            if enemy_locY >= player_y and enemy_locY <= player_y + 30:
                if player_x <= enemy_loc[i] and player_x + 30 >= enemy_loc[i]:
                    time.sleep(1) #작동 방식?
                    showText("Game Over", 60, 130, 250, RED)
                    #showText("Score : " + str(score), 60, 130, 300, RED)
                    finish = True
                    #RunGame()

        #바닥에 닿을때
        if enemy_locY > 600:
            enemy_count = 0
            enemy_loc.clear() 
            enemy_locY = 102
        #속도 제한
            if speed <= 0.8:
                speed += 0.02
            else:
                pass
        #점수 출력
        showText('SCORE', 30, 210, 0, RED)
        showText(str(score), 30, 230, 30, WHITE)
        pygame.display.update()

def initGame():
    global clock, screen, player, background, background2,player_bullet, bullSound, enemy, boom

    #기본 설정
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Galaga")
    clock = pygame.time.Clock()
    player = pygame.image.load('player1.png')
    player = pygame.transform.scale(player, (30, 30))
    player_bullet = pygame.image.load('player_gun.png')
    player_bullet = pygame.transform.scale(player_bullet, (10, 10))
    background = pygame.image.load('back.png')
    background2 = pygame.image.load('back.png')
    boom = pygame.image.load('boom.png')
    
if __name__ == '__main__':
    RunGame()