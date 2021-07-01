import pygame


class Frigiel(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.state = "move" # wait / move, speak, give, smack
        self.wait_time = None
        self.wait_for = None
        self.discussion_phase = 0
        self.text = None
        self.velocity = 5
        self.stop = game.player.rect.x + game.player.rect.width + 50
        self.image = pygame.image.load("assets/frigiel.png")
        self.rect = self.image.get_rect()
        self.rect.x = game.width
        self.rect.y = game.ground - self.rect.height

    def check(self):
        if self.state == "waiting":
            self.waiting()
        elif self.state == "move":
            self.move()
        elif self.state == "speak":
            self.speak()

    def move(self):
        self.rect.x -= self.velocity
        if self.rect.x <= self.stop:
            self.rect.x = self.stop
            self.wait(20, 0)

    def speak(self):
        if self.discussion_phase == 1:
            self.text = "Heyy Siphano !"
            self.wait(100, 0)
        elif self.discussion_phase == 2:
            self.text = "Tu a reussi toute ces epreuves"
            self.wait(130, 0)
        elif self.discussion_phase == 3:
            self.text = "Voici ta recompense !"
            self.wait(100, 0)
        elif self.discussion_phase == 4:
            self.text = "Vous avez gagné: Un Bisou De Frigiel"
            self.wait(100, 0)

    def wait(self, time, status):
        self.wait_time = time
        self.wait_for = status
        self.state = "waiting"

    def waiting(self):
        self.wait_time -= 1
        if self.wait_time == 0:
            if isinstance(self.wait_for, str):
                self.state = self.wait_for
            else:
                self.discussion_phase += 1
                self.state = "speak"
            self.wait_for = None
            self.wait_time = None