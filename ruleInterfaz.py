import tkinter as tk  # Importa la biblioteca tkinter para crear la interfaz gráfica
from tkinter import messagebox, simpledialog  # Importa cuadros de diálogo y mensajes
import random  # Importa la biblioteca random para generar números aleatorios
from collections import Counter  # Importa Counter para contar elementos en una lista
import time  # Importa time para hacer pausas en la ejecución

class JuegoRuleta:
    def __init__(self, master):
        self.master = master  # Guarda la referencia a la ventana principal
        self.master.title("Juego de Ruleta Profesional")  # Título de la ventana
        self.master.geometry("800x600")  # Tamaño de la ventana
        self.master.configure(bg="#222831")  # Color de fondo de la ventana

        # Variables de inicialización
        self.ruleta = list(range(0, 37))  # Lista de números de la ruleta (0-36)
        self.rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25, 27, 30, 32, 34, 36]  # Números rojos
        self.negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 19, 20, 22, 24, 26, 28, 29, 31, 33, 35]  # Números negros
        self.fondo = 1000  # Saldo inicial del jugador
        self.historial_resultados = []  # Lista para almacenar los resultados de las tiradas

        # Estilo de fuentes
        self.label_font = ("Helvetica", 16, "bold")  # Fuente para las etiquetas

        # Frame principal
        main_frame = tk.Frame(master, bg="#222831")  # Crea un marco principal
        main_frame.pack(pady=20)  # Añade el marco a la ventana

        # Saldo
        self.balance_label = tk.Label(main_frame, text=f"Saldo: ${self.fondo}", font=self.label_font, bg="#222831", fg="#eeeeee")  # Etiqueta para mostrar el saldo
        self.balance_label.grid(row=0, column=0, pady=(0, 15))  # Coloca la etiqueta en la cuadrícula

        # Números calientes y fríos
        self.calientes_label = tk.Label(main_frame, text="Números Calientes: ", font=("Helvetica", 12), bg="#222831", fg="#00adb5")  # Etiqueta para números calientes
        self.calientes_label.grid(row=1, column=0, pady=(10, 0))  # Coloca la etiqueta en la cuadrícula
        
        self.numeros_calientes = tk.Label(main_frame, text="", font=("Helvetica", 10), bg="#222831", fg="#eeeeee")  # Etiqueta para mostrar los números calientes
        self.numeros_calientes.grid(row=1, column=1, pady=(10, 0))  # Coloca la etiqueta en la cuadrícula

        self.fríos_label = tk.Label(main_frame, text="Números Fríos: ", font=("Helvetica", 12), bg="#222831", fg="#00adb5")  # Etiqueta para números fríos
        self.fríos_label.grid(row=2, column=0, pady=(10, 0))  # Coloca la etiqueta en la cuadrícula

        self.numeros_fríos = tk.Label(main_frame, text="", font=("Helvetica", 10), bg="#222831", fg="#eeeeee")  # Etiqueta para mostrar los números fríos
        self.numeros_fríos.grid(row=2, column=1, pady=(10, 0))  # Coloca la etiqueta en la cuadrícula

        # Tablero de apuestas
        self.tablero_frame = tk.Frame(master, bg="#222831")  # Crea un marco para el tablero de apuestas
        self.tablero_frame.pack(pady=20)  # Añade el marco a la ventana

        self.tablero_label = tk.Label(self.tablero_frame, text="Tablero de Apuestas", font=("Helvetica", 14), bg="#222831", fg="#00adb5")  # Etiqueta para el tablero
        self.tablero_label.grid(row=0, column=0, columnspan=3)  # Coloca la etiqueta en la cuadrícula

        self.fichas = []  # Lista para almacenar los botones de apuestas
        for i in range(37):  # Crea botones para cada número de la ruleta
            color = "#00adb5"  # Color por defecto para los botones
            if i == 0:
                color = "green"  # Color para el número 0
            elif i in self.rojos:
                color = "red"  # Color para los números rojos
            elif i in self.negros:
                color = "black"  # Color para los números negros
            
            # Crea un botón para cada número que llama a la función de apostar
            def crear_comando(numero):
                return lambda: self.apostar(numero)
            ficha = tk.Button(self.tablero_frame, text=str(i), command=crear_comando(i), bg=color, fg="#ffffff", width=5, height=2)
            ficha.grid(row=(i // 12) + 1, column=i % 12, padx=5, pady=5)  # Coloca el botón en la cuadrícula
            self.fichas.append(ficha)  # Añade el botón a la lista de fichas

        # Botones para apostar en rojo y negro
        self.boton_rojo = tk.Button(self.tablero_frame, text="Apostar en Rojo", command=lambda: self.apostar_color("rojo"), bg="#ff4d4d", fg="#ffffff", width=15, height=2)  # Botón para apostar en rojo
        self.boton_rojo.grid(row=4, column=0, padx=5, pady=5)  # Coloca el botón en la cuadrícula

        self.boton_negro = tk.Button(self.tablero_frame, text="Apostar en Negro", command=lambda: self.apostar_color("negro"), bg="#4d4dff", fg="#ffffff", width=15, height=2)  # Botón para apostar en negro
        self.boton_negro.grid(row=4, column=1, padx=5, pady=5)  # Coloca el botón en la cuadrícula

        # Botón para girar la ruleta
        self.boton_girar = tk.Button(self.tablero_frame, text="Girar Ruleta", command=self.girar_ruleta, bg="#00adb5", fg="#ffffff", width=15, height=2)  # Botón para girar la ruleta
        self.boton_girar.grid(row=4, column=2, padx=5, pady=5)  # Coloca el botón en la cuadrícula

        # Botón de salida
        self.boton_salir = tk.Button(main_frame, text="Salir", command=self.master.quit, font=self.label_font, bg="#f05454", fg="#eeeeee", activebackground="#d94141", width=15, height=2)  # Botón para salir del juego
        self.boton_salir.grid(row=3, column=0, pady=10)  # Coloca el botón en la cuadrícula

    def actualizar_numeros_calientes_y_frios(self):
        if len(self.historial_resultados) == 0:  # Verifica si hay resultados en el historial
            return

        contador = Counter(self.historial_resultados)  # Cuenta los resultados
        numeros_calientes = contador.most_common(3)  # Obtiene los 3 números más comunes
        numeros_frios = contador.most_common()[:-4:-1]  # Obtiene los 3 números menos comunes

        calientes = [str(num[0]) for num in numeros_calientes]  # Extrae los números calientes
        frios = [str(num[0]) for num in numeros_frios]  # Extrae los números fríos

        self.numeros_calientes.config(text=", ".join(calientes))  # Actualiza la etiqueta de números calientes
        self.numeros_fríos.config(text=", ".join(frios))  # Actualiza la etiqueta de números fríos

    def apostar(self, numero):
        if self.fondo <= 0:  # Verifica si el saldo es cero
            messagebox.showinfo("Fin del juego", "No tienes más saldo para seguir jugando.")  # Muestra un mensaje
            return

        cantidad = simpledialog.askinteger("Apuesta", f"Elige tu apuesta para el número {numero}: $", minvalue=1, maxvalue=self.fondo)  # Solicita la cantidad a apostar
        if cantidad is None:  # Si el usuario cancela
            return

        if cantidad > self.fondo:  # Verifica si la apuesta es mayor que el saldo
            messagebox.showerror("Error", "No tienes suficiente saldo para realizar esta apuesta.")  # Muestra un mensaje de error
            return

        self.fondo -= cantidad  # Resta la apuesta del fondo
        self.balance_label.config(text=f"Saldo: ${self.fondo}")  # Actualiza la etiqueta del saldo

        # Simulación de giro
        self.resultado_label.config(text="Girando la ruleta...", fg="#ffd369")  # Muestra un mensaje de giro
        self.master.update()  # Actualiza la interfaz
        time.sleep(1)  # Pausa para simular el giro

        # Animación de cuenta regresiva
        for i in range(3, 0, -1):  # Cuenta regresiva de 3 a 1
            self.resultado_label.config(text=f"Girando... {i}")  # Actualiza el mensaje
            self.master.update()  # Actualiza la interfaz
            time.sleep(0.5)  # Pausa entre números

        aleatorio = random.choice(self.ruleta)  # Selecciona un número aleatorio de la ruleta
        self.resultado_label.config(text=f"El número que salió es el {aleatorio}", fg="#ffd369")  # Muestra el resultado

        # Añadir resultado al historial
        self.historial_resultados.append(aleatorio)  # Agrega el resultado al historial

        # Actualizar números calientes y fríos
        self.actualizar_numeros_calientes_y_frios()  # Llama a la función para actualizar los números

        # Evaluación de la apuesta
        if numero == aleatorio:  # Si el número apostado es el mismo que el resultado
            ganancia = cantidad * 36  # Calcula la ganancia
            self.fondo += ganancia  # Aumenta el saldo
            messagebox.showinfo("Resultado", f"¡Ganaste en el número {numero}! Ganancia: ${ganancia}")  # Muestra el mensaje de victoria
        else:
            messagebox.showinfo("Resultado", f"Perdiste en el número {numero}! Apuesta: ${cantidad}")  # Muestra el mensaje de pérdida

        self.balance_label.config(text=f"Saldo: ${self.fondo}")  # Actualiza la etiqueta del saldo

        # Fin del juego si saldo es cero
        if self.fondo <= 0:  # Si el saldo es cero
            messagebox.showinfo("Fin del juego", "No tienes más saldo para seguir jugando.")  # Muestra un mensaje de fin de juego

    def apostar_color(self, color):
        if self.fondo <= 0:  # Verifica si el saldo es cero
            messagebox.showinfo("Fin del juego", "No tienes más saldo para seguir jugando.")  # Muestra un mensaje
            return

        cantidad = simpledialog.askinteger("Apuesta", f"Elige tu apuesta para {color}: $", minvalue=1, maxvalue=self.fondo)  # Solicita la cantidad a apostar
        if cantidad is None:  # Si el usuario cancela
            return

        if cantidad > self.fondo:  # Verifica si la apuesta es mayor que el saldo
            messagebox.showerror("Error", "No tienes suficiente saldo para realizar esta apuesta.")  # Muestra un mensaje de error
            return

        self.fondo -= cantidad  # Resta la apuesta del fondo
        self.balance_label.config(text=f"Saldo: ${self.fondo}")  # Actualiza la etiqueta del saldo

        # Simulación de giro
        self.resultado_label.config(text="Girando la ruleta...", fg="#ffd369")  # Muestra un mensaje de giro
        self.master.update()  # Actualiza la interfaz
        time.sleep(1)  # Pausa para simular el giro

        # Animación de cuenta regresiva
        for i in range(3, 0, -1):  # Cuenta regresiva de 3 a 1
            self.resultado_label.config(text=f"Girando... {i}")  # Actualiza el mensaje
            self.master.update()  # Actualiza la interfaz
            time.sleep(0.5)  # Pausa entre números

        aleatorio = random.choice(self.ruleta)  # Selecciona un número aleatorio de la ruleta
        self.resultado_label.config(text=f"El número que salió es el {aleatorio}", fg="#ffd369")  # Muestra el resultado

        # Añadir resultado al historial
        self.historial_resultados.append(aleatorio)  # Agrega el resultado al historial

        # Actualizar números calientes y fríos
        self.actualizar_numeros_calientes_y_frios()  # Llama a la función para actualizar los números

        # Evaluación de la apuesta
        if color == "rojo":  # Si se apostó en rojo
            if aleatorio in self.rojos:  # Verifica si el número aleatorio está en los números rojos
                ganancia = cantidad * 2  # Calcula la ganancia
                self.fondo += ganancia  # Aumenta el saldo
                messagebox.showinfo("Resultado", f"¡Ganaste en rojo! Ganancia: ${ganancia}")  # Muestra el mensaje de victoria
            else:
                messagebox.showinfo("Resultado", f"Perdiste en rojo! Apuesta: ${cantidad}")  # Muestra el mensaje de pérdida
        elif color == "negro":  # Si se apostó en negro
            if aleatorio in self.negros:  # Verifica si el número aleatorio está en los números negros
                ganancia = cantidad * 2  # Calcula la ganancia
                self.fondo += ganancia  # Aumenta el saldo
                messagebox.showinfo("Resultado", f"¡Ganaste en negro! Ganancia: ${ganancia}")  # Muestra el mensaje de victoria
            else:
                messagebox.showinfo("Resultado", f"Perdiste en negro! Apuesta: ${cantidad}")  # Muestra el mensaje de pérdida

        self.balance_label.config(text=f"Saldo: ${self.fondo}")  # Actualiza la etiqueta del saldo

        # Fin del juego si saldo es cero
        if self.fondo <= 0:  # Si el saldo es cero
            messagebox.showinfo("Fin del juego", "No tienes más saldo para seguir jugando.")  # Muestra un mensaje de fin de juego

    def girar_ruleta(self):
        # Simulación de giro
        self.resultado_label = tk.Label(self.tablero_frame, text="Girando la ruleta...", font=("Helvetica", 14), bg="#222831", fg="#ffd369")  # Muestra un mensaje de giro
        self.resultado_label.grid(row=5, column=0, columnspan=3)  # Coloca la etiqueta en la cuadrícula
        self.master.update()  # Actualiza la interfaz
        time.sleep(1)  # Pausa para simular el giro

        # Animación de cuenta regresiva
        for i in range(3, 0, -1):  # Cuenta regresiva de 3 a 1
            self.resultado_label.config(text=f"Girando... {i}")  # Actualiza el mensaje
            self.master.update()  # Actualiza la interfaz
            time.sleep(0.5)  # Pausa entre números

        aleatorio = random.choice(self.ruleta)  # Selecciona un número aleatorio de la ruleta
        self.resultado_label.config(text=f"El número que salió es el {aleatorio}", fg="#ffd369")  # Muestra el resultado

        # Añadir resultado al historial
        self.historial_resultados.append(aleatorio)  # Agrega el resultado al historial

        # Actualizar números calientes y fríos
        self.actualizar_numeros_calientes_y_frios()  # Llama a la función para actualizar los números

if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal
    juego = JuegoRuleta(root)  # Inicializa el juego de ruleta
    root.mainloop()  # Inicia el bucle principal de la interfaz gráfica