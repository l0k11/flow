import uuid
cadena = str(uuid.uuid4())
contador = 0
for caracter in cadena:
    contador += 1

print(f"La cadena tiene {contador} caracteres alfanuméricos")

