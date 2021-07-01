import pygame
import random


class Booster(pygame.sprite.Sprite):

    def __init__(self, game, type):
        super().__init__()
        self.game = game
        self.type = type
        self.collected = False
        self.velocity = 5
        self.time = 1000
        self.changed_data = None
        self.image = pygame.image.load("assets/booster/" + str(type) + ".png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, game.width - 50)
        self.rect.y = - self.image.get_height()
        self.ground = game.ground - self.rect.height

    def check(self):
        if self.collected:
            self.undo_effect()
            if self.time == 0:
                self.game.all_boosters.remove(self)
                return
            self.apply_effect()
            self.time -= 1
        elif self.rect.y < self.ground:
            self.rect.y += self.velocity
            if self.rect.y > self.ground:
                self.rect.y = self.ground
        if (self.game.check_collide_right(self, self.game.player, True)
            or self.game.check_collide_left(self, self.game.player, True)) and \
                self.rect.y >= self.game.ground - self.game.player.rect.height:
            self.collect()

    def collect(self):
        self.collected = True
        self.rect.x = self.game.width / 2 - self.rect.width / 2
        self.rect.y = 0

    def apply_effect(self):
        if self.type == 0:
            result = self.game.player.health + self.game.player.max_health / 2
            if result > self.game.player.max_health:
                self.game.player.health = self.game.player.max_health
            else:
                self.game.player.health = result
            self.game.all_boosters.remove(self)
        elif self.type == 1:
            self.changed_data = self.game.player.attack
            self.game.player.attack += 3

    def undo_effect(self):
        if self.changed_data is not None:
            if self.type == 1:
                self.game.player.attack = self.changed_data
