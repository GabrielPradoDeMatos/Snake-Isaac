#Coisas para arrumar em algum momento:
#1 - As texturas estão deformando apos aplicar o pygame.transform.scale
#2 - Adicionar animacao nas texturas

import pygame
import sys
import os
import json
import time

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
    sprites: dict[str, any]
    
    score_font: pygame.font.Font
    game_over_font: pygame.font.Font
    restart_font: pygame.font.Font
        
    def __init__(self):
        
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        pygame.display.set_caption("Snake - Isaac")        

        self._load_assets()
        self._create_fonts()
        
        self.game_state = "playing"

        self._start_new_game()        
        
        self.debug_event_time = 0.0
        self.debug_update_time = 0.0
        self.debug_draw_time = 0.0
        self.debug_frame_count = 0
    
    def run(self) -> None: 
               
        while True:            

            start_time = time.perf_counter()

            self._handle_events()

            time_after_events = time.perf_counter()

            self._update()

            time_after_update = time.perf_counter()

            self._draw()

            time_after_draw = time.perf_counter()

            self.clock.tick(FPS)

            self.debug_event_time += (time_after_events - start_time)
            self.debug_update_time += (time_after_update - time_after_events)
            self.debug_draw_time += (time_after_draw - time_after_update)
            self.debug_frame_count += 1

            if self.debug_frame_count >= FPS:
                avg_event = (self.debug_event_time / self.debug_frame_count) * 1000
                avg_update = (self.debug_update_time / self.debug_frame_count) * 1000
                avg_draw = (self.debug_draw_time / self.debug_frame_count) * 1000

                print(f"--- Média de Tempo (últimos {self.debug_frame_count} frames) ---")
                print(f"Eventos: {avg_event:.4f} ms")
                print(f"Update:  {avg_update:.4f} ms")
                print(f"Draw:    {avg_draw:.4f} ms")
                print("---------------------------------")

                self.debug_event_time = 0.0
                self.debug_update_time = 0.0
                self.debug_draw_time = 0.0
                self.debug_frame_count = 0
    
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

        if self.snake.check_collision_food(self.food.rect):
            self.food.respawn() 

        if self.snake.check_collision_wall() or self.snake.check_collision_self():
            print("---------------------------Colisão detectada!---------------------------")
            print("-------------------------------Game Over-------------------------------")
            self.game_state = "game_over"
    
    def _draw(self) -> None:   

        self.screen.blit(self.sprites['background'][0], (0, 0)) 

        self.food.draw(self.screen)
        self.snake.draw_body(self.screen)
        self.snake.draw_head(self.screen)

        self._draw_score()

        if self.game_state == "game_over":
            self._draw_game_over_overlay()

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
            'food': [],
            'background':[],
            'leftover': []
        }
        
        try:
            print(f"Carregando spritesheet de: {full_spritesheet_path}")
            my_spritesheet = Spritesheet(full_spritesheet_path)
            
            print("Extraindo sprites da cabeça da cobra, lá ele...")
            for name in HEAD_SPRITE_NAMES['horizontal']:
                sprite = my_spritesheet.parse_sprite(name)
                self.sprites['head']['horizontal'].append(sprite) #self.sprites['head']['horizontal'].append(pygame.transform.scale(sprite, HEAD_SIZE))
            for name in HEAD_SPRITE_NAMES['vertical']:
                sprite = my_spritesheet.parse_sprite(name)
                self.sprites['head']['vertical'].append(sprite)

            print("Extraindo sprites da cobra (corpo)...")
            for name in BODY_SPRITE_NAMES['horizontal']:
                sprite = my_spritesheet.parse_sprite(name)
                self.sprites['body']['horizontal'].append(sprite)
            for name in BODY_SPRITE_NAMES['vertical']:
                sprite = my_spritesheet.parse_sprite(name)
                self.sprites['body']['vertical'].append(sprite)
            
            print("Extraindo sprite da comida...")
            for name in FOOD_SPRITE_NAMES['food']:
                sprite = my_spritesheet.parse_sprite(name)
                self.sprites['food'].append(sprite)          
                   
            print("Carregando cenário...")
            background_path = os.path.join(ASSET_PATH, ARENA_FILENAME)
            self.sprites['background'].append(pygame.image.load(background_path).convert())
            
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
            self.sprites['food'] = [fallback_food]
            self.sprites['background'] = [fallback_background]

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
              
        print("Iniciando novo jogo...\n")
        
        self.game_state = "playing"        
        self.snake = Snake(self.sprites) 
        self.food = Food(self.sprites)

    def _draw_score(self) -> None:
        score_text = f"Placar: {self.snake.score}"        
        score_surf = self.score_font.render(score_text, True, COLOR_WHITE) #Para desenhar texto na tela é necessário criar uma surface com o texto
        score_rect = score_surf.get_rect(center=(SCORE_X_POSITION, SCORE_Y_POSITION))
        self.screen.blit(score_surf, score_rect)

    def _draw_game_over_overlay(self) -> None:
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        go_surf = self.game_over_font.render(MENSAGE_GO, True, COLOR_WHITE)
        go_rect = go_surf.get_rect(center=(MENSAGE_GO_X_POSITION, MENSAGE_GO_Y_POSITION))
        
        restart_surf = self.restart_font.render(MENSAGE_RESTART, True, COLOR_WHITE)
        restart_rect = restart_surf.get_rect(center=(MENSAGE_RESTART_X_POSITION, MENSAGE_RESTART_Y_POSITION))
        
        self.screen.blit(go_surf, go_rect)
        self.screen.blit(restart_surf, restart_rect)

if __name__ == "__main__": # __name__ == "__main__" quando o arquivo main.py é executado diretamente    
    game = Game()   
    game.run()