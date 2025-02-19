import pygame

def mostrar_intro(screen, font):
    historia = [
        "Hace siglos, la Aldea Arcana fue hogar de magos sabios.",
        "Pero la paz fue destruida por el Señor Oscuro, quien corrompió a los magos.",
        "Geralt, el último hechicero libre, debe restaurar la paz.",
        "Presiona ENTER para continuar..."
    ]

    screen.fill((0, 0, 0))

    for i, linea in enumerate(historia):
        texto = font.render(linea, True, (255, 255, 255))
        screen.blit(texto, (50, 100 + i * 50))

    pygame.display.flip()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                esperando = False
