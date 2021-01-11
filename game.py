import pygame
import os
from enemies.red import Red
from enemies.ghost import Ghost
from enemies.wiz import Wiz
from towers.archer_tower import ArcherTowerLong, ArcherTowerShort
from towers.assistant_tower import RangeTower, DamageTower
from menu import star
from menu import VerticalMenu, PausePlayButton

import random
import time

pygame.font.init()

health_img = pygame.image.load(os.path.join("game_assets", "heart.png"))
menu_side= pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu-side.png")), (90, 480))

menu_side_icon1= pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu-icon.png")), (70, 70))
menu_side_icon2= pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu-icon2.png")), (70, 70))
menu_side_icon3= pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu-icon3.png")), (70, 70))
menu_side_icon4= pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu-icon4.png")), (70, 70))

start_btn= pygame.transform.scale(pygame.image.load(os.path.join("game_assets/buttons", "start.png")), (110, 45))
pause_btn=pygame.transform.scale(pygame.image.load(os.path.join("game_assets/buttons", "pause.png")), (110, 45))

play_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/buttons", "play.png")), (70, 70))

attack_tower_names = ["archer", "archer2"]
assistant_tower_names = ["range", "damage"]
# star_img = pygame.image.load(os.path.join("game_assets", "star.png"))


#fale wrogów
#(ghost, red, wizard)
waves= [[20,0,0],[40,0,0],[60,0,0],[0,20,0],[0,40,0],[0,60,0],[20,40,0],[20,30,20],[30,50,60],[40,60,80],[100,60,50]]

