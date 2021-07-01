import pygame


class Projectile(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 6
        self.direction = player.direction
        self.player = player
        if self.direction:
            self.image = pygame.image.load("assets/projectile_right.png")
            self.rect = self.image.get_rect()
            self.rect.x = player.rect.x + 35
            self.rect.y = player.rect.y + 50
        else:
            self.image = pygame.image.load("assets/projectile_left.png")
            self.rect = self.image.get_rect()
            self.rect.x = player.rect.x - 20
            self.rect.y = player.rect.y + 50

    def move(self):
        if self.direction:
            self.rect.x += self.velocity
        else:
            self.rect.x -= self.velocity
        if self.rect.x > 1080 or self.rect.x < - self.image.get_rect().width:
            self.player.all_projectiles.remove(self)