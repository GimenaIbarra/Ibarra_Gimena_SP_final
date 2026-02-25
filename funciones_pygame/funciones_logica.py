
from funciones_pygame.botones import crear_boton, dibujar_boton
from logica_juego.funciones import *
from configs import *
import pygame as pg 
import time

def generar_palabras(dificultad:list, diccionario_palabras: dict) -> list:
    """Funcion que se encarga de generar una lista de palabras

    Args:
        dificultad (list): Lista de dificultades
        diccionario_palabras (dict): Diccionario con las palabras

    Returns:
        list: Lista de palabras
    """    
    lista_palabras = []
    for i in range(len(dificultad)):
        palabra_generada = obtener_palabra(diccionario_palabras,dificultad[i])
        lista_palabras.append(palabra_generada)
        
    return lista_palabras

def generar_lista_matrices (dificultad:list ,lista_palabras: list,intentos:int) -> list:
    """Funcion que se encarga de generar una lista de matrices

    Args:
        dificultad (list): Lista de dificultades
        lista_palabras (list): Lista de palabras
        intentos (int): Cantidad de intentos

    Returns:
        list: Lista de matrices
    """    
    lista_matrices = []
    for i in range(len(dificultad)):
        matriz = generar_matriz(lista_palabras[i],intentos)
        lista_matrices.append(matriz)
    return lista_matrices

def verificar_palabra_p(palabra_ingresada: str, palabra_obtenida: dict, matriz: list,intentos:int)-> set:
    """Funcion que se encarga de verificar si la palabra ingresada es correcta

    Args:
        palabra_ingresada (str): Palabra ingresada por el usuario
        palabra_obtenida (dict): Palabra obtenida de la lista de palabras
        matriz (list): Matriz que se muestra en pantalla
        intentos (int): Cantidad de intentos

    Returns:
        set: Set de indices acertados
    """    
    set_acertados = set()
    for i in range(len(palabra_obtenida["pais"])):
        if palabra_ingresada[i] == palabra_obtenida["pais"][i]:
            matriz[intentos][i] =  palabra_ingresada[i] 
            set_acertados.add(i)
        else:
            matriz[intentos][i] = palabra_ingresada[i]
    return set_acertados

def mostrar_matriz_p(ventana: pg.Surface, matriz:list, fuente:tuple, color:str|tuple, color_fondo:str|tuple,palabra:dict):
    """Funcion que se encarga de mostrar la matriz en pantalla

    Args:
        ventana (pg.Surface): Ventana de pygame
        matriz (list): Matriz que se muestra en pantalla
        fuente (tuple): Fuente de pygame
        color (str | tuple): Color de la fuente
        color_fondo (str | tuple): Color de fondo
        palabra (dict): Palabra obtenida de la lista de palabras
    """    
    ventana_size = ventana.get_size()
    boton_ancho, boton_alto = 50, 50
    x, y = ventana_size[0] / 2 - 150, 100
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == palabra["pais"][j]:
                boton = crear_boton(ventana, (x, y), (boton_ancho, boton_alto), matriz[i][j], fuente, color, "green", False)
            elif matriz[i][j] in palabra["pais"]:
                boton = crear_boton(ventana, (x, y), (boton_ancho, boton_alto), matriz[i][j], fuente, color, "yellow", False)
            elif matriz[i][j] == "_":
                boton = crear_boton(ventana, (x, y), (boton_ancho, boton_alto), matriz[i][j], fuente, color, color_fondo, False)
            else:
                boton = crear_boton(ventana, (x, y), (boton_ancho, boton_alto), matriz[i][j], fuente, color, (68, 65, 65), False)
            
            dibujar_boton(boton)
            x += 50  
        x = ventana_size[0] / 2 - 150
        y += 50  
        
def verificar_perdio_gano(entrada:dict, diccionario_partidas:dict, diccionario_rondas:dict,palabras:dict):
    """Funcion que se encarga de verificar si el jugador perdio o gano

    Args:
        entrada (dict): Diccionario con la entrada del usuario
        diccionario_partidas (dict): Diccionario con los datos de la partida
        diccionario_rondas (dict): Diccionario con los datos de la ronda
        palabras (dict): Diccionario con las palabras
    """    
    ventana = diccionario_partidas["ventana"].get_size()
    bandera = False
    bandera = verificar_perdio(diccionario_rondas,diccionario_partidas,ventana,entrada,bandera)
    bandera = verificar_gano(diccionario_partidas,diccionario_rondas,entrada,palabras, ventana,bandera)
    pg.display.update()
    diccionario_rondas["tiempo_final"] = time.time()
    reiniciar_ronda(bandera,diccionario_rondas,diccionario_partidas, palabras)
    


        
def reiniciar_variables (diccionario_rondas:dict,palabras:dict, dificultades:list):
    """Funcion que se encarga de reiniciar las variables de la ronda

    Args:
        diccionario_rondas (dict): Diccionario con los datos de la ronda
        palabras (dict): Diccionario con las palabras
        dificultades (list): Lista de dificultades
    """    
    for i in range(len(diccionario_rondas["lista_matrices"])):
        
        diccionario_rondas["lista_palabras"][i] = obtener_palabra(palabras, dificultades[i])
        diccionario_rondas["lista_matrices"][i] = generar_matriz(diccionario_rondas["lista_palabras"][i], 6)
        diccionario_rondas["lista_intentos"][i] = 0
        
        
