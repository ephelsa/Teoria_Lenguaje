import re as regex

'''
El script Tokenizer.py nos sirve para modificar la data entrante a objetos usables para nosotros.
'''

'''
Limpiamos las entradas iniciales que ingresan separadas por comas (,). Luego
le quitamos todos los espacios que esta posea para evitar futuros problemas que nos puedan causar.

@param input Es una cadena de texto, la cual limpiaremos.

@return array Array de objetos con los datos separados.
'''
def tokenizerSimple(input):
    array = str(input).split(',')

    for (index, item) in enumerate(array):
        array[index] = regex.sub(r"\s+", "", item)
    
    return array

'''
Limpia la cadena que se ingresa como fila al momento de armar la Tabla de Transiciones.

Primero, se le realiza una limpieza simple con el metodo tokenizerSimple para separar los datos y obtener
el estado actual y los simbolos junto con sus transiciones.

Segundo, a los simbolos con transiciones se separan para obtener los simbolos de entrada y las transiciones 
a la que ira. 

@param input Es una cadena de texto, la cual limpiaremos.

@return filaTransicion Se retorna un diccionario con los datos separados para la fila.
'''
def tokenizerTransiciones(input):
    fila = tokenizerSimple(input)
    
    estado_actual = fila[0]

    filaTransicion = {'estado_actual' : estado_actual}
    for transicion in fila[1:]:
        data = transicion.split('=')
        simbolo = data[0]

        estados = data[1].split(';')
        for (index, item) in enumerate(estados):
            estados[index] = regex.sub(r"\s+", "", item)


        filaTransicion.update({simbolo : estados})

    return filaTransicion