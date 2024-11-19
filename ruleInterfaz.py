import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from collections import Counter
import time

class JuegoRuleta:
    def __init__(self, master):
        self.master = master
        self.master.title("Juego de Ruleta Profesional")
        self.master.geometry("800x600")  # Aumentar el tamaño para más espacio
        self.master.configure(bg="#222831")

        # Variables de inicialización
        self.ruleta = list(range(0, 37))
        self.rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25, 27, 30, 32, 34, 36]
        self.negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 19, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        self.fondo = 1000
        self.historial_resultados = []

        # Estilo de fuentes
        self.label_font = ("Helvetica", 16, "bold")
        
        # Frame principal
        main_frame = tk.Frame(master, bg="#222831")
        main_frame.pack(pady=20)

        # Saldo
        self.balance_label = tk.Label(main_frame, text=f"Saldo: ${self.fondo}", font=self.label_font, bg="#222831", fg="#eeeeee")
        self.balance_label.grid(row=0, column=0, pady=(0, 15))

        # Números calientes y fríos
        self.calientes_label = tk.Label(main_frame, text="Números Calientes: ", font=("Helvetica", 12), bg="#222831", fg="#00adb5")
        self.calientes_label.grid(row= 1, column=0, pady=(10, 0))
        
        self.numeros_calientes = tk.Label(main_frame, text="", font=("Helvetica", 10), bg="#222831", fg="#eeeeee")
        self.numeros_calientes.grid(row=1, column=1, pady=(10, 0))

        self.fríos_label = tk.Label(main_frame, text="Números Fríos: ", font=("Helvetica", 12), bg="#222831", fg="#00adb5")
        self.fríos_label.grid(row=2, column=0, pady=(10, 0))

        self.numeros_fríos = tk.Label(main_frame, text="", font=("Helvetica", 10), bg="#222831", fg="#eeeeee")
        self.numeros_fríos.grid(row=2, column=1, pady=(10, 0))

        # Tablero de apuestas
        self.tablero_frame = tk.Frame(master, bg="#222831")
        self.tablero_frame.pack(pady=20)

        self.tablero_label = tk.Label(self.tablero_frame, text="Tablero de Apuestas", font=("Helvetica", 14), bg="#222831", fg="#00adb5")
        self.tablero_label.grid(row=0, column=0, columnspan=3)

        self.fichas = []
        for i in range(37):
            color = "#00adb5"  # Default color
            if i == 0:
                color = "green"  # Color for 0
            elif i in self.rojos:
                color = "red"  # Color for red numbers
            elif i in self.negros:
                color = "black"  # Color for black numbers
            
            ficha = tk.Button(self.tablero_frame, text=str(i), command=lambda i=i: self.apostar(i), bg=color, fg="#ffffff", width=5, height=2)
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
        self.boton_salir = tk.Button(main_frame, text="Salir", command=self.master.quit,
                                     font=self.label_font, bg="#f05454", fg="#eeeeee", activebackground="#d94141", width=15, height=2)
        self.boton_salir.grid(row=3, column=0, pady=10)

    def actualizar_numeros_calientes_y_frios(self):
        if len(self.historial_resultados) == 0:
            return

        contador = Counter(self.historial_resultados)
        numeros_calientes = contador.most_common(3)  # Obtener los 3 números más comunes
        numeros_frios = contador.most_common()[:-4:-1]  # Obtener los 3 números menos comunes

        calientes = [str(num[0]) for num in numeros_calientes]
        frios = [str(num[0]) for num in numeros_frios]

        self.numeros_calientes.config(text=", ".join(calientes))
        self.numeros_fríos.config(text=", ".join(frios))

    def apostar(self, numero):
        if self.fondo <= 0:
            messagebox.showinfo("Fin del juego", "No tienes más saldo para seguir jugando.")
            return

        cantidad = simpledialog.askinteger("Apuesta", f"Elige tu apuesta para el número {numero}: $", minvalue=1, maxvalue=self.fondo)
        if cantidad is None:
            return

        if cantidad > self .fondo:
            messagebox.showerror("Error", "No tienes suficiente saldo para realizar esta apuesta.")
            return

        self.fondo -= cantidad  # Restar la apuesta del fondo
        self.balance_label.config(text=f"Saldo: ${self.fondo}")

        # Simulación de giro
        self.resultado_label.config(text="Girando la ruleta...", fg="#ffd369")
        self.master.update()
        time.sleep(1)

        # Animación de cuenta regresiva
        for i in range(3, 0, -1):
            self.resultado_label.config(text=f"Girando... {i}")
            self.master.update()
            time.sleep(0.5)

        aleatorio = random.choice(self.ruleta)
        self.resultado_label.config(text=f"El número que salió es el {aleatorio}", fg="#ffd369")

        # Añadir resultado al historial
        self.historial_resultados.append(aleatorio)

        # Actualizar números calientes y fríos
        self.actualizar_numeros_calientes_y_frios()

        # Evaluación de la apuesta
        if numero == aleatorio:
            ganancia = cantidad * 36
            self.fondo += ganancia
            messagebox.showinfo("Resultado", f"¡Ganaste en el número {numero}! Ganancia: ${ganancia}")
        else:
            messagebox.showinfo("Resultado", f"Perdiste en el número {numero}! Apuesta: ${cantidad}")

        self.balance_label.config(text=f"Saldo: ${self.fondo}")

        # Fin del juego si saldo es cero
        if self.fondo <= 0:
            messagebox.showinfo("Fin del juego", "No tienes más saldo para seguir jugando.")

    def apostar_color(self, color):
        if self.fondo <= 0:
            messagebox.showinfo("Fin del juego", "No tienes más saldo para seguir jugando.")
            return

        cantidad = simpledialog.askinteger("Apuesta", f"Elige tu apuesta para {color}: $", minvalue=1, maxvalue=self.fondo)
        if cantidad is None:
            return

        if cantidad > self.fondo:
            messagebox.showerror("Error", "No tienes suficiente saldo para realizar esta apuesta.")
            return

        self.fondo -= cantidad  # Restar la apuesta del fondo
        self.balance_label.config(text=f"Saldo: ${self.fondo}")

        # Simulación de giro
        self.resultado_label.config(text="Girando la ruleta...", fg="#ffd369")
        self.master.update()
        time.sleep(1)

        # Animación de cuenta regresiva
        for i in range(3, 0, -1):
            self.resultado_label.config(text=f"Girando... {i}")
            self.master.update()
            time.sleep(0.5)

        aleatorio = random.choice(self.ruleta)
        self.resultado_label.config(text=f"El número que salió es el {aleatorio}", fg="#ffd369")

        # Añadir resultado al historial
        self.historial_resultados.append(aleatorio)

        # Actualizar números calientes y fríos
        self.actualizar_numeros_calientes_y_frios()
        # Evaluación de la apuesta
        if color == "rojo":
            if aleatorio in self.rojos:
                ganancia = cantidad * 2
                self.fondo += ganancia
                messagebox.showinfo("Resultado", f"¡Ganaste en rojo! Ganancia: ${ganancia}")
            else:
                messagebox.showinfo("Resultado", f"Perdiste en rojo! Apuesta: ${cantidad}")
        elif color == "negro":
            if aleatorio in self.negros:
                ganancia = cantidad * 2
                self.fondo += ganancia
                messagebox.showinfo("Resultado", f"¡Ganaste en negro! Ganancia: ${ganancia}")
            else:
                messagebox.showinfo("Resultado", f"Perdiste en negro! Apuesta: ${cantidad}")

        self.balance_label.config(text=f"Saldo: ${self.fondo}")

        # Fin del juego si saldo es cero
        if self.fondo <= 0:
            messagebox.showinfo("Fin del juego", "No tienes más saldo para seguir jugando.")

    def girar_ruleta(self):
        # Simulación de giro
        self.resultado_label = tk.Label(self.tablero_frame, text="Girando la ruleta...", font=("Helvetica", 14), bg="#222831", fg="#ffd369")
        self.resultado_label.grid(row=5, column=0, columnspan=3)
        self.master.update()
        time.sleep(1)

        # Animación de cuenta regresiva
        for i in range(3, 0, -1):
            self.resultado_label.config(text =f"Girando... {i}")
            self.master.update()
            time.sleep(0.5)

        aleatorio = random.choice(self.ruleta)
        self.resultado_label.config(text=f"El número que salió es el {aleatorio}", fg="#ffd369")

        # Añadir resultado al historial
        self.historial_resultados.append(aleatorio)

        # Actualizar números calientes y fríos
        self.actualizar_numeros_calientes_y_frios()

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoRuleta(root)
    root.mainloop()