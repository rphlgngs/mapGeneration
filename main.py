import pygame
from map import *

# Initialisation de pygame
pygame.init()

infos_ecran = pygame.display.Info()

# Création de la surface sur laquelle on dessinera
screen = pygame.display.set_mode((1080, 768))

images_ground = [pygame.image.load('assets/ground/sand.png'),
                 pygame.image.load('assets/ground/sand_with_stone.png')]

images_ressources = [pygame.image.load('assets/ressources/stone1.png'),
                     pygame.image.load('assets/ressources/stone2.png')]

map = Map(screen, ((1080 / 2) - 32, (768 / 4)), images_ground, images_ressources, 11)

# Variable pour la boucle principale
running = True

# Boucle principale
while running:

    # On écoute les évenements
    for event in pygame.event.get():
        # Si l'évenement est "quitter"
        if event.type == pygame.QUIT:
            # La variable running devient fausse
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                map.update(pygame.K_SPACE)
            if event.key == pygame.K_UP:
                map.update(pygame.K_UP)
            if event.key == pygame.K_RIGHT:
                map.update(pygame.K_RIGHT)
            if event.key == pygame.K_LEFT:
                map.update(pygame.K_LEFT)
            if event.key == pygame.K_DOWN:
                map.update(pygame.K_DOWN)

        if pygame.mouse.get_pressed()[0]:
            map.recolte(pygame.mouse.get_pos())

    # On affiche un fond noir
    screen.fill(pygame.Color("black"))

    map.draw()
    map.mouse_detection(pygame.mouse.get_pos())

    # On rafraichit l'écran
    pygame.display.flip()
