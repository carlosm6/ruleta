import tkinter as tk
from tkinter import simpledialog
import time
import random
from JuegoRuleta import JuegoRuleta

class InterfazRuleta:
    def __init__(self, master):
        self.master = master
        self.master.title("Juego de Ruleta")
        self.master.geometry("1000x1000")
        self.master.configure(bg="#222831")

        self.juego = JuegoRuleta()  # Inicializa la lógica del juego

        self.fichas = []
        self.apuestas = [] 
        # Frame principal
        main_frame = tk.Frame(master, bg="#222831")
        main_frame.pack(pady=20)

        # Saldo
        self.balance_label = tk.Label(main_frame, text=f"Saldo: €{self.juego.fondo}", font=("Helvetica", 14), bg="#222831", fg="white")
        self.balance_label.grid(row=20, column=0, pady=(0, 15))

        # Mensaje para mostrar resultados
        self.result_label = tk.Label(main_frame, text="", font=("Helvetica", 14), bg="#222831", fg="white")
        self.result_label.grid(row=0, column=0, pady=(0, 15))

        # Tablero de apuestas
        self.tablero_frame = tk.Frame(master, bg="#222831")
        self.tablero_frame.pack(pady=20)

        self.tablero_label = tk.Label(self.tablero_frame, text="Tablero de Apuestas", font=("Helvetica", 14), bg="#222831", fg="white")
        self.tablero_label.grid(row=0, column=0, columnspan=12)

        num_columnas = 12
        

        for i in range(37):
            color = "#00adb5"
            if i == 0:
                color = "green"
            elif i in self.juego.rojos:
                color = "red"
            elif i in self.juego.negros:
                color = "black"

            def crear_comando(numero):
                return lambda: self.apostar(numero)

            ficha = tk.Button(self.tablero_frame, text=str(i), command=crear_comando(i), bg=color, 
                fg="#ffffff", width=5, height=2)
            fila = i // num_columnas + 1  # +1 para dejar espacio para el label
            columna = i % num_columnas
            ficha.grid(row=fila, column=columna, padx=5, pady=5, sticky="nsew")
            self.fichas.append(ficha)
        
       # Frame para los botones de color y girar ruleta
        botones_frame = tk.Frame(master, bg="#222831")
        botones_frame.pack(pady=20)  # Puedes ajustar el padding según sea necesario

        # Botones para apostar en rojo y negro
        self.boton_rojo = tk.Button(botones_frame, text="Apostar en Rojo", 
            command=lambda: self.apostar_color("rojo"), bg="#ff4d4d", fg="#ffffff", width=15, height=2)
        self.boton_rojo.grid(row=0, column=0, padx=5, pady=5)

        self.boton_negro = tk.Button(botones_frame, text="Apostar en Negro", 
            command=lambda: self.apostar_color("negro"), bg="black", fg="#ffffff", width=15, height=2)
        self.boton_negro.grid(row=0, column=1, padx=5, pady=5)

        self.boton_girar = tk.Button(botones_frame, text="Girar Ruleta", 
            command=self.girar_ruleta, bg="#00adb5", fg="white", width=15, height=2)
        self.boton_girar.grid(row=0, column=2, padx=5, pady=5)

        # Botón de salida
        self.boton_salir = tk.Button(master, text="Salir", command=self.master.quit, 
            font=("Helvetica", 14), bg="red", fg="#eeeeee", activebackground="#d94141", width=15, height=2)
        self.boton_salir.pack(pady=10) 

        self.apuestas_label = tk.Label(self.tablero_frame, text="Apuestas realizadas:\n", 
            font=("Helvetica", 12), bg="#222831", fg="white", anchor="w", justify="left")
        self.apuestas_label.grid(row=fila + 1, column=0, columnspan=12, pady=(10, 0), sticky="w")  # Coloca el label debajo de los botones

    def apostar(self, numero):
        if self.juego.fondo <= 0:  # Verifica si el saldo es cero
            self.result_label.config(text="No tienes más saldo para seguir jugando.")  # Actualiza el mensaje en la interfaz
            return

        cantidad = simpledialog.askinteger("Apuesta", f"Elige tu apuesta para el número {numero}: €", minvalue=1, maxvalue=self.juego.fondo)  # Solicita la cantidad a apostar
        if cantidad is None:  # Si el usuario cancela
            return

        self.juego.fondo -= cantidad  # Resta la cantidad apostada del saldo
        self.apuestas.append((numero, cantidad))  # Agrega la apuesta a la lista
        self.balance_label.config(text=f"Saldo: €{self.juego.fondo}")  # Actualiza la etiqueta del saldo

        apuestas_text = "\n".join([f"Número: {apuesta[0]}, Cantidad: €{apuesta[1]}" for apuesta in self.apuestas])
        self.apuestas_label.config(text=f"Apuestas realizadas:\n{apuestas_text}")
    def apostar_color(self, color):
        if self.juego.fondo <= 0:  # Verifica si el saldo es cero
            self.result_label.config(text="No tienes más saldo para seguir jugando.")  # Actualiza el mensaje en la interfaz
            return

        cantidad = simpledialog.askinteger("Apuesta", f"Elige tu apuesta para el color {color}: €", minvalue=1, maxvalue=self.juego.fondo)  # Solicita la cantidad a apostar
        if cantidad is None:  # Si el usuario cancela
            return

        self.juego.fondo -= cantidad  # Resta la cantidad apostada del saldo
        self.apuestas.append((color, cantidad))  # Agrega la apuesta a la lista
        self.balance_label.config(text=f"Saldo: €{self.juego.fondo}")  # Actualiza la etiqueta del saldo
         # Actualiza la etiqueta de apuestas realizadas
        apuestas_text = "\n".join([f"Número: {apuesta[0]}, Cantidad: €{apuesta[1]}" 
            if isinstance(apuesta[0], int) 
            else f"Color: {apuesta[0]}, Cantidad: €{apuesta[1]}" for apuesta in self.apuestas])
        self.apuestas_label.config(text=f"Apuestas realizadas:\n{apuestas_text}")
    def girar_ruleta(self):
        if not self.apuestas:  # Verifica si hay apuestas
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

        aleatorio = random.choice(self.juego.ruleta)  # Selecciona un número aleatorio de la ruleta
        resultado_mensaje = f"La ruleta ha terminado de girar. Número: {aleatorio}\n"

        total_ganancias = 0  # Inicializa las ganancias totales
        todas_perdidas = True  # Variable para verificar si todas las apuestas fueron pérdidas

        # Procesar las apuestas
        for apuesta in self.apuestas:
            if isinstance(apuesta[0], int):  # Si es una apuesta a un número
                resultado, mensaje = self.juego.apostar([apuesta])  # Realiza la apuesta
                if isinstance(resultado, int):  # Asegúrate de que resultado es un entero
                    total_ganancias += resultado  # Suma las ganancias
                    todas_perdidas = False  # Al menos una apuesta fue ganadora
                resultado_mensaje += mensaje + "\n"
            else:  # Si es una apuesta a un color
                color_apostado = apuesta[0]
                if (color_apostado == "rojo" and aleatorio in self.juego.rojos) or \
                   (color_apostado == "negro" and aleatorio in self.juego.negros):
                    ganancia = apuesta[1] * 2  # Por ejemplo, duplicas la apuesta
                    total_ganancias += ganancia
                    todas_perdidas = False  # Al menos una apuesta fue ganadora
                    resultado_mensaje += f"Apostaste en {color_apostado} y ganaste €{ganancia}!\n"
                else:
                    resultado_mensaje += f"Apostaste en {color_apostado} y perdiste.\n"

        self.juego.fondo += total_ganancias  # Actualiza el fondo con las ganancias totales

        # Muestra el resultado final en la interfaz
        if not todas_perdidas:
            resultado_mensaje = f"¡Has ganado €{total_ganancias}! Número salido: {aleatorio}"  # Mensaje de ganancia
        else:
            resultado_mensaje = f"Perdiste tus apuestas. Número salido: {aleatorio}"  # Mensaje de pérdida

        self.result_label.config(text=resultado_mensaje)  # Actualiza el mensaje final en la interfaz

        self.apuestas.clear()  # Limpia las apuestas después de girar la ruleta
        self.balance_label.config(text=f"Saldo: €{self.juego.fondo}")  # Actualiza la etiqueta del saldo

if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal
    app = InterfazRuleta(root)  # Inicializa la interfaz del juego
    root.mainloop()  # Inicia el bucle principal de la