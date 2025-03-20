def dos_simbolos():
    a = int(input("Ingrese el primer número: "))
    b = int(input("Ingrese el segundo número: "))
    c = input("Seleccione un operador (% para módulo o * para multiplicación): ")

    if c == "*":
        print(a * b)
    elif c == "%":
        if b != 0:  # Verifica que 'b' no sea cero
            print(a % b)
        else:
            print("Error: No se puede dividir por cero.")
    else:
        print("Operador no válido.")



dos_simbolos()


    
    

  