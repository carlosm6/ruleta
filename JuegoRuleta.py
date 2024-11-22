
import random
import time

class JuegoRuleta:
    def __init__(self):
        self.ruleta = list(range(0, 37))  # Lista de números de la ruleta (0-36)
        self.rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25, 27, 30, 32, 34, 36]  # Números rojos
        self.negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 19, 20, 22, 24, 26, 28, 29, 31, 33, 35]  # Números negros
        self.fondo = 1000  # Saldo inicial del jugador

    def apostar(self, apuestas):
        total_apuesta = sum(cantidad for _, cantidad in apuestas)
        if self.fondo <= 0 or total_apuesta > self.fondo:  # Verifica si el saldo es cero o si la apuesta total es mayor que el saldo
            return "Error", "No tienes suficiente saldo para realizar esta apuesta."

        self.fondo -= total_apuesta  # Resta la apuesta total del fondo

        resultados = []
        for numero, cantidad in apuestas:
            # Simulación de giro
            time.sleep(1)  # Pausa para simular el giro
            aleatorio = random.choice(self.ruleta)  # Selecciona un número aleatorio de la ruleta

            # Evaluación de la apuesta
            if numero == aleatorio:  # Si el número apostado es el mismo que el resultado
                ganancia = cantidad * 36  # Calcula la ganancia
                self.fondo += ganancia  # Aumenta el saldo
                resultados.append(f"¡Ganaste en el número {numero}! Ganancia: ${ganancia}")
            else:
                resultados.append(f"Perdiste en el número {numero}! Apuesta: ${cantidad}")

        return "Resultados", "\n".join(resultados)

    def apostar_color(self, apuestas_color):
        total_apuesta = sum(cantidad for _, cantidad in apuestas_color)
        if self.fondo <= 0 or total_apuesta > self.fondo:  # Verifica si el saldo es cero o si la apuesta total es mayor que el saldo
            return "Error", "No tienes suficiente saldo para realizar esta apuesta."

        self.fondo -= total_apuesta  # Resta la apuesta total del fondo

        resultados = []
        for color, cantidad in apuestas_color:
            # Simulación de giro
            time.sleep(1)  # Pausa para simular el giro
            aleatorio = random.choice(self.ruleta)  # Selecciona un número aleatorio de la ruleta

            # Evaluación de la apuesta
            if color == "rojo" and aleatorio in self.rojos:
                ganancia = cantidad * 2
                self.fondo += ganancia
                resultados.append(f"¡Ganaste en rojo! Ganancia: ${ganancia}")
            elif color == "negro" and aleatorio in self.negros:
                ganancia = cantidad * 2
                self.fondo += ganancia
                resultados.append(f"¡Ganaste en negro! Ganancia: ${ganancia}")
            else:
                resultados.append(f"Perdiste en {color}! Apuesta: ${cantidad}")

        return "Resultados", "\n".join(resultados)