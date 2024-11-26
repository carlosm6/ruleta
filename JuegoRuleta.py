
import random
import time

import random

class JuegoRuleta:
    def __init__(self):
        self.fondo = 1000  # Saldo inicial del jugador
        self.ruleta = list(range(37))  # Números de la ruleta (0-36)
        self.rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]  # Números rojos
        self.negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]  # Números negros

    def apostar(self, apuesta):
        numero_apostado, cantidad_apostada = apuesta[0]
        aleatorio = random.choice(self.ruleta)  # Selecciona un número aleatorio de la ruleta
        ganancia = 0
        
        if numero_apostado == aleatorio:  # Si la apuesta coincide con el número ganador
            ganancia = cantidad_apostada * 35  # Por ejemplo, paga 35 veces la apuesta
        mensaje = f"Apostaste en {numero_apostado} y {'ganaste' if ganancia > 0 else 'perdiste'} ${ganancia}!"
        return ganancia, mensaje  # Devuelve la ganancia y el mensaje

    def apostar_color(self, color, cantidad_apostada):
        aleatorio = random.choice(self.ruleta)  # Selecciona un número aleatorio de la ruleta
        ganancia = 0
        
        if (color == "rojo" and aleatorio in self.rojos) or (color == "negro" and aleatorio in self.negros):
            ganancia = cantidad_apostada * 2  # Duplicas la apuesta
            mensaje = f"Apostaste en {color} y ganaste ${ganancia}!"
        else:
            mensaje = f"Apostaste en {color} y perdiste ${cantidad_apostada}."
        
        return ganancia, mensaje  # Devuelve la ganancia y el mensaje