import random
import pygame as pg

#! ARREGLARLA RETURN CONDICIONAL
def obtener_palabra(lista_palabras:list, dificultad:int) -> dict:
    """Obtiene una palabra de la lista de palabras que coincida con la dificultad

    Args:
        lista_palabras (dict): Lista de palabras
        dificultad (int): Dificultad de la palabra

    Returns:
        dict: Palabra obtenida
    """    
    try:
        palabra_obtenida = random.choice(lista_palabras)
        if palabra_obtenida["caracteres"] == dificultad:
            salida = palabra_obtenida
        else:
            salida = obtener_palabra(lista_palabras, dificultad)
        return salida
    except :
        print("No se encontraron palabras con esa dificultad")
        quit()            

# def obtener_palabra(lista_palabras,dificultad):
#     if len(lista_palabras) >0 :
#         while True:
#             palabra_obtenida = random.choice(lista_palabras)
#             for i in range(len(lista_palabras)):
#                 if palabra_obtenida["caracteres"] == dificultad:
#                     salida = palabra_obtenida
#                     break
#                 else:
#                     salida = None
#     else:
#         salida = None
#     return salida



# def obtener_palabra(lista_palabras, dificultad):
#     # Filtrar palabras que coincidan con la dificultad
#     palabras_filtradas = [palabra for palabra in lista_palabras if palabra["caracteres"] == dificultad]
    
#     if palabras_filtradas:
#         # Elegir una palabra aleatoria de las filtradas
#         return random.choice(palabras_filtradas)
#     else:
#         print("No se encontraron palabras con esa dificultad")
#         return None  # O puedes lanzar una excepción si prefieres

# def obtener_palabra(lista_palabras, dificultad, intentos=10):
#     # Filtrar palabras que coincidan con la dificultad
#     palabras_filtradas = [palabra for palabra in lista_palabras if palabra["caracteres"] == dificultad]
    
#     if palabras_filtradas:
#         # Elegir una palabra aleatoria de las filtradas
#         return random.choice(palabras_filtradas)
#     else:
#         # Si no se encontraron palabras, y todavía tenemos intentos
#         if intentos > 0:
#             print("No se encontraron palabras con esa dificultad. Intentando de nuevo...")
#             return obtener_palabra(lista_palabras, dificultad, intentos - 1)
#         else:
#             print("No se encontraron palabras con esa dificultad después de varios intentos.")
#             return None  # O lanzar una excepción si prefieres
def generar_matriz(palabra_obtenida: dict, intentos:int) -> list:
    """Genera una matriz de la palabra obtenida
    
    Args:
        palabra_obtenida (dict): Palabra obtenida de la lista de palabras
        intentos (int): Cantidad de intentos

    Returns:
        list: Matriz generada
    """    
    matriz = []
    for i in range(intentos):
        matriz_temporal = ["_"] * palabra_obtenida["caracteres"]
        matriz.append(matriz_temporal)
    return matriz


def modificar_puntuacion_nuevo(diccionario_ronda: dict,
                               lista_puntuacion: list) -> int:
    """Modifica la puntuacion del jugador en la ronda actual

    Args:
        diccionario_ronda (dict): Diccionario con los datos de la ronda
        lista_puntuacion (list): Lista con los datos de la puntuacion

    Returns:
        int: Puntuacion obtenida
    """    

    puntuacion = 0
    if len(diccionario_ronda["sets_acertados"]) == len(diccionario_ronda["lista_palabras"][diccionario_ronda["indice_actual"]]["pais"]):
        intentos = diccionario_ronda["lista_intentos"][diccionario_ronda["indice_actual"]] - 1
        for i in range(len(lista_puntuacion)):
            if diccionario_ronda["lista_palabras"][diccionario_ronda["indice_actual"]]["caracteres"] == lista_puntuacion[i][0]:
                puntuacion += lista_puntuacion[i][1]
                if intentos > 1:
                    puntuacion -= lista_puntuacion[i][2] * intentos
    return puntuacion

      # generar_letra_random(diccionario_rondas["lista_palabras"][diccionario_rondas["indice_actual"]], diccionario_rondas["lista_matrices"][diccionario_rondas["indice_actual"]], diccionario_rondas["lista_intentos"][diccionario_rondas["indice_actual"]], diccionario_rondas["sets_acertados"])
