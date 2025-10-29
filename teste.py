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

print((50//5)%2)

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             quit()
#     screen.fill((255,255,255))
    
#     #sprite.fill((0,0,0))
#     sprite_sheet = pygame.image.load(r'C:\Users\C129704\GitHub\Snake-Isaac\assets\snake_sprites.png').convert_alpha()
#     sprite = pygame.Surface((27,21), pygame.SRCALPHA)
    
#     sprite.blit(sprite_sheet, (0, 0), (1, 83, 27, 21))
#     #nova_sprite = sprite.get_rect()
#     #print(nova_sprite)
#     screen.blit(pygame.transform.scale(sprite,(27,23)),(50,50))
#     pygame.display.update()
    