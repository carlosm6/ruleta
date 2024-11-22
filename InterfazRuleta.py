import tkinter as tk  # Importa la biblioteca tkinter para crear la interfaz gráfica
from tkinter import messagebox, simpledialog  # Importa cuadros de diálogo y mensajes
from JuegoRuleta import JuegoRuleta  # Importa la clase JuegoRuleta desde el archivo juego_ruleta.py
import random
import time

class InterfazRuleta:
    def __init__(self, master):
        self.master = master
        self.master.title("Juego de Ruleta")
        self.master.geometry("900x600")
        self.master.configure(bg="#222831")

        self.juego = JuegoRuleta()  # Inicializa la lógica del juego

        # Frame principal
        main_frame = tk.Frame(master, bg="#222831")
        main_frame.pack(pady=20)

        # Saldo
        self.balance_label = tk.Label(main_frame, text=f"Saldo: ${self.juego.fondo}", font=("Helvetica", 14), bg="#222831", fg="#eeeeee")
        self.balance_label.grid(row=0, column=0, pady=(0, 15))

        # Tablero de apuestas
        self.tablero_frame = tk.Frame(master, bg="#222831")
        self.tablero_frame.pack(pady=20)

        self.tablero_label = tk.Label(self.tablero_frame, text="Tablero de Apuestas", font=("Helvetica", 14), bg="#222831", fg="#00adb5")
        self.tablero_label.grid(row=0, column=0, columnspan=3)

        self.fichas = []
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

            ficha = tk.Button(self.tablero_frame, text=str(i), command=crear_comando(i), bg=color, fg="#ffffff", width=5, height=2)
            ficha.grid(row=(i // 12) + 1, column=i % 12, padx=5, pady=5)
            self.fichas.append(ficha)

        # Botones para apostar en rojo y negro
        self.boton_rojo = tk.Button(self.tablero_frame, text="Apostar en Rojo", command=lambda: self.apostar_color("rojo"), bg="#ff4d4d", fg="#ffffff", width=15, height=2)
        self.boton_rojo.grid(row=4, column=0, padx=5, pady=5)

        self.boton_negro = tk.Button(self.tablero_frame, text="Apostar en Negro", command=lambda: self.apostar_color("negro"), bg="#4d4dff", fg="#ffffff", width=15, height=2)
        self.boton_negro.grid(row=4, column=1, padx=5, pady=5)

        # Botón para girar la ruleta
        self.boton_girar = tk.Button(self.tablero_frame, text="Girar Ruleta", command=self.girar_ruleta, bg="#00adb5", fg="#ffffff", width=15, height=2)
        self.boton_girar.grid(row=4, column=2, padx=5, pady=5)

        # Botón de salida
        self.boton_salir = tk.Button(main_frame, text="Salir", command=self.master.quit, font=("Helvetica", 14), bg="#f05454", fg="#eeeeee", activebackground="#d94141", width=15, height=2)
        self.boton_salir.grid(row=3, column=0, pady=10)

    def apostar(self, numero):
        if self.juego.fondo <= 0:  # Verifica si el saldo es cero
            messagebox.showinfo("Fin del juego", "No tienes más saldo para seguir jugando.")  # Muestra un mensaje
            return

        cantidad = simpledialog.askinteger("Apuesta", f"Elige tu apuesta para el número {numero}: $", minvalue=1, maxvalue=self.juego.fondo)  # Solicita la cantidad a apostar
        if cantidad is None:  # Si el usuario cancela
            return

        resultado, mensaje = self.juego.apostar(numero, cantidad)  # Realiza la apuesta
        messagebox.showinfo(resultado, mensaje)  # Muestra el resultado de la apuesta
        self.balance_label.config(text=f"Saldo: ${self.juego.fondo}")  # Actualiza la etiqueta del saldo

        # Fin del juego si saldo es cero
        if self.juego.fondo <= 0:  # Si el saldo es cero
            messagebox.showinfo("Fin del juego", "No tienes más saldo para seguir jugando.")  # Muestra un mensaje de fin de juego

    def apostar_color(self, color):
        if self.juego.fondo <= 0:  # Verifica si el saldo es cero
            messagebox.showinfo("Fin del juego", "No tienes más saldo para seguir jugando.")  # Muestra un mensaje
            return

        cantidad = simpledialog.askinteger("Apuesta", f"Elige tu apuesta para el color {color}: $", minvalue=1, maxvalue=self.juego.fondo)  # Solicita la cantidad a apostar
        if cantidad is None:  # Si el usuario cancela
            return

        resultado, mensaje = self.juego.apostar_color(color, cantidad)  # Realiza la apuesta
        messagebox.showinfo(resultado, mensaje)  # Muestra el resultado de la apuesta
        self.balance_label.config(text=f"Saldo: ${self.juego.fondo}")  # Actualiza la etiqueta del saldo

        # Fin del juego si saldo es cero
        if self.juego.fondo <= 0:  # Si el saldo es cero
            messagebox.showinfo("Fin del juego", "No tienes más saldo para seguir jugando.")  # Muestra un mensaje de fin de juego

    def girar_ruleta(self):
        messagebox.showinfo("Girar Ruleta", "La ruleta está girando...")  # Mensaje de giro
        time.sleep(1)  # Simula el tiempo de giro
        aleatorio = random.choice(self.juego.ruleta)  # Selecciona un número aleatorio de la ruleta
        messagebox.showinfo("Resultado", f"La ruleta ha terminado de girar. Número: {aleatorio}")  # Mensaje de finalización del giro

if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal
    app = InterfazRuleta(root)  # Inicializa la interfaz del juego
    root.mainloop()  # Inicia el bucle principal de la interfaz