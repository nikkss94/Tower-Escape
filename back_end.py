from tkinter import *
import time
import random
from pathlib import Path


class Game():
    def __init__(self, canvas, teleportation, list_coins, monsters):
        self.canvas = canvas
        self.platform = Platform(self.canvas)
        self.pos_list = []
        self.teleportation = teleportation
        self.hero = Hero(self.canvas, self.teleportation)
        self.hero_pos = self.hero.get_pos()
        self.flag = True
        self.monsters = monsters
        self.list_coins = list_coins
        self.score = 0
        self.start_game_time = time.time()
        self.flag = False

    def coins_list_pos(self):
        self.hero_pos = self.hero.get_pos()
        self.coins_pos = []
        for c in self.list_coins:
            if c is not None:
                pos = self.canvas.coords(c.get_id())
                if pos[0] == self.hero_pos[0] and \
                   (self.hero_pos[1] - pos[1] < 60):
                    self.canvas.delete(c.get_id())
                    self.list_coins.remove(c)
                    self.score += 1
                    self.platform.draw_score(self.score)
        self.canvas.after(10, self.coins_list_pos)

    def draw_bomb(self):
        monster_life = 0
        if self.hero.bomb_id is not None:
            bomb_pos = self.canvas.coords(self.hero.bomb_id)
            for monster in self.monsters:
                monster_pos = monster.get_pos()
                if (bomb_pos[0] == monster_pos[0] + 30) and \
                   (bomb_pos[1] - monster_pos[1] < 100):
                    self.canvas.delete(self.hero.bomb_id)
                    self.hero.bomb_id = None
                    monster_life = monster.get_life()
                    if monster_life == 0:
                        monster.set_flag()
                        self.canvas.delete(monster.id)
                        self.monsters.remove(monster)
        self.canvas.after(10, self.draw_bomb)

    def draw_platform(self):
        self.platform.draw_background()
        self.platform.draw_paddle()
        self.platform.draw_door()
        self.platform.draw_fire()
        self.platform.draw_score(0)
        for teleport in self.teleportation:
            teleport.draw_teleport()
        for coin in self.list_coins:
            if coin is not None:
                coin.draw_coins()

    def draw_monsters(self):
        for monster in self.monsters:
            monster.draw()
            monster.move()

    def draw_hero(self):
        self.hero.draw_hero()
        self.hero.animate()

    def start_game(self):
        self.draw_platform()
        self.draw_monsters()
        self.draw_hero()
        self.coins_list_pos()
        self.draw_bomb()
        self.win_game()
        self.game_over()

    def game_over(self):
        self.hero_pos = self.hero.get_pos()
        for monster in self.monsters:
            monster_pos = monster.get_pos()
            if (self.hero_pos[0] == monster_pos[0] + 30) and\
               (self.hero_pos[1] - monster_pos[1] < 100):
                # stop all afters
                self.canvas.create_text(500, 300, text='Game Over !',
                                        font=('Tempus Sans ITC', 60), fill="white")
                for monster in self.monsters:
                    monster.stop_draw()
                self.hero.stop_draw()
                self.flag = True
        self.canvas.after(10, self.game_over)

    def win_game(self):
        self.hero_pos = self.hero.get_pos()
        if self.hero_pos[0] <= 100 and self.hero_pos[1] <= 135.0:
            self.canvas.create_text(500, 300, text='YOU WIN !',
                                    font=('Tempus Sans ITC', 60), fill="white")
            self.flag = True
            if self.flag:
                current_time = time.time()
                total_time = current_time - self.start_game_time
                bonus_score = 100 - int(total_time)
                self.platform.draw_score(bonus_score)
                self.flag = False
                for monster in self.monsters:
                    monster.stop_draw()
                self.hero.stop_draw()
        self.canvas.after(10, self.win_game)


class Platform():
    def __init__(self, canvas):
        self.canvas = canvas
        self.score = 0
        self.text = None

    def draw_background(self):
        self.bg = PhotoImage(file=convert("images/wall.gif"))
        w = self.bg.width()
        h = self.bg.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x * w, y * h, image=self.bg,
                                         anchor='nw')

    def draw_paddle(self):
        self.b = PhotoImage(file=convert("images/jump.gif"))
        w = self.b.width()
        h = self.b.height()
        for x in range(0, 4):
            paddle_1 = self.canvas.create_image(
                x * w, h * 3, image=self.b, anchor='nw')
            paddle_2 = self.canvas.create_image(
                x * w, h * 8, image=self.b, anchor='nw')
            paddle_3 = self.canvas.create_image(
                x * w, h * 13.7, image=self.b, anchor='nw')

    def draw_door(self):
        self.photo_image = PhotoImage(file=convert("images/tower.gif"))
        self.door_id = self.canvas.create_image(
            10, 10, image=self.photo_image, anchor='nw')
        self.door_pos = self.canvas.coords(self.door_id)

    def draw_fire(self):
        self.fire_image = PhotoImage(file=convert("images/fire1.gif"))
        self.canvas.create_image(140, 30, image=self.fire_image, anchor='nw')
        self.canvas.create_image(440, 30, image=self.fire_image, anchor='nw')
        self.canvas.create_image(740, 30, image=self.fire_image, anchor='nw')
        self.canvas.create_image(100, 160, image=self.fire_image, anchor='nw')
        self.canvas.create_image(700, 160, image=self.fire_image, anchor='nw')
        self.canvas.create_image(800, 360, image=self.fire_image, anchor='nw')
        self.canvas.create_image(300, 510, image=self.fire_image, anchor='nw')

    def draw_score(self, score):
        if score > 0:
            self.score = score
        else:
            self.score = 0
        self.canvas.delete(self.text)
        self.text = self.canvas.create_text(880, 40, text='Score:' + str(score),
                                            font=('Helvetica', 20))


