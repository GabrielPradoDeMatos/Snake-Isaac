import pygame
import json
import os

class Spritesheet:
    
    filename: str
    sprite_sheet: pygame.Surface
    meta_data: str
    data:dict[str,
              dict[str,
                   dict[str,int]]]   
    
    
    
    def __init__(self, filename: str):
        self.filename = filename
        try:            
            self.sprite_sheet = pygame.image.load(filename).convert_alpha() #convert_alpha : otimiza a imagem para o formato da tela e preserva a transparência
        except pygame.error as e:
            print(f"Erro, {e} ,ao carregar a imagem da spritesheet: {filename}")
            raise e
        
        self.meta_data = self.filename.replace('.png', '.json') #Pegar os dados do arquivo JSON para mapear as texturas
        
        try:
            with open(self.meta_data) as f:                
                self.data = json.load(f) #Atributo data recebe um dicionário de dicionários com as informacoes do JSON
        except FileNotFoundError:
            print(f"Erro: Não foi encontrado o arquivo JSON: {self.meta_data}")
            raise
        except json.JSONDecodeError:
            print(f"Erro: O arquivo JSON não está em um formato adequado: {self.meta_data}")
            raise

    def parse_sprite(self, name: str) -> pygame.Surface:
        try:                    
            sprite_data = self.data['frames'][name]['frame'] #Recebe um dicionário com as informacoes, x,y,w,h da sprite solicitada 
            x = sprite_data["x"]
            y = sprite_data["y"]
            w = sprite_data["w"]
            h = sprite_data["h"]

            image = self.get_sprite(x, y, w, h)
            return image
        except KeyError:
            print(f"Erro: Sprite com o nome '{name}' não encontrado no JSON ({self.meta_data}).")
            raise

    def get_sprite(self, x: int, y: int, w: int, h: int) -> pygame.Surface:        
        sprite = pygame.Surface((w, h), pygame.SRCALPHA) #Cria uma surface que suporta transparência        
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h)) #Argumento opcional do blit é Area = An optional area rectangle can be passed as well. This represents a smaller portion of the source Surface to draw.
        return sprite