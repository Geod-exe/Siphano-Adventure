import pygame


class Kikoo(pygame.sprite.Sprite):

    def __init__(self, game, direction):
        super().__init__()
        self.game = game
        self.health = 15
        self.max_health = self.health
        self.cooldown = 0
        self.max_cooldown = 20
        self.attack = 1
        self.velocity = 4
        self.direction = direction
        if self.direction:
            self.image = pygame.image.load("assets/kikoo_right.png")
            self.rect = self.image.get_rect()
            self.rect.x = 0 - self.rect.width
        else:
            self.image = pygame.image.load("assets/kikoo_left.png")
            self.rect = self.image.get_rect()
            self.rect.x = game.width
        self.rect.y = game.ground - self.rect.height

    def check_death(self):
        if self.health <= 0:
            self.game.all_kikoos.remove(self)
            self.game.player.add_score(50)
            if (self.game.player.score >= 1500 and self.game.state == "kikoo") or self.game.skip:
                if len(self.game.all_kikoos) == 0:
                    self.game.skip = False
                    self.game.meteor()
                return
            self.game.spawn_kikoo(self.direction)
            if len(self.game.all_kikoos) == 1:
                self.game.spawn_kikoo(self.game.opposite(self.direction))

    def check_projectile(self, direction):
        for projectile in self.game.player.all_projectiles:
            if direction:
                result = projectile.rect.x - self.rect.x
            else:
                result = self.rect.x - projectile.rect.x
            if 0 < result < projectile.rect.width:
                self.health -= self.game.player.attack
                self.game.player.add_score(10)
                self.check_death()
                self.game.player.all_projectiles.remove(projectile)
                return True
        return False

    def move(self):
        if self.direction:
            self.check_projectile(True)
            if not self.game.check_collide_right(self, self.game.player, True):
                self.rect.x += self.velocity
            else:
                self.attack_player()
        else:
            self.check_projectile(False)
            if not self.game.check_collide_left(self, self.game.player, True):
                self.rect.x -= self.velocity
            elif self.cooldown == 0:
                self.game.player.damage(self.attack)
                self.cooldown = self.max_cooldown
            else:
                self.cooldown -= 1

    def attack_player(self):
        if self.cooldown == 0:
            self.game.player.damage(self.attack)
            self.cooldown = self.max_cooldown
        else:
            self.cooldown -= 1