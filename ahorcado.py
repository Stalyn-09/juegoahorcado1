# -*- coding: utf-8 -*-
"""
Juego del Ahorcado (consola) - Versión Mejorada y Comentada
Autor: tú :)
Descripción:
    - Adivina la palabra letra por letra o completa.
    - Acepta palabras con tildes (se normalizan para comparar).
    - Muestra letras usadas, intentos restantes y dibujo del ahorcado.
    - Pide el nombre del jugador y usa asteriscos para ocultar las letras.
"""

# Importamos las librerías que necesitamos:
import random      # Para elegir palabras al azar
import unicodedata # Para manejar caracteres especiales como tildes
import os          # Para limpiar la pantalla

# ---- Dibujos del ahorcado por etapas ----
# Esta lista contiene 7 dibujos del ahorcado, desde el más completo (perdiste) hasta vacío (empezando)
# Índice 0 = ahorcado completo (perdiste el juego)
# Índice 6 = solo la horca (empezando el juego)
HANGMANPICS = [
    # Dibujo 0: Ahorcado completo - Has perdido el juego (0 intentos restantes)
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
    """,
    # Dibujo 1: Sin pie derecho (1 intento restante)
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    # Dibujo 2: Sin piernas (2 intentos restantes)
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    # Dibujo 3: Sin brazo derecho (3 intentos restantes)
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    # Dibujo 4: Sin brazos (4 intentos restantes)
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    # Dibujo 5: Solo cabeza (5 intentos restantes)
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    # Dibujo 6: Solo la horca vacía (6 intentos restantes - empezando)
    r"""
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
]

# ---- Lista de palabras para el juego ----
# Aquí guardamos todas las palabras posibles que el jugador puede adivinar
# Puedes agregar más palabras a esta lista si quieres
PALABRAS = [
    "programación", "python", "desarrollo", "computadora", "variable",
    "universidad", "ahorcado", "tecnología", "algoritmo", "internet",
    "ecuador", "servidor", "cliente", "archivo", "función", "memoria",
    "depuración", "microservicio", "contenedor", "docker", "inteligencia",
    "artificial", "aprendizaje", "máquina", "datos", "ciencia"
]

# ---- FUNCIONES DEL JUEGO ----
# Las funciones son como "mini-programas" que hacen una tarea específica

def limpiar_consola():
    """
    Esta función limpia la pantalla de la consola
    Funciona tanto en Windows como en Linux/Mac
    """
    # Si estamos en Windows, usa el comando "cls", si no, usa "clear"
    os.system("cls" if os.name == "nt" else "clear")

def normalizar(texto: str) -> str:
    """
    Esta función quita las tildes de las palabras y las convierte a mayúsculas
    Esto nos ayuda a comparar palabras sin importar si tienen tildes o no
    Ejemplo: 'programación' se convierte en 'PROGRAMACION'
    """
    # Esto quita las tildes de las letras
    nfkd = unicodedata.normalize("NFKD", texto)
    sin_tildes = "".join(c for c in nfkd if not unicodedata.combining(c))
    # Convertimos todo a mayúsculas para comparar más fácil
    return sin_tildes.upper()

def elegir_palabra() -> str:
    """
    Esta función elige una palabra al azar de nuestra lista de palabras
    Es como sacar una carta al azar de una baraja
    """
    return random.choice(PALABRAS)

def mostrar_bienvenida():
    """
    Esta función muestra la pantalla de inicio del juego y pide el nombre del jugador
    No deja continuar hasta que el jugador escriba su nombre
    """
    limpiar_consola()  # Limpiamos la pantalla
    # Mostramos un mensaje bonito de bienvenida
    print("🎮" + "="*50 + "🎮")
    print("    ¡BIENVENIDO AL JUEGO DEL AHORCADO!")
    print("🎮" + "="*50 + "🎮")
    print()
    
    # Este bucle se repite hasta que el jugador escriba su nombre
    while True:
        nombre = input("Por favor, ingresa tu nombre: ").strip()  # .strip() quita espacios extra
        # Si el nombre no está vacío, lo devolvemos
        if nombre:
            return nombre
        # Si está vacío, mostramos un mensaje de error y volvemos a preguntar
        print("⚠️ El nombre no puede estar vacío. Inténtalo de nuevo.")

