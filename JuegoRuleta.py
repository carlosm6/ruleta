import random
import pymysql
""""
conexion = pymysql.connect(host = 'localhost', user = 'root', password = 'root', database = 'datosRuleta')
cur = conexion.cursor()
cur.execute("SELECT * FROM ruleta")
"""


class JuegoRuleta:
    """
    Clase que modela un juego de ruleta.

    Atributos:
    ----------
    MULTIPLICADOR_NUMERO : int
        Constante que representa el multiplicador de ganancias para apuestas a números (36 veces).
    MULTIPLICADOR_COLOR : int
        Constante que representa el multiplicador de ganancias para apuestas a colores (2 veces).
    fondo : int
        El saldo inicial del jugador.
    ruleta : list[int]
        Lista de números disponibles en la ruleta (0-36).
    rojos : list[int]
        Números considerados "rojos" en la ruleta.
    negros : list[int]
        Números considerados "negros" en la ruleta.

    Métodos:
    --------
    __init__():
        Inicializa los atributos de la clase, como los números de la ruleta y los colores.
    apostar(apuesta):
        Realiza una apuesta a un número específico.
    apostar_color(color, cantidad_apostada):
        Realiza una apuesta a un color específico (rojo/negro).
    """
    MULTIPLICADOR_NUMERO = 36
    MULTIPLICADOR_COLOR = 2


    def __init__(self):
        """
        Constructor de la clase JuegoRuleta.

        Inicializa el saldo del jugador (`fondo`) y las configuraciones estándar de la ruleta,
        incluyendo la lista de números disponibles y sus colores asociados (rojo y negro).
        """
        self.fondo = 1000 
        self.ruleta = list(range(37))  
        self.rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36] 
        self.negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]  


    def _seleccionar_numero(self):
        """
        Selecciona y devuelve un número aleatorio de la ruleta.

            Retorna:
            --------
            int:
            Número seleccionado de la ruleta (0-36).
        """
        return random.choice(self.ruleta)


    def _generar_mensaje(self, resultado, cantidad_apostada, tipo, ganancia=0):
        """
        Genera un mensaje indicando si se ganó o perdió la apuesta.

        Parámetros:
        -----------
        resultado : bool
            Indica si el resultado de la apuesta es favorable (True) o no (False).
        cantidad_apostada : float
            Cantidad de dinero apostada por el jugador.
        tipo : str
            Tipo de apuesta realizada (número o color).
        ganancia : float, opcional
            Cantidad ganada en caso de resultado favorable (por defecto 0).

        Retorna:
        --------
        str:
            Mensaje informativo sobre el resultado de la apuesta.
        """
        if resultado:
            return f"Apostaste en {tipo} y ganaste €{ganancia}!"
        else:
            return f"Apostaste en {tipo} y perdiste €{cantidad_apostada}."



    def apostar(self, apuesta):
        """
        Realiza una apuesta sobre un número específico.

        Parámetros:
        -----------
        apuesta : tuple
            Una tupla que contiene el número apostado y la cantidad apostada.

        Retorna:
        --------
        tuple:
            - La ganancia obtenida (float, 0 si se pierde).
            - Mensaje informativo sobre el resultado de la apuesta (str).
        """
        numero_apostado, cantidad_apostada = apuesta[0]
        aleatorio = self._seleccionar_numero() 
        ganancia = 0
        
        if numero_apostado == aleatorio:  
            ganancia = cantidad_apostada * self.MULTIPLICADOR_NUMERO
        
        mensaje = self._generar_mensaje(ganancia > 0, cantidad_apostada, numero_apostado, ganancia)
        return ganancia, mensaje  
    

    def apostar_color(self, color, cantidad_apostada):
        """
        Realiza una apuesta sobre un color específico (rojo o negro).

        Parámetros:
        -----------
        color : str
            El color en el que se apuesta. Debe ser "rojo" o "negro".
        cantidad_apostada : float
            Cantidad de dinero apostada por el jugador.

        Retorna:
        --------
        tuple:
            - La ganancia obtenida (float, 0 si se pierde).
            - Mensaje informativo sobre el resultado de la apuesta (str).
        """
        aleatorio = self._seleccionar_numero() 
        ganancia = 0
        
        if (color == "rojo" and aleatorio in self.rojos) or (color == "negro" and aleatorio in self.negros):
            ganancia = cantidad_apostada * self.MULTIPLICADOR_COLOR
            
        mensaje = self._generar_mensaje(ganancia > 0, cantidad_apostada, color, ganancia)
        return ganancia, mensaje  