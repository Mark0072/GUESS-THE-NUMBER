print('strings')
name = 'nisanproxd'
print(name.title()) #convierte la primera letra en mayuscula

print(name.upper()) #convierte todas las letras en mayusculas

print(name.lower())

f_n = 'noila'
l_n = 'faster'
full_name = f'{f_n} {l_n}'
print(f' hello {full_name.lstrip()}')

#Whitespace (n) Tab(n)


print(f'\t{name}')
print(f'\n{full_name}')

#prefixes eliminar el dato de una varible que no queremos que se muestre

nostarch_url = 'https://nostarch.com'    
nostarch_url.removeprefix('https://')