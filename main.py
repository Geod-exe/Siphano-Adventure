import random
import pygame
from game import Game

pygame.init()

(width, length) = 1080, 720
pygame.display.set_caption("Siphano's Adventures")
screen = pygame.display.set_mode((width, length))
pygame.display.set_icon(pygame.image.load("assets/icon.ico"))

game = Game(width, length)

background = pygame.image.load("assets/bg.png")
banner = pygame.image.load("assets/banner.png")
loose = pygame.image.load("assets/loose.jpg")
siphano = pygame.image.load("assets/siphano's head.jpg")

play_text = pygame.font.SysFont('Comic Sans MS', 30)
play_text = play_text.render("Appuyez sur espace pour jouer", False, (255, 255, 255))

tuto = pygame.font.SysFont('Comic Sans MS', 30)
tuto = tuto.render("Utilisez le fleches directionneles pour bouger", False, (255, 255, 255))

tuto2 = pygame.font.SysFont('Comic Sans MS', 30)
tuto2 = tuto2.render("Utilisez espace pour tirer", False, (255, 255, 255))

reset_text = pygame.font.SysFont('Comic Sans MS', 30)
reset_text = reset_text.render("Appuyez sur espace pour rejouer", False, (255, 255, 255))

easter_egg = pygame.font.SysFont('Comic Sans MS', 30)
easter_egg = easter_egg.render("Vous avez trouvé l'easter egg", False, (255, 255, 255))

running = True
while running:

    screen.blit(background, (0, 0))
    if game.state != "victory":
        for meteor in game.all_meteors:
            meteor.check()
        for booster in game.all_boosters:
            booster.check()
        for kikoo in game.all_kikoos:
            kikoo.move()
        for projectile in game.player.all_projectiles:
            projectile.move()

        game.all_meteors.draw(screen)
        game.all_boosters.draw(screen)
        game.all_kikoos.draw(screen)
        game.player.all_projectiles.draw(screen)

        if game.pressed.get(pygame.K_RIGHT) or game.pressed.get(pygame.K_d):
            game.player.move_right()
        if game.pressed.get(pygame.K_LEFT) or game.pressed.get(pygame.K_q):
            game.player.move_left()
        screen.blit(game.player.image, game.player.rect)

        if game.easter_egg:
            screen.blit(easter_egg, (width / 2 - easter_egg.get_width() / 2, length - 75))
            screen.blit(siphano, (0, length - siphano.get_height()))
            screen.blit(siphano, (width - siphano.get_width(), length - siphano.get_height()))

        if game.state == "start":
            screen.blit(banner, (width / 2 - banner.get_width() / 2, 0))
            screen.blit(play_text, (width / 2 - play_text.get_width() / 2, length / 2))
            screen.blit(game.best_text, (width / 2 - game.best_text.get_width() / 2, length - 100))
        elif game.state == "tuto":
            screen.blit(tuto, (width / 2 - tuto.get_width() / 2, length / 2.3))
            screen.blit(tuto2, (width / 2 - tuto2.get_width() / 2, length / 2.1))
        elif game.state == "kikoo":
            pv = pygame.font.SysFont('Comic Sans MS', 30)
            pv = pv.render("    Pv : " + str(game.player.health) + "/" + str(game.player.max_health), False,
                           (255, 255, 255))
            screen.blit(pv, (0, 0))

            score = pygame.font.SysFont('Comic Sans MS', 30)
            score = score.render("Score : " + str(game.player.score) + "    ", False, (255, 255, 255))
            screen.blit(score, (width - score.get_width(), 0))
        elif game.state == "meteor":
            game.check_meteor()

            pv = pygame.font.SysFont('Comic Sans MS', 30)
            pv = pv.render("    Pv : " + str(game.player.health) + "/" + str(game.player.max_health), False,
                           (255, 255, 255))
            screen.blit(pv, (0, 0))

            score = pygame.font.SysFont('Comic Sans MS', 30)
            score = score.render("Score : " + str(game.player.score) + "    ", False, (255, 255, 255))
            screen.blit(score, (width - score.get_width(), 0))
        elif game.state == "loose":
            screen.blit(loose, (0, 0))
            screen.blit(reset_text, (width / 2 - reset_text.get_width() / 2, length - 200))
    else:
        game.frigiel.check()

        if game.frigiel.discussion_phase > 0:
            frigiel = pygame.font.SysFont('Comic Sans MS', 30)
            frigiel = frigiel.render(game.frigiel.text, False, (255, 255, 255))
            screen.blit(frigiel, (width / 2 - frigiel.get_width() / 2, length - 100))

        screen.blit(game.player.image, game.player.rect)
        screen.blit(game.frigiel.image, game.frigiel.rect)

        if game.frigiel.discussion_phase > 4:
            screen.blit(pygame.image.load("assets/The End.png"), (0, 0))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_SPACE:
                if game.state == "tuto" or game.state == "kikoo" or game.state == "meteor":
                    game.player.launch_projectile()
                elif game.state == "start":
                    game.start()
                elif game.state == "loose":
                    game = Game(width, length)

            if event.key == pygame.K_h:
                if game.state == "kikoo":
                    game.easter_egg = True

            if event.key == pygame.K_j:
                if game.state == "kikoo":
                    game.skip = True
                elif game.state == "meteor":
                    game.victory()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
