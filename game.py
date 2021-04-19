from time import sleep_ms,sleep
import framebuf
from pyb import *

class Game:
    def __init__(self,width=160,height=128):
        self.width=width
        self.height=height
        self.player={}
        self.enemys=[]
        self.foods=[]
        self.bullets=[]
        self.bgs=[]
        self.gameover=False
        self.score=0
        self.btnA = Pin('BTNA', Pin.IN, Pin.PULL_UP)
        self.btnB = Pin('BTNB', Pin.IN, Pin.PULL_UP)
        self.btnUp = Pin('UP', Pin.IN, Pin.PULL_UP)
        self.btnDown = Pin('DOWN', Pin.IN, Pin.PULL_UP)
        self.btnLeft = Pin('LEFT', Pin.IN, Pin.PULL_UP)
        self.btnRight = Pin('RIGHT', Pin.IN, Pin.PULL_UP)
        self.tft = SCREEN()
        self.fb = framebuf.FrameBuffer(bytearray(160*128), 160, 128, framebuf.PL8)
    def clear(self):
        self.fb.fill(0)
    def set_player_sprite(self,sprite):
        self.player=sprite
        self.bak_player=sprite
    def add_bullets_sprite(self,sprite):
        self.bullets.append(sprite)
    def add_foods_sprite(self,sprite):
        self.foods.append(sprite)
    def add_enemy_sprite(self,sprite):
        self.enemys.append(sprite)
    def add_bg_sprite(self,sprite):
        self.bgs.append(sprite)

    def on_player_collision_with_food(self,player,food):
        pass
    def on_player_collision_with_enemy(self,player,enemy):
        pass
    def on_enemy_collision_with_food(self,enemy,food):
        pass
    def on_bullet_collision_with_enemy(self,bullet,enemy):
        pass
    def horizontal_overlap(self,char, obj):
        return char.x + char.w > obj.x and char.x < obj.x + obj.w
    def vertical_overlap(self,char, obj):
        return obj.y + obj.h > char.y and obj.y < char.y + char.h
    def collision(self):
        # player vs enemy
        for enemy in self.enemys:
            if self.horizontal_overlap(self.player, enemy) and self.vertical_overlap(self.player, enemy):
                self.on_player_collision_with_enemy(self.player,enemy)
        
        # player vs food
        for food in self.foods:
            if self.horizontal_overlap(self.player, food) and self.vertical_overlap(self.player, food):
                self.on_player_collision_with_food(self.player,food)
        
        # bullet vs enemy
        for bullet in self.bullets:
            for enemy in self.enemys:
                if self.horizontal_overlap(bullet, enemy) and self.vertical_overlap(bullet, enemy):
                    self.on_bullet_collision_with_enemy(bullet,enemy)
        
        # enemy vs food
        for food in self.foods:
            for enemy in self.enemys:
                if self.horizontal_overlap(enemy,food) and self.vertical_overlap(enemy,food):
                    self.on_enemy_collision_with_food(enemy,food)
    def on_btn_up(self):
        pass
    def on_btn_down(self):
        pass
    def on_btn_left(self):
        pass
    def on_btn_right(self):
        pass
    def on_btn_a(self):
        pass
    def on_btn_b(self):
        pass
    def input(self):
        if self.btnUp.value()==0:
            self.on_btn_up()
        if self.btnDown.value()==0:
            self.on_btn_down()
        if self.btnLeft.value()==0:
            self.on_btn_left()
        if self.btnRight.value()==0:
            self.on_btn_right()
        if self.btnA.value()==0:
            self.on_btn_a()
        if self.btnB.value()==0:
            self.on_btn_b()
    def update(self):
        for enemy in self.enemys:
            enemy.update()
            if enemy.life==0:
                self.enemys.remove(enemy)
        for food in self.foods:
            food.update()
            if food.life==0:
                self.foods.remove(food)
        for bullet in self.bullets:
            bullet.update()
            if bullet.life==0:
                self.bullets.remove(bullet)
        for bg in self.bgs:
            bg.update()
        self.player.update()
        self.collision()
        if self.player.life==0:
            self.gameover=True
        
    def show(self):
        self.tft.show(self.fb,1)
    def render(self):
        for enemy in self.enemys:
            enemy.render(self.fb)
        for food in self.foods:
            food.render(self.fb)
        for bullet in self.bullets:
            bullet.render(self.fb)
        for bg in self.bgs:
            bg.render(self.fb)
        self.player.render(self.fb)
        score_x = 160 - len(str(self.score))*8
        self.fb.text(str(self.score), score_x, 10, 1)
    def start(self):
        while self.gameover==False:
            sleep_ms(10)
            self.clear()
            self.input()
            self.update() 
            self.render()
            self.show()
        self.fb.text('game over',45, int(128/2), 1)
        self.show()
    def restart(self):
        print('restart')
        if self.gameover==True:
            self.enemys=[]
            self.foods=[]
            self.bullets=[]
            self.score=0
            self.player=self.bak_player
            self.gameover=False