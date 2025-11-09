import pygame
import random
from settings import *

class Food(pygame.sprite.Sprite):
    
    sprites: list[pygame.Surface]     
    image: pygame.Surface
    mask: pygame.Mask
    rect: pygame.Rect
    sprite_index: int
    position_history: list[tuple[tuple[int,int],int]]
    
    def __init__(self, sprites_dict: dict[str,any]):
                
        super().__init__()
                
        self.food_sprites = sprites_dict['food']    
        self.leftover_sprites = sprites_dict['leftover'] 
              
        self.food_image = self.food_sprites[0]
        self.sprite_index = 0
        
        self.rect = self.food_image.get_rect()
        
        self.position_history = []
        self.respawn()

    def respawn(self) -> None:        
                
        self._update_food_sprite()
      
        rand_x = random.randint(ARENA_LEFT + FOOD_PADDING, ARENA_RIGHT - FOOD_PADDING)
        rand_y = random.randint(ARENA_TOP + FOOD_PADDING, ARENA_BOTTOM - FOOD_PADDING)
        self.rect.center = (rand_x, rand_y)
        leftover_rect = self.rect.move(0,10)
        self.position_history.append((self.sprite_index,leftover_rect.copy()))
        
    def _update_food_sprite(self):
        
        max_index = len(self.food_sprites)
        random_index = random.choices(range(max_index),FOOD_RESPAWN_WEIGHTS,k=1)
        self.sprite_index = random_index[0]
        self.food_image = self.food_sprites[self.sprite_index]
        self.mask = pygame.mask.from_surface(self.food_image)

    def draw(self, surface: pygame.Surface) -> None: 
        self._draw_leftover(surface)                      
        surface.blit(self.food_image, self.rect)        
                
    def _draw_leftover(self,surface: pygame.Surface) -> None:                  
        for sprite_index,rect in self.position_history[:-1]:            
            surface.blit(self.leftover_sprites[sprite_index],rect)
