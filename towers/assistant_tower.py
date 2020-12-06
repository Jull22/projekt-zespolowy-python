import pygame
from .tower import Tower
import os
import math
import time

range_img= [pygame.transform.scale(pygame.image.load(os.path.join("game_assets/supportTower", "range_tower" + ".png")),(100, 130)),
        pygame.transform.scale(pygame.image.load(os.path.join("game_assets/supportTower", "range_tower2" + ".png")),(190, 150))]


class RangeTower(Tower):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.zone = 150
        self.tower_imgs= range_img[:]
        self.effect=[0.2, 0.4]

    def draw(self, win):
        super().draw(win)
        super().draw_zone(win)


    def support(self, towers):

        effected = []
        for tower in towers:
            x= tower.x
            y= tower.y

            dis= math.sqrt((self.x - x)**2 + (self.y - y)** 2)

            if dis <= self.zone:
                effected.append(tower)

        for tower in effected:
            tower.zone += round(tower.zone * self.effect[self.level - 1])





damage_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("game_assets/supportTower", "damage_tower" + ".png")),(150, 150)),
                                      pygame.transform.scale(pygame.image.load(os.path.join("game_assets/supportTower", "damage_tower2" + ".png")),(150, 150))]

class DamageTower(RangeTower):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.zone = 150
        self.tower_imgs= damage_imgs[:]
        self.effect= [1, 2]


    def draw(self, win):

        super().draw(win)
        super().draw_zone(win)

    def support(self, towers):
        """zwiększa zasięg wieży w zasięgu """
        effected = []
        for tower in towers:
            x= tower.x
            y= tower.y

            dis= math.sqrt((self.x - x)**2 + (self.y - y)** 2)

            if dis <= self.zone:
                effected.append(tower)

        for tower in effected:
            tower.damage += tower.original_zone + round(tower.zone * self.effect[self.level - 1])

