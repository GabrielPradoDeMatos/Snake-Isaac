import os

# --- 1. Configuracões de Tela ---
SCREEN_WIDTH = 918
SCREEN_HEIGHT = 612

# --- 1.1 Configuracões de Mensagens ---
MENSAGE_GO = "VOCÊ PERDEU!"
MENSAGE_RESTART = "Pressione [R] para reiniciar"

MENSAGE_GO_X_POSITION = SCREEN_WIDTH // 2
MENSAGE_GO_Y_POSITION = SCREEN_HEIGHT // 2 - 40

MENSAGE_RESTART_X_POSITION = SCREEN_WIDTH // 2
MENSAGE_RESTART_Y_POSITION = SCREEN_HEIGHT // 2 + 20

# --- 1.2 Configuracões do Placar ---
SCORE_Y_POSITION = 15
SCORE_X_POSITION = SCREEN_WIDTH//2

# --- 2. Configuracões do Jogo ---
FPS = 30
SNAKE_SPEED = 8

# --- 3. Configuracões da Arena ---
ARENA_WIDTH = 710
ARENA_HEIGHT = 404

ARENA_LEFT = (SCREEN_WIDTH - ARENA_WIDTH) // 2
ARENA_RIGHT = ARENA_LEFT + ARENA_WIDTH
ARENA_TOP = (SCREEN_HEIGHT - ARENA_HEIGHT) // 2
ARENA_BOTTOM = ARENA_TOP + ARENA_HEIGHT

# --- 4. Configurações da Cobra ---
HEAD_SIZE = (35, 38)
BODY_SIZE = (27, 23)

HEAD_P = 0.75 #Percentual da cabeça para cooldown de curva
BODY_SPACING = 4 #Espaçamento entre os segmentos do corpo

# --- 5. Configurações da Comida ---
FOOD_SIZE = (27, 28)
FOOD_PADDING  = 10 #Padding para comida não nascer colada na parede

# --- 6. Cores ---
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# --- 7. Cores (Usadas como fallback) ---
COLOR_HEAD_FALLBACK = (0, 200, 0)
COLOR_BODY_FALLBACK = (0, 150, 0)
COLOR_FOOD_FALLBACK = (200, 0, 0)
COLOR_BACKGROUND_FALLBACK = (0,0,0)

# --- 8. Configuracões de Path ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) #Retorna o caminho absoluto do script
ASSET_PATH = os.path.join(SCRIPT_DIR, "assets") 
SPRITESHEET_FILENAME = "snake_sprites.png"
ARENA_FILENAME = "Arena.png"

# --- 9. Configuracões de Fonte ---
SCORE_FONT_SIZE = 50
GAME_OVER_FONT_SIZE = 75
RESTART_FONT_SIZE = 40
MAIN_GAME_FONT = "upheavtt.ttf"
MAIN_FONT_PATH = os.path.join(ASSET_PATH,MAIN_GAME_FONT)

# --- 10. Configuracões de Animacão ---
ANIMATION_DELAY_HEAD = 2 #Velocidade da animação (mudar de sprite a cada X frames do jogo)
ANIMATION_DELAY_BODY = 8 #Velocidade da animação (mudar de sprite a cada X frames do jogo)
BODY_VERTICAL_TAIL_COUNT = 2

# --- 11. Configuracões de Sprite ---
HEAD_SPRITE_NAMES = {
    'horizontal': ["head_h_1", "head_h_2"],
    'vertical':   ["head_v_1", "head_v_2"]
}

BODY_SPRITE_NAMES = {
    'horizontal': ['body_h_1', 'body_h_2', 'body_h_3', 'body_h_4'],
    'vertical':   ['body_v_1', 'body_v_2', 'body_v_3', 'body_v_4']
}

FOOD_SPRITE_NAMES = {
    'food': ['food_1', 'food_2', 'food_3', 'food_4','food_5','food_6','food_7']  
}

LEFTOVER_SPRITE_NAMES = {
    'leftover': ['leftover_1', 'leftover_2', 'leftover_3', 'leftover_4','leftover_5','leftover_6','leftover_7']  
}