# -*- coding: utf-8 -*-
"""
Juego del Ahorcado - Siguiendo el Diagrama de Flujo
Versión simplificada que sigue exactamente el flujo del diagrama

CÓMO FUNCIONA EL JUEGO:
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
# Esta es nuestra "base de datos" de palabras posibles
# El juego elegirá una al azar de esta lista
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

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

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
    print("🎮 JUEGO DEL AHORCADO 🎮")
    print("=" * 30)
    
    # Mostrar el dibujo del ahorcado
    print(HANGMAN_PICS[intentos_restantes])
    
    # Mostrar los espacios con letras adivinadas
    espacios = mostrar_espacios_vacios(palabra_secreta, letras_adivinadas)
    print(f"Palabra: {espacios}")
    print(f"Letras incorrectas: {', '.join(sorted(letras_incorrectas)) if letras_incorrectas else 'Ninguna'}")
    print(f"Intentos restantes: {intentos_restantes}")
    print("=" * 30)

def jugador_teclea_letra():
    """Pide al jugador que teclee una letra"""
    while True:
        letra = input("Ingresa una letra: ").strip().upper()
        
        if len(letra) != 1:
            print("⚠️ Por favor ingresa solo una letra.")
            continue
            
        if not letra.isalpha():
            print("⚠️ Por favor ingresa solo letras.")
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
        respuesta = input("¿Quieres jugar otra vez? (S/N): ").strip().upper()
        if respuesta in ['S', 'SI', 'Y', 'YES']:
            return True
        elif respuesta in ['N', 'NO']:
            return False
        else:
            print("⚠️ Por favor responde S para Sí o N para No.")

def main():
    """Función principal que sigue el diagrama de flujo"""
    print("¡Bienvenido al Juego del Ahorcado!")
    input("Presiona Enter para comenzar...")
    
    while True:  # Bucle principal para múltiples juegos
        
        # 1. INICIO - Generar una palabra secreta
        palabra_secreta = generar_palabra_secreta()
        letras_adivinadas = set()
        letras_incorrectas = set()
        intentos_restantes = 6
        
        print(f"\n🎯 Nueva palabra generada (tiene {len(palabra_secreta)} letras)")
        
        # Bucle principal del juego
        while True:
            
            # 2. Mostrar los espacios vacíos
            mostrar_estado_juego(palabra_secreta, letras_adivinadas, intentos_restantes, letras_incorrectas)
            
            # 3. Indicar al jugador que adivine una letra
            # 4. El jugador teclea la letra
            letra = jugador_teclea_letra()
            
            # Verificar si ya se usó esta letra
            if letra in letras_adivinadas or letra in letras_incorrectas:
                print(f"⚠️ Ya intentaste la letra '{letra}'. Intenta con otra.")
                input("Presiona Enter para continuar...")
                continue
            
            # 5. ¿Letra correcta?
            if letra_correcta(letra, palabra_secreta):
                print(f"✅ ¡Correcto! La letra '{letra}' está en la palabra.")
                letras_adivinadas.add(letra)
                
                # Verificar si el jugador completó la palabra
                if jugador_completa_palabra(palabra_secreta, letras_adivinadas):
                    mostrar_estado_juego(palabra_secreta, letras_adivinadas, intentos_restantes, letras_incorrectas)
                    print(f"🎉 ¡FELICIDADES! ¡Ganaste!")
                    print(f"La palabra era: {palabra_secreta}")
                    break
                    
            else:
                # 6. ¿Letra incorrecta?
                print(f"❌ Incorrecto. La letra '{letra}' no está en la palabra.")
                letras_incorrectas.add(letra)
                intentos_restantes -= 1
                
                # Verificar si el jugador se quedó sin intentos
                if jugador_sin_intentos(intentos_restantes):
                    mostrar_estado_juego(palabra_secreta, letras_adivinadas, intentos_restantes, letras_incorrectas)
                    print(f"💀 ¡Perdiste! Te quedaste sin intentos.")
                    print(f"La palabra era: {palabra_secreta}")
                    break
            
            input("Presiona Enter para continuar...")
        
        # 7. Preguntar al jugador si quiere hacer otro intento
        if not preguntar_otro_intento():
            break
    
    # FIN
    print("¡Gracias por jugar! 👋")

# Ejecutar el programa
if __name__ == "__main__":
    main()