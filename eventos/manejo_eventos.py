import pygame as pg
from funciones_pygame.funciones_logica import *
from archivo.funciones_archivo import recuperar_puntuacion_mas_alta


def manejar_eventos(ventana: pg.Surface, boton_modos: list, entrada: dict, diccionario_ronda:dict, diccionario_partida:dict, palabras:dict, lista_botones_pistas:list[dict], carteles: dict[dict], MOVE_RECT_EVENT: pg.event, direccion: list[int], velocidad: list[int],evento_post: pg.event) -> bool:
    """

    Args:
        ventana (pg.Surface): ventana
        boton_modos (list): Lista de botones dificultad
        entrada (dict): Diccionario del boton que maneja los inputs
        diccionario_ronda (dict): Diccionario que contiene variables usadas en ronda
        diccionario_partida (dict): Dict que contiene var usadas en la partida
        palabras (dict): Diccionario de palabras leidas de archivo
        lista_botones_pistas (list[dict]): Lista de botones para las pistas
        carteles (dict[dict]): Carteles de la pantalla
        MOVE_RECT_EVENT (pg.event): Evento Customizado
        direccion (list[int]): Dirección de movimiento del rectangulo
        velocidad (list[int]): Velocidad de movimiento del rectangulo
        evento_post (pg.event): Evento customizado

    Returns:
        bool: si es falso cierra el juego
    """    
    validacion = True
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            validacion = False
        if evento.type == pg.MOUSEBUTTONDOWN:
            manejar_click_mouse(boton_modos, entrada, evento, diccionario_ronda, lista_botones_pistas, ventana, carteles, diccionario_partida)
        if evento.type == pg.KEYDOWN:
            manejar_teclado( entrada, evento, diccionario_ronda, diccionario_partida, palabras)
        if evento.type == MOVE_RECT_EVENT:
            pg.event.post(pg.event.Event(evento_post))
        if evento.type == evento_post: 
            evento_propio(diccionario_partida, carteles, velocidad, direccion )
    return validacion

#region teclado 


def manejar_teclado( entrada: dict, evento: pg.event, diccionario_ronda:dict, diccionario_partida:dict, palabras:dict):
    """Maneja los eventos de teclado

    Args:
        entrada (dict): Diccionario del input
        evento (pg.event): Lista de eventos
        diccionario_ronda (dict): Diccionario de ronda
        diccionario_partida (dict): Diccionario de partida
        palabras (dict): Diccionario de palabras
    """    

    manejar_escritura(entrada,evento,diccionario_ronda,diccionario_partida)

    manejar_enter(evento,diccionario_partida,diccionario_ronda,entrada,palabras)


def manejar_escritura (entrada:dict,evento: pg.event ,diccionario_ronda:dict ,diccionario_partida:dict):
    """Maneja la escritura en el input

    Args:
        entrada (dict): Diccionario del input
        evento (pg.event): Evento de teclado
        diccionario_ronda (dict): Diccionario de ronda
        diccionario_partida (dict): Diccionario de partida
    """    
    if entrada["Activo"]:
        if evento.key == pg.K_BACKSPACE:
            entrada["Texto"] = entrada["Texto"][:-1]
        elif len(entrada["Texto"]) < diccionario_ronda["dificultad_actual"] and evento.unicode.isalpha():
            entrada["Texto"] += evento.unicode.lower()
        elif diccionario_partida["bandera_pantalla_final"] and evento.unicode.isalpha() and len(entrada["Texto"]) <= 7:
            entrada["Texto"] += evento.unicode.lower()

def manejar_enter(evento: pg.event,diccionario_partida:dict ,diccionario_ronda: dict ,entrada: dict ,palabras: dict):
    """Maneja el evento de enter

    Args:
        evento (pg.event): Evento de teclado
        diccionario_partida (dict): Diccionario de partida
        diccionario_ronda (dict): Diccionario de ronda
        entrada (dict): Diccionario del input
        palabras (dict): Diccionario de palabras
    """    
    if evento.key == pg.K_RETURN:
            if diccionario_partida["bandera_pantalla_final"] and len(entrada["Texto"]) > 0:
                diccionario_partida["bandera_pantalla_final"] = False
                diccionario_partida["nombre_usuario"] = entrada["Texto"]
                entrada["Texto"] = ""

            verificar_entrada( entrada, diccionario_ronda,diccionario_partida,palabras)

