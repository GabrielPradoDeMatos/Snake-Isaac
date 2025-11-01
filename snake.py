# snake.py
# Classe que representa a Cobra lá ele

import pygame
from settings import *


class Snake:
    
    sprites: dict[str,
                dict[str,
                        list[pygame.Surface]]] 
    
    original_head_img: pygame.Surface
    head_img: pygame.Surface
    body_imgs: list[pygame.Surface]
    rect: pygame.Rect
    position_history: list[
                        tuple[
                            tuple[int,int],
                            pygame.math.Vector2]]
     
    body_rects: list[
                    tuple[int,int]]  
    
    DIR_RIGHT: pygame.math.Vector2
    DIR_LEFT: pygame.math.Vector2
    DIR_UP: pygame.math.Vector2
    DIR_DOWN: pygame.math.Vector2
    
    direction: pygame.math.Vector2
    
    pending_direction:pygame.math.Vector2    
    last_turn_position = tuple[int,int]
    last_direction: pygame.math.Vector2
    turn_cooldown_distance: float    
    score: int
    
    animation_count_head: int
    animation_count_body: int
    
    def __init__(self, sprites_dict: dict[str,
                                          dict[str,
                                               list[pygame.Surface]]]):
        
        self.sprites = sprites_dict                      

        self.original_head_img = self.sprites['head']['horizontal'][0]
        self.body_imgs = []
        self.animation_count_body = 0
        self.animation_count_head = 0
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
    def handle_input(self, event: pygame.event.Event) -> None:        
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

    def update(self) -> None:

        self._apply_turn()

        sprite_list, flip_h, flip_v = self._get_head_config()
        
        # 3. Define a imagem da cabeça (sprite + flip) #self.current_frame_index
        #Chamar a funcao para definir a sprite
        self._update_head_sprite()
        #raw_head_sprite = sprite_list[0]
        #self.head_img = pygame.transform.flip(raw_head_sprite, flip_h, flip_v)
        
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
            
               
        #Chamar a funcao para definir a sprite        
        #self._update_body_sprite()
        #Pegar a nova posicao do corpo
        self._update_body_rects()
        
        #Essa funcão vai atualizar o self.head_img
   
    def _update_head_sprite(self) -> None:
        sprite_list, flip_h, flip_v = self._get_head_config()
        sprite_index = (self.animation_count_head // ANIMATION_DELAY_HEAD) % len(sprite_list)
        self.head_img = pygame.transform.flip(sprite_list[sprite_index],flip_h,flip_v)
        self.animation_count_head += 1

    def _update_body_sprite(self, update_animation_count:bool, direction: pygame.math.Vector2,initial_index: int) -> pygame.Surface:   
        
        sprite_list,_,_ = self._get_body_config(direction)
        
        initial_sprite = initial_index % len(sprite_list)
        #Mudar a cada ANIMATION_DELAY_BODY frames o index da lista     
              
        if update_animation_count and (direction == self.DIR_UP or direction == self.DIR_DOWN):
            self.animation_count_body += 1
            sprite_index = ((self.animation_count_body // ANIMATION_DELAY_BODY)) % SNAKE_LAST_SPRITE_VERTICAL_QTD            
        elif not(update_animation_count) and (direction == self.DIR_UP or direction == self.DIR_DOWN):
            sprite_index = ((self.animation_count_body // ANIMATION_DELAY_BODY) + initial_sprite) % len(sprite_list)
            if sprite_index == 0 or sprite_index == 1:
                sprite_index += SNAKE_LAST_SPRITE_VERTICAL_QTD
        elif update_animation_count:
            self.animation_count_body += 1
            sprite_index = ((self.animation_count_body // ANIMATION_DELAY_BODY) + initial_sprite) % len(sprite_list)  
        else:
            sprite_index = ((self.animation_count_body // ANIMATION_DELAY_BODY) + initial_sprite) % len(sprite_list)  
            
        return sprite_list[sprite_index]    
        
    def _apply_turn(self) -> None:
        
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
             
    def _get_head_config(self) -> tuple[list[pygame.Surface], bool, bool]:
            if self.direction == self.DIR_RIGHT:
                return self.sprites['head']['horizontal'], False, False
            elif self.direction == self.DIR_LEFT:
                return self.sprites['head']['horizontal'], True, False
            elif self.direction == self.DIR_UP:
                return self.sprites['head']['vertical'], False, False
            elif self.direction == self.DIR_DOWN:
                return self.sprites['head']['vertical'], False, True
            
    def _get_body_config(self, direction: pygame.math.Vector2) -> tuple[list[pygame.Surface], bool, bool]:
        if direction == self.DIR_RIGHT:
            return self.sprites['body']['horizontal'], False, False
        elif direction == self.DIR_LEFT:
            return self.sprites['body']['horizontal'], True, False
        elif direction == self.DIR_UP:
            return self.sprites['body']['vertical'], False, False
        elif direction == self.DIR_DOWN:
            return self.sprites['body']['vertical'], False, True           
    
    def grow(self) -> None:
        self.score += 1

    def _update_body_rects(self) -> None:
        #Limpa a lista de body_rects, pois é mais facil criar uma nova lista do que movimentar todos os elementos da lista antiga
        self.body_rects.clear()
        self.body_imgs.clear()
        update_animation_count = False
        #O tamanho do corpo da cobra é igual a quantidade de pontos, portanto para cada ponto eu preciso de um pedaço de corpo
        #print(self.position_history)
        
        for i in range(self.score):
            #Define qual será a possicao do corpo da cobra. (i + 1) garante que o primeiro pedaço do corpo nao fique colado na cabeca,
            #pois o index 0 da lista position_history é sempre a posicão atual da cabeca.
            #multiplicar pelo BODY_SPACING é importante para nao ter sobreposicão, significa pegar um "delay" de BODY_SPACING posicões
            history_index = (i + 1) * BODY_SPACING
            if history_index < len(self.position_history):
                segment_pos, segment_dir = self.position_history[history_index]
                #body_sprites, _, _ = self._get_body_config(segment_dir)
                #Tendo a direcao do segmento do corpo eu posso charmar o_ get_body_config
                #Para ter a lista com todas as sprites que eu posso usar no segmento
                
                if i == self.score - 1:
                    update_animation_count = True
                
                self.body_imgs.append(self._update_body_sprite(update_animation_count,segment_dir,i))
                #print(f"{sprite_index}, {len(body_sprites)}")
                #Fazer o esquema de calculo usando o history_index para
                #definir a sprite que vou usar no segmento
                #Calculo: history_index % (comprimento da lista)
                #Quero que fique intercalando entre cada parte do segmento
                #O ultimo segmento tem quer ter a bundinha
                #print(f"Esse é dentro da funcao {len(self.body_imgs)}")
                
                #self.body_imgs.append(body_sprites[sprite_index])
                #Cada segmento terá sempre a mesma sprite, agr so implementar uma funcao de altere essa sprite
                body_rect = self.body_imgs[i].get_rect(center=segment_pos)                
                self.body_rects.append(body_rect)
      
      
    def draw_body(self, surface: pygame.Surface) -> None:
        """Desenha apenas o corpo na tela (usando os rects já calculados)."""
        for i in range(len(self.body_rects)):          
            surface.blit(self.body_imgs[i], self.body_rects[i])
            

    def draw_head(self, surface: pygame.Surface) -> None:
        """Desenha apenas a cabeça na tela (por cima do corpo)."""
        surface.blit(self.head_img, self.rect)

    def check_collision_food(self, food_rect: pygame.Rect) -> bool:
        if self.rect.colliderect(food_rect):
            self.grow()
            return True
        return False

    def check_collision_wall(self) -> bool:
        return (self.rect.left < ARENA_LEFT or
                self.rect.right > ARENA_RIGHT or
                self.rect.top < ARENA_TOP or
                self.rect.bottom > ARENA_BOTTOM)

    def check_collision_self(self) -> bool:
        # Pula os primeiros segmentos (para não colidir com o "pescoço")
        ignore_segments = int(self.turn_cooldown_distance / SNAKE_SPEED) + 1 
        
        # Itera sobre os rects do corpo (exceto o pescoço)
        for body_rect in self.body_rects[ignore_segments:]:
            if self.rect.colliderect(body_rect):
                return True
        return False