def verificar_gano(diccionario_partidas:dict,diccionario_rondas:dict,entrada:dict,palabras:dict, ventana:pg.Surface, bandera:bool)->bool:
    """Funcion que se encarga de verificar si el jugador gano

    Args:
        diccionario_partidas (dict): Diccionario con los datos de la partida
        diccionario_rondas (dict): Diccionario con los datos de la ronda
        entrada (dict): Diccionario con la entrada del usuario
        palabras (dict): Diccionario con las palabras
        ventana (pg.Surface): Ventana de pygame
        bandera (bool): Bandera que indica si el jugador gano

    Returns:
        bool: Bandera que indica si el jugador gano
    """    
    cartel_gano = crear_boton(diccionario_partidas["ventana"],(0,0),(ventana[0],ventana[1]),"",("Arial", 30),"goldenrod1","mediumturquoise", imagen= r"images\gano.png")
    if diccionario_rondas["lista_palabras"][diccionario_rondas["indice_actual"]]["pais"] == entrada["Texto"]:
        diccionario_partidas["cantidad_palabras_acertadas"][0] += 1
        bandera = True
        cartel_pais =crear_boton(diccionario_partidas["ventana"],(0,0),(ventana[0],ventana[1]),f"Acertaste el pais era {diccionario_rondas['lista_palabras'][diccionario_rondas['indice_actual']]['pais']}",("Arial", 40),"black",(164, 187, 254))
        dibujar_boton(cartel_pais)
        pg.display.update()
        pg.time.wait(2000)
        dibujar_boton(cartel_gano)
        if diccionario_partidas["sonido"]:
            pg.mixer_music.load(r"sounds\gano.mp3")
            pg.mixer_music.play()
    return bandera

def verificar_perdio (diccionario_rondas:dict,diccionario_partidas:dict,ventana:pg.surface, entrada:dict, bandera:bool)->bool:
    """Funcion que se encarga de verificar si el jugador perdio

    Args:
        diccionario_rondas (dict): Diccionario con los datos de la ronda
        diccionario_partidas (dict): Diccionario con los datos de la partida
        ventana (pg.surface): Ventana de pygame
        entrada (dict): Diccionario con la entrada del usuario
        bandera (bool): Bandera que indica si el jugador perdio

    Returns:
        bool: Bandera que indica si el jugador perdio
    """    
    cartel_perdio = crear_boton(diccionario_partidas["ventana"],(0,0),(ventana[0],ventana[1]),"",("Arial", 30),"Red3", "seashell4",imagen=r"images\perdio.webp")
    if diccionario_rondas["lista_intentos"][diccionario_rondas["indice_actual"]] == 6 and diccionario_rondas["lista_palabras"][diccionario_rondas["indice_actual"]]["pais"] != entrada["Texto"]:
        diccionario_partidas["cantidad_palabras_falladas"][0] += 1
        bandera = True
        cartel_pais =crear_boton(diccionario_partidas["ventana"],(0,0),(ventana[0],ventana[1]),f"Fallaste perro era {diccionario_rondas['lista_palabras'][diccionario_rondas['indice_actual']]['pais']}",("Arial", 40),"black",(164, 187, 254))
        dibujar_boton(cartel_pais)
        pg.display.update()
        pg.time.wait(2000)
        dibujar_boton(cartel_perdio)
        if diccionario_partidas["sonido"]:

            pg.mixer_music.load(r"sounds\perdio.mp3")
            pg.mixer_music.play()
            
    return bandera
        
def reiniciar_ronda(bandera:bool, diccionario_rondas:dict, diccionario_partidas:dict, palabras:dict):
    """Funcion que se encarga de reiniciar la ronda

    Args:
        bandera (bool): Bandera que indica si el jugador gano
        diccionario_rondas (dict): Diccionario con los datos de la ronda
        diccionario_partidas (dict): Diccionario con los datos de la partida
        palabras (dict): Diccionario con las palabras
    """    
    if bandera:
        diccionario_partidas["tiempo_rondas"].append( diccionario_rondas["tiempo_final"] - diccionario_rondas["tiempo_inicio"] )
        pg.time.wait(10000)
        diccionario_rondas["tiempo_inicio"] = time.time()
        
        palabratemp = obtener_palabra(palabras, diccionario_rondas["dificultad_actual"])
        print(palabratemp)
        diccionario_rondas["lista_palabras"][diccionario_rondas["indice_actual"]]= palabratemp
        diccionario_rondas["lista_matrices"][diccionario_rondas["indice_actual"]] = generar_matriz(palabratemp, 6)
        diccionario_partidas["puntaje"].append(modificar_puntuacion_nuevo(diccionario_rondas, POINTS_FOR_DIFICULTY))
        diccionario_rondas["lista_intentos"][diccionario_rondas["indice_actual"]] = 0
        diccionario_partidas["cantidad_intentos_actuales"] += 1

        print(diccionario_partidas["tiempo_rondas"])
        diccionario_rondas["sets_acertados"] = set()
        
