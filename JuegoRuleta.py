import random
import pymysql

conexion = pymysql.connect(host = 'localhost', user = 'root', password = 'root', database = 'datosRuleta')
cur = conexion.cursor()
cur.execute("SELECT * FROM ruleta")



class JuegoRuleta:
    MULTIPLICADOR_NUMERO = 36
    MULTIPLICADOR_COLOR = 2

    # Inicializa el saldo del jugador y las configuraciones de la ruleta.
    def __init__(self):
        self.fondo = 1000 
        self.ruleta = list(range(37))  
        self.rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36] 
        self.negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]  

    # Selecciona y devuelve un número aleatorio de la ruleta.
    def _seleccionar_numero(self):
        return random.choice(self.ruleta)

    # Genera un mensaje que indica si se ha ganado o perdido la apuesta.
    # resultado: booleano que indica si se ganó o no.
    # cantidad_apostada: la cantidad de dinero apostada.
    # tipo: el tipo de apuesta (número o color).
    # ganancia: la cantidad ganada en caso de ganar.
    def _generar_mensaje(self, resultado, cantidad_apostada, tipo, ganancia=0):
       
        if resultado:
            return f"Apostaste en {tipo} y ganaste ${ganancia}!"
        else:
            return f"Apostaste en {tipo} y perdiste ${cantidad_apostada}."


    # Realiza una apuesta en un número específico.
    # apuesta: una tupla que contiene el número apostado y la cantidad apostada.
    # Devuelve la ganancia y un mensaje sobre el resultado de la apuesta.
    def apostar(self, apuesta):
        numero_apostado, cantidad_apostada = apuesta[0]
        aleatorio = self._seleccionar_numero() 
        ganancia = 0
        
        if numero_apostado == aleatorio:  
            ganancia = cantidad_apostada * self.MULTIPLICADOR_NUMERO
        
        mensaje = self._generar_mensaje(ganancia > 0, cantidad_apostada, numero_apostado, ganancia)
        return ganancia, mensaje  
    
    # Realiza una apuesta en un color específico (rojo o negro).
    # color: el color en el que se apuesta (debe ser "rojo" o "negro").
    # cantidad_apostada: la cantidad de dinero apostada.
    # Devuelve la ganancia y un mensaje sobre el resultado de la apuesta.
    def apostar_color(self, color, cantidad_apostada):
        aleatorio = self._seleccionar_numero() 
        ganancia = 0
        
        if (color == "rojo" and aleatorio in self.rojos) or (color == "negro" and aleatorio in self.negros):
            ganancia = cantidad_apostada * self.MULTIPLICADOR_COLOR
            
        mensaje = self._generar_mensaje(ganancia > 0, cantidad_apostada, color, ganancia)
        return ganancia, mensaje  