class Teleport():
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.teleport = PhotoImage(file=convert("images/teleport.gif"))
        self.x = x
        self.y = y
        self.teleport_id = None

    def draw_teleport(self):
        self.teleport_id = self.canvas.create_image(
            self.x, self.y, image=self.teleport, anchor='nw')


class Coins():
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.photo = PhotoImage(file=convert("images/coin.gif"))
        self.x = x
        self.y = y
        self.id = None

    def draw_coins(self):
        self.id = self.canvas.create_image(self.x, self.y,
                                           image=self.photo, anchor='nw')

    def get_id(self):
        return self.id


class Monster():
    def __init__(self, canvas, x, y, monster_photo, life):
        self.canvas = canvas
        self.life = life
        self.x = x
        self.y = y
        self.monster_photo = monster_photo
        self.photo_image = PhotoImage(file=convert(self.monster_photo))
        self.move_x = -1
        self.move_y = 0
        self.flag = True
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.id = None
        self.flag = True

    def get_pos(self):
        return self.canvas.coords(self.id)

    def draw(self):
        self.id = self.canvas.create_image(
            self.x, self.y, image=self.photo_image, anchor='nw')

    def stop_draw(self):
        self.flag = False

    def get_life(self):
        self.life -= 1
        return self.life

    def move(self):
        if self.flag:
            self.canvas.move(self.id, self.move_x, self.move_y)
            pos = self.canvas.coords(self.id)
            if self.flag and pos[0] <= -20:
                self.move_x = 1
            if self.flag and pos[0] >= 900 and pos[0] <= 960:
                self.move_x = -1
        self.canvas.after(10, self.move)

    def set_flag(self):
        self.flag = False

    def destroy_monster(self):
        canvas.delete(self.id)


class Hero():
    def __init__(self, canvas, teleportation):
        self. teleportation = teleportation
        self.canvas = canvas
        self.flag = True
        self.id = None
        self.x = -4
        self.y = 0
        self.bomb_id = None
        self.current_image = 0
        self.current_image_add = 1
        self.last_time = time.time()
        canvas.bind_all('<KeyPress-Left>', self.turn_left)
        canvas.bind_all('<KeyPress-Right>', self.turn_right)
        canvas.bind_all('<space>', self.gun)
        self.hit_bottom = False
        self.photo_1 = PhotoImage(file=convert("images/figure-R1.gif"))
        self.photo_2 = PhotoImage(file=convert("images/figure-R2.gif"))
        self.photo_3 = PhotoImage(file=convert("images/figure-R3.gif"))
        self.images_right = [self.photo_1, self.photo_2, self.photo_3]
        pos_1 = self.canvas.coords(self.photo_1)
        pos_2 = self.canvas.coords(self.photo_2)
        pos_3 = self.canvas.coords(self.photo_3)
        self.photo_4 = PhotoImage(file=convert("images/figure-L1.gif"))
        self.photo_5 = PhotoImage(file=convert("images/figure-L2.gif"))
        self.photo_6 = PhotoImage(file=convert("images/figure-L3.gif"))
        self.images_left = [self.photo_4, self.photo_5, self.photo_6]
        self.image = self.canvas.create_image(
            100, 570, image=self.images_left[0], anchor='nw')

    def draw_hero(self):
        self.image = self.canvas.create_image(
            100, 570, image=self.images_left[0], anchor='nw')

    def stop_draw(self):
        self.flag = False

    def get_pos(self):
        return self.canvas.coords(self.image)

    def turn_left(self, evt):
        if self.y == 0:
            self.x = -4

    def turn_right(self, evt):
        if self.y == 0:
            self.x = 4

    def gun(self, evt):
        if self.flag:
            pos1 = self.canvas.coords(self.image)
            self.bomb = PhotoImage(file=convert("images/bomb.gif"))
            self.bomb_id = self.canvas.create_image(
                pos1[0] + 2, pos1[1], image=self.bomb, anchor='nw')

    def animate(self):  # make hero moves
        if self.flag:
            if self.x != 0 and self.y == 0:
                if time.time() - self.last_time > 0.1:
                    self.last_time = time.time()
                    self.current_image += self.current_image_add
                    if self.current_image >= 2:
                        self.current_image_add = -1
                    if self.current_image <= 0:
                        self.current_image_add = 1
            if self.x < 0:
                self.canvas.itemconfig(
                    self.image, image=self.images_left[self.current_image])
            elif self.x > 0:
                self.canvas.itemconfig(
                    self.image, image=self.images_right[self.current_image])
            self.canvas.move(self.image, self.x, self.y)
            pos1 = self.canvas.coords(self.image)
            if self.x >= 990:
                self.x = 0
                right = False
            if self.x <= 0:
                self.x = 0
                left = False
                right = False
            elif self.x > 0:
                self.x = 0
                left = False
            if pos1[0] == 932.0 and pos1[1] == 570:
                self.canvas.delete(self.image)
                self.image = self.canvas.create_image(900, 435,
                                                      image=self.images_left[0], anchor='nw')
            if pos1[0] == 40:
                self.canvas.delete(self.image)
                self.image = self.canvas.create_image(10, 245,
                                                      image=self.images_left[0], anchor='nw')

            if pos1[0] == 930.0 and pos1[1] == 245:
                self.canvas.delete(self.image)
                self.image = self.canvas.create_image(500, 73,
                                                      image=self.images_left[0], anchor='nw')
        self.canvas.after(10, self.animate)


def convert(a):  # take adress of gif image
    p = Path(a).resolve()
    path = str(p)
    rawstr = r"\ "
    path.replace(rawstr[0], "/")
    return path
