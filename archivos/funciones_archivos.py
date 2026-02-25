import re
import json


def obtener_lista_palabras(path: str = "palabras.csv") -> list:
    """
    Obtiene una lista de palabras de un archivo csv.

    Args:
        path (str, optional): Path hacia el archivo csv. Defaults to "palabras.csv".

    Returns:
        list: Lista de palabras.
    """
    lista = []

    with open(path, "r", encoding="utf-8") as archivo:
        archivo.readline().split(",")
        for linea in archivo:

            lectura = re.split(",|\n", linea)
            for i in range(len(lectura)):
                lectura[i] = lectura[i].lower()
            lista.append(lectura)
    lista = normalizar_en_diccionario(lista)
    return lista


def normalizar_en_diccionario(palabras: list) -> list[dict]:
    """Funcion que se encarga de normalizar una lista de palabras en un diccionario

    Args:
        palabras (list): Lista de palabras

    Returns:
        list[dict]: Lista de diccionarios con las palabras normalizadas
    """    
    diccionario = []

    for palabra in palabras:
        diccionario_temporal = {}
        diccionario_temporal["palabra"] = palabra[0]
        diccionario_temporal["caracteres"] = int(palabra[1])
        diccionario_temporal["categoria"] = palabra[2]
        diccionario_temporal["mezclada"] = palabra[3]
        diccionario.append(diccionario_temporal)

    return diccionario

#region guardar 


def guardar_puntuacion(lista_botones_comodines:list,diccionario_partidas:dict) -> tuple[int, int]:
    """Funcion que se encarga de guardar la puntuacion del jugador en un archivo .JSON

    Args:
        lista_botones_comodines (list): Lista de botones de comodin
        diccionario_partidas (dict): Diccionario con los datos de la partida

    Returns:
        tuple[int, int]: Tiempo total y puntuacion total
    """    
    # tiempo_rondas: list, contador_victorias: int, lista_puntuacion: list,usos_comodines: list, nombre_ingresado: str
    tiempo_rondas = diccionario_partidas["tiempo_rondas"]
    contador_victorias = diccionario_partidas["cantidad_palabras_acertadas"][0]
    lista_puntuacion = diccionario_partidas["puntaje"]
    usos_comodines = lista_botones_comodines
    nombre_ingresado = diccionario_partidas["nombre_usuario"]
    tiempo_total = [0]
    puntaje_total = calcular_valores_a_guardar(tiempo_rondas, contador_victorias, lista_puntuacion, usos_comodines,tiempo_total, diccionario_partidas)
    partidas_jugadas = diccionario_partidas["cantidad_palabras_acertadas"] + diccionario_partidas["cantidad_palabras_falladas"]
    puntuaciones = comprobar_si_existe_archivo("puntuaciones.json")
    puntuaciones.append(
        {"nombre": nombre_ingresado, "partidas_jugadas": partidas_jugadas, "contador_victorias": contador_victorias,"tiempo_promedio": tiempo_total[0] / len(tiempo_rondas), "puntaje_total": puntaje_total})

    with open("puntuaciones.json", "w", encoding="utf-8") as archivo:
        json.dump(puntuaciones, archivo, indent=4, ensure_ascii=False)
    return tiempo_total[0], puntaje_total



def comprobar_si_existe_archivo(path: str) -> list:
    """Funcion que se encarga de comprobar si existe el archivo

    Args:
        path (str): Path del archivo a comprobar si existe .JSON

    Returns:
        list: Lista de puntuaciones
    """
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            puntuaciones = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        puntuaciones = []
    return puntuaciones


def calcular_valores_a_guardar(tiempo_rondas: list, contador_victorias: int, lista_puntuacion: list,
                                lista_botones: list, tiempo_total: list, diccionario_partidas: dict) -> int:
    """Funcion que se encarga de calcular los valores a guardar en el archivo .JSON

    Args:
        tiempo_rondas (list): Lista para el tiempo de c ronda
        contador_victorias (int): entero de victorias
        lista_puntuacion (list): Lista de puntuaciones
        lista_botones (list): Lista de botones
        tiempo_total (list): Tiempo de las rondas
        diccionario_partidas (dict): Dicconario con los datos de la partida

    Returns:
        int: Puntuacion total
    """    
    suma_tiempo_total = sumar_lista(tiempo_rondas)
    puntaje_total = sumar_lista(lista_puntuacion)
    puntaje_total = puntuar_por_tiempo(suma_tiempo_total, contador_victorias, puntaje_total,diccionario_partidas)
    puntaje_total = restar_puntuacion_comodines(puntaje_total, lista_botones)
    
    tiempo_total[0] = suma_tiempo_total
    return puntaje_total


def restar_puntuacion_comodines(puntuacion: int, lista_botones:list) -> int:
    """Funcion que se encarga de restar puntuacion por comodines no usados

    Args:
        puntuacion (int): Puntuacion actual
        lista_botones (list): Lista de botones

    Returns:
        int: Puntuacion modificada
    """    
    if lista_botones[0]["usos"] == 0:
        puntuacion -= 15
    if lista_botones[1]["usos"] == 0:
        puntuacion -= 25
    if lista_botones[2]["usos"] == 0:
        puntuacion -= 10
    return puntuacion
    


def sumar_lista(lista: list) -> int:
    """Funcion que se encarga de sumar los valores de una lista

    Args:
        lista (list): Lista a sumar

    Returns:
        int: Suma de los valores de la lista
    """
    suma = 0
    for numero in lista:
        suma += numero
    return suma

def puntuar_por_tiempo(tiempo_total: int, contador_victorias: int, puntuacion: int,diccionario_partidas: dict) -> int:
    """Puntua al jugador en base al tiempo que le tomo ganar y la cantidad de victorias que tiene

    Args:
        tiempo_total (int): Tiempo total que le tomo al jugador ganar
        contador_victorias (int): Cantidad de victorias que tiene el jugador
        puntuacion (int): Puntuacion actual del jugador
        diccionario_partidas (dict): Diccionario con los datos de la partida

    Returns:
        int: Puntuacion modificada
    """
    if tiempo_total / 60 <= 15 and contador_victorias == 5:
        puntuacion += 100
        diccionario_partidas["bandera_puntuo_por_tiempo"] = True
    return puntuacion

def recuperar_puntuacion_mas_alta(path: str) -> tuple[int, str]:
    """Funcion que se encarga de recuperar la puntuacion mas alta de un archivo .JSON

    Args:
        path (str): Path del archivo .JSON

    Returns:
        tuple[int, str]: Puntuacion mas alta y nombre del jugador
    """    
    puntuaciones = comprobar_si_existe_archivo(path)
    puntuacion_mas_alta = 0
    nombre = ""
    if len(puntuaciones) != 0:
        for puntuacion in puntuaciones:
            if puntuacion["puntaje_total"] > puntuacion_mas_alta:
                puntuacion_mas_alta = puntuacion["puntaje_total"]
                nombre = puntuacion["nombre"]
                
    return puntuacion_mas_alta, nombre
    