def verificar_entrada( entrada:dict ,diccionario_ronda:dict ,diccionario_partida:dict,palabras:dict):
    """Verifica la entrada del usuario

    Args:
        entrada (dict): Diccionario del input
        diccionario_ronda (dict): Diccionario de ronda
        diccionario_partida (dict): Diccionario de partida
        palabras (dict): Diccionario de palabras
    """    
    
    if len(entrada["Texto"]) == (diccionario_ronda["dificultad_actual"]):
        diccionario_ronda["sets_acertados"] = verificar_palabra_p(
            entrada["Texto"],
            diccionario_ronda["lista_palabras"][diccionario_ronda["indice_actual"]],
            diccionario_ronda["lista_matrices"][diccionario_ronda["indice_actual"]],
            diccionario_ronda["lista_intentos"][diccionario_ronda["indice_actual"]]
        )
        diccionario_ronda["lista_intentos"][diccionario_ronda["indice_actual"]] += 1
        verificar_perdio_gano(entrada,
        diccionario_partida,
        diccionario_ronda,
        palabras
        )
        entrada["Texto"] = ""

#endregion

#region mouse
def manejar_click_mouse(boton_modos : list, entrada :dict, evento :pg.event, diccionario_ronda:dict ,lista_botones_pistas:list, ventana: pg.surface, carteles:dict, diccionario_partida: dict):
    """Maneja el evento de click del mouse

    Args:
        boton_modos (list): Lista de botones de dificultad
        entrada (dict): Diccionario del input
        evento (pg.event): Evento de mouse
        diccionario_ronda (dict): Diccionario de ronda
        lista_botones_pistas (list): Lista de botones de pistas
        ventana (pg.surface): Ventana
        carteles (dict): Carteles
        diccionario_partida (dict): Diccionario de partida
    """    
    if diccionario_partida["estado_juego"] == "pantalla_inicio":
        
        manejar_pantalla_pincipal(diccionario_partida,carteles,evento, diccionario_ronda)
    
    elif diccionario_partida["estado_juego"] == "pantalla_ayuda":
        
        manejar_ayuda(diccionario_partida,carteles,evento)
    else:
        manejar_pistas(lista_botones_pistas,evento, diccionario_ronda, ventana)

        manejar_dificultad(boton_modos,evento,diccionario_ronda,entrada)

        manejar_input_activo(entrada,evento)
        
        manejar_reiniciar_juego(carteles, diccionario_partida, evento, lista_botones_pistas, diccionario_ronda)


def manejar_pantalla_pincipal (diccionario_partida :dict, carteles: pg.Surface,evento: pg.event, diccionario_ronda:dict):
    """Maneja la pantalla principal

    Args:
        diccionario_partida (dict): Diccionario de partida
        carteles (pg.Surface): Carteles
        evento (pg.event): Evento de mouse
        diccionario_ronda (dict): Diccionario de ronda
    """    
    if carteles["boton_jugar"]["rectangulo"].collidepoint(evento.pos):
        diccionario_partida["estado_juego"] = "pantalla_juego"
        diccionario_ronda["tiempo_inicio"] = time.time()
        diccionario_partida["mayor_puntaje"], diccionario_partida["mayor_nombre"] = recuperar_puntuacion_mas_alta("puntuaciones.json")
        
    elif carteles["boton_ayuda"]["rectangulo"].collidepoint(evento.pos):
        diccionario_partida["estado_juego"] = "pantalla_ayuda"
    elif carteles["Activar_Sonido"]["rectangulo"].collidepoint(evento.pos) and not carteles["Activar_Sonido"]["Presionado"]:
        carteles["Activar_Sonido"]["accion"](diccionario_partida, carteles)
        print(diccionario_partida["sonido"])
    elif carteles["Desactivar_Sonido"]["rectangulo"].collidepoint(evento.pos) and not carteles["Desactivar_Sonido"]["Presionado"]:
        carteles["Desactivar_Sonido"]["accion"](diccionario_partida, carteles)
        print(diccionario_partida["sonido"])

def evento_propio( diccionario_partida:dict, carteles:dict, velocidad:list, direccion:list):
    """Maneja el evento propio

    Args:
        diccionario_partida (dict): Diccionario de partida
        carteles (dict): Carteles
        velocidad (list): Velocidad de movimiento
        direccion (list): Direccion de movimiento
    """    
    rectangulo = carteles["jugar_otra_vez"]["rectangulo"]
    ancho_ventana = diccionario_partida["ventana"].get_width()

    if rectangulo.x <= 0:
        direccion[0] = 1  
 
    elif rectangulo.x >= ancho_ventana - rectangulo.width:
        direccion[0] = -1  
    
    rectangulo.x += velocidad * direccion[0]

def manejar_ayuda(diccionario_partida:dict, carteles:dict , evento : pg.event):
    """Maneja la pantalla de ayuda

    Args:
        diccionario_partida (dict): Diccionario de partida
        carteles (dict): Carteles
        evento (pg.event): Evento de mouse
    """    
    if carteles["boton_volver"]["rectangulo"].collidepoint(evento.pos):
        diccionario_partida["estado_juego"] = "pantalla_inicio"

