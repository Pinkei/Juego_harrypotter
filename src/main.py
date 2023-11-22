import pygame
from aleatorias import *
from config import * 
from pygame.time import Clock
from pygame import display
from random import randint
from colisiones import *
from pygame.locals import *
from funciones import *

#Inicializar los modulos de pygame
pygame.init()

#configuaracion pantalla principal
screen = display.set_mode(size_screen) 
display.set_caption("Harry potter")

#creo un reloj
clock = Clock()

#_____________________________________seteo de sonidos
#cortito caundo choca:
harry_sound = pygame.mixer.Sound("./src/sonidos/lanza_hechizos.mp3")
game_over_sound = pygame.mixer.Sound("./src/sonidos/game_over.mp3")
ganador_sound = pygame.mixer.Sound("./src/sonidos/ganador.mp3")


#____________________________________MUSICA DE FONDO_________________:
pygame.mixer.music.load("./src/sonidos/vin-harry-potter.mp3")
pygame.mixer.music.set_volume(0.1)
playing_music = True

#_______________________________________seteo de imagenes__________________________
image_player = pygame.image.load("./src/sonidos/harry_potter_jugador.png")
image_dementor = pygame.image.load("./src/sonidos/dementores.png")
image_mortifago = pygame.image.load("./src/sonidos/mortifago.png")
#hechizo = pygame.image.load("./src/sonidos/hechizo.png") 
background = pygame.transform.scale(pygame.image.load("./src/sonidos/fondo.jpg"), size_screen)
background_principal = pygame.transform.scale(pygame.image.load("./src/sonidos/portada.jpg"), size_screen)
background_final = pygame.transform.scale(pygame.image.load("./src/sonidos/harry_derrotado.jpg"), size_screen)

contador = 0
max_contador = 0
cont_grande = 0
count_harrys = 20

#para que vengan mas lentos
truco_lento = False

#direccion movimiento tecla, en false para que cuando detectemos que se presiopno una tecla es true
move_up = False
move_down = False
move_right = False
move_left = False

hechizo = None

#_______________________________SETEO FUENTE:
fuente= pygame.font.SysFont(None, 48)


#_________creo varios bloques  
block = crear_bloque(image_player, randint(0, ANCHO - BLOCK_ANCHO),
                    randint(0, ALTO - BLOCK_ALTO),
                    BLOCK_ANCHO, BLOCK_ALTO, red, radio = 25)


