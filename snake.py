# snake.py
# Classe que representa a Cobra lá ele

import pygame
from settings import *

class Snake:
    # Para iniciar a cobra é necessário passar o dicionário de sprites
    def __init__(self, sprites_dict):
        
        self.sprites = sprites_dict
        
        # Pega uma sprite base para criar os Rects (importante para colisão)
        self.body_base_img = self.sprites['body']['horizontal'][0]
        # Imagem atual da cabeça (será atualizada a cada frame)
        self.head_img = self.sprites['head']['horizontal'][0] 

        self.rect = self.head_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # self.position_history agora guarda (posição, direção)
        self.position_history = [] 
        
        # self.body_rects é para colisão (como antes)
        self.body_rects = []
        # self.body_segments é para desenho (guarda pos e dir)
        self.body_segments = []
        
        # Vetores de direcão.
        self.DIR_RIGHT = pygame.math.Vector2(SNAKE_SPEED, 0)
        self.DIR_LEFT = pygame.math.Vector2(-SNAKE_SPEED, 0)
        self.DIR_UP = pygame.math.Vector2(0, -SNAKE_SPEED)
        self.DIR_DOWN = pygame.math.Vector2(0, SNAKE_SPEED)
        
        # Início da cobra
        self.direction = self.DIR_RIGHT
                       
        #---------------------------------------------------------------------------------------------------------------
        # Lógica de cooldown de curva (excelente, vamos manter!)
        self.pending_direction = None
        self.last_turn_position = self.rect.center
        self.last_direction = self.direction.copy()
        self.turn_cooldown_distance = HEAD_SIZE[0] * HEAD_P
        #---------------------------------------------------------------------------------------------------------------
       
        # --- Lógica de Animação ---
        self.anim_counter = 0
        self.current_frame_index = 0
       
        self.score = 0
   
    # Verificar teclas pressionadas
    def handle_input(self, event):        
        if event.type != pygame.KEYDOWN:
            return
           
        # Não permite registrar uma nova intencão se já houver uma
        if self.pending_direction is None:
            # Bloquear inversão da direcão
            if event.key == pygame.K_UP and self.direction != self.DIR_DOWN:
                self.pending_direction = self.DIR_UP
            
            elif event.key == pygame.K_DOWN and self.direction != self.DIR_UP:
                self.pending_direction = self.DIR_DOWN
            
            elif event.key == pygame.K_LEFT and self.direction != self.DIR_RIGHT:
                self.pending_direction = self.DIR_LEFT
            
            elif event.key == pygame.K_RIGHT and self.direction != self.DIR_LEFT:
                self.pending_direction = self.DIR_RIGHT
            
          

    def _apply_turn(self):
        
        if self.pending_direction is None:
            return

        #---------------------------------------------------------------------------------------------------------------
        # Sua lógica de cooldown de curva (mantida 100%)
        is_u_turn = (self.pending_direction == -self.last_direction)
        
        can_turn = False
        if not is_u_turn:
            can_turn = True
        else:
            current_pos = pygame.math.Vector2(self.rect.center)
            last_turn_pos = pygame.math.Vector2(self.last_turn_position)
            distance_since_turn = current_pos.distance_to(last_turn_pos)
            
            if distance_since_turn > self.turn_cooldown_distance:
                can_turn = True
        
        if can_turn:
            self.last_direction = self.direction.copy()
            self.direction = self.pending_direction
            self.last_turn_position = self.rect.center
            # Reseta a animação a cada curva para ficar mais fluido
            self.current_frame_index = 0
            self.anim_counter = 0
        
        # Limpar o comando de virar
        self.pending_direction = None
        #---------------------------------------------------------------------------------------------------------------
    
    def _get_head_config(self):
        """Retorna a lista de sprites da cabeça, e se deve flipar (h, v)"""
        if self.direction == self.DIR_RIGHT:
            return self.sprites['head']['horizontal'], False, False
        elif self.direction == self.DIR_LEFT:
            return self.sprites['head']['horizontal'], True, False
        elif self.direction == self.DIR_UP:
            return self.sprites['head']['vertical'], False, False
        elif self.direction == self.DIR_DOWN:
            return self.sprites['head']['vertical'], False, True
            
    def _get_body_config(self, direction):
        """Retorna a lista de sprites do CORPO para uma direção, e se deve flipar (h, v)"""
        if direction == self.DIR_RIGHT:
            return self.sprites['body']['horizontal'], False, False
        elif direction == self.DIR_LEFT:
            return self.sprites['body']['horizontal'], True, False
        elif direction == self.DIR_UP:
            return self.sprites['body']['vertical'], False, False
        elif direction == self.DIR_DOWN:
            return self.sprites['body']['vertical'], False, True
        #else:
            #return self.sprites['body']['horizontal'], False, False

             
    def update(self):

        self._apply_turn()

        # 1. Pega a configuração da cabeça (lista de sprites e flip)
        sprite_list, flip_h, flip_v = self._get_head_config()

        # 2. Atualiza o frame da animação
        self.anim_counter = (self.anim_counter + 1) % ANIMATION_SPEED
        num_frames = len(sprite_list)
        if self.anim_counter == 0 and num_frames > 0:
            self.current_frame_index = (self.current_frame_index + 1) % num_frames

        # 3. Define a imagem da cabeça (sprite + flip)
        raw_head_sprite = sprite_list[self.current_frame_index]
        self.head_img = pygame.transform.flip(raw_head_sprite, flip_h, flip_v)

        # 4. Move a cobra (lógica original adaptada)
        new_head_rect = self.head_img.get_rect(center=self.rect.center)
        new_head_rect.move_ip(self.direction)
        self.rect = new_head_rect

        # 5. Adiciona a (posição, direção) ao histórico
        self.position_history.insert(0, (self.rect.center, self.direction.copy()))

        # 6. Limita o tamanho do histórico com base no placar
        max_history_len = (self.score + 2) * BODY_SPACING
        if len(self.position_history) > max_history_len:
            self.position_history.pop()
            
        # 7. (IMPORTANTE) Atualiza a lista de rects (colisão) e segments (desenho)
        self._update_body_segments()
        


    def grow(self):
        """Aumenta o placar (e consequentemente o corpo)."""
        self.score += 1



    def _update_body_segments(self):
        """Cria os rects (colisão) e segments (desenho) do corpo."""
        self.body_rects.clear()
        self.body_segments.clear()
        
        for i in range(self.score):
            history_index = (i + 1) * BODY_SPACING
            if history_index < len(self.position_history):
                # Agora pegamos a posição E a direção do histórico
                segment_pos, segment_dir = self.position_history[history_index]
                
                # 1. Criar Rect para colisão (usa a imagem base)
                body_rect = self.body_base_img.get_rect(center=segment_pos)
                self.body_rects.append(body_rect)
                
                # 2. Guardar Posição e Direção para desenho
                self.body_segments.append((segment_pos, segment_dir))

    def draw_body(self, surface):
        """Desenha o corpo na tela, usando os segmentos."""
        
        # Itera sobre os segmentos (posição, direção)
        for seg_pos, seg_dir in self.body_segments:
            
            # Pega a configuração de sprite/flip para AQUELE segmento
            sprite_list, flip_h, flip_v = self._get_body_config(seg_dir)
            
            # Pega o frame (sincronizado com a cabeça)
            num_frames = len(sprite_list)
            frame_index = self.current_frame_index % num_frames # Garante que não dê erro
            
            raw_body_sprite = sprite_list[frame_index]
            
            # Aplica o flip
            body_sprite = pygame.transform.flip(raw_body_sprite, flip_h, flip_v)
            
            # Cria o rect e desenha
            body_rect = body_sprite.get_rect(center=seg_pos)
            surface.blit(body_sprite, body_rect)


    def draw_head(self, surface):
        """Desenha apenas a cabeça (já definida no update)."""
        surface.blit(self.head_img, self.rect)

    def check_collision_food(self, food_rect):
        """Verifica colisão com a comida."""
        if self.rect.colliderect(food_rect):
            self.grow()
            return True
        return False

    def check_collision_wall(self):
        """Verifica colisão com as paredes."""
        return (self.rect.left < 0 or
                self.rect.right > SCREEN_WIDTH or
                self.rect.top < 0 or
                self.rect.bottom > SCREEN_HEIGHT)

    def check_collision_self(self):
        """Verifica colisão com o próprio corpo."""
        # Sua lógica original de ignorar o pescoço (mantida 100%)
        ignore_segments = int(self.turn_cooldown_distance / SNAKE_SPEED) + 1 
        
        # Itera sobre os rects do corpo (exceto o pescoço)
        for body_rect in self.body_rects[ignore_segments:]:
            if self.rect.colliderect(body_rect):
                return True
        return False