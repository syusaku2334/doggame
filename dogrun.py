import pygame
import sys
import random
from pygame.locals import *
from dog import Dog

#色
SKY = (156, 192, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TITLE = (255, 100, 88)
BROUN = (80, 50, 0)
RED = (255, 0, 0)

# 画像
shizuku = pygame.image.load('shizuku0.png')
sakura = pygame.image.load('sakura0.png')
rakio = pygame.image.load('rakio0.png')
bgimg = pygame.image.load('background.png')
wood = pygame.image.load('wood.png')
date = pygame.image.load('date.png')
food_img = pygame.image.load('food0.png')
second_food = pygame.image.load('second_food0.png')
timeup = pygame.image.load('timeup.png')

shi_left = pygame.transform.flip(shizuku, True, False)
sak_left = pygame.transform.flip(sakura, True, False)
rak_left = pygame.transform.flip(rakio, True, False)

shi_d = pygame.image.load('shizuku1.png')
sak_d = pygame.image.load('sakura1.png')
rak_d = pygame.image.load('rakio1.png')


dog_img = [shizuku, shi_left, sakura, sak_left, rakio, rak_left, shi_d, sak_d, rak_d]



# 変数
idx = 0
tmr = 0

# 犬情報
dog0_character = ['ふわふわのかわいいわんこ。', 'あまえんぼうではあるが、','たまに凶暴になることも。', '家族にしかなつかない。']
dog1_character = ['くいしんぼうのかわいいわんこ。', '基本的にはよってこないが、', '優しいよりそいタイプ。', 'ちょっとどんくさい。']
dog2_character = ['あまえんぼうのかわいいわんこ。', '犬にも人にもなつっこいが、', '家族に抱っこしてもらうのが', '一番好き。']
dogs_character = [dog0_character, dog1_character, dog2_character]

dog0 = Dog('しずく', 2, 3)
dog1 = Dog('さくら', 1, 1)
dog2 = Dog('ラッキー', 1.5, 2,)

dogs = [dog0, dog1, dog2]


def draw_dog(bg, shi_x, shi_y, sak_x, sak_y, rak_x, rak_y):
        bg.blit(shizuku, [shi_x, shi_y])
        bg.blit(sakura, [sak_x, sak_y])
        bg.blit(rakio, [rak_x, rak_y])

# 影付き文字
def draw_text(bg, txt, x, y, fnt, col):
        text = fnt.render(txt, True, BLACK)
        bg.blit(text, [x+1, y+2])
        text = fnt.render(txt, True, col)
        bg.blit(text, [x, y])

# 文字
def draw_txt(bg, txt, x, y, fnt, col):
    text = fnt.render(txt, True, col)
    bg.blit(text, [x, y])
    
# コマンド操作
cmd = 0
def dog_command(key, bg, fnt):
    global cmd
    iy = 0
    cy = 0
    ent = False
    if key[K_UP] and cmd > 0 :
        cmd -= 1
        se[3].play()
    if key[K_DOWN] and cmd < 2:
        cmd += 1
        se[3].play()
    if key[K_RETURN]:
        ent = True
    for i in range(3):
        namet = fnt.render(dogs[i].name, True, BLACK)
        bg.blit(namet, [40, 230+iy])
        iy += 180
    for i in range(3):
        if cmd == i:
            pygame.draw.polygon(bg, RED, [[80, 280+cy], [60, 300+cy], [100, 300+cy]])
        cy += 180
    return ent

# セットと表示と左右の移動
player_x = 350
player_y = 600
pl_m = 0
dog_blink = 0
player_hp = 0
player_hpmax = 300

def set_dog(key):
    global pl_m, player_hp, player_hpmax
    r = 0
    for i in range(3):
        if cmd == i:
            if key[K_RIGHT] == 1:
                pl_m = i + r
            if key[K_LEFT] == 1:
                pl_m = i + r + 1
        r += 1

def draw_dogs(bg):
    global dog_blink
    player_y = 645 - dog_img[pl_m].get_height()
    if dog_blink % 2 == 0:
        bg.blit(dog_img[pl_m], [player_x, player_y])
    if dog_blink > 0:
        dog_blink -= 1


def move_dog(bg, key):
    global player_x
    draw_dogs(bg)
    for i in range(3):
        if cmd == i:
            player_speed = dogs[i].speed
    if player_x >= 50 and key[K_LEFT] == 1:
        player_x -= 30*player_speed
    if player_x <= 860 - dog_img[pl_m].get_width() and key[K_RIGHT] == 1:
        player_x += 30*player_speed

# 食べ物が落ちる処理
food_x = 0
food_y = 0
kind = 0
se = None

score = 0
high_score = 0
catch = False

def set_food():
    global food_img, food_x, food_y, kind, catch
    kind = random.randint(0, 4)
    food_img = pygame.image.load('food' + str(kind) + '.png')
    food_x = random.randint(5, 790)
    catch = False

def fall_food(bg):
    global food_x, food_y, idx, tmr
    bg.blit(food_img, [food_x, food_y])
    food_y += 70
    if food_y > 720:
        idx = 2
        tmr = 35
        food_y = -100
        set_food()
    

skind = 0
food_sx = 0
food_sy = 0

def set_sfood():
    global second_food, skind, food_sx, catch
    skind = random.randint(0, 4)
    second_food = pygame.image.load('second_food'+str(skind)+'.png')
    food_sx = random.randint(5, 790)
    catch = False
    
def fall_sfood(bg):
    global food_sx, food_sy, idx, tmr
    bg.blit(second_food, [food_sx, food_sy])
    food_sy += 70
    if food_sy >= 720:
        food_sy = -200
        set_sfood()
        idx = 2
        tmr = 35




# スコア表示
def draw_score(bg, fnt):
    scoret = 'スコア {}'.format(score)
    draw_txt(bg, scoret, 30, 60, fnt, BLACK)
    if high_score > 0:
        draw_txt(bg, 'ハイスコア {}'.format(high_score), 30, 20, fnt, BROUN)

# 嫌いな食べ物判定
def catch_food():
    global score, pl_m, idx, tmr, dog_blink, player_hp, food_y, catch, food_sy, catch_s
    if player_y <= food_y + 40 and food_y + 40 <= player_y + 50:
        if player_x <= food_x + 40 and food_x + 40 <= player_x + dog_img[pl_m].get_width():
            food_y = -100
            score += 5
            player_hp += 5
            se[0].play()
            catch = True
    if player_y <= food_sy + 40 and food_sy + 40 <= player_y + 50:
        if player_x <= food_sx + 40 and food_sx + 40 <= player_x + dog_img[pl_m].get_width():
            food_sy = -200
            score += 5
            player_hp += 5
            se[0].play()
            set_sfood()
    return catch

def ng_check():
    global score, dog_blink, player_hp, pl_m, idx, tmr
    if catch_food() == True:
        if cmd == 0:
            for i in range(3):
                if kind == i:
                    score -= 8
                    se[1].play()
                    pl_m = 6
                    idx = 3
                    dog_blink += 5
                    tmr = 0
                    player_hp -= 5
            else:
                set_food()
        if cmd == 1:
            if kind == 0:
                score -= 8
                se[1].play()
                pl_m = 7
                idx = 3
                tmr = 0
                dog_blink += 5
                player_hp -= 5
            else:
                set_food()
        if cmd == 2:
            for i in range(2):
                if kind == i:
                    score -= 8
                    se[1].play()
                    pl_m = 8
                    idx = 3
                    tmr = 0
                    dog_blink += 5
                    player_hp -= 5
            else:
                set_food()
    
# 体力ゲージ
def draw_hp(bg, x, y, w, h, val, max):
    pygame.draw.rect(bg, WHITE, [x-2, y-2, w+4, h+4])
    pygame.draw.rect(bg, BLACK, [x, y, w, h])
    if val > 0:
        pygame.draw.rect(bg, (240, 150, 0), [x, y, w*val/max, h])

# ゲームオーバー画面選択
r_cmd = 0

def return_cmd(bg, key):
    global r_cmd
    ent = False
    rc = 0
    if key[K_UP] == 1 and r_cmd > 0:
        r_cmd = 0
        se[3].play()
    if key[K_DOWN] == 1 and r_cmd < 1:
        r_cmd = 1
        se[3].play()
    if key[K_RETURN] == 1:
        ent = True
    for i in range(2):
        if r_cmd == i:
            pygame.draw.polygon(bg, RED, [[440, 420+rc], [420, 440+rc], [460, 440+rc]])
        rc += 80
    return ent

# 中央ぞろえ
def center_txt(bg, txt, fnt, col, y):
    text = fnt.render(txt, True, col)
    bg.blit(text, [440-text.get_width()/2, y])

def main():
    global idx, pl_m, tmr, se, score, player_hp, player_hpmax, high_score, food_y, food_sy

    pygame.init()
    pygame.display.set_caption('DOG RUN')
    screen = pygame.display.set_mode((880, 720))
    fontM1 = pygame.font.Font('mamelon_hireg\Mamelon-5-Hi-Regular.otf', 90)
    fontM2 = pygame.font.Font('mamelon_hireg\Mamelon-3-Hi-Regular.otf', 30)
    fontM3 = pygame.font.Font('mamelon_hireg\Mamelon-3-Hi-Regular.otf', 50)
    fontN = pygame.font.Font('ipaexg00201\ipaexg.ttf', 30)
    clock = pygame.time.Clock()

    se = [
        pygame.mixer.Sound('ぱくっ.mp3'),
        pygame.mixer.Sound('othr01.mp3'),
        pygame.mixer.Sound('決定、ボタン押下46.mp3'),
        pygame.mixer.Sound('決定、ボタン押下34.mp3')
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

               
        
        screen.blit(bgimg, [0, 0])
        pygame.event.pump()
        key = pygame.key.get_pressed()

        tmr += 1
        player_hp -= 1

        if idx == 0:
            if tmr == 1:
                pygame.mixer.music.load('洗濯日和.mp3')
                pygame.mixer.music.play(-1)
            draw_dog(screen, 420, 530, 15, 480, 260, 510)
            screen.blit(wood, [0, 0])
            if tmr%6 != 0:
                draw_txt(screen, '--- スペースキーをおしてください ---', 110, 400, fontM2, BROUN)
            if high_score > 0:
                center_txt(screen, 'ハイスコア: {}'.format(high_score), fontM2, BROUN, 20)
            if key[K_SPACE] == 1:
                idx = 1
                score = 0
                se[2].play()

        elif idx == 1:
            draw_text(screen, 'おやつをたべるワンちゃんをえらんでください', 120, 50, fontM2, WHITE)
            draw_dog(screen, 160, 180, 130, 320, 160, 520)
            screen.blit(date, [0, 0])
            if dog_command(key, screen, fontM2) == True:
                se[2].play()
                for i in range(3):
                    if cmd == i:
                        set_food()
                        idx = 2
                        tmr = 0
                        pl_m = i * 2
                        food_y = 0
                        food_sy = -200
                        player_hp = player_hpmax
                        

        elif idx == 2:
            draw_score(screen, fontM2)
            set_dog(key)
            if 1 <= tmr <= 10:
                center_txt(screen, str(3), fontM1, BLACK, 330)
            if 11 <= tmr <= 21:
                center_txt(screen, str(2), fontM1, BLACK, 330)
            if 22 <= tmr <= 32:
                center_txt(screen, str(1), fontM1, BLACK, 330)
            if tmr >= 35:
                draw_hp(screen, 600, 30, 250, 30, player_hp, player_hpmax)
                move_dog(screen, key)
                fall_food(screen)
                fall_sfood(screen)
                ng_check()
            if player_hp < 0:
                player_hp = 0
                idx = 4
                tmr = 0

        elif idx == 3:
            draw_score(screen, fontM2)
            draw_hp(screen, 600, 30, 250, 30, player_hp, player_hpmax)
            draw_dogs(screen)
            fall_food(screen)
            fall_sfood(screen)
            if tmr == 30:
                move_dog(screen, key)
                set_food()
                

        elif idx == 4:
            if tmr == 1:
                pygame.mixer.music.stop()
            if tmr == 2:
                pygame.mixer.music.load('ジングル・ほのぼの01.mp3')
                pygame.mixer.music.play(0)
            screen.blit(timeup, [60, 100])
            center_txt(screen, 'スコア:   {}'.format(score), fontM3, BLACK, 250)
            if score > high_score:
                high_score = score
            draw_dogs(screen)
            if tmr >= 40:
                center_txt(screen, '- タイトルにもどる -', fontM2, BLACK, 380)
                for i in range(3):
                    if cmd == i:
                        center_txt(screen, '- {}でもう一度やり直す -'.format(dogs[i].name), fontM2, BLACK, 460)
                if return_cmd(screen, key) == True:
                    se[2].play()
                    if r_cmd == 0:
                        idx = 0
                        tmr = 0
                    if r_cmd == 1:
                        idx = 2
                        tmr = 0
                        player_hp = player_hpmax
                        score = 0
                        pygame.mixer.music.load('洗濯日和.mp3')
                        pygame.mixer.music.play(-1)   

        


        pygame.display.update()
        clock.tick(8)
            

        

if __name__ == '__main__':
    main()  