def mostrar_estado(palabra_mostrada, usadas, intentos, nombre_jugador):
    """
    Esta función muestra toda la información del juego en la pantalla:
    - El nombre del jugador
    - El dibujo del ahorcado (según los intentos restantes)
    - La palabra con asteriscos y letras adivinadas
    - Las letras que ya se han usado
    - Cuántos intentos quedan
    """
    # Calculamos qué dibujo mostrar según los intentos restantes
    # Si tienes 6 intentos = dibujo 6 (horca vacía)
    # Si tienes 0 intentos = dibujo 0 (ahorcado completo)
    indice = max(0, min(len(HANGMANPICS) - 1, len(HANGMANPICS) - 1 - intentos))
    
    # Mostramos toda la información del juego
    print(f"👤 Jugador: {nombre_jugador}")
    print("="*40)  # Línea decorativa
    print(HANGMANPICS[indice])  # El dibujo del ahorcado
    print(f"Palabra:  {' '.join(palabra_mostrada)}")  # La palabra con espacios entre letras
    # Si hay letras usadas, las mostramos ordenadas; si no, decimos "(ninguna)"
    print(f"Usadas:   {', '.join(sorted(usadas)) if usadas else '(ninguna)'}")
    print(f"Intentos restantes: {intentos}")
    print("="*40)  # Otra línea decorativa

def jugar_una_partida(nombre_jugador):
    """
    Esta es la función principal del juego. Aquí ocurre toda la acción:
    - Elige una palabra secreta
    - Permite al jugador adivinar letras
    - Verifica si gana o pierde
    """
    # PREPARACIÓN DEL JUEGO
    palabra_real = elegir_palabra()              # Elegimos la palabra secreta (puede tener tildes)
    palabra_norm = normalizar(palabra_real)      # La misma palabra pero sin tildes para comparar
    
    # Creamos la palabra que el jugador ve: asteriscos (*) para letras, otros caracteres iguales
    palabra_mostrada = ["*" if ch.isalpha() else ch for ch in palabra_real]
    
    usadas = set()           # Conjunto para guardar las letras que ya se probaron
    intentos = 6            # El jugador empieza con 6 intentos

    # Mostramos información inicial
    print(f"\n¡Hola {nombre_jugador}! 🎯")
    print(f"La palabra tiene {len([ch for ch in palabra_real if ch.isalpha()])} letras.")
    input("Presiona Enter para comenzar...")

    # BUCLE PRINCIPAL DEL JUEGO
    # Este bucle se repite mientras el jugador tenga intentos restantes
    while intentos >= 0:
        limpiar_consola()  # Limpiamos la pantalla
        mostrar_estado(palabra_mostrada, usadas, intentos, nombre_jugador)  # Mostramos el estado actual

        # VERIFICAMOS SI EL JUGADOR YA GANÓ
        # Si la palabra mostrada (sin tildes) es igual a la palabra real (sin tildes), ¡ganó!
        if normalizar("".join(palabra_mostrada)) == palabra_norm:
            print(f"🎉 ¡Felicidades {nombre_jugador}! ¡Ganaste!")
            print(f"La palabra era: {palabra_real}")
            return True  # Devolvemos True porque ganó

        # PEDIMOS AL JUGADOR QUE HAGA SU JUGADA
        print(f"\n{nombre_jugador}, es tu turno:")
        intento = input("Ingresa una letra o arriesga la palabra completa: ").strip()

        # Si no escribió nada, le pedimos que intente de nuevo
        if not intento:
            print("⚠️ No ingresaste nada.")
            input("Pulsa Enter para continuar...")
            continue  # Volvemos al inicio del bucle

        # CASO 1: EL JUGADOR INTENTA ADIVINAR LA PALABRA COMPLETA
        # Si escribió más de una letra, está intentando adivinar toda la palabra
        if len(intento) > 1:
            # Comparamos su intento (sin tildes) con la palabra real (sin tildes)
            if normalizar(intento) == palabra_norm:
                # ¡Adivinó correctamente! Mostramos toda la palabra
                palabra_mostrada = list(palabra_real)
                limpiar_consola()
                mostrar_estado(palabra_mostrada, usadas, intentos, nombre_jugador)
                print(f"🎉 ¡Increíble {nombre_jugador}! ¡Adivinaste la palabra completa!")
                print(f"La palabra era: {palabra_real}")
                return True  # Ganó
            else:
                # Se equivocó, pierde un intento
                print(f"❌ Palabra incorrecta, {nombre_jugador}.")
                intentos -= 1
                if intentos > 0:
                    print(f"Te quedan {intentos} intentos.")
                input("Pulsa Enter para continuar...")
                continue  # Volvemos al inicio del bucle

        # CASO 2: EL JUGADOR INTENTA UNA SOLA LETRA
        # Normalizamos la letra (quitamos tildes y convertimos a mayúscula)
        letra = normalizar(intento)[0]

        # Verificamos que sea realmente una letra (no un número o símbolo)
        if not letra.isalpha():
            print("⚠️ Solo puedes ingresar letras.")
            input("Pulsa Enter para continuar...")
            continue  # Volvemos al inicio del bucle

        # Verificamos si ya había intentado esa letra antes
        if letra in usadas:
            print("ℹ️ Ya intentaste esa letra antes.")
            input("Pulsa Enter para continuar...")
            continue  # Volvemos al inicio del bucle

        # Agregamos la letra a las letras usadas
        usadas.add(letra)

        # VERIFICAMOS SI LA LETRA ESTÁ EN LA PALABRA
        acierto = False  # Variable para saber si acertó
        # Revisamos cada letra de la palabra real
        for i, ch in enumerate(palabra_real):
            # Si la letra de la palabra (sin tildes) es igual a la letra que probó
            if normalizar(ch) == letra:
                palabra_mostrada[i] = ch  # Revelamos esa letra (con tildes originales)
                acierto = True  # Marcamos que acertó

        # Mostramos el resultado del intento
        if acierto:
            print(f"✅ ¡Excelente {nombre_jugador}! La letra '{intento.upper()}' está en la palabra.")
        else:
            print(f"❌ Lo siento {nombre_jugador}, la letra '{intento.upper()}' no está en la palabra.")
            intentos -= 1  # Pierde un intento
            if intentos > 0:
                print(f"Te quedan {intentos} intentos.")

        input("Pulsa Enter para continuar...")

    # SI LLEGAMOS AQUÍ, EL JUGADOR SE QUEDÓ SIN INTENTOS
    limpiar_consola()
    print(HANGMANPICS[0])  # Mostramos el ahorcado completo
    print(f"💀 Lo siento {nombre_jugador}, te quedaste sin intentos.")
    print(f"La palabra era: {palabra_real}")
    return False  # Devolvemos False porque perdió

