# -*- coding: utf-8 -*-
#Crear una clase coche.
class Coche:
  def __init__(self, modelo,ano, velocidad ):
    self.modelo = modelo
    self.ano = ano
    self.velocidad = velocidad

  def acelear(self, cantidad):
    self.velocidad += cantidad
    return (f"El coche ha acelerado {cantidad} km/h. Velocidad actual: {self.velocidad} km/h")
  
  def frenar(self, cantidad):
    self.frenar = max(0,self.velocidad - cantidad)
    return (f"El coche ha frenado {cantidad} km/h. Velocidad actual: {self.velocidad} km/h")
      
      

  def monstrar_info(self):
    return  (f"Modelo: {self.modelo}, Año: {self.ano}, Velocidad: {self.velocidad} km/h")
  
mi_coche = Coche("Toyota Corolla", 2022, 50)
print(mi_coche.monstrar_info()) # Salida: Modelo: Toyota Corolla, Año: 2022, Velocidad: 50 km/h

      
   

