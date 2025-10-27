import pygame

sprites = {
    'head': {'horizontal': [], 'vertical': []},
    'body': {'horizontal': [], 'vertical': []},
    'food': None
}

sprites['head']['horizontal'].append('esse')




print(sprites['head']['horizontal'])


pygame.init()
screen = pygame.display.set_mode((500,500))


#Cria uma surface que suporta transparência



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    screen.fill((50,50,100))
    sprite = pygame.Surface((35,37), pygame.SRCALPHA)
    #sprite.fill((0,0,0))
    sprite_sheet = pygame.image.load(r'C:\Users\C129704\Snake Isaac - Copy\assets\snake_sprites.png').convert_alpha()
    sprite.blit(sprite_sheet, (0, 0), (1, 2, 35, 37))
    nova_sprite = sprite.get_rect()
    print(nova_sprite)
    screen.blit(sprite,(50,50))
    pygame.display.update()