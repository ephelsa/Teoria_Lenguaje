from automata.Automata import Automata
from tokenizer.Tokenizer import tokenizerSimple

'''
Leemos los datos necesarios para empezar a procesar el automata.

Tokenizamos las entradas para obtenerlas en forma de array.
'''
simbolos_entrada = tokenizerSimple(input("Simbolos de entrada >> "))
estados = tokenizerSimple(input("Estados >> "))
estado_inicial = tokenizerSimple(input("Estado inicial >> "))
estados_aceptacion = tokenizerSimple(input("Estados de Aceptacion >> "))

# Creamos una nueva instancia de tipo Automata.
automata = Automata(simbolos_entrada, estados, estado_inicial, estados_aceptacion)



#print("Entrada -->", automata.simbolos_entrada)
#print("Estados -->", automata.estados)
#print("Inicial -->", automata.estado_inicial)
#print("Aceptacion -->", automata.estados_aceptacion)
