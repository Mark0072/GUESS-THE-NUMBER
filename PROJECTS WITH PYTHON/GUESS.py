import random
import time

class TaskTrackerGame:
    def __init__(self, user_name):
        self.user_name = user_name
        self.dificultad = None
        self.chances = 0
        self.numero_secreto = random.randint(1, 100)

    def saludar(self):
        print(f"¡Hola, {self.user_name}! Bienvenido al juego de adivinar el número.")

    def reglas(self):
        print("""
        Este juego consiste en adivinar un número secreto entre 1 y 100.
        Puedes intentar adivinar el número dentro de los intentos que te corresponden según la dificultad.
        """)

    def seleccionar_dificultad(self):
        print("\nSelecciona la dificultad del juego:")
        print("1. Fácil")
        print("2. Intermedio")
        print("3. Difícil")

        opcion = input("Introduce el número de la dificultad: ")

        if opcion == "1":
            self.dificultad = "Fácil"
            self.chances = 10
        elif opcion == "2":
            self.dificultad = "Intermedio"
            self.chances = 5
        elif opcion == "3":
            self.dificultad = "Difícil"
            self.chances = 3
        else:
            print("Opción no válida, se seleccionará 'Fácil' por defecto.")
            self.dificultad = "Fácil"
            self.chances = 10

        print(f"Dificultad seleccionada: {self.dificultad}")
        print(f"Chances disponibles: {self.chances}")

    def adivinar_numero(self):
        self.numero_secreto = random.randint(1, 100)
        print("\n¡Empecemos a adivinar el número entre 1 y 100!")

        start_time = time.time()  # Inicia el temporizador

        while self.chances > 0:
            try:
                guess = int(input(f"Tienes {self.chances} intentos restantes. Ingresa tu número: "))
                if guess < self.numero_secreto:
                    print("El número es mayor. ¡Sigue intentando!")
                elif guess > self.numero_secreto:
                    print("El número es menor. ¡Sigue intentando!")
                else:
                    end_time = time.time()  # Detiene el temporizador
                    tiempo_total = end_time - start_time
                    print(f"¡Felicidades, {self.user_name}! Adivinaste el número correctamente.")
                    print(f"Tiempo total: {tiempo_total:.2f} segundos.")
                    return True
                self.chances -= 1
            except ValueError:
                print("Por favor, ingresa un número válido.")
        
        end_time = time.time()  # Detiene el temporizador si se quedan sin intentos
        tiempo_total = end_time - start_time
        print("Game Over. Te quedaste sin intentos.")
        print(f"El número secreto era: {self.numero_secreto}")
        print(f"Tiempo total: {tiempo_total:.2f} segundos.")
        return False

    def jugar(self):
        self.saludar()
        self.reglas()

        while True:
            self.seleccionar_dificultad()
            if self.adivinar_numero():
                print("\n¡Has ganado! ¿Quieres jugar otra vez?")
            else:
                print("\n¡Perdiste! ¿Quieres jugar otra vez?")
            
            jugar_otra_vez = input("¿Quieres jugar otra ronda? (sí/no): ").lower()
            if jugar_otra_vez != 'sí':
                print("¡Gracias por jugar! ¡Hasta la próxima!")
                break

# Uso de la clase
usuario = TaskTrackerGame("Juan")
usuario.jugar()
