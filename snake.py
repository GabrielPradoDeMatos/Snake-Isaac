# snake.py
# Classe que representa a Cobra lá ele

import pygame
from settings import *

class Snake:
    def __init__(self, sprites_dict):
        self.sprites = sprites_dict                      

        self.original_head_img = self.sprites['head']['horizontal'][0]
        self.body_img = self.sprites['body']['horizontal'][0]
        self.head_img = self.original_head_img
        #rect representa a posicão da cabeca
        self.rect = self.head_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        #Guarda todo histórico de movimentacões da cobra, cada elemento dessa lista é uma dupla de tupla, a primeira armazena a posicão (X,Y) e a segunda armazena a direcão (X,Y)
        self.position_history = []
        #Guarda a posicão atual de todas as partes do corpo
        self.body_rects = []
        
        #Vetores de direcão. No pygame o eixo Y é ao contrário e o 0° é no lugar do 90°, (0=Cima, 90=Esquerda, 180=Baixo, 270=Direita)
        #Será utilizado ma movimentar o rect da cabeca da cobra
        self.DIR_RIGHT = pygame.math.Vector2(SNAKE_SPEED, 0)
        self.DIR_LEFT = pygame.math.Vector2(-SNAKE_SPEED, 0)
        self.DIR_UP = pygame.math.Vector2(0, -SNAKE_SPEED)
        self.DIR_DOWN = pygame.math.Vector2(0, SNAKE_SPEED)
        
        #Início da cobra. Olhando para direita        
        self.direction = self.DIR_RIGHT
       
        self.pending_direction = None    
        self.last_turn_position = self.rect.center
        self.last_direction = self.direction.copy()
        self.turn_cooldown_distance = HEAD_SIZE[0] * HEAD_P
       
        self.score = 0

    #Após uma tecla ser pressionada o metodo verifica se é um movimento válido, caso seja, atribui a pending_direction a direcão da tecla pressionada
    #Essa direcão só será atualizada no metodo update
    def handle_input(self, event):        
        if event.type != pygame.KEYDOWN:
            return
           
        #pending_direction Não permite registrar uma nova intencão se já houver uma na fila para ser atualizada
        #também será utilizado para impedir curvas fechadas      
        #Ou seja, só será atualizado uma nova direcão após o metodo snake.update for executado
        if self.pending_direction is None:
            #Bloquear inversão da direcão exemplo: cobra andando para baixo e aperto para cima ou cobra indo para direita e aperto para esquerda
            #Atribui o vetor direcão para a direcão pendente
            if event.key == pygame.K_UP and self.direction != self.DIR_DOWN:
                self.pending_direction = self.DIR_UP
            
            elif event.key == pygame.K_DOWN and self.direction != self.DIR_UP:
                self.pending_direction = self.DIR_DOWN

            elif event.key == pygame.K_LEFT and self.direction != self.DIR_RIGHT:
                self.pending_direction = self.DIR_LEFT
            
            elif event.key == pygame.K_RIGHT and self.direction != self.DIR_LEFT:
                self.pending_direction = self.DIR_RIGHT

    def update(self):

        self._apply_turn()

        sprite_list, flip_h, flip_v = self._get_head_config()
        
        # 3. Define a imagem da cabeça (sprite + flip) #self.current_frame_index
        raw_head_sprite = sprite_list[0]
        self.head_img = pygame.transform.flip(raw_head_sprite, flip_h, flip_v)
        
        # 4. Move a cobra (lógica original adaptada)
        new_head_rect = self.head_img.get_rect(center=self.rect.center)
        new_head_rect.move_ip(self.direction)
        self.rect = new_head_rect        

        # 5. Adiciona a (posição, direção) ao histórico
        self.position_history.insert(0, (self.rect.center, self.direction.copy()))
                
        
        # 4. Limita o tamanho do histórico com base no placar
        max_history_len = (self.score + 2) * BODY_SPACING
        if len(self.position_history) > max_history_len:
            self.position_history.pop()
            
        # 5. (IMPORTANTE) Atualiza a lista de rects do corpo para colisões
        self._update_body_rects()
        
    def _apply_turn(self):
        
        if self.pending_direction is None:
            return
        #---------------------------------------------------------------------------------------------------------------
        #Ao fazer uma curva muito fechada a cabeca da cobra bate no corpo, por esse motivo
        #será necessário implementar uma trava para que seja impossível fazer curvas muito fechadas.
        #exemplo: cobra indo para direita, pressiona para cima e depois esquerda
        # Verifica se é uma "curva em U" (180 graus)
        is_u_turn = (self.pending_direction == -self.last_direction)
        
        can_turn = False
        if not is_u_turn:
            #Curva que não é fechada
            can_turn = True
        else:
            #Curva em U só é permitida após o cooldown de distância, ou seja, após a cabeca virar por completo
            current_pos = pygame.math.Vector2(self.rect.center)
            last_turn_pos = pygame.math.Vector2(self.last_turn_position)
            distance_since_turn = current_pos.distance_to(last_turn_pos)
            
            if distance_since_turn > self.turn_cooldown_distance:
                can_turn = True
        
        if can_turn:
            self.last_direction = self.direction.copy()
            self.direction = self.pending_direction

            self.last_turn_position = self.rect.center
        
        #Limpar o comando de virar mesmo que ele não tenha sido executado
        self.pending_direction = None

        
             
             
             
    def _get_head_config(self):
            if self.direction == self.DIR_RIGHT:
                return self.sprites['head']['horizontal'], False, False
            elif self.direction == self.DIR_LEFT:
                return self.sprites['head']['horizontal'], True, False
            elif self.direction == self.DIR_UP:
                return self.sprites['head']['vertical'], False, False
            elif self.direction == self.DIR_DOWN:
                return self.sprites['head']['vertical'], False, True
            
    def _get_body_config(self, direction):
        if direction == self.DIR_RIGHT:
            return self.sprites['body']['horizontal'], False, False
        elif direction == self.DIR_LEFT:
            return self.sprites['body']['horizontal'], True, False
        elif direction == self.DIR_UP:
            return self.sprites['body']['vertical'], False, False
        elif direction == self.DIR_DOWN:
            return self.sprites['body']['vertical'], False, True           
     

    def grow(self):
        """Aumenta o placar (e consequentemente o corpo)."""
        self.score += 1


    def _update_body_rects(self):
        #Limpa a lista de body_rects, pois é mais facil criar uma nova lista do que movimentar todos os elementos da lista antiga
        self.body_rects.clear()
        #O tamanho do corpo da cobra é igual a quantidade de pontos, portanto para cada ponto eu preciso de um pedaço de corpo
        #print(self.position_history)
        
        for i in range(self.score):
            #Define qual será a possicao do corpo da cobra. (i + 1) garante que o primeiro pedaço do corpo nao fique colado na cabeca,
            #pois o index 0 da lista position_history é sempre a posicão atual da cabeca.
            #multiplicar pelo BODY_SPACING é importante para nao ter sobreposicão, significa pegar um "delay" de BODY_SPACING posicões
            history_index = (i + 1) * BODY_SPACING
            if history_index < len(self.position_history):
                segment_pos, segment_dir = self.position_history[history_index]
                body_rect = self.body_img.get_rect(center=segment_pos)
                self.body_rects.append(body_rect)
        #print(self.body_rects)
                

    def draw_body(self, surface):
        """Desenha apenas o corpo na tela (usando os rects já calculados)."""
        for rect in self.body_rects:
            surface.blit(self.body_img, rect)

    def draw_head(self, surface):
        """Desenha apenas a cabeça na tela (por cima do corpo)."""
        surface.blit(self.head_img, self.rect)

    def check_collision_food(self, food_rect):
        if self.rect.colliderect(food_rect):
            self.grow()
            return True
        return False

    def check_collision_wall(self):
        return (self.rect.left < ARENA_LEFT or
                self.rect.right > ARENA_RIGHT or
                self.rect.top < ARENA_TOP or
                self.rect.bottom > ARENA_BOTTOM)

    def check_collision_self(self):
        # Pula os primeiros segmentos (para não colidir com o "pescoço")
        ignore_segments = int(self.turn_cooldown_distance / SNAKE_SPEED) + 1 
        
        # Itera sobre os rects do corpo (exceto o pescoço)
        for body_rect in self.body_rects[ignore_segments:]:
            if self.rect.colliderect(body_rect):
                return True
        return False