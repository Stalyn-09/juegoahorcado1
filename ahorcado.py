# -*- coding: utf-8 -*-
"""
Juego del Ahorcado (consola)
Autor: tú :)
Descripción:
    - Adivina la palabra letra por letra o completa.
    - Acepta palabras con tildes (se normalizan para comparar).
    - Muestra letras usadas, intentos restantes y dibujo del ahorcado.
"""

import random
import unicodedata
import os

# ---- Dibujo del ahorcado por etapas (0 = ahorcado completo) ----
HANGMANPICS = [
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
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

# ---- Lista de palabras (puedes añadir más) ----
PALABRAS = [
    "programación", "python", "desarrollo", "computadora", "variable",
    "universidad", "ahorcado", "tecnología", "algoritmo", "internet",
    "ecuador", "servidor", "cliente", "archivo", "función", "memoria",
    "depuración", "microservicio", "contenedor", "docker"
]

def limpiar_consola():
    """Limpia la pantalla (Windows/Linux/Mac)."""
    os.system("cls" if os.name == "nt" else "clear")

def normalizar(texto: str) -> str:
    """
    Quita tildes y pasa a mayúsculas para comparar de forma estable.
    Ej: 'programación' -> 'PROGRAMACION'
    """
    nfkd = unicodedata.normalize("NFKD", texto)
    sin_tildes = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sin_tildes.upper()

def elegir_palabra() -> str:
    """Devuelve una palabra al azar de la lista."""
    return random.choice(PALABRAS)

def mostrar_estado(palabra_mostrada, usadas, intentos):
    """Dibuja el tablero y la información de la partida."""
    # El índice del dibujo se calcula desde el final:
    # intentos = 6 -> último dibujo (sin muñeco)
    # intentos = 0 -> ahorcado completo
    indice = max(0, min(len(HANGMANPICS) - 1, len(HANGMANPICS) - 1 - intentos))
    print(HANGMANPICS[indice])
    print(f"Palabra:  {' '.join(palabra_mostrada)}")
    print(f"Usadas:   {', '.join(sorted(usadas)) if usadas else '(ninguna)'}")
    print(f"Intentos: {intentos}\n")

def jugar_una_partida():
    """Lógica principal de una partida."""
    palabra_real = elegir_palabra()              # Puede tener tildes
    palabra_norm = normalizar(palabra_real)      # Sin tildes para comparar
    palabra_mostrada = ["_" if ch.isalpha() else ch for ch in palabra_real]
    usadas = set()
    intentos = 6                                 # Ajusta si quieres más/menos intentos

    while intentos >= 0:
        limpiar_consola()
        mostrar_estado(palabra_mostrada, usadas, intentos)

        # ¿Ya se adivinó todo?
        if normalizar("".join(palabra_mostrada)) == palabra_norm:
            print("🎉 ¡Ganaste! La palabra era:", palabra_real)
            return

        # Pedir intento
        intento = input("Ingresa una letra o arriesga la palabra completa: ").strip()

        if not intento:
            continue  # vacío, vuelve a pedir

        # ----- Intento de palabra completa -----
        if len(intento) > 1:
            if normalizar(intento) == palabra_norm:
                # Revela toda la palabra con sus tildes originales
                palabra_mostrada = list(palabra_real)
                limpiar_consola()
                mostrar_estado(palabra_mostrada, usadas, intentos)
                print("🎉 ¡Ganaste! La palabra era:", palabra_real)
                return
            else:
                print("❌ Palabra incorrecta.")
                intentos -= 1
                input("Pulsa Enter para continuar...")
                continue

        # ----- Intento de una letra -----
        letra = normalizar(intento)[0]

        if not letra.isalpha():
            # No es letra (número, símbolo, etc.)
            print("⚠️ Ingresa solo letras.")
            input("Pulsa Enter para continuar...")
            continue

        if letra in usadas:
            print("ℹ️ Ya intentaste esa letra.")
            input("Pulsa Enter para continuar...")
            continue

        usadas.add(letra)

        # Comprobar si la letra está en la palabra
        acierto = False
        for i, ch in enumerate(palabra_real):
            if normalizar(ch) == letra:
                palabra_mostrada[i] = ch  # conserva tildes originales
                acierto = True

        if acierto:
            print("✅ ¡Bien! La letra está en la palabra.")
        else:
            print("❌ No está.")
            intentos -= 1

        input("Pulsa Enter para continuar...")

    # Si salimos del bucle, se acabaron los intentos
    limpiar_consola()
    print(HANGMANPICS[0])
    print("💀 Te quedaste sin intentos.")
    print("La palabra era:", palabra_real)

def main():
    """Loop principal: permite jugar varias partidas."""
    while True:
        jugar_una_partida()
        otra = input("\n¿Jugar otra vez? (S/N): ").strip().upper()
        if otra != "S":
            print("¡Gracias por jugar! 👋")
            break

if __name__ == "__main__":
    main()