while True:
    #pantalla de inicio antes de entrar al juegito
    screen.blit(background_principal, origin)
    mostrar_text(screen, "Harry potter- la batalla", fuente, (ANCHO // 2, 20), white, None)
    mostrar_text(screen, "Presione una tecla para comenzar...", fuente, (ANCHO // 2, ALTO // 2), white, None)
    
    pygame.display.flip()
    wait_user()
    
    #INICIA el juego
    lives = 3
    pygame.mouse.set_visible(False) #para que no se vea el cursor en la pantalla 
    contador = 0 #para el puntaje
    texto = fuente.render(f"Eliminados: {contador}", True, brown) 
    rect_texto = texto.get_rect()  
    rect_texto.topleft = (30, 40)
    #Texto de las vidas
    texto_lives = fuente.render(f"Vidas: {lives}", True, brown) 
    rect_texto_lives = texto_lives.get_rect(topright = (ANCHO - 30, 40))
    is_running = True
    pygame.mixer.music.play(-1)

#crear lista de dementores
    harrys = []
    hechizos = []
    rafaga = False
    cargar_lista_harry(harrys, count_harrys, image_dementor)

    while is_running:
        clock.tick(FPS)

        #---> ___________DETECTA los eventos 
        for event in pygame.event.get():       
            if event.type == pygame.QUIT:
                is_running = False

            #______evento de moover las teclas:
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_f: 
                    if rafaga:
                        midleft = block["rect"].midleft
                        hechizo_ancho, hechizo_alto = size_hechizo
                        # creo el bloque del hechizo par lanzarlo:
                        hechizos.append( crear_bloque(None, midleft[0] - hechizo_ancho, midleft[1] - hechizo_alto //2,
                                                hechizo_ancho, hechizo_alto, red, speed_x= speed_hechizo ))
                    else:
                        if not hechizo:
                            midleft = block["rect"].midleft
                            hechizo_ancho, hechizo_alto = size_hechizo
                            hechizo = crear_bloque(None, midleft[0] - hechizo_ancho, midleft[1] - hechizo_alto //2,
                                                    hechizo_ancho, hechizo_alto, green, speed_x= speed_hechizo )

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
                    move_right = True
                    move_left = False

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_left = True
                    move_right = False

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move_up = True
                    move_down = False

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move_down = True
                    move_up = False
                
                #PARA PAUSAR LA MUSICA:
                if event.key == pygame.K_m:
                    if playing_music:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

                    playing_music = not playing_music

                #evento pausa:
                if event.key == pygame.K_p:
                    if playing_music:
                        pygame.mixer.music.pause()
                        mostrar_text(screen, "Pausa", fuente, center_screen, red )
                    pygame.display.flip() 
                    wait_user()
                    if playing_music:
                        pygame.mixer.music.unpause()

            #botones para mas lento 
                if event.key == pygame.K_l:
                    truco_lento = True

        # ____ la rafaga
                if event.key == pygame.K_e:
                    rafaga = not rafaga
                    
            
            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_right = False

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_left = False

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move_up = False

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move_down = False

                if event.key == pygame.K_ESCAPE:
                    is_running = False

                if event.key == pygame.K_l:
                    truco_lento = False


            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1:
                    if rafaga:
                        midleft = block["rect"].midleft
                        hechizo_ancho, hechizo_alto = size_hechizo
                        hechizos.append( crear_bloque(None, midleft[0] - hechizo_ancho, midleft[1] - hechizo_alto //2,
                                                hechizo_ancho, hechizo_alto, red, speed_x= speed_hechizo ))
                    else:
                        if not hechizo:
                            midleft = block["rect"].midleft
                            hechizo_ancho, hechizo_alto = size_hechizo
                            hechizo = crear_bloque(None, midleft[0] - hechizo_ancho, midleft[1] - hechizo_alto //2,
                                                    hechizo_ancho, hechizo_alto, green, speed_x= speed_hechizo )

            if event.type == pygame.MOUSEMOTION:    #es caundo movemos en la pantalla el mouse
                block["rect"].center = (event.pos[0], event.pos[1])


    #_________MUEVO EL RECTANGULO de acuerdo a su direccion ______actualizar los elementos y los posiciona
        
        if move_right and block["rect"].right <= (ANCHO - SPEED):
            #derecha
            block["rect"].left += SPEED
                                                
        if move_left and block["rect"].left >= SPEED:
            #Izquierda
            block["rect"].left -= SPEED      

        if move_up and block["rect"].top >= (0 + SPEED):
            #arriba
            block["rect"].top -= SPEED
        if move_down and block["rect"].bottom <= (ALTO - SPEED):      #PARA QUE NO SE ME vAyA DE LA PANTALLA_______
            #queda UR ultima opcion
            #abajo
            block["rect"].top += SPEED

        # PARA QUE EL CURSOR SIGA AL PERSONAJE SI USO LOS TECLADOS:
        pygame.mouse.set_pos(block["rect"].centerx, block["rect"].centery)

    #______________________________ MUEVO LOS DEMENTORES:
        for harry in harrys:
            if not truco_lento :
                harry["rect"].move_ip(harry["speed_x"], 0)  #ip significa in place, en el lugar, que lo posicione en un lugar particular
        
            elif truco_lento:
                harry["rect"].move_ip(1, 0)

        #________________MUEVO EL HECHIZO:
        if rafaga:
            for hechizo in hechizos[:]:
                if hechizo["rect"].right >= 0: 
                    hechizo["rect"].move_ip(-hechizo["speed_x"],0 )
                else:
                    hechizos.remove(hechizo)
        else:
            if hechizo:
                if hechizo["rect"].right >= 0: 
                    hechizo["rect"].move_ip(-hechizo["speed_x"],0 )
                else:
                    hechizo = None

        for harry in harrys[:]:
            if harry["rect"].right > ANCHO:
                harry["rect"].x = harry["rect"].width 
                                                    

            #______________detecta colision 
        for harry in harrys[ : ]: # [ : ] --> copia una lista completa,
            if detectar_colision_circ(harry["rect"], block["rect"]):
                harrys.remove(harry)
                #VIDAS:
                if lives > 1:
                    lives -= 1
                    texto_lives = fuente.render(f"Vidas: {lives}", True, brown) 
                    rect_texto_lives = texto_lives.get_rect(topright = (ANCHO - 30, 40))
                else:
                    is_running = False

                if playing_music: 
                    harry_sound.play() 

        #aparecen mas despues de que no hay mas dementores
                if len(harrys) == 0:
                    cargar_lista_harry(harrys, count_harrys, image_mortifago) 
                    ganador_sound.play() #para que haga victoria cuando termine

#__________ COLISION CON EL HECHIZO
        if rafaga:
            for hechizo in hechizos[:]:
                colision = False
                for harry in harrys[ : ]:
                    if detectar_colision_circ(harry["rect"], hechizo["rect"]):
                        harrys.remove(harry)
                        contador += 1 
                        texto = fuente.render(f"Eliminados: {contador}", True, brown) 
                        rect_texto = texto.get_rect(topleft = (30, 40))  
                        cont_grande = 30
                        colision = True
                        if playing_music: 
                            harry_sound.play() 
                            
                #aparecen mas despues de que no hay mas
                        if len(harrys) == 0:
                            cargar_lista_harry(harrys, count_harrys, image_mortifago) 
                            ganador_sound.play()
                            
                if colision == True:
                    hechizos.remove(hechizo)

        else:
            if hechizo:
                colision = False
                for harry in harrys[ : ]:
                    if detectar_colision_circ(harry["rect"], hechizo["rect"]):
                        harrys.remove(harry)
                        contador += 1 
                        texto = fuente.render(f"Eliminados: {contador}", True, brown) 
                        rect_texto = texto.get_rect(topleft = (30, 40))  
                        cont_grande = 30
                        colision = True
                        if playing_music: #para pausar tambien el sonido este
                            harry_sound.play() #para que haga ese sonido cuando colisiones
                            
                #aparecen mas despues de que no hay mas monedas
                        if len(harrys) == 0:
                            cargar_lista_harry(harrys, count_harrys, image_mortifago) 
                            ganador_sound.play()
                            
                if colision == True:
                    hechizo = None


        # ----> dibuja la pantalla, lleno de color la pantalla. la superficie,:
        screen.blit(background, origin)

        dibujar_dementores(screen, harrys)
        
        #dibujo el hechizo
        if rafaga:
            for hechizo in hechizos:
                pygame.draw.rect(screen, hechizo["color"], hechizo["rect"])
        else:
            if hechizo:
                pygame.draw.rect(screen, hechizo["color"], hechizo["rect"])

        #para el jugador tenga imagen
        screen.blit(block["imagen"], block["rect"])

        screen.blit(texto, rect_texto)
        screen.blit(texto_lives, rect_texto_lives)

        # ---> actualizar pantalla 
        display.flip()

    if contador > max_contador:
        max_contador = contador

    #pantalla de inicio antes de entrar al juegito
    screen.blit(background_final, origin)
    pygame.mixer.music.stop()
    game_over_sound.play()
    mostrar_text(screen, "GAME OVER", fuente, (ANCHO // 2, 20), red)
    mostrar_text(screen, "Presione una tecla para volver a jugar...", fuente, (ANCHO // 2, ALTO // 2), white, None)
    mostrar_text(screen, f"Maximo puntaje: {max_contador}", fuente, (ANCHO // 2, ALTO - 30), red)
    pygame. display.flip() #hago que se pinte la pantalla
    wait_user()

terminar()