class Game:
    def __init__(self):
        self.width = 1200
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = []
        self.support_towers = [DamageTower(200, 300), RangeTower(850, 200)]
        self.attack_towers = [ArcherTowerLong(300, 300), ArcherTowerShort(900, 300)]
        self.lives = 10
        self.money = 2500
        self.bg = pygame.image.load(os.path.join("game_assets", "background.jpg"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        # self.clicks=[]  #needed just to get PATH
        self.timer = time.time()
        self.health_font = pygame.font.SysFont("sourcesanspro", 40, bold=200)
        self.selected_tower = None
        self.moving_object= None
        self.wave= 0
        self.current_wave= waves[self.wave][:]
        self.pause= True
        self.pausePlayBtn = PausePlayButton(start_btn, pause_btn, self.width-300,  self.height-50)

        self.menu= VerticalMenu(self.width- menu_side.get_width() + 20, 350, menu_side)
        self.menu.add_btn(menu_side_icon1, "buy_damage", 1500)
        self.menu.add_btn(menu_side_icon2, "buy_range", 1000)
        self.menu.add_btn(menu_side_icon3, "buy_archer", 500)
        self.menu.add_btn(menu_side_icon4, "buy_archer2", 700)


    def gen_enemies(self):
        """
        generuje wrogów dla odpowiednich poziomów trudności
        :return:enemy
        """
        if sum(self.current_wave) == 0 :
            self.wave+= 1
            self.current_wave= waves[self.wave]
            self.pause = True
        else:
            enemies_names = [Ghost(), Red(), Wiz()]

            for x in range(len(self.current_wave)):
                if self.current_wave[x] !=0:
                    self.enemys.append(enemies_names[x])
                    self.current_wave[x] = self.current_wave[x] - 1
                    break


    def run(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            # pygame.time.delay(0)
            clock.tick(80)
            if self.pause==False :
                if time.time() - self.timer >= 0.5:  # co ile sekund ma wychodzić nowy wróg
                    self.timer = time.time()
                    self.gen_enemies()

            position = pygame.mouse.get_pos()
            if self.moving_object:
                self.moving_object.move(position[0]-20,position[1]+50)

           #główna pętla
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    run = False

                # pos= pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.moving_object:

                        if self.moving_object.name in attack_tower_names:
                            self.attack_towers.append(self.moving_object)
                        elif self.moving_object.name in assistant_tower_names:
                            self.support_towers.append(self.moving_object)

                        self.moving_object.moving = False
                        self.moving_object = None


                    else:
                        #sprawdza czy gra jest w stanie start/pause
                        if (self.pausePlayBtn.click(position[0], position[1])):
                            self.pause = not(self.pause)
                            self.pausePlayBtn.paused=self.pause  #zmiana obrazka na start lub pause


                        #sprawdza czy wybieramy opcję z menu bocznego

                        side_menu_button= self.menu.get_clicked(position[0],position[1])
                        if side_menu_button:
                            cost=self.menu.get_item_cost(side_menu_button)
                            if self.money >= cost:
                                self.money-= cost
                                self.add_tower(side_menu_button)


                        #sprawdza czy wieża jest wybrana
                        btn_clicked= None
                        if self.selected_tower:
                            btn_clicked =  self.selected_tower.menu.get_clicked(position[0], position[1])
                            if btn_clicked:
                                if btn_clicked == "Upgrade":
                                    cost= self.selected_tower.get_upgrade_cost()
                                    if self.money >= cost:
                                        self.money-= cost
                                        self.selected_tower.upgrade()

                        if not(btn_clicked):
                            for tw in self.attack_towers:
                                if tw.click(position[0], position[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                    if btn_clicked == "Upgrade":
                                        cost = self.selected_tower.get_upgrade_cost()
                                        if self.money >= cost:
                                            self.money -= cost
                                            self.selected_tower.upgrade()
                                else:
                                    tw.selected = False

                            for tow in self.support_towers:
                                tow.selected= False
                                if tow.click(position[0], position[1]):
                                    tow.selected = True
                                    self.selected_tower = tow
                                    if btn_clicked == "Upgrade":
                                        cost = self.selected_tower.get_upgrade_cost()
                                        if self.money >= cost:
                                            self.money -= cost
                                            self.selected_tower.upgrade()

                                else:
                                    tow.selected = False

            if self.pause==False:
                to_delete = []
                for en in self.enemys:
                    en.move()
                    if en.x < -20:
                        to_delete.append(en)
                        self.lives-=1

                # usuwa wrogów, którzy wyszli poza ekran
                for d in to_delete:
                    self.enemys.remove(d)

                # przechodzi przez wieże i sprawdza czy wróg jest w strefie ataku
                for tow in self.attack_towers:
                    self.money+= tow.attack(self.enemys)

                # sprawdza czy wieże atakujące się w strefie
                for t in self.support_towers:
                    t.support(self.attack_towers)

                # przegrana
                if self.lives <= 0:
                    print("Porażka")
                    run = False

            self.draw()



        pygame.quit()

    def draw(self):

        self.win.blit(self.bg, (0, 0))
        # for click in self.clicks:
        #     pygame.draw.circle(self.win, (255,0,0), (click[0], click[1]), 3, 1)

        # narysuj wroga
        for enemy in self.enemys:
            enemy.draw(self.win)

        if self.moving_object:
            self.moving_object.draw(self.win)

        # narysuj wieże i łuczników
        for tow in self.attack_towers:
            tow.draw(self.win)

        # narysuj wieże wspierające
        for tower in self.support_towers:
            tower.draw(self.win)

        # narysuj serca- życia
        text = self.health_font.render(str(self.lives), 1, (0, 0, 0))

        life = pygame.transform.scale(health_img, (50, 50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 1, 30))
        self.win.blit(life, (start_x, 25))

        # narysuj gwiazdki jako waluta
        text = self.health_font.render(str(self.money), 1, (0, 0, 0))

        money = pygame.transform.scale(star, (50, 50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 1, 100))
        self.win.blit(money, (start_x, 100))

        #narysuj menu boczne
        self.menu.draw(self.win)

        #narysuj przyciski start/pause
        self.pausePlayBtn.draw(self.win)

        pygame.display.update()

    def add_tower(self, name):
        x, y=pygame.mouse.get_pos()
        name_list=["buy_damage", "buy_range", "buy_archer2", "buy_archer"]
        object_list = [DamageTower(x,y), RangeTower(x,y), ArcherTowerLong(x,y), ArcherTowerShort(x,y) ]

        try:
            obj=object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as exc:
            print(str(exc) + "wrong name")



g = Game()
g.run()
