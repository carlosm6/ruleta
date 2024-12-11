"""
interfaz_ruleta.py
-------------------

Este módulo implementa una interfaz gráfica para un juego de ruleta utilizando
la biblioteca Tkinter y combinada con la lógica incluida en la clase `JuegoRuleta`.

Clases:
-------
InterfazRuleta:
    Genera y gestiona la interfaz gráfica del juego de ruleta.

Ejemplo de uso:
---------------
from interfaz_ruleta import InterfazRuleta
root = tk.Tk()
app = InterfazRuleta(root)
root.mainloop()
"""

import tkinter as tk
from tkinter import simpledialog
import time
import random
from JuegoRuleta import JuegoRuleta


class InterfazRuleta:
    """
    Clase que implementa la interfaz gráfica del juego de ruleta.

    Atributos:
    ----------
    master : tk.Tk
        Ventana principal de la interfaz gráfica.
    juego : JuegoRuleta
        Instancia del juego de ruleta que gestiona la lógica.
    fichas : list[tk.Button]
        Lista de botones utilizados para cada número en el tablero de ruleta.
    apuestas : list[tuple]
        Lista de apuestas realizadas por el jugador.
    balance_label : tk.Label
        Etiqueta que muestra el saldo actual del jugador.
    result_label : tk.Label
        Etiqueta que muestra mensajes del resultado de juego.
    tablero_frame : tk.Frame
        Contenedor del tablero de la ruleta.
    apuestas_label : tk.Label
        Etiqueta que muestra las apuestas realizadas por el jugador.

    Métodos:
    --------
    __init__(master):
        Inicializa la interfaz gráfica del juego.
    apostar(numero):
        Permite realizar una apuesta en un número específico.
    apostar_color(color):
        Permite realizar una apuesta en un color específico.
    girar_ruleta():
        Simula el giro de la ruleta y evalúa los resultados.
    """

    def __init__(self, master):
        """
        Inicializa la ventana principal de la interfaz gráfica.

        Parámetros:
        -----------
        master : tk.Tk
            Ventana principal donde se renderiza la interfaz.
        """
        self.master = master
        self.master.title("Juego de Ruleta")
        self.master.geometry("1000x1000")
        self.master.configure(bg="#222831")

        # Configuración del juego
        self.juego = JuegoRuleta()
        self.fichas = []
        self.apuestas = []

        # Frame principal para saldo y resultados
        main_frame = tk.Frame(master, bg="#222831")
        main_frame.pack(pady=20)

        # Etiqueta del saldo del jugador
        self.balance_label = tk.Label(main_frame, text=f"Saldo: €{self.juego.fondo}",
                                      font=("Helvetica", 14), bg="#222831", fg="white")
        self.balance_label.grid(row=20, column=0, pady=(0, 15))

        # Etiqueta del resultado del juego
        self.result_label = tk.Label(main_frame, text="", font=("Helvetica", 14),
                                     bg="#222831", fg="white")
        self.result_label.grid(row=0, column=0, pady=(0, 15))

        # Frame del tablero de la ruleta
        self.tablero_frame = tk.Frame(master, bg="#222831")
        self.tablero_frame.pack(pady=20)

        # Etiqueta del tablero
        self.tablero_label = tk.Label(self.tablero_frame, text="Tablero de Apuestas",
                                      font=("Helvetica", 14), bg="#222831", fg="white")
        self.tablero_label.grid(row=0, column=0, columnspan=12)

        # Metodo para crear tablero
        self._crear_tablero()

        # Botones para apostar
        self._crear_botones_apuesta()

        # Frame separado para apuestas realizadas (ahora el botón "36" no se tapa)
        self.apuestas_frame = tk.Frame(master, bg="#393e46")
        self.apuestas_frame.pack(fill=tk.BOTH, padx=20, pady=(10, 0))

        # Etiqueta donde se mostrarán todas las apuestas realizadas
        self.apuestas_label = tk.Label(self.tablero_frame, text="Apuestas realizadas:\n",
                                       font=("Helvetica", 12), bg="#222831", fg="white",
                                       anchor="w", justify="left")
        self.apuestas_label.grid(row=5, column=0, columnspan=12, pady=(10, 0), sticky="w")

    def _crear_tablero(self):
        """
        Crea el tablero de números de la ruleta con botones interactivos.
        """
        num_columnas = 12

        for i in range(37):
            color = "#00adb5"  # Color por defecto
            if i == 0:
                color = "green"  # Verde para el número 0
            elif i in self.juego.rojos:
                color = "red"  # Números rojos
            elif i in self.juego.negros:
                color = "black"  # Números negros

            def crear_comando(numero):
                return lambda: self.apostar(numero)

            # Botón del número
            ficha = tk.Button(self.tablero_frame, text=str(i), command=crear_comando(i), bg=color,
                              fg="#ffffff", width=5, height=2)
            fila = i // num_columnas + 1
            columna = i % num_columnas
            ficha.grid(row=fila, column=columna, padx=5, pady=5, sticky="nsew")
            self.fichas.append(ficha)

    def _crear_botones_apuesta(self):
        """
        Crea los botones para apostar en colores y para girar la ruleta.
        """
        botones_frame = tk.Frame(self.master, bg="#222831")
        botones_frame.pack(pady=20)

        # Botón para apostar en los números rojos
        self.boton_rojo = tk.Button(botones_frame, text="Apostar en Rojo",
                                    command=lambda: self.apostar_color("rojo"),
                                    bg="#ff4d4d", fg="#ffffff", width=15, height=2)
        self.boton_rojo.grid(row=0, column=0, padx=5, pady=5)

        # Botón para apostar en los números negros
        self.boton_negro = tk.Button(botones_frame, text="Apostar en Negro",
                                     command=lambda: self.apostar_color("negro"),
                                     bg="black", fg="#ffffff", width=15, height=2)
        self.boton_negro.grid(row=0, column=1, padx=5, pady=5)

        # Botón para girar la ruleta
        self.boton_girar = tk.Button(botones_frame, text="Girar Ruleta",
                                     command=self.girar_ruleta, bg="#00adb5",
                                     fg="white", width=15, height=2)
        self.boton_girar.grid(row=0, column=2, padx=5, pady=5)

        # Botón para salir del juego
        self.boton_salir = tk.Button(self.master, text="Salir", command=self.master.quit,
                                     font=("Helvetica", 14), bg="red", fg="#eeeeee",
                                     activebackground="#d94141", width=15, height=2)
        self.boton_salir.pack(pady=10)

    def apostar(self, numero):
        """
        Permite al jugador apostar en un número específico.

        Parámetros:
        -----------
        numero : int
            Número seleccionado para la apuesta.
        """
        if self.juego.fondo <= 0:
            self.result_label.config(text="No tienes más saldo para seguir jugando.")
            return

        cantidad = simpledialog.askinteger("Apuesta", f"Elige tu apuesta para el número {numero}: €",
                                           minvalue=1, maxvalue=self.juego.fondo)
        if cantidad is None:
            return

        self.juego.fondo -= cantidad
        self.apuestas.append((numero, cantidad))
        self.balance_label.config(text=f"Saldo: €{self.juego.fondo}")

        apuestas_text = "\n".join([f"Número: {apuesta[0]}, Cantidad: €{apuesta[1]}" for apuesta in self.apuestas])
        self.apuestas_label.config(text=f"Apuestas realizadas:\n{apuestas_text}")

    def apostar_color(self, color):
        """
        Permite al jugador apostar en un color (rojo o negro).

        Parámetros:
        -----------
        color : str
            Color seleccionado para la apuesta ("rojo" o "negro").
        """
        if self.juego.fondo <= 0:
            self.result_label.config(text="No tienes más saldo para seguir jugando.")
            return

        cantidad = simpledialog.askinteger("Apuesta", f"Elige tu apuesta para el color {color}: €",
                                           minvalue=1, maxvalue=self.juego.fondo)
        if cantidad is None:
            return

        self.juego.fondo -= cantidad
        self.apuestas.append((color, cantidad))
        self.balance_label.config(text=f"Saldo: €{self.juego.fondo}")

        apuestas_text = "\n".join([f"Número: {apuesta[0]}, Cantidad: €{apuesta[1]}" if isinstance(apuesta[0], int)
                                   else f"Color: {apuesta[0]}, Cantidad: €{apuesta[1]}" for apuesta in self.apuestas])
        self.apuestas_label.config(text=f"Apuestas realizadas:\n{apuestas_text}")

    def girar_ruleta(self):
        """
        Simula el giro de la ruleta y evalúa las apuestas realizadas.
        """
        if not self.apuestas:
            self.result_label.config(text="Debes realizar al menos una apuesta antes de girar la ruleta.")
            return

        self.result_label.config(text="La ruleta está girando... 3")
        self.master.update()
        time.sleep(1)

        self.result_label.config(text="La ruleta está girando... 2")
        self.master.update()
        time.sleep(1)

        self.result_label.config(text="La ruleta está girando... 1")
        self.master.update()
        time.sleep(1)

        aleatorio = random.choice(self.juego.ruleta)
        resultado_mensaje = f"La ruleta ha terminado de girar. Número: {aleatorio}\n"

        total_ganancias = 0
        todas_perdidas = True

        for apuesta in self.apuestas:
            if isinstance(apuesta[0], int):
                resultado, mensaje = self.juego.apostar([apuesta])
                if isinstance(resultado, int):
                    total_ganancias += resultado
                    todas_perdidas = False
                resultado_mensaje += mensaje + "\n"
            else:
                color_apostado = apuesta[0]
                if (color_apostado == "rojo" and aleatorio in self.juego.rojos) or \
                        (color_apostado == "negro" and aleatorio in self.juego.negros):
                    ganancia = apuesta[1] * 2
                    total_ganancias += ganancia
                    todas_perdidas = False
                    resultado_mensaje += f"Apostaste en {color_apostado} y ganaste €{ganancia}!\n"
                else:
                    resultado_mensaje += f"Apostaste en {color_apostado} y perdiste.\n"

        self.juego.fondo += total_ganancias

        if not todas_perdidas:
            resultado_mensaje = f"¡Has ganado €{total_ganancias}! Número salido: {aleatorio}"
        else:
            resultado_mensaje = f"Perdiste tus apuestas. Número salido: {aleatorio}"

        self.result_label.config(text=resultado_mensaje)

        self.apuestas.clear()
        self.balance_label.config(text=f"Saldo: €{self.juego.fondo}")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazRuleta(root)
    root.mainloop()
