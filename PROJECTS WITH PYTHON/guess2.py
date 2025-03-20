import random
import time

class JuegoUsuario:
    def __init__(self):
        self.usuario = None
        self.dificultad = None

    class Temporizador:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def iniciar(self):
            self.start_time = time.time()
        
        def detener(self):
            self.end_time = time.time()
        
        def tiempo_total(self):
            return self.end_time - self.start_time if self.end_time else 0

    class Juego:
        def __init__(self, dificultad, usuario):
            self.dificultad = dificultad
            self.chances = self.establecer_chances()
            self.numero_secreto = random.randint(1, 100)
            self.usuario = usuario
            self.temporizador = JuegoUsuario.Temporizador()

        def establecer_chances(self):
            if self.dificultad == "fácil":
                return 10
            elif self.dificultad == "intermedio":
                return 5
            elif self.dificultad == "difícil":
                return 3
            return 10

        def dar_pista(self, guess):
            if guess < self.numero_secreto:
                print("Pista: El número secreto es mayor que tu intento.")
            elif guess > self.numero_secreto:
                print("Pista: El número secreto es menor que tu intento.")

        def jugar(self):
            self.temporizador.iniciar()

            while self.chances > 0:
                try:
                    guess = int(input(f"Tienes {self.chances} intentos restantes. Ingresa tu número: "))
                    if guess == self.numero_secreto:
                        self.temporizador.detener()
                        print(f"¡Felicidades, {self.usuario}! Adivinaste el número correctamente.")
                        print(f"Tiempo total: {self.temporizador.tiempo_total():.2f} segundos.")
                        return True
                    else:
                        self.dar_pista(guess)
                        self.chances -= 1
                except ValueError:
                    print("Por favor, ingresa un número válido.")
            
            self.temporizador.detener()
            print(f"Game Over. Te quedaste sin intentos. El número secreto era: {self.numero_secreto}")
            print(f"Tiempo total: {self.temporizador.tiempo_total():.2f} segundos.")
            return False

    def saludar(self):
        self.usuario = input("¡Hola! ¿Cuál es tu nombre? ")

    def seleccionar_dificultad(self):
        print("\nSelecciona la dificultad del juego:")
        print("1. Fácil")
        print("2. Intermedio")
        print("3. Difícil")
        opcion = input("Introduce el número de la dificultad: ")

        if opcion == "1":
            self.dificultad = "fácil"
        elif opcion == "2":
            self.dificultad = "intermedio"
        elif opcion == "3":
            self.dificultad = "difícil"
        else:
            print("Opción no válida, se seleccionará 'Fácil' por defecto.")
            self.dificultad = "fácil"

    def jugar(self):
        self.saludar()
        while True:
            self.seleccionar_dificultad()
            juego = self.Juego(self.dificultad, self.usuario)
            if juego.jugar():
                print("\n¡Has ganado! ¿Quieres jugar otra vez?")
            else:
                print("\n¡Perdiste! ¿Quieres jugar otra vez?")
            
            jugar_otra_vez = input("¿Quieres jugar otra ronda? (sí/no): ").lower()
            if jugar_otra_vez != 'sí':
                print("¡Gracias por jugar! ¡Hasta la próxima!")

# Uso de la clase
juego_usuario = JuegoUsuario()
juego_usuario.jugar()
