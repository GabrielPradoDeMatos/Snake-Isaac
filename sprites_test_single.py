import pygame
import json
import os
import sys

# --- CLASSE SPRITESHEET (Copiada do seu spritesheet.py) ---
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
            self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Erro, {e} ,ao carregar a imagem da spritesheet: {filename}")
            raise e
        
        self.meta_data = self.filename.replace('.png', '.json')
        
        try:
            with open(self.meta_data) as f:                
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"Erro: Não foi encontrado o arquivo JSON: {self.meta_data}")
            raise
        except json.JSONDecodeError:
            print(f"Erro: O arquivo JSON não está em um formato adequado: {self.meta_data}")
            raise

    def parse_sprite(self, name: str) -> pygame.Surface:
        try:                    
            sprite_data = self.data['frames'][name]['frame'] 
            x = sprite_data["x"]
            y = sprite_data["y"]
            w = sprite_data["w"]
            h = sprite_data["h"]

            image = self.get_sprite(x, y, w, h)
            return image
        except KeyError:
            # Em vez de quebrar o programa, levantamos um KeyError
            # para que o loop principal possa capturá-lo
            raise KeyError(f"Sprite '{name}' não encontrado no JSON.")

    def get_sprite(self, x: int, y: int, w: int, h: int) -> pygame.Surface:        
        sprite = pygame.Surface((w, h), pygame.SRCALPHA)       
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h)) 
        return sprite

# --- 1. Configurações do Visualizador ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
COLOR_BACKGROUND = (30, 30, 30) # Cinza escuro
COLOR_WHITE = (230, 230, 230)
COLOR_ERROR = (255, 100, 100)
COLOR_INPUT_BOX = (50, 50, 50)

# --- 2. Inicialização do Pygame ---
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Testador Individual de Sprites (Digite o nome e pressione Enter)")
clock = pygame.time.Clock()

# Fontes
font_ui = pygame.font.Font(None, 32)
font_sprite_name = pygame.font.Font(None, 24)
font_error = pygame.font.Font(None, 30)

# --- 3. Lógica de Carregamento de Assets ---
# (Exatamente como no seu settings.py)
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd() 

ASSET_PATH = os.path.join(SCRIPT_DIR, "assets") 
SPRITESHEET_FILENAME = "snake_sprites.png"
full_spritesheet_path = os.path.join(ASSET_PATH, SPRITESHEET_FILENAME)

# Variáveis de estado
loading_failed = False
load_error_message = ""
my_spritesheet = None

# Variáveis para o testador
input_text = ""
current_sprite = None
current_sprite_name = ""
display_error_message = ""


try:
    print(f"Carregando spritesheet de: {full_spritesheet_path}")
    my_spritesheet = Spritesheet(full_spritesheet_path)
    print("Spritesheet carregada com sucesso.")
    print("Digite o nome de um sprite (ex: head_h_1, food_3) e pressione Enter.")

except Exception as e:
    print(f"\n--- ERRO FATAL AO CARREGAR ASSETS ---")
    print(f"Erro: {e}")
    loading_failed = True
    load_error_message = str(e)


# --- 4. Loop Principal (Interativo) ---
running = True
while running:
    
    # --- Tratamento de Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            # Se a spritesheet foi carregada, permite digitação
            if not loading_failed:
                if event.key == pygame.K_RETURN: # Tecla Enter
                    if input_text:
                        try:
                            # Tenta carregar o sprite
                            current_sprite = pygame.transform.scale_by(my_spritesheet.parse_sprite(input_text),8)
                            current_sprite_name = input_text
                            display_error_message = ""
                        except KeyError as e:
                            # Erro se o nome não for encontrado
                            current_sprite = None
                            current_sprite_name = ""
                            display_error_message = str(e)
                        input_text = "" # Limpa o texto
                
                elif event.key == pygame.K_BACKSPACE: # Tecla Backspace
                    input_text = input_text[:-1] # Remove o último caractere
                else:
                    input_text += event.unicode # Adiciona o caractere digitado

    # --- Lógica de Desenho ---
    screen.fill(COLOR_BACKGROUND)

    if loading_failed:
        # Erro fatal: Não foi possível carregar o .png ou .json
        title_surf = font_error.render("Falha ao carregar assets:", True, COLOR_ERROR)
        msg_surf = font_error.render(load_error_message, True, COLOR_WHITE)
        help_surf = font_error.render("Verifique o console. Pressione ESC para sair.", True, COLOR_WHITE)
        screen.blit(title_surf, (20, 20))
        screen.blit(msg_surf, (20, 60))
        screen.blit(help_surf, (20, 120))
        
    else:
        # --- Desenha a UI Interativa ---
        
        # 1. Instruções
        help_text = font_ui.render("Digite o nome do sprite e pressione Enter:", True, COLOR_WHITE)
        screen.blit(help_text, (20, 30))
        
        # 2. Caixa de input
        input_box_rect = pygame.Rect(20, 70, SCREEN_WIDTH - 40, 40)
        pygame.draw.rect(screen, COLOR_INPUT_BOX, input_box_rect)
        pygame.draw.rect(screen, COLOR_WHITE, input_box_rect, 1) # Borda
        
        input_surf = font_ui.render(input_text, True, COLOR_WHITE)
        screen.blit(input_surf, (input_box_rect.x + 10, input_box_rect.y + 10))

        # 3. Área de exibição do Sprite
        display_area_y = 140
        
        if current_sprite:
            # Se um sprite foi carregado, exibe
            screen.blit(current_sprite, (40, display_area_y))
            
            # Desenha o nome e dimensões
            w = current_sprite.get_width()
            h = current_sprite.get_height()
            name_text = f"Nome: '{current_sprite_name}' (Tam: {w}x{h}px)"
            name_surf = font_sprite_name.render(name_text, True, COLOR_WHITE)
            screen.blit(name_surf, (40 + w + 20, display_area_y + 10))
            
        elif display_error_message:
            # Se deu erro ao carregar (ex: nome errado), exibe o erro
            error_surf = font_error.render(display_error_message, True, COLOR_ERROR)
            screen.blit(error_surf, (40, display_area_y))


    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60) # Roda a 60 FPS para input suave

# --- 5. Fim ---
pygame.quit()
sys.exit()