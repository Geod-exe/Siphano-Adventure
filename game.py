import pygame

from frigiel import Frigiel
from booster import Booster
from kikoo import Kikoo
from meteor import Meteor
from player import Player
from os import path


class Game:

    def __init__(self, width, length):
        self.state = "start"  # start, tuto, kikoo, meteor, loose, victory
        (self.width, self.length) = width, length
        (self.mid, self.ground) = (width/2 - 25, 600)
        self.player = Player(self)
        self.frigiel = None
        self.easter_egg = False
        self.spawn = 8
        self.max_spawn = self.spawn
        self.all_kikoos = pygame.sprite.Group()
        self.all_boosters = pygame.sprite.Group()
        self.all_meteors = pygame.sprite.Group()
        self.pressed = {}
        self.border = 50
        self.skip = False
        if not path.isfile("best.txt"):
            with open("best.txt", "w+") as file:
                file.write("0")
                file.close()
        with open("best.txt", "r") as file:
            self.best = int(file.read())
            file.close()
        self.best_text = pygame.font.SysFont('Comic Sans MS', 60)
        self.best_text = self.best_text.render("Meilleur Score : " + str(self.best), False, (255, 255, 255))

    def spawn_booster(self, type):
        if self.state == "meteor":
            self.all_boosters.add(Booster(self, 0))
        else:
            self.all_boosters.add(Booster(self, type))

    def spawn_kikoo(self, direction):
        self.all_kikoos.add(Kikoo(self, direction))

    def spawn_meteor(self):
        self.all_meteors.add(Meteor(self))

    def check_meteor(self):
        if self.player.score >= 3500:
            if len(self.all_meteors) == 0:
                self.victory()
            return
        if self.spawn == 0:
            self.spawn_meteor()
            self.spawn = self.max_spawn
        else:
            self.spawn -= 1

    def start(self):
        self.state = "tuto"
        self.player.rect.x = self.mid
        self.player.rect.y = self.ground - self.player.rect.height
        self.player.image = pygame.image.load("assets/body.png")

    def play(self):
        self.state = "kikoo"
        self.spawn_kikoo(self.opposite(self.player.direction))

    def meteor(self):
        self.easter_egg = False
        self.state = "meteor"

    def loose(self):
        self.state = "loose"
        if self.best < self.player.score:
            with open("best.txt", "w") as file:
                file.write(str(self.player.score))
                file.close()

    def victory(self):
        self.easter_egg = False
        self.state = "victory"
        self.frigiel = Frigiel(self)
        self.player.move_right()
        if self.best < self.player.score:
            with open("best.txt", "w") as file:
                file.write(str(self.player.score))
                file.close()

    def opposite(self, boolean):
        if boolean:
            opposite = False
        else:
            opposite = True
        return opposite

    def check_collide_right(self, sprite, target, mode):
        if mode:
            if target.rect.x > sprite.rect.x and 0 < target.rect.x - sprite.rect.x < sprite.rect.width + 10:
                return True
            else:
                return False
        else:
            for targets in target:
                if targets.rect.x > sprite.rect.x and 0 < targets.rect.x - sprite.rect.x < sprite.rect.width + 10:
                    return True
            return False


    def check_collide_left(self, sprite, target, mode):
        if mode:
            if target.rect.x < sprite.rect.x and 0 < sprite.rect.x - target.rect.x < sprite.rect.width + 20:
                return True
            else:
                return False
        else:
            for targets in target:
                if targets.rect.x < sprite.rect.x and 0 < sprite.rect.x - targets.rect.x < sprite.rect.width + 20:
                    return True
            return False

    def tuto(self):
        if self.state == "tuto":
            self.player.has_moved = True