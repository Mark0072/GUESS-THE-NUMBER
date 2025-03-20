def energia_potencial():
  m = float(input('Ingrese el valor de m:'))
  h = float(input('Ingrese el valor de h:'))
  G = 9.81
  ep = float(m*G*h)
  print(f'{ep} es la energia potencial')
  return ep

energia_potencial()