def generar_letra_random(ventana:pg.Surface, diccionario_rondas:dict, fuente:tuple) -> None:  
    """Genera una letra random en la matriz

    Args:
        ventana (pg.Surface): Ventana de pygame
        diccionario_rondas (dict): Diccionario con los datos de la ronda
        fuente (tuple): Fuente de pygame
    """    
    validacion = True
    letras_sin_acertar = recuperar_letras_no_acertadas(diccionario_rondas["lista_palabras"][diccionario_rondas["indice_actual"]],  diccionario_rondas["sets_acertados"])
    while validacion:
        letra_random = random.choice(letras_sin_acertar)
        if verificar_que_la_letra_no_se_haya_adivinado(letra_random, diccionario_rondas["lista_matrices"][diccionario_rondas["indice_actual"]],diccionario_rondas["sets_acertados"]):
            diccionario_rondas["lista_matrices"][diccionario_rondas["indice_actual"]][diccionario_rondas["lista_intentos"][diccionario_rondas["indice_actual"]]][letra_random] = diccionario_rondas["lista_palabras"][diccionario_rondas["indice_actual"]]["pais"][letra_random] 
            diccionario_rondas["lista_intentos"][diccionario_rondas["indice_actual"]], diccionario_rondas["sets_acertados"].add(letra_random)
            validacion = False


def recuperar_letras_no_acertadas(palabra: dict, indices_acertados: set) -> list:
    """Recupera las letras no acertadas de la palabra

    Args:
        palabra (dict): Palabra obtenida de la lista de palabras
        indices_acertados (set): Indices correctos de la palabra

    Returns:
        list: Letras no acertadas de la palabra
    """
    letras_no_acertadas = []
    for i in range(len(palabra["pais"])):
        if validar_indice_en_lista(i, indices_acertados):
            letras_no_acertadas.append(i)
            print(letras_no_acertadas)
    return letras_no_acertadas


def verificar_que_la_letra_no_se_haya_adivinado(letra: str, matriz: list, indices_acertados: set) -> bool:
    """Verifica que la letra no se haya adivinado anteriormente

    Args:
        letra (str): Letra a verificar
        matriz (list): Matriz que se muestra en pantalla
        indices_acertados (set): Indices correctos de la palabra

    Returns:
        bool: True si la letra no se ha adivinado, False si se ha adivinado
    """
    validacion = True
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if letra == matriz[i][j] and not validar_indice_en_lista(j, indices_acertados):
                validacion = False
    return validacion


def validar_indice_en_lista(indice: int, lista: set) -> bool:
    """Valida si un indice se encuentra en una lista

    Args:
        indice (int): Indice a validar
        lista (list): Lista en la que se quiere validar el indice

    Returns:
        bool: True si el indice no se encuentra en la lista, False si se encuentra
    """
    validacion = True
    for elemento in lista:
        if elemento == indice:
            validacion = False
    return validacion

def activar_sonido(diccionario_partida:dict, carteles:dict):
    """Activa el sonido

    Args:
        diccionario_partida (dict): Diccioanrio con los datos de la partida
        carteles (dict): Diccionario con los carteles
    """    
    diccionario_partida["sonido"] = True
    carteles["Activar_Sonido"]["Presionado"] = True
    carteles["Desactivar_Sonido"]["Presionado"] = False

def desactivar_sonido(diccionario_partida:dict, carteles:dict):
    """Desactiva el sonido

    Args:
        diccionario_partida (dict): Diccionario con los datos de la partida
        carteles (dict): Diccionario con los carteles
    """    
    diccionario_partida["sonido"] = False
    carteles["Activar_Sonido"]["Presionado"] = False
    carteles["Desactivar_Sonido"]["Presionado"] = True
    