def manejar_reiniciar_juego(carteles: pg.Surface, diccionario_partida:dict, evento:dict, lista_botones_pistas:dict, diccionario_rondas:dict):
    """Maneja el reinicio del juego

    Args:
        carteles (pg.Surface): Carteles
        diccionario_partida (dict): Diccionario de partida
        evento (dict): Evento de mouse
        lista_botones_pistas (dict): Lista de botones de pistas
        diccionario_rondas (dict): Diccionario de ronda
    """    
    if carteles["jugar_otra_vez"]["rectangulo"].collidepoint(evento.pos) and carteles["jugar_otra_vez"]["Presionado"]:
        diccionario_partida["bandera_pantalla_final"] = False
        diccionario_partida["bandera_archivo_guardado"] = False
        diccionario_partida["nombre_usuario"] = None
        diccionario_partida["cantidad_palabras_acertadas"] = [0]
        diccionario_partida["cantidad_palabras_falladas"] = [0]
        diccionario_partida["cantidad_intentos_actuales"] = 0
        diccionario_partida["tiempo_rondas"] = [0]
        diccionario_partida["puntaje"] = [0]
        diccionario_rondas["tiempo_inicio"] = time.time()
        diccionario_partida["mayor_puntaje"],diccionario_partida["mayor_nombre"] = recuperar_puntuacion_mas_alta("puntuaciones.json")
        lista_path = [r"images\continente.webp",r"images\letras.jpg",r"images\comida.webp"]
        
        
        for boton in lista_botones_pistas:
            boton["usos"] = 1
            boton["Presionado"] = False
            img = pg.image.load(lista_path[lista_botones_pistas.index(boton)])
            boton["superficie"] = pg.transform.scale(img,boton["dimension"])
            
        carteles["jugar_otra_vez"]["Presionado"] = False
        pg.display.update()
    


def manejar_input_activo (entrada:dict,evento:pg.event):
    """Maneja el input activo

    Args:
        entrada (dict): Diccionario del input
        evento (pg.event): Evento de mouse
    """    
    if entrada["Rectangulo"].collidepoint(evento.pos):
        entrada["Activo"] = True
        entrada["Color_Actual"] = entrada["Color_Activado"]
    else:
        entrada["Activo"] = False
        entrada["Color_Actual"] = entrada["Color_Desactivado"]

def manejar_dificultad (boton_modos: list, evento:pg.event, diccionario_ronda:dict,entrada:dict):
    """Maneja la dificultad

    Args:
        boton_modos (list): Lista de botones de dificultad
        evento (pg.event): Evento de mouse
        diccionario_ronda (dict): Diccionario de ronda
        entrada (dict): Diccionario del input
    """    
    for i in range(len(boton_modos)):
        if boton_modos[i]["rectangulo"].collidepoint(evento.pos):
            boton_modos[i]["Presionado"] = True
            entrada["Texto"] = ""
            diccionario_ronda["indice_actual"] = i
            diccionario_ronda["dificultad_actual"] = boton_modos[i]["dificultad"]

        else:
            boton_modos[i]["Presionado"] = False

#region "PISTAAASS"
def manejar_pistas (lista_botones_pistas: list[pg.Surface],evento:dict, diccionario_rondas:dict,ventana:pg.surface):
    """Maneja las pistas

    Args:
        lista_botones_pistas (list[pg.Surface]): Lista de botones de pistas
        evento (dict): Evento de mouse
        diccionario_rondas (dict): Diccionario de ronda
        ventana (pg.surface): Ventana
    """    
    for i in range(len(lista_botones_pistas)):
        if lista_botones_pistas[i]["rectangulo"].collidepoint(evento.pos):
            
            if not lista_botones_pistas[i]["Presionado"]:
                mostrar_pista(lista_botones_pistas,diccionario_rondas,ventana, i)
                lista_botones_pistas[i]["usos"] -= 1
                
            if lista_botones_pistas[i]["usos"] == 0 :
                lista_botones_pistas[i]["Presionado"] = True
                lista_botones_pistas[i]["superficie"].fill("grey")


def mostrar_pista(lista_botones_pistas:list,diccionario_rondas:dict,ventana:pg.surface, pista_presionada:int) -> None:
    """Muestra la pista

    Args:
        lista_botones_pistas (list): Lista de botones de pistas
        diccionario_rondas (dict): Diccionario de ronda
        ventana (pg.surface): Ventana
        pista_presionada (int): Pista presionada
    """    
    fuente = ("Arial", 40)
    for boton in lista_botones_pistas:
        if pista_presionada == lista_botones_pistas.index(boton) and boton["usos"] > 0:
            boton["accion"](ventana,diccionario_rondas,fuente)
