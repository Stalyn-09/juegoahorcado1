# -*- coding: utf-8 -*-
"""
Juego del Ahorcado - Con Menú Principal
Versión completa con menú, instrucciones y estadísticas

COMO FUNCIONA EL JUEGO:
1. La computadora elige una palabra secreta al azar
2. El jugador ve espacios vacíos (_ _ _) representando cada letra
3. El jugador adivina letra por letra
4. Si la letra está en la palabra, se revela en su posición
5. Si no está, se pierde un intento y se dibuja parte del ahorcado
6. El jugador gana si completa la palabra antes de 6 intentos fallidos
7. El jugador pierde si se completa el dibujo del ahorcado (6 fallos)
"""

# Importamos las librerías que necesitamos:
import random  # Para elegir palabras al azar de nuestra lista
import os      # Para limpiar la pantalla de la consola

# ---- Lista de palabras para el juego ----
PALABRAS = [
    "programacion", "python", "desarrollo", "computadora", "variable",
    "universidad", "ahorcado", "tecnologia", "algoritmo", "internet",
    "ecuador", "servidor", "cliente", "archivo", "funcion", "memoria"
]

# Dibujos del ahorcado por intentos restantes
HANGMAN_PICS = [
    # 0 intentos restantes - Perdiste
    """
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
    """,
    # 1 intento restante
    """
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    # 2 intentos restantes
    """
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    # 3 intentos restantes
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    # 4 intentos restantes
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    # 5 intentos restantes
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    # 6 intentos restantes - Inicio
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """
]

# Variables globales para estadísticas
estadisticas = {
    'partidas_jugadas': 0,
    'partidas_ganadas': 0,
    'partidas_perdidas': 0
}

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu_principal():
    """Muestra el menú principal del juego"""
    limpiar_pantalla()
    print("JUEGO DEL AHORCADO")
    print("==================")
    print()
    print("1. Jugar")
    print("2. Como jugar")
    print("3. Estadisticas")
    print("4. Salir")
    print()

def obtener_opcion_menu():
    """Obtiene la opción seleccionada por el usuario"""
    while True:
        try:
            opcion = int(input("Selecciona una opcion (1-4): "))
            if opcion in [1, 2, 3, 4]:
                return opcion
            else:
                print("Por favor selecciona una opcion valida (1-4)")
        except ValueError:
            print("Por favor ingresa un numero valido")

def mostrar_instrucciones():
    """Muestra las instrucciones del juego"""
    limpiar_pantalla()
    print("COMO JUGAR")
    print("==========")
    print()
    print("1. La computadora elegira una palabra secreta al azar")
    print("2. Veras espacios vacios (_ _ _) representando cada letra")
    print("3. Debes adivinar letra por letra")
    print("4. Si la letra esta en la palabra, se revelara en su posicion")
    print("5. Si no esta, perderas un intento y se dibujara parte del ahorcado")
    print("6. Ganas si completas la palabra antes de 6 intentos fallidos")
    print("7. Pierdes si se completa el dibujo del ahorcado (6 fallos)")
    print()
    print("CONSEJOS:")
    print("- Comienza con vocales (A, E, I, O, U)")
    print("- Luego prueba consonantes comunes (R, S, T, L, N)")
    print("- Piensa en el contexto de las palabras")
    print()
    input("Presiona Enter para volver al menu principal...")

def mostrar_estadisticas():
    """Muestra las estadísticas del jugador"""
    limpiar_pantalla()
    print("ESTADISTICAS")
    print("============")
    print()
    print(f"Partidas jugadas: {estadisticas['partidas_jugadas']}")
    print(f"Partidas ganadas: {estadisticas['partidas_ganadas']}")
    print(f"Partidas perdidas: {estadisticas['partidas_perdidas']}")
    
    if estadisticas['partidas_jugadas'] > 0:
        porcentaje_victoria = (estadisticas['partidas_ganadas'] / estadisticas['partidas_jugadas']) * 100
        print(f"Porcentaje de victoria: {porcentaje_victoria:.1f}%")
    else:
        print("Porcentaje de victoria: 0.0%")
    
    print()
    input("Presiona Enter para volver al menu principal...")

def generar_palabra_secreta():
    """Genera una palabra secreta aleatoria de la lista"""
    return random.choice(PALABRAS).upper()

def mostrar_espacios_vacios(palabra_secreta, letras_adivinadas):
    """Muestra los espacios vacíos con las letras adivinadas"""
    espacios = ""
    for letra in palabra_secreta:
        if letra in letras_adivinadas:
            espacios += letra + " "
        else:
            espacios += "_ "
    return espacios.strip()

def mostrar_estado_juego(palabra_secreta, letras_adivinadas, intentos_restantes, letras_incorrectas):
    """Muestra el estado actual del juego"""
    limpiar_pantalla()
    print("JUEGO DEL AHORCADO")
    print("==================")
    
    # Mostrar el dibujo del ahorcado
    print(HANGMAN_PICS[intentos_restantes])
    
    # Mostrar los espacios con letras adivinadas
    espacios = mostrar_espacios_vacios(palabra_secreta, letras_adivinadas)
    print(f"Palabra: {espacios}")
    print(f"Letras incorrectas: {', '.join(sorted(letras_incorrectas)) if letras_incorrectas else 'Ninguna'}")
    print(f"Intentos restantes: {intentos_restantes}")
    print("==================")

def jugador_teclea_letra():
    """Pide al jugador que teclee una letra"""
    while True:
        letra = input("Ingresa una letra: ").strip().upper()
        
        if len(letra) != 1:
            print("Por favor ingresa solo una letra.")
            continue
            
        if not letra.isalpha():
            print("Por favor ingresa solo letras.")
            continue
            
        return letra

def letra_correcta(letra, palabra_secreta):
    """Verifica si la letra está en la palabra secreta"""
    return letra in palabra_secreta

def jugador_completa_palabra(palabra_secreta, letras_adivinadas):
    """Verifica si el jugador ha completado la palabra"""
    for letra in palabra_secreta:
        if letra not in letras_adivinadas:
            return False
    return True

def jugador_sin_intentos(intentos_restantes):
    """Verifica si el jugador se quedó sin intentos"""
    return intentos_restantes <= 0

def preguntar_otro_intento():
    """Pregunta al jugador si quiere hacer otro intento (jugar de nuevo)"""
    while True:
        respuesta = input("Quieres jugar otra vez? (S/N): ").strip().upper()
        if respuesta in ['S', 'SI', 'Y', 'YES']:
            return True
        elif respuesta in ['N', 'NO']:
            return False
        else:
            print("Por favor responde S para Si o N para No.")

def jugar_partida():
    """Ejecuta una partida completa del juego y retorna True si ganó, False si perdió"""
    # Generar una palabra secreta
    palabra_secreta = generar_palabra_secreta()
    letras_adivinadas = set()
    letras_incorrectas = set()
    intentos_restantes = 6
    
    print(f"\nNueva palabra generada (tiene {len(palabra_secreta)} letras)")
    input("Presiona Enter para comenzar...")
    
    # Bucle principal del juego
    while True:
        # Mostrar los espacios vacíos
        mostrar_estado_juego(palabra_secreta, letras_adivinadas, intentos_restantes, letras_incorrectas)
        
        # El jugador teclea la letra
        letra = jugador_teclea_letra()
        
        # Verificar si ya se usó esta letra
        if letra in letras_adivinadas or letra in letras_incorrectas:
            print(f"Ya intentaste la letra '{letra}'. Intenta con otra.")
            input("Presiona Enter para continuar...")
            continue
        
        # ¿Letra correcta?
        if letra_correcta(letra, palabra_secreta):
            print(f"Correcto! La letra '{letra}' esta en la palabra.")
            letras_adivinadas.add(letra)
            
            # Verificar si el jugador completó la palabra
            if jugador_completa_palabra(palabra_secreta, letras_adivinadas):
                mostrar_estado_juego(palabra_secreta, letras_adivinadas, intentos_restantes, letras_incorrectas)
                print(f"FELICIDADES! Ganaste!")
                print(f"La palabra era: {palabra_secreta}")
                input("Presiona Enter para continuar...")
                return True  # Victoria
                
        else:
            # Letra incorrecta
            print(f"Incorrecto. La letra '{letra}' no esta en la palabra.")
            letras_incorrectas.add(letra)
            intentos_restantes -= 1
            
            # Verificar si el jugador se quedó sin intentos
            if jugador_sin_intentos(intentos_restantes):
                mostrar_estado_juego(palabra_secreta, letras_adivinadas, intentos_restantes, letras_incorrectas)
                print(f"Perdiste! Te quedaste sin intentos.")
                print(f"La palabra era: {palabra_secreta}")
                input("Presiona Enter para continuar...")
                return False  # Derrota
        
        input("Presiona Enter para continuar...")

def ejecutar_juego():
    """Ejecuta el modo de juego con múltiples partidas"""
    while True:
        # Jugar una partida
        resultado = jugar_partida()
        
        # Actualizar estadísticas
        estadisticas['partidas_jugadas'] += 1
        if resultado:
            estadisticas['partidas_ganadas'] += 1
        else:
            estadisticas['partidas_perdidas'] += 1
        
        # Preguntar si quiere jugar otra vez
        if not preguntar_otro_intento():
            break

def main():
    """Función principal que maneja el menú"""
    print("Bienvenido al Juego del Ahorcado!")
    input("Presiona Enter para continuar...")
    
    while True:
        mostrar_menu_principal()
        opcion = obtener_opcion_menu()
        
        if opcion == 1:  # Jugar
            ejecutar_juego()
        elif opcion == 2:  # Como jugar
            mostrar_instrucciones()
        elif opcion == 3:  # Estadísticas
            mostrar_estadisticas()
        elif opcion == 4:  # Salir
            limpiar_pantalla()
            print("Gracias por jugar!")
            break

# Ejecutar el programa
if __name__ == "__main__":
    main()