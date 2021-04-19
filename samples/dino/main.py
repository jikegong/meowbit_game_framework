from game import Game
from sprite import Sprite
from res import dino,dino_a,dino_b,cactus

class MyGame(Game):
    def __init__(self):
        super().__init__()
    # override    
    def on_player_collision_with_enemy(self,player,enemy):
        player.life-=1
        enemy.life-=1
    # override
    def on_btn_up(self):
        # jump 
        if self.player.vy==0 and game.gameover==False:
            self.player.vy=-5
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

game = MyGame()

class Player(Sprite):
    def __init__(self):
        super().__init__(img=dino,x=10,y=110,vx=0,vy=0)
        self.time=0
    # override
    def update(self):
        super().update()
        if self.y<=70:
            self.vy=5
        if self.y>110:
            self.vy=0
            self.y=110
        self.time+=1
        if self.time % 2==0:
            self.setimg(dino_a)
        if self.time % 4==0:
            self.setimg(dino_b)
        if self.time % 40==0:
            game.add_enemy_sprite(Cactus())

player = Player()

class Cactus(Sprite):
    def __init__(self):
        super().__init__(img=cactus,x=160,y=110,vx=-5,vy=0)
    # override
    def update(self):
        if self.x<=-1*self.w:
            self.life=0
            game.score+=1
        super().update()

game.set_player_sprite(player)
game.add_enemy_sprite(Cactus())
game.start()
