import random
import pygame


class Meteor(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.damage = 2
        self.velocity = 6
        self.image = pygame.image.load("assets/meteor_" + str(random.randint(0, 1)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, game.width - 50)
        self.rect.y = - self.image.get_height()
        self.ground = game.ground - self.rect.height

    def check(self):
        if self.rect.y < self.ground:
            self.rect.y += self.velocity
        else:
            self.delete()
            self.game.player.add_score(15)
        if (self.game.check_collide_right(self, self.game.player, True)
            or self.game.check_collide_left(self, self.game.player, True)) and \
                self.rect.y >= self.game.ground - self.game.player.rect.height:
            self.touch_player()

    def touch_player(self):
        self.delete()
        self.game.player.damage(self.damage)

    def delete(self):
        self.game.all_meteors.remove(self)