def mostrar_estadisticas(partidas_ganadas, partidas_totales, nombre_jugador):
    """
    Esta función muestra las estadísticas del jugador:
    - Cuántas partidas ha jugado en total
    - Cuántas ha ganado
    - Su porcentaje de victorias
    """
    # Solo mostramos estadísticas si ha jugado al menos una partida
    if partidas_totales > 0:
        # Calculamos el porcentaje: (ganadas ÷ totales) × 100
        porcentaje = (partidas_ganadas / partidas_totales) * 100
        # Mostramos toda la información
        print(f"\n📊 Estadísticas de {nombre_jugador}:")
        print(f"Partidas jugadas: {partidas_totales}")
        print(f"Partidas ganadas: {partidas_ganadas}")
        print(f"Porcentaje de victorias: {porcentaje:.1f}%")  # .1f significa 1 decimal

def main():
    """
    Esta es la función principal que controla todo el programa:
    - Pide el nombre del jugador
    - Permite jugar múltiples partidas
    - Lleva el conteo de victorias
    - Pregunta si quiere seguir jugando
    """
    # INICIALIZACIÓN
    nombre_jugador = mostrar_bienvenida()  # Pedimos el nombre del jugador
    partidas_ganadas = 0    # Contador de partidas ganadas (empieza en 0)
    partidas_totales = 0    # Contador de partidas totales (empieza en 0)
    
    # BUCLE PRINCIPAL DEL PROGRAMA
    # Este bucle permite jugar múltiples partidas hasta que el jugador decida parar
    while True:
        partidas_totales += 1  # Aumentamos el contador de partidas jugadas
        
        # Jugamos una partida y guardamos si ganó (True) o perdió (False)
        ganó = jugar_una_partida(nombre_jugador)
        
        # Si ganó, aumentamos el contador de victorias
        if ganó:
            partidas_ganadas += 1
        
        # Mostramos las estadísticas después de cada partida
        mostrar_estadisticas(partidas_ganadas, partidas_totales, nombre_jugador)
        
        # PREGUNTAMOS SI QUIERE JUGAR DE NUEVO
        print(f"\n{nombre_jugador}, ¿quieres jugar otra vez?")
        otra = input("Ingresa 'S' para Sí o cualquier otra tecla para No: ").strip().upper()
        
        # Si no escribió 'S', salimos del bucle y terminamos el programa
        if otra != "S":
            print(f"¡Gracias por jugar, {nombre_jugador}! 👋")
            # Mostramos las estadísticas finales
            mostrar_estadisticas(partidas_ganadas, partidas_totales, nombre_jugador)
            break  # Salimos del bucle while

# INICIO DEL PROGRAMA
# Esta línea verifica si estamos ejecutando este archivo directamente
# (no importándolo como módulo en otro programa)
if __name__ == "__main__":
    main()  # Llamamos a la función principal para empezar el juego