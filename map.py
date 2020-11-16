import pygame
import random


# Classe "Tiles" représentant les sprites de la map (dalles du sol, objets ...)
class Tiles(pygame.sprite.Sprite):

    def __init__(self, images, id_image, position, zoom):
        super().__init__()  # On initialise le constructeur de la classe mère

        self.zoom = zoom

        # Attributs de la classe
        self.id_image = id_image
        self.images = self.__transform_image(images)
        self.image = self.images[self.id_image]
        self.rect = self.image.get_rect()   # On récupère le rectangle de l'image
        self.rect.x, self.rect.y = position   # On place le rectangle de l'image à la position désirée

    def __transform_image(self, images):
        lst_conv = []
        for image in images:
            lst_conv.append(pygame.transform.rotozoom(image, 0, self.zoom).convert_alpha())

        return lst_conv

    def update_id_image(self, new_id):
        self.id_image = new_id
        self.image = self.images[self.id_image]


# Classe map représentant la map
class Map:

    def __init__(self, surface, origine, images_ground, images_ressources, size):

        self.surface = surface
        self.size = size
        self.origine_x, self.origine_y = origine
        self.images_ground = images_ground
        self.images_ressources = images_ressources

        self.all_sprite = []
        self.all_ressource = pygame.sprite.Group()

        self.__generate_sprite()

    def __generate_sprite(self):
        """
        Fonction qui permet de générer la map
        """
        self.all_sprite.clear()
        for line in range(self.size):
            self.all_sprite.append([])
            for column in range(self.size):
                id_image = random.randint(0, 50)
                if id_image < 50:
                    id_image = 0
                else:
                    id_image = 1
                x = self.origine_x + (column * self.images_ground[id_image].get_rect().height / 2) - \
                    (line * self.images_ground[id_image].get_rect().height / 2)
                y = self.origine_y + (line * self.images_ground[id_image].get_rect().height / 4) + \
                    (column * self.images_ground[id_image].get_rect().width / 4)
                self.all_sprite[line].append(Tiles(self.images_ground, id_image, (x, y), 1.05))

    def draw(self):
        for line in range(self.size):
            for column in range(self.size):
                self.surface.blit(self.all_sprite[line][column].image, (self.all_sprite[line][column].rect.x,
                                                                        self.all_sprite[line][column].rect.y))

    def update(self, key):
        if key == pygame.K_SPACE:
            self.__generate_sprite()
        if key == pygame.K_UP:
            copy = self.__copy_dir(self.all_sprite, "up")

            # Effet de déplacement vers le haut
            for line in range(1, self.size):
                for column in range(1, self.size):
                    self.all_sprite[line][column].update_id_image(copy[line - 1][column - 1])
                    if line - 1 == 0:
                        self.__change_on_move(line-1, column-1)
                    if column - 1 == 0:
                        self.__change_on_move(line-1, column-1)

            del copy
        if key == pygame.K_RIGHT:
            copy = self.__copy_dir(self.all_sprite, "right")
            for line in range(1, self.size):
                for column in range(self.size - 1):
                    self.all_sprite[line][column].update_id_image(copy[line-1][column])
                    if line - 1 == 0:
                        self.__change_on_move(line - 1, column)
                    else:
                        self.__change_on_move(line - 1, self.size - 1)
            del copy
        if key == pygame.K_LEFT:
            copy = self.__copy_dir(self.all_sprite, "left")
            for line in range(self.size - 1):
                self.__change_on_move(line, 0)
                for column in range(1, self.size):
                    self.all_sprite[line][column].update_id_image(copy[line][column-1])
                    if line + 1 == self.size - 1:
                        self.__change_on_move(line+1, column-1)
            del copy
        if key == pygame.K_DOWN:
            copy = self.__copy_dir(self.all_sprite, "down")

            for line in range(self.size - 1):
                for column in range(self.size - 1):
                    self.all_sprite[line][column].update_id_image(copy[line][column])
                    if line + 1 == self.size - 1:
                        self.__change_on_move(line + 1, column + 1)
                    if column + 1 == self.size - 1:
                        self.__change_on_move(line + 1, column + 1)

            del copy

    def __change_on_move(self, line, column):
        id_image = random.randint(0, 50)
        if id_image < 50:
            id_image = 0
        else:
            id_image = 1
        self.all_sprite[line][column] = Tiles(self.images_ground, id_image,
                                              (self.all_sprite[line][column].rect.x,
                                               self.all_sprite[line][column].rect.y), 1.05)

    @staticmethod
    def __copy_dir(matrice, direction):
        copy = []
        if direction == "up":
            len_copy = len(matrice) - 1
            for i in range(len_copy):
                copy.append([])
                for j in range(len_copy):
                    copy[i].append(matrice[i][j].id_image)
        elif direction == "down":
            len_copy = len(matrice)
            for i in range(1, len_copy):
                copy.append([])
                for j in range(1, len_copy):
                    copy[i-1].append(matrice[i][j].id_image)
        elif direction == "right":
            for i in range(len(matrice)):
                copy.append([])
                for j in range(1, len(matrice)):
                    copy[i].append(matrice[i][j].id_image)
        elif direction == "left":

            for i in range(1, len(matrice)):
                copy.append([])
                for j in range(len(matrice) - 1):
                    copy[i-1].append(matrice[i][j].id_image)

        return copy

    def mouse_detection(self, mouse_position):
        for line in self.all_sprite:
            for sprite in line:
                if sprite.rect.collidepoint(mouse_position) and sprite.id_image == 1:
                    font = pygame.font.Font(None, 24)
                    text = font.render("Stone", 1, (255, 255, 255))
                    self.surface.blit(text, (mouse_position[0] + 10, mouse_position[1] - 15))

    def recolte(self, mouse_position):
        for line in self.all_sprite:
            for sprite in line:
                if sprite.rect.collidepoint(mouse_position) and sprite.id_image == 1:
                    sprite.id_image = 0
                    sprite.image = pygame.transform.rotozoom(self.images_ground[0], 0, 1.05).convert_alpha()
