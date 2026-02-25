import pygame as pg
from configs import *
from archivos.funciones_archivos import *
from funciones_pygame.botones import *
from logica_juego.funciones_main import crear_diccionario_partida, crear_diccionario_ronda, manejar_inicio, manejar_ayuda, manejar_juego, crear_fuentes
from eventos.manejo_eventos import manejar_eventos

pg.init()

def main():
    bandera_juego = True
    reloj = pg.time.Clock()
    ventana = pg.display.set_mode(SIZE_WINDOW)

    pg.display.set_caption("Adivina la palabra")
    fuentes = crear_fuentes()
    palabras = obtener_lista_palabras("words.csv")
    diccionario_partida = crear_diccionario_partida(ventana)
    diccionario_ronda = crear_diccionario_ronda(DIFICULTYS, palabras, TRYS)
    boton_modos = crear_lista_botones_dificultad(ventana, fuentes["fuente_palabras"], "Black","salmon", DIFICULTYS)
    carteles = crear_carteles(ventana,SIZE_WINDOW,fuentes)
    lista_boton_pistas = boton_pistas(ventana, fuentes["fuente_pistas"], "black", "aquamarine4", CLUES)
    entrada = crear_text_box(ventana, fuentes["fuente_matriz"], "chartreuse3", "grey36", (SIZE_WINDOW[0]/2 - 75, SIZE_WINDOW[1] - 50), (150, 50))
    print(diccionario_ronda["lista_palabras"])
    MOVE_RECT_EVENT = pg.USEREVENT + 1
    pg.time.set_timer(MOVE_RECT_EVENT, 50)
    MOVE_RECT_EVENT_POST = pg.USEREVENT + 2
    direccion = [1]
    velocidad = 50
    while bandera_juego:
        bandera_juego = manejar_eventos(ventana, boton_modos, entrada, diccionario_ronda, diccionario_partida, palabras, lista_boton_pistas, carteles, MOVE_RECT_EVENT, direccion, velocidad, MOVE_RECT_EVENT_POST)
        manejar_inicio(diccionario_partida,ventana,carteles,fuentes)
        manejar_juego(diccionario_partida, ventana, diccionario_ronda, fuentes, entrada, palabras, DIFICULTYS, carteles, lista_boton_pistas, boton_modos)
        reloj.tick(20)
        pg.display.update()
    pg.quit()

main()
