import random
import pygame
from projectile import Projectile


class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.has_moved = False
        self.boost = 0
        self.score = 0
        self.health = 20
        self.max_health = self.health
        self.attack = 5
        self.velocity = 5
        self.direction = True
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load("assets/body.png")
        self.rect = self.image.get_rect()
        self.rect.x = game.mid
        self.rect.y = game.ground - self.rect.height

    def launch_projectile(self):
        if self.game.state == "meteor" or self.game.state == "loose":
            return
        if self.game.easter_egg:
            self.game.spawn_booster(random.randint(0, 1))
        if self.has_moved:
            if self.game.state == "tuto":
                self.game.play()
            if len(self.all_projectiles) < 4:
                self.all_projectiles.add(Projectile(self))

    def move_right(self):
        self.game.tuto()
        if self.game.width - self.game.border > self.rect.x + self.rect.width:
            self.image = pygame.image.load("assets/player_right.png")
            self.direction = True
            if self.game.check_collide_right(self, self.game.all_kikoos, False):
                return
            self.rect.x += self.velocity

    def move_left(self):
        self.game.tuto()
        if self.rect.x > self.game.border:
            self.image = pygame.image.load("assets/player_left.png")
            self.direction = False
            if self.game.check_collide_left(self, self.game.all_kikoos, False):
                return
            self.rect.x -= self.velocity

    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.game.loose()

    def add_score(self, number):
        self.score += number
        if (self.score >= 1000 and self.boost == 0) or (self.score >= 2000 and self.boost == 1) or \
                (self.score >= 3000 and self.boost == 2):
            self.game.spawn_booster(random.randint(0, 1))
            self.boost += 1