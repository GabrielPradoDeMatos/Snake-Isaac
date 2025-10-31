# Classe que representa o coco da cobra
# Se sobrar tempo implementar a funcao de seed
import pygame
import random
from settings import *

#Para iniciar a comida é necessário passar a textura da comida
class Food:
    
    sprites: dict[str,
                    dict[str,
                            list[pygame.Surface]]] 
    
    image: pygame.Surface
    rect: pygame.Rect
    
    
    def __init__(self, sprites_dict: dict[str,
                                          dict[str,
                                               list[pygame.Surface]]]):
        
        self.sprites = sprites_dict
        
        self.image = self.sprites['food']['food'][0]
        self.rect = self.image.get_rect()
        
        self.respawn()

    #Gera a comida em um lugar aleatório no mapa
    def respawn(self) -> None:
        #Transformar isso em uma funcão
        self.image = self.sprites['food']['food'][random.randint(0,6)]
        
        # Gera a comida DENTRO dos limites da arena
        # Adiciona um pequeno "padding" (ex: 10 pixels) para não nascer colado na parede
        padding = 10 
        
        rand_x = random.randint(ARENA_LEFT + padding, ARENA_RIGHT - padding)
        rand_y = random.randint(ARENA_TOP + padding, ARENA_BOTTOM - padding)
        self.rect.center = (rand_x, rand_y)

    #Desenha a comida na tela
    def draw(self, surface: pygame.Surface) -> None:  
                     
        surface.blit(self.image, self.rect)