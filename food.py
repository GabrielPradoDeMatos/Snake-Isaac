import pygame
import random
from settings import *

class Food:
    
    sprites: list[pygame.Surface]     
    image: pygame.Surface
    rect: pygame.Rect
    sprite_index: int
    
    def __init__(self, sprites_dict: dict[str,any]):
        
        self.sprites = sprites_dict['food']        
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        
        self.respawn()

    def respawn(self) -> None:        
        
        self._update_food_sprite()
      
        rand_x = random.randint(ARENA_LEFT + FOOD_PADDING, ARENA_RIGHT - FOOD_PADDING)
        rand_y = random.randint(ARENA_TOP + FOOD_PADDING, ARENA_BOTTOM - FOOD_PADDING)
        self.rect.center = (rand_x, rand_y)


    def _update_food_sprite(self):
        max_index = len(self.sprites)
        random_index = random.choices(range(max_index),FOOD_RESPAWN_WEIGHTS,k=1)
        self.sprite_index = random_index[0]
        self.image = self.sprites[self.sprite_index]



    def draw(self, surface: pygame.Surface) -> None:  
                     
        surface.blit(self.image, self.rect)
        
