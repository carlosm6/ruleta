import random
import time

class JuegoRuleta:
    def __init__(self):
        self.ruleta = list(range(0, 37))  # Lista de números de la ruleta (0-36)
        self.rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25, 27, 30, 32, 34, 36]  # Números rojos
        self.negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 19, 20, 22, 24, 26, 28, 29, 31, 33, 35]  # Números negros
        self.fondo = 1000  # Saldo inicial del jugador

    def apostar(self, numero, cantidad):
        if self.fondo <= 0:  # Verifica si el saldo es cero
            return "Fin del juego", "No tienes más saldo para seguir jugando."

        if cantidad > self.fondo:  # Verifica si la apuesta es mayor que el saldo
            return "Error", "No tienes suficiente saldo para realizar esta apuesta."

        self.fondo -= cantidad  # Resta la apuesta del fondo

        # Simulación de giro
        time.sleep(1)  # Pausa para simular el giro

        aleatorio = random.choice(self.ruleta)  # Selecciona un número aleatorio de la ruleta

        # Evaluación de la apuesta
        if numero == aleatorio:  # Si el número apostado es el mismo que el resultado
            ganancia = cantidad * 36  # Calcula la ganancia
            self.fondo += ganancia  # Aumenta el saldo
            return "Ganaste", f"¡Ganaste en el número {numero}! Ganancia: ${ganancia}"
        else:
            return "Perdiste", f"Perdiste en el número {numero}! Apuesta: ${cantidad}"

    def apostar_color(self, color, cantidad):
        if self.fondo <= 0:  # Verifica si el saldo es cero
            return "Fin del juego", "No tienes más saldo para seguir jugando."

        if cantidad > self.fondo:  # Verifica si la apuesta es mayor que el saldo
            return "Error", "No tienes suficiente saldo para realizar esta apuesta."

        self.fondo -= cantidad  # Resta la apuesta del fondo

        # Simulación de giro
        time.sleep(1)  # Pausa para simular el giro

        aleatorio = random.choice(self.ruleta)  # Selecciona un número aleatorio de la ruleta

        # Evaluación de la apuesta
        if color == "rojo":  # Si se apostó en rojo
            if aleatorio in self.rojos:  # Verifica si el número aleatorio está en los números rojos
                ganancia = cantidad * 2  # Calcula la ganancia
                self.fondo += ganancia  # Aumenta el saldo
                return "Ganaste", f"¡Ganaste en rojo! Ganancia: ${ganancia}"
            else:
                return "Perdiste", f"Perdiste en rojo! Apuesta: ${cantidad}"
        elif color == "negro":  # Si se apostó en negro
            if aleatorio in self.negros:  # Verifica si el número aleatorio está en los números negros
                ganancia = cantidad * 2  # Calcula la ganancia
                self.fondo += ganancia  # Aumenta el saldo
                return "Ganaste", f"¡Ganaste en negro! Ganancia: ${ganancia}"
            else:
                return "Perdiste", f"Perdiste en negro! Apuesta: ${cantidad}"