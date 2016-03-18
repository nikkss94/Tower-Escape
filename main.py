from tkinter import *
from pathlib import Path
from back_end import *
from database import *


class Begining():
    def __init__(self, tk):
        self.tk = tk
        self.tk.title("Tower Escape")
        self.canvas = Canvas(self.tk, width=990, height=600)
        self.canvas.pack()
        self.flag_levels = False
        self.flag_quit = False
        self.name = StringVar()
        self.background()
        self.score = 0
        self.flag_level1 = False
        self.flag_level2 = False
        self.flag_level3 = False
        self.f = False
        self.check_name = False
        self.data_inp_1 = ""

    def save_score(self):
        self.player = self.name.get()
        add_player(self.player, self.score)

    def star(self):
        self.data_inp_1 = self.name.get()
        if self.data_inp_1 != "":
            self.check_name = True
            self.flag_levels = True
            self.save_score()
            self.entry.destroy()
            self.canvas.delete("all")
            self.background()
            self.levels()
        else:
            self.canvas.create_text(480, 500, text='Please enter your nickname!',
                                    font=('Tempus Sans ITC', 25), fill="red")

    def background(self):
        self.bg = PhotoImage(file=convert("images/back.gif"))
        w = self.bg.width()
        h = self.bg.height()
        for x in range(0, 4):
            for y in range(0, 4):
                self.canvas.create_image(
                    x * w, y * h, image=self.bg, anchor='nw')

    def levels(self):
        level3_button = Button(self.tk, text="Level 3", width=15,
                               command=self.start_level_3, bg="black", fg="white", font=('Tempus Sans ITC', 15))
        level2_button = Button(self.tk, text="Level 2", command=self.start_level_2, width=15,
                               bg="black", fg="white", font=('Tempus Sans ITC', 15))
        level1_button = Button(self.tk, text="Level 1", command=self.start_game, width=15,
                               bg="black", fg="white", font=('Tempus Sans ITC', 15))
        level3_button_window = self.canvas.create_window(
            475, 360, anchor='n', window=level2_button)
        level2_button_window = self.canvas.create_window(
            475, 260, anchor='n', window=level1_button)
        level1_button_window = self.canvas.create_window(
            475, 460, anchor='n', window=level3_button)
        self.canvas.create_text(
            480, 100, text='Levels', font=('Tempus Sans ITC', 100), fill="white")
        if self.flag_level1 == True:
            self.start_game()
        if self.flag_level2 == True:
            self.start_level_2()
        if self.flag_level3 == True:
            self.start_level_3()

    def main(self):
        self.entry = Entry(
            self.tk, textvariable=self.name, width=15, font=('Tempus Sans ITC', 20))
        self.entry.place(x=340, y=250)
        quit_button = Button(self.tk, text="Quit", command=self.quit, width=15, bg="black", fg="white",
                             font=('Tempus Sans ITC', 15))
        start_button = Button(self.tk, text="Start", command=self.star, width=15, bg="black", fg="white",
                              font=('Tempus Sans ITC', 15))
        best_score_button = Button(self.tk, text="Best Score", command=self.best_score, width=15, bg="black", fg="white",
                              font=('Tempus Sans ITC', 15))
        quit_button_window = self.canvas.create_window(
            640, 400, anchor='n', window=quit_button)
        start_button_window = self.canvas.create_window(
            360, 400, anchor='n', window=start_button)
        best_score_button_window = self.canvas.create_window(
            500, 500, anchor='n', window=best_score_button)
        self.canvas.create_text(
            500, 100, text='Tower Escape', font=('Tempus Sans ITC', 80), fill="white")
        if self.flag_levels == True:
            self.star()
        if self.flag_quit == True:
            self.quit()

    def best_score(self):
        self.entry.destroy()
        self.canvas.delete("all")
        self.background()
        self.canvas.create_text(
            500, 100, text='Best Score', font=('Tempus Sans ITC', 80), fill="white")
        best_score = best_player()
        x = 0
        count = 0
        for score in best_score:
            count += 1
            self.canvas.create_text(
            400, 240 + x, text=str(score[0]), font=('Tempus Sans ITC', 30), fill="white")
            self.canvas.create_text(
            550, 240 + x, text=str(score[1]), font=('Tempus Sans ITC', 30), fill="white")
            x += 50
            if count == 6:
                break


    def quit(self):
        self.flag_quit = True
        self.tk.destroy()

    def start_game(self):
        self.canvas.delete("all")
        self.flag_level1 = True
        self.Level_1()

    def start_level_2(self):
        self.canvas.delete("all")
        self.flag_level2 = True
        self.Level_2()

    def start_level_3(self):
        self.canvas.delete("all")
        self.flag_level3 = True
        self.Level_3()

    def Level_1(self):
        teleportation = [Teleport(self.canvas, 880, 500), Teleport(self.canvas, -15, 360),
                         Teleport(self.canvas, 880, 165)]
        list_coins = [
            Coins(self.canvas, 200, 550), Coins(self.canvas, 900, 420)]
        monsters = [Monster(self.canvas, 600, 175, "images/moch.gif", 1), Monster(
            self.canvas, 600, 505, "images/moch.gif", 1)]
        game = Game(self.canvas, teleportation, list_coins, monsters)
        game.start_game()
        

    def Level_2(self):
        teleportation = [Teleport(self.canvas, 880, 500), Teleport(
            self.canvas, -15, 360), Teleport(self.canvas, 880, 165)]
        list_coins = [Coins(self.canvas, 200, 550), Coins(self.canvas, 900, 420), Coins(self.canvas, 840, 420),
                      Coins(self.canvas, 780, 420), Coins(self.canvas, 300, 220)]
        monsters = [Monster(self.canvas, 800, 505, "images/moch.gif", 1), Monster(self.canvas, 900, 505, "images/moch.gif", 1),
                    Monster(self.canvas, 600, 5, "images/moch.gif", 1), Monster(self.canvas, 800, 175, "images/moch.gif", 1)]
        game = Game(self.canvas, teleportation, list_coins, monsters)
        game.start_game()
        

    def Level_3(self):
        teleportation = [Teleport(self.canvas, 880, 500), Teleport(
            self.canvas, -15, 360), Teleport(self.canvas, 880, 165)]
        list_coins = [Coins(self.canvas, 200, 550), Coins(self.canvas, 900, 420), Coins(self.canvas, 840, 420),
                      Coins(self.canvas, 780, 420), Coins(
                          self.canvas, 300, 220), Coins(self.canvas, 780, 45),
                      Coins(self.canvas, 360, 220), Coins(self.canvas, 720, 45)]
        monsters = [Monster(self.canvas, 300, 368, "images/moch.gif", 1), Monster(self.canvas, 200, 368, "images/moch.gif", 1),
                    Monster(self.canvas, 600, 175, "images/moch.gif", 1), Monster(
                        self.canvas, 800, 505, "images/moch.gif", 1),
                    Monster(self.canvas, 100, 160, "images/big_one.gif", 2), Monster(self.canvas, 800, 5, "images/moch.gif", 1)]
        game = Game(self.canvas, teleportation, list_coins, monsters)
        game.start_game()
        
    


tk = Tk()
begin = Begining(tk)
begin.main()
tk.mainloop()
