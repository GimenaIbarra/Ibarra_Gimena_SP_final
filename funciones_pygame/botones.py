import pygame as pg
#from eventos.manejo_eventos import pista_comida, pista_continente
from logica_juego.funciones import generar_letra_random, activar_sonido, desactivar_sonido
def dibujar_boton(boton: dict):
    boton["pantalla"].blit(boton["superficie"], boton["rectangulo"])

def crear_lista_botones_dificultad(ventana: pg.Surface,fuente:list, color:str|tuple, color_fondo:str|tuple ,dificultades: list ) -> list:
    """Funcion que se encarga de crear una lista de botones con las dificultades

    Args:
        ventana (pg.Surface): Ventana de pygame
        fuente (list): Fuente de pygame
        color (str | tuple): Color de la fuente
        color_fondo (str | tuple): Color de fondo
        dificultades (list): Lista de dificultades

    Returns:
        list: Lista de botones
    """    
    boton_modos = []
    ventana_size = ventana.get_size()
    posicion_botones_x = ventana_size[0] / 2 - 225
    posicion_botones_y = 0
    for i in range(len(dificultades)):
        boton = crear_boton(ventana, (posicion_botones_x, posicion_botones_y), (150, 50), f"{dificultades[i]} caracteres", fuente, color, color_fondo)
        boton["dificultad"] = dificultades[i]
        boton_modos.append(boton)
        posicion_botones_x += 150
    return boton_modos

def boton_pistas(ventana: pg.Surface, fuente :tuple, color:str|tuple, color_fondo:str|tuple, pistas: dict) -> list:
    """Funcion que se encarga de crear una lista de botones con las pistas

    Args:
        ventana (pg.Surface): Ventana de pygame
        fuente (tuple): Fuente de pygame
        color (str | tuple): Color de la fuente
        color_fondo (str | tuple): Color de fondo
        pistas (dict): Diccionario con las pistas

    Returns:
        list: Lista de botones
    """    
    lista = []
    lista_path = [r"images\continente.webp",r"images\letras.jpg",r"images\comida.webp"]
    lista_acciones = [pista_continente,generar_letra_random,pista_comida]
    WINDOW_SIZE = ventana.get_size()
    posicion_y = 80
    indice = 0
    for elemento in pistas:
        boton = crear_boton(ventana, (WINDOW_SIZE[0] - 180, posicion_y), (180, 100), "", fuente, color, color_fondo,imagen=lista_path[indice])
        boton["usos"] = pistas[elemento]
        boton["accion"] = lista_acciones[indice]
        indice += 1
        print(boton["usos"])
        posicion_y += 105
        lista.append(boton)
    return lista

def dibujar_input(text_box: dict):
    """Funcion que se encarga de dibujar un input

    Args:
        text_box (dict): Diccionario con los datos del input
    """    
    #
    superficie = text_box["Fuente"].render(text_box["Texto"], True, "Black")
    rect_texto = superficie.get_rect()
    rect_texto.center = text_box["Rectangulo"].center
    text_box["Ventana"].blit(superficie, rect_texto)
    pg.draw.rect(text_box["Ventana"], text_box["Color_Actual"], text_box["Rectangulo"], 2)
    

def dibujar_lineas(superficie: pg.Surface, texto:str, x:int, y:int, fuente:tuple, color:str|tuple):
    """Funcion que se encarga de dibujar lineas de texto

    Args:
        superficie (pg.Surface): Superficie de pygame
        texto (str): Texto a dibujar
        x (int): Posicion x
        y (int): Posicion y
        fuente (str | tuple): Fuente de pygame
        color (str | tuple): Color de la fuente
    """    
    fuente_p = pg.font.SysFont(fuente[0], fuente[1])
    
    lineas = texto.splitlines()
    for linea in lineas:
        superficie_texto = fuente_p.render(linea, True, color)
        superficie.blit(superficie_texto, (x, y))
        y += fuente_p.get_height()

def crear_text_box(ventana:pg.surface, fuente:str|tuple, color_activo:str|tuple, color_desactivado:str|tuple, posicion:tuple, dimensiones:tuple) -> dict:
    """Funcion que se encarga de crear un input

    Args:
        ventana (pg.surface): Ventana de pygame
        fuente (str | tuple): Fuente de pygame
        color_activo (str | tuple): Color de el rectangulo activo
        color_desactivado (str | tuple): Color de el rectangulo desactivado
        posicion (tuple): Posicion del input
        dimensiones (tuple): Dimensiones del input

    Returns:
        dict: Diccionario con los datos del input
    """    
    text_box = {}
    text_box["Ventana"] = ventana
    text_box["Color_Activado"] = color_activo
    text_box["Color_Desactivado"] = color_desactivado
    text_box["Texto"] = ""
    text_box["Activo"] = False
    text_box["Fuente"] = pg.font.SysFont(fuente[0], fuente[1])
    text_box["Rectangulo"] = pg.Rect(posicion[0], posicion[1], dimensiones[0], dimensiones[1])
    text_box["Color_Actual"] = color_desactivado
    return text_box

