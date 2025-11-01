#Coisas para arrumar em algum momento:
#1 - As texturas estão deformando apos aplicar o pygame.transform.scale
#2 - Adicionar animacao nas texturas

import pygame
import sys
import os
import json


from settings import *
from spritesheet import Spritesheet
from snake import Snake
from food import Food

class Game:
    
    snake: Snake
    food: Food
    
    screen: pygame.Surface
    clock: pygame.time.Clock
    
    game_state: str
    sprites: dict[str,
                dict[str,
                        list[pygame.Surface]]]
    
    score_font: pygame.font.Font
    game_over_font: pygame.font.Font
    restart_font: pygame.font.Font
        
    def __init__(self):
        
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        pygame.display.set_caption("Snake - Isaac")        

        #Carregar as texturas, caso as texturas nao sejam carregadas serão subistituidas por cores sólidas que estão definidas no arquivo settings.py
        self._load_assets()
        self._create_fonts()
        
        self.game_state = "playing"

        #Cria os objetos do jogo
        self._start_new_game()
        
    #Loop principal
    def run(self) -> None:        
        while True:
            # 1. Processar Eventos (Input)
            self._handle_events()
            
            # 2. Atualizar Lógica do Jogo
            self._update()
            
            # 3. Desenhar na Tela
            self._draw()
            
            # 4. Controlar FPS, ou seja, esse loop é executado a cada (1/FPS)segundos, 
            self.clock.tick(FPS)
    
    def _handle_events(self) -> None:
        #pygame.event.get() pega TODOS os evendos registrados desde a última vez que o comando pygame.event.get() foi chamado
        #ao chamar o o pygame.event.get() a fila de eventos que foi registrada é resetada
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()            

            if self.game_state == "playing":
                self.snake.handle_input(event)
                
            elif self.game_state == "game_over":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self._start_new_game()

    def _update(self) -> None:       
        if self.game_state != "playing":
            return
                    
        self.snake.update()
        
        #Verifica colisão da cobra com a comida
        if self.snake.check_collision_food(self.food.rect):
            #Se comer a comida muda de lugar
            self.food.respawn() 
            
        #Verifica colisões de fim de jogo
        if self.snake.check_collision_wall() or self.snake.check_collision_self():
            print("---------------------------Colisão detectada!---------------------------")
            print("-------------------------------Game Over-------------------------------")
            self.game_state = "game_over"
    
    def _draw(self) -> None:   

        self.screen.blit(self.sprites['background']['background'][0], (0, 0)) 

        self.food.draw(self.screen)
        self.snake.draw_body(self.screen)
        self.snake.draw_head(self.screen)
        
        #Desenha o placar
        self._draw_score()
        
        # 4. Desenha a tela de Game Over (se aplicável)
        if self.game_state == "game_over":
            self._draw_game_over_overlay()

        # 5. Atualiza o display
        pygame.display.flip()

    def _quit_game(self) -> None:
        print("Encerrando o jogo...")
        pygame.quit()
        quit()             

    def _load_assets(self) -> None:
        full_spritesheet_path = os.path.join(ASSET_PATH, SPRITESHEET_FILENAME)
        
        #Dicionário para armazenar as sprites
        self.sprites = {
            'head': {'horizontal': [], 'vertical': []},
            'body': {'horizontal': [], 'vertical': []},
            'food': {'food':[]},
            'background':{'background':[]},
            'leftover': {'leftover':[]}
        }
        
        try:
            print(f"Carregando spritesheet de: {full_spritesheet_path}")
            my_spritesheet = Spritesheet(full_spritesheet_path)
            
            print("Extraindo sprites da cabeça da cobra, lá ele...")
            for name in HEAD_SPRITE_NAMES['horizontal']:
                sprite = my_spritesheet.parse_sprite(name)
                self.sprites['head']['horizontal'].append(pygame.transform.scale(sprite, HEAD_SIZE))
            for name in HEAD_SPRITE_NAMES['vertical']:
                sprite = my_spritesheet.parse_sprite(name)
                self.sprites['head']['vertical'].append(pygame.transform.scale(sprite, HEAD_SIZE))

            print("Extraindo sprites da cobra (corpo)...")
            for name in BODY_SPRITE_NAMES['horizontal']:
                sprite = my_spritesheet.parse_sprite(name)
                self.sprites['body']['horizontal'].append(pygame.transform.scale(sprite, BODY_SIZE))
            for name in BODY_SPRITE_NAMES['vertical']:
                sprite = my_spritesheet.parse_sprite(name)
                self.sprites['body']['vertical'].append(pygame.transform.scale(sprite, BODY_SIZE))
            
            print("Extraindo sprite da comida...")
            for name in FOOD_SPRITE_NAMES['food']:
                sprite = my_spritesheet.parse_sprite(name)
                self.sprites['food']['food'].append(pygame.transform.scale(sprite,FOOD_SIZE))            
                   
            print("Carregando cenário...")
            background_path = os.path.join(ASSET_PATH, ARENA_FILENAME)
            self.sprites['background']['background'].append(pygame.image.load(background_path).convert())
            
            print("Sprites carregadas com sucesso! :^}\n")

        except (pygame.error, FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"--- Erro! ---")
            print(f"Erro: Não foi possível carregar as texturas: {e}")
            print("O jogo será carregado com texturas sólidas :^| .")
            print("-------------------------------------------------\n")            
       
            fallback_head = self._create_fallback_surface(HEAD_SIZE, COLOR_HEAD_FALLBACK)
            fallback_body = self._create_fallback_surface(BODY_SIZE, COLOR_BODY_FALLBACK)
            fallback_food = self._create_fallback_surface(FOOD_SIZE,COLOR_FOOD_FALLBACK)
            fallback_background = self._create_fallback_surface((SCREEN_WIDTH,SCREEN_HEIGHT),COLOR_BACKGROUND_FALLBACK)
                        
            self.sprites['head']['horizontal'] = [fallback_head]
            self.sprites['head']['vertical'] = [fallback_head]
            self.sprites['body']['horizontal'] = [fallback_body]
            self.sprites['body']['vertical'] = [fallback_body]
            self.sprites['food']['food'] = [fallback_food]
            self.sprites['background']['background'] = [fallback_background]

    def _create_fallback_surface(self, size: int, color: tuple[int,int,int]) -> pygame.Surface:
        surface = pygame.Surface(size)
        surface.fill(color)
        return surface
    
    def _create_fonts(self) -> None:
        try:
            self.score_font = pygame.font.Font(MAIN_FONT_PATH, SCORE_FONT_SIZE)
            self.game_over_font = pygame.font.Font(MAIN_FONT_PATH, GAME_OVER_FONT_SIZE)
            self.restart_font = pygame.font.Font(MAIN_FONT_PATH, RESTART_FONT_SIZE)
        except(FileNotFoundError) as e:
            
            print(f"--- Erro! ---")
            print(f"Erro: Não foi possível carregar as fontes: {e}")
            print("O jogo será carregado com fontes padrão :^| .")
            print("-------------------------------------------------\n") 
               
            self.score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
            self.game_over_font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
            self.restart_font = pygame.font.Font(None, RESTART_FONT_SIZE)
        
    def _start_new_game(self) -> None:  
              
        print("Iniciando novo jogo...")
        
        self.game_state = "playing"        
        self.snake = Snake(self.sprites) 
        self.food = Food(self.sprites)

    def _draw_score(self) -> None:
        score_text = f"Placar: {self.snake.score}"
        #Para desenhar texto na tela é necessário criar uma surface com o texto
        score_surf = self.score_font.render(score_text, True, COLOR_WHITE)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(score_surf, score_rect)

    def _draw_game_over_overlay(self) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        go_surf = self.game_over_font.render("VOCÊ PERDEU!", True, COLOR_WHITE)
        go_rect = go_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        
        restart_surf = self.restart_font.render("Pressione [R] para reiniciar", True, COLOR_WHITE)
        restart_rect = restart_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        
        self.screen.blit(go_surf, go_rect)
        self.screen.blit(restart_surf, restart_rect)




# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    # 1. Cria uma instância do Jogo
    game = Game()
    # 2. Inicia o loop principal
    game.run()