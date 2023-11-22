import pygame
from config import *
from random import randint

def terminar():
    pygame.quit()
    exit()

def mostrar_text(superficie,texto,fuente, coordenadas, color_fuente, color_fondo = black):
        sup_texto = fuente.render(texto, True, color_fuente, color_fondo ) 
        rect_texto = sup_texto.get_rect()  
        rect_texto.center = coordenadas
        superficie.blit(sup_texto, rect_texto) 
        

def wait_user():
    while True:
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                terminar()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminar()
                return None


def crear_bloque(imagen = None, left = 0, top = 0, ancho = 40, alto = 40, color = (255, 255, 255), dir = 3, borde = 0, radio = -1, speed_x = 5, speed_y = 5):
    rec = pygame.Rect(left, top, ancho, alto)
    if imagen:
        imagen = pygame.transform.scale(imagen, (ancho, alto))
    return {"rect":rec ,"color": color , "dir": dir,
            "borde": borde , "radio": radio, "speed_x": speed_x, "speed_y": speed_y, "imagen": imagen }


def cargar_lista_harry(harrys, cantidad, imagen= None):
    for i in range(cantidad):
        size_harry = randint(size_min_harry, size_max_harry) 
        speed_harry = randint(speed_min_harry, speed_max_harry)
        harrys.append(crear_bloque(imagen, randint(-ANCHO, size_harry - ANCHO),
                    randint(0, ALTO - size_harry),
                    size_harry, size_harry, yellow , speed_x = speed_harry, radio = size_harry // 2))

def dibujar_dementores(superficie, harrys):
    for harry in harrys:
        if harry["imagen"]:
            superficie.blit(harry["imagen"], harry["rect"]) #paso los dementores
        else:
            pygame.draw.rect(
                superficie, harry["color"], harry["rect"], harry["borde"], harry["radio"])