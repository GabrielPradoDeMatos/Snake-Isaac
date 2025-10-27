# settings.py
# Arquivo para guardar todas as constantes e configurações do jogo.

import os

# --- 1. Configurações de Tela e Jogo ---
SCREEN_WIDTH = 918
SCREEN_HEIGHT = 612
FPS = 30
SNAKE_SPEED = 8

# --- 2. Configurações da Cobra ---
HEAD_SIZE = (35, 38)
BODY_SIZE = (27, 23)
#HEAD_SIZE = (35, 35)
#BODY_SIZE = (27, 22)
HEAD_P = 0.75 # Percentual da cabeça para cooldown de curva
BODY_SPACING = 4 # Espaçamento entre os segmentos do corpo

# --- 3. Configurações da Comida ---
FOOD_SIZE = (27, 28)

# --- 4. Cores (Usadas como fallback e para UI) ---
COLOR_BLACK = (255, 255, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_HEAD_FALLBACK = (0, 200, 0)
COLOR_BODY_FALLBACK = (0, 150, 0)
COLOR_FOOD_FALLBACK = (200, 0, 0)



SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


ASSET_PATH = os.path.join(SCRIPT_DIR, 'assets') 
SPRITESHEET_FILENAME = 'snake_sprites.png'


# --- 6. NOVAS Configurações de Animação e Sprite ---

# Velocidade da animação (mudar de frame a cada X ticks do jogo)
ANIMATION_SPEED = 10000000000000000 

# Nomes das sprites como estão no seu snake_sprites.json
# Adicione ou remova nomes aqui conforme sua spritesheet crescer
HEAD_SPRITE_NAMES = {
    'horizontal': ['head_h_1', 'head_h_2'],
    'vertical':   ['head_v_1', 'head_v_2']
}

BODY_SPRITE_NAMES = {
    'horizontal': ['body_h_1', 'body_h_2', 'body_h_3', 'body_h_4'],
    'vertical':   ['body_v_1', 'body_v_2', 'body_v_3', 'body_v_4']
}

FOOD_SPRITE_NAMES = {
    'tipe': ['food_1', 'food_2', 'food_3', 'food_4','food_5','food_6','food_7']  
}

LEFTOVER_SPRITE_NAMES = {
    'tipe': ['leftover_1', 'leftover_2', 'leftover_3', 'leftover_4','leftover_5','leftover_6','leftover_7']  
}