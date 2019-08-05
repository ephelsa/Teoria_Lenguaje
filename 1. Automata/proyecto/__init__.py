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



#print(automata.simbolos_entrada)
#print(automata.estados)
#print(automata.estado_inicial)
#print(automata.estados_aceptacion)
