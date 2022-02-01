import pygame
import random
import time

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255,0,0)

crashed = False
#玩家本體相關
carImg = pygame.image.load('fox.jpg')
car_width = 120
car_heigh = 90
x = display_width/2
y = display_height/2
x_change = 0
y_change = 0
car_speed = 0

#目標物相關
rikuImg = pygame.image.load('riku.jpg')
riku_width = 120
riku_height = 67
riku_x = random.randrange(0, display_width - riku_width)
riku_y = random.randrange(0, display_height - riku_height)

#障礙物相關
rock_x = random.randrange(0, display_width)
rock_y = -600
rock_speed = 7
rock_width = 100
rock_height = 100
rock_crash = False

#計分
global score
score = 0

#建立本體和目標的位置(記憶體裡，要用pygame.display.update來顯示在畫面)
def photo(x, y):
   gameDisplay.blit(carImg, (x, y))
   gameDisplay.blit(rikuImg, (riku_x, riku_y))

#目標被吃之後重生
def reriku():
   x = random.randrange(0, display_width - riku_width)
   y = random.randrange(0, display_height - riku_height)
   global score
   score += 1
   return x,y

#字幕
def message():
   largeText = pygame.font.Font('LucidaBrightDemiBold.ttf', 20)	#字體跟20大小的Font物件
   s = 'Score: '+ str(score)
   TextSurf = largeText.render(s, True, black)				#Font物件的render
   TextRect = TextSurf.get_rect()					#字幕的圖
   TextRect.center = (50,20)						#字幕圖的中心位置
   gameDisplay.blit(TextSurf,TextRect)				#建立在記憶體
   pygame.display.update()						#刷新畫上


while not crashed:

   for event in pygame.event.get():
       #print(event)
       if event.type == pygame.QUIT:
           crashed = True
       #############移動###############
       if event.type == pygame.KEYDOWN:
           if event.unicode == 'a':
               x_change = -5
           elif event.key == pygame.K_d:
               x_change = 5
           elif event.key == 119:
               y_change = -5
           elif event.key == pygame.K_s:
               y_change = 5
       if event.type == pygame.KEYUP:
           if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s:
               x_change = 0
               y_change = 0
       ######################

   ##		超出畫面偵測
   x += x_change
   y += y_change
   if x > display_width - 1:
       x = 0 - car_width +1
   elif x < 0 - car_width + 1:
       x = display_width - 1
   if y > display_height - 1:
       y = 0 - car_heigh + 1
   elif y < 0 - car_heigh + 1:
       y = display_height - 1
   ##		跟目標物的接觸偵測
   if (x > riku_x and x < riku_x + riku_width) or (x + car_width > riku_x and x + car_width < riku_x + riku_width):
       if (y > riku_y and y < riku_y + riku_height) or (y + car_heigh > riku_y and y + car_heigh < riku_y + riku_height):
           riku_x,riku_y = reriku()
   ##		跟障礙物的接觸偵測

   rock_y += rock_speed

   if rock_y > display_height:
       rock_y = 0 - rock_height
       rock_x = random.randrange(0, display_width)


   if (x > rock_x and x < rock_x + rock_width) or (x + car_width > rock_x and x + car_width < rock_x + rock_width):
       if (y > rock_y and y < rock_y + rock_height) or (y + car_heigh > rock_y and y + car_heigh < rock_y + rock_height):
           if rock_crash == False and score > 0:
               score -= 1
               rock_crash = True			#鎖住，避免多次扣分
   else:
       rock_crash = False
   ##
   gameDisplay.fill(white)			#畫面刷白
   photo(x, y)					#畫本體和目標物
   pygame.draw.rect(gameDisplay, red, [rock_x, rock_y, rock_width, rock_height])	#畫障礙物
   message()					#顯示字幕
   pygame.display.update()			#把更新內容放上畫面
   clock.tick(60)				#每秒60次

pygame.quit()
quit()