def crear_boton(ventana: pg.Surface, posicion:tuple, dimension:tuple, texto:str, fuente:tuple, color:str|tuple, color_fondo:str|tuple, bandera= False, posicion_texto = None, accion = None, imagen: str = None) -> dict:
    """Funcion que se encarga de crear un boton

    Args:
        ventana (pg.Surface): Ventana de pygame
        posicion (tuple): Posicion del boton
        dimension (tuple): Dimensiones del boton
        texto (str): Texto del boton
        fuente (tuple): Fuente del boton
        color (str | tuple): Color de la fuente
        color_fondo (str | tuple): Color de fondo
        bandera (bool, optional): Bandera de centralizacion. Defaults to False.
        posicion_texto (_type_, optional): Posicion del texto. Defaults to None.
        accion (function, optional): Accion que puede hacer el boton, funciones. Defaults to None.
        imagen (str, optional): Path del archivo . Defaults to None.

    Returns:
        dict: Diccionario con los datos del boton
    """    
    boton = {}
    boton["pantalla"] = ventana
    boton["posicion"] = posicion
    boton["dimension"] = dimension
    boton["Presionado"] = False
    boton["superficie"] = pg.Surface(dimension)
    boton["superficie"].fill(color_fondo)

    if accion != None:
        boton["accion"] = accion
    if imagen != None:
        img = pg.image.load(imagen)
        boton["superficie"] = pg.transform.scale(img,boton["dimension"])

    boton["rectangulo"] = pg.Rect(posicion, dimension)
    boton["rectangulo"].topleft = boton["posicion"]

    if texto != None and fuente != None:
        boton["texto"] = texto
        fuente_texto = pg.font.SysFont(fuente[0], fuente[1])
        texto_renderizado = fuente_texto.render(texto, True, color)
        boton["fuente"] = texto_renderizado
        texto_rect = texto_renderizado.get_rect(center = (dimension[0] // 2, dimension[1] // 2))
        
        boton["superficie"].blit(texto_renderizado,texto_rect)

    return boton

def pista_continente(ventana:pg.surface, diccionario_rondas:dict, fuente:tuple):
    """Funcion que se encarga de mostrar la pista del continente

    Args:
        ventana (pg.surface): Ventana de pygame
        diccionario_rondas (dict): Diccionario de las rondas
        fuente (tuple): Fuente de pygame
    """    
    pista = crear_boton(ventana, (200, 100), (400, 400), diccionario_rondas["lista_palabras"][diccionario_rondas["indice_actual"]]["continente"], fuente, "black", "salmon")
    dibujar_boton(pista)
    pg.display.update()
    pg.time.wait(5000)

def pista_comida(ventana:pg.surface,diccionario_rondas:dict,fuente:tuple):
    """Funcion que se encarga de mostrar la pista de la comida

    Args:
        ventana (pg.surface): Ventana de pygame
        diccionario_rondas (dict): Diccionario de las rondas
        fuente (tuple): Fuente de pygame
    """    
    pista = crear_boton(ventana, (200, 100), (400, 400), diccionario_rondas["lista_palabras"][diccionario_rondas["indice_actual"]]["comida"], fuente, "black", "salmon")
    dibujar_boton(pista)
    pg.display.update()
    pg.time.wait(5000)

def crear_carteles (ventana:pg.surface,SIZE_WINDOW:tuple,fuentes:tuple) -> dict:
    """Funcion que se encarga de crear los carteles

    Args:
        ventana (pg.surface): Ventana de pygame
        SIZE_WINDOW (tuple): Tamaño de la ventana
        fuentes (tuple): Fuentes de pygame

    Returns:
        dict: Diccionario con los carteles
    """    
    carteles = {}
    carteles["pantalla_inicio"] = crear_boton(ventana,(0,0),(SIZE_WINDOW[0],SIZE_WINDOW[1]),"Bienvenido a Palabrini", fuentes["fuente_palabras"], "black", "white", imagen= r"images\fondo_pantalla_inicio.png")
    carteles["Activar_Sonido"] = crear_boton(ventana,(400, 250),(50,50),"",None,"black","black",imagen= r"images\sonido_on.png", accion= activar_sonido)
    carteles["Desactivar_Sonido"] = crear_boton(ventana,(400, 250),(50,50),"",None,"black","black",imagen= r"images\sonido_off.png", accion=desactivar_sonido)
    carteles["Desactivar_Sonido"]["Presionado"] = True
    carteles["cartel_usuario"]= crear_boton(ventana,(0,0),(SIZE_WINDOW[0],SIZE_WINDOW[1]),"Ingrese su nombre de usuario",("Arial", 40),"black",(164, 187, 254))
    carteles["jugar_otra_vez"] = crear_boton(ventana,(SIZE_WINDOW[0] / 2 - 150,0),(300,100),"Jugar otra vez",("Arial", 30),"black","salmon")
    carteles["boton_volver"] = crear_boton(ventana,(SIZE_WINDOW[0] - 200 - 150,SIZE_WINDOW[1] - 100),(350,80),"Volver al menu principal",("Arial", 30),"black","tomato3")
    return carteles
