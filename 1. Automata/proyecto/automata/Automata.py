from tokenizer.Tokenizer import tokenizerSimple
from tokenizer.Tokenizer import tokenizerTransiciones

'''
La clase Automata permite gestionar todo lo relacionado con el automata que ingrese el usuario.
'''
class Automata:
    
    '''
    Atributos necesarios para la creacion de la tabla de transiciones y validacion del automata.
    '''
    simbolos_entrada = {}
    estados = {}
    estado_inicial = {}
    estados_aceptacion = {}

    '''
    Constructor
    '''
    def __init__(self, simbolos_entrada, estados, estado_inicial, estados_aceptacion):
        self.simbolos_entrada = simbolos_entrada
        self.estados = estados
        self.estado_inicial = estado_inicial 
        self.estados_aceptacion = estados_aceptacion

        self.tabla_transiciones = self.TablaTransiciones()

        # Array con todas las filas de transiciones.
        filas_transiciones = []
        for index in range(len(estados)):
            filas_transiciones.append(tokenizerTransiciones(input("Fila[{0}] >> ".format(index + 1))))

        #print(filas_transiciones)
        print(self.automataValido(filas_transiciones))

### Before
    def automataValido(self, filas_transiciones):
        ################ 
        inicial_existente = False
        aceptacion_existente = []
        estados_existentes = []


        ################ Total de filas congruente con los estados
        if len(self.estados) != len(filas_transiciones):
            print("El total de Transiciones no tienen el mismo tamano que el total de Estados.")
            return False

        ################## Seteo de los estados de aceptacion en falso para empezar a validar
        for aceptacion in self.estados_aceptacion:
            aceptacion_existente.append(False)

        ################## Seteo de los estados existentes en falso para empezar a validar
        for estados in self.estados:
            estados_existentes.append(False)

        for (i_fila, fila) in enumerate(filas_transiciones):

            ################### Estados existentes
            for (i_estado, estado) in enumerate(self.estados):
                if fila['estado_actual'] == estado:
                    estados_existentes[i_estado] = True

                ################# Total de simbolos por fila
                if len(self.simbolos_entrada) != (len(fila) - 1):
                    print("La entrada #{0} no posee todos los simbolos de entrada.".format(str(i_estado + 1)))
                    return False

                ################# Estado inicial
                if fila['estado_actual'] == self.estado_inicial[0]:
                    inicial_existente = True
            
            #################### Estados de aceptacion
            for (i_aceptacion, aceptacion) in enumerate(self.estados_aceptacion):
                if aceptacion == fila['estado_actual']:
                    aceptacion_existente[i_aceptacion] = True

            #################### Seteo de las entradas en falso para comenzar a validar si existen
            entradas_existentes = []
            for entrada in self.simbolos_entrada:
                entradas_existentes.append(False)

            #################### Simbolos de entrada correspondientes a la fila
            fila_entradas = []
            for (i_entrada, entrada) in enumerate(self.simbolos_entrada):
                if fila[entrada]:
                    entradas_existentes[i_entrada] = True

                    fila_entradas.append({entrada : fila[entrada]})

            #### Insertamos la fila en la tabla de transiciones
            self.tabla_transiciones.insertarFila(fila['estado_actual'], fila_entradas, fila['estado_actual'] in self.estados_aceptacion)
            ########################## Validamos que los simbolos de entrada existen en la fila
            for (i_existente, existente) in enumerate(entradas_existentes):
                if not existente:
                    print("Error en los simbolos de entrada en secuencia #{0}".format(str(i_existente + 1)))
                    return False

            print("Entrada " + fila['estado_actual'] + "=> " + str(entradas_existentes))
        
        
        ######### Validdamos los otros existentes
        if not inicial_existente:
            print("El estado inicial {0} no fue encontrado en las secuencias ingresadas.".format(str(self.estado_inicial[0])))
            return False
        
        for (i_aceptacion, aceptacion) in enumerate(aceptacion_existente):
            if not aceptacion:
                print("El estado de aceptacion {0} no se encuentra en las secuencias ingresadas.".format(str(self.estados_aceptacion[i_aceptacion])))
                return False

        for (i_estado, estado) in enumerate(estados_existentes):
            if not estado:
                print("El estado {0} no fue encontrado en las secuencias ingresadas".format(str(self.estados[i_estado])))
                return False

        print("Estados => " + str(estados_existentes))
        print("Inicial => " + str(inicial_existente))
        print("Aceptacion  => " + str(aceptacion_existente))


        return True

#a, 0=a;c, 1=c
#b, 0=c, 1=b
#c, 0=b;c, 1=a

    '''
    DAO para las filas de la Tabla de transiciones para la creacion del automata finito
    '''
    class TablaTransiciones:
        
        estados_actuales = []
        transiciones = []
        aceptados = []

        def insertarFila(self, estado_actual, transiciones, aceptado = False):
            self.estados_actuales.append(estado_actual)
            self.transiciones.append(transiciones)
            self.aceptados.append(aceptado)

        def totalTransiciones(self, index):
            return len(self.transiciones[index])

        def mostrar(self):
            
