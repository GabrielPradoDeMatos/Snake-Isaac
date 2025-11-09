#Implementar Record
#Implementar Menu

#Menu de inicio
#   -Nova partida
#       -Solicitar o nome do jogador antes de iniciar
#   -Records (Listar os top 10)
#   -Sair
#Menu de pausa
#   -Retornar
#   -Nova partida
#   -Sair
#Som
#    -Book_page_tur ao mudar de menu
#   -character_select_left e right
#    -Menu, (Repentant,Those Responsible, The Binding of Issac,Greed, in the biginning, Penance )
#    - Apos inicar o jogo Unknown Depths Below
#   - Jogo ( Divine Combat, Repentant, S4cr1f1c14__, Dreadful, Burning Ambush)
#   - Perder derp.mp3
#   - Pegar comida SMB_large_chews_4
#   - Nascer coco fart.mp3
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
        
        self.debug_draw_bg = 0.0
        self.debug_draw_food = 0.0
        self.debug_draw_snake_body = 0.0
        self.debug_draw_snake_head = 0.0
        self.debug_draw_ui = 0.0
        self.debug_draw_flip = 0.0 # Medir o flip é MUITO importante
    
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
        # --- ATUALIZE O BLOCO DE IMPRESSÃO ---
                
                # Calcula médias
                avg_event = (self.debug_event_time / self.debug_frame_count) * 1000
                avg_update = (self.debug_update_time / self.debug_frame_count) * 1000
                
                # Novas médias de desenho
                avg_draw_bg = (self.debug_draw_bg / self.debug_frame_count) * 1000
                avg_draw_food = (self.debug_draw_food / self.debug_frame_count) * 1000
                avg_draw_body = (self.debug_draw_snake_body / self.debug_frame_count) * 1000
                avg_draw_head = (self.debug_draw_snake_head / self.debug_frame_count) * 1000
                avg_draw_ui = (self.debug_draw_ui / self.debug_frame_count) * 1000
                avg_draw_flip = (self.debug_draw_flip / self.debug_frame_count) * 1000
                
                avg_draw_total = avg_draw_bg + avg_draw_food + avg_draw_body + avg_draw_head + avg_draw_ui + avg_draw_flip

                # Imprime o novo relatório
                print(f"--- Média de Tempo (últimos {self.debug_frame_count} frames) ---")
                print(f"Eventos: {avg_event:.4f} ms")
                print(f"Update:  {avg_update:.4f} ms")
                print(f"Draw:    {avg_draw_total:.4f} ms")
                print(f"  ├─ Fundo:   {avg_draw_bg:.4f} ms")
                print(f"  ├─ Comida:  {avg_draw_food:.4f} ms")
                print(f"  ├─ Corpo:   {avg_draw_body:.4f} ms")
                print(f"  ├─ Cabeça:  {avg_draw_head:.4f} ms")
                print(f"  ├─ UI/Texto:{avg_draw_ui:.4f} ms")
                print(f"  └─ Flip:    {avg_draw_flip:.4f} ms") # O "Flip" é a atualização da tela
                print("---------------------------------")

                # Reseta os contadores
                self.debug_event_time = 0.0
                self.debug_update_time = 0.0
                self.debug_frame_count = 0
                self.debug_draw_bg = 0.0
                self.debug_draw_food = 0.0
                self.debug_draw_snake_body = 0.0
                self.debug_draw_snake_head = 0.0
                self.debug_draw_ui = 0.0
                self.debug_draw_flip = 0.0
    
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

        if self._check_collision_food(self.snake,self.food):
            self.snake.grow(self.food.sprite_index)
            self.food.respawn()

        if self.snake.check_collision_wall() or self.snake.check_collision_self():
            print("---------------------------Colisão detectada!---------------------------")
            print("-------------------------------Game Over-------------------------------")
            self.game_state = "game_over"
    
    def _draw(self) -> None:   

            # --- CAMINHO DE DEBUG (COM MEDIÇÃO) ---
            
            # t0 = Início da função _draw
            t0 = time.perf_counter() 
            
            self.screen.blit(self.sprites['background'][0], (0, 0))
            # t1 = Depois de desenhar o fundo
            t1 = time.perf_counter() 

            self.food.draw(self.screen)
            # t2 = Depois de desenhar a comida
            t2 = time.perf_counter()

            self.snake.draw_body(self.screen)
            # t3 = Depois de desenhar o corpo
            t3 = time.perf_counter()

            self.snake.draw_head(self.screen)
            # t4 = Depois de desenhar a cabeça
            t4 = time.perf_counter()

            self._draw_score()
            if self.game_state == "game_over":
                self._draw_game_over_overlay()
            # t5 = Depois de desenhar a UI (placar/game over)
            t5 = time.perf_counter()

            pygame.display.flip()
            # t6 = Depois de atualizar a tela (flip)
            t6 = time.perf_counter()

            # --- Acumula os tempos de cada etapa ---
            self.debug_draw_bg += (t1 - t0)
            self.debug_draw_food += (t2 - t1)
            self.debug_draw_snake_body += (t3 - t2)
            self.debug_draw_snake_head += (t4 - t3)
            self.debug_draw_ui += (t5 - t4)
            self.debug_draw_flip += (t6 - t5)
            
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
            
            print("Extraindo sprite das migalhas...")
            for name in LEFTOVER_SPRITE_NAMES['leftover']:
                sprite = my_spritesheet.parse_sprite(name)
                self.sprites['leftover'].append(sprite)        
                   
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
            fallback_leftover = self._create_fallback_surface(LEFTOVER_SIZE,COLOR_LEFTOVER_FALLBACK)
            
            fallback_arena = self._create_fallback_surface((ARENA_WIDTH,ARENA_HEIGHT),COLOR_ARENA_FALLBACK)
            fallback_background_arena = self._create_fallback_surface((SCREEN_WIDTH,SCREEN_HEIGHT),COLOR_BACKGROUND_FALLBACK)
            
            fallback_background_arena.blit(fallback_arena,(ARENA_LEFT,ARENA_TOP))
            
            num_head_h = len(HEAD_SPRITE_NAMES['horizontal'])
            num_head_v = len(HEAD_SPRITE_NAMES['vertical'])
            num_body_h = len(BODY_SPRITE_NAMES['horizontal'])
            num_body_v = len(BODY_SPRITE_NAMES['vertical'])
            num_food = len(FOOD_SPRITE_NAMES['food'])
            num_leftover = len(LEFTOVER_SPRITE_NAMES['leftover'])
            
            self.sprites['head']['horizontal'] = [fallback_head] * num_head_h
            self.sprites['head']['vertical'] = [fallback_head] * num_head_v
            self.sprites['body']['horizontal'] = [fallback_body] * num_body_h
            self.sprites['body']['vertical'] = [fallback_body] * num_body_v
            self.sprites['food'] = [fallback_food] * num_food
            self.sprites['leftover'] = [fallback_leftover] * num_leftover
            self.sprites['background'] = [fallback_background_arena]

    def _create_fallback_surface(self, size: tuple[int,int], color: tuple[int,int,int]) -> pygame.Surface:
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

    def _check_collision_food(self, snake: Snake, food: Food) -> bool:
        return pygame.sprite.collide_mask(snake, food)

if __name__ == "__main__":
    game = Game()   
    game.run()