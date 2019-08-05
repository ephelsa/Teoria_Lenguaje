from terminaltables import AsciiTable

from tokenizer.Tokenizer import tokenizerSimple
from tokenizer.Tokenizer import tokenizerTransiciones

'''
La clase Automata permite gestionar todo lo relacionado con el automata que ingrese el usuario.
'''
class Automata:
    
    '''
    Atributos necesarios para la creacion de la tabla de transiciones y validacion del automata.
    '''
    simbolos_entrada = []
    estados = []
    estado_inicial = []
    estados_aceptacion = []

    '''
    Constructor
    '''
    def __init__(self, simbolos_entrada, estados, estado_inicial, estados_aceptacion):
        self.simbolos_entrada = simbolos_entrada
        self.estados = estados
        self.estado_inicial = estado_inicial[0]
        self.estados_aceptacion = estados_aceptacion

        self.tabla_transiciones = self.TablaTransiciones(self.simbolos_entrada, self.estado_inicial)

        # Array con todas las filas de transiciones.
        filas_transiciones = []
        for index in range(len(estados)):
            filas_transiciones.append(tokenizerTransiciones(input("Fila[{0}] >> ".format(index + 1))))

        #print(filas_transiciones)
        if self.__automataValido(filas_transiciones):
            self.tabla_transiciones.mostrar()


    def __automataValido(self, filas_transiciones):
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
                if fila['estado_actual'] == self.estado_inicial:
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
            fila_entradas = {}
            for (i_entrada, entrada) in enumerate(self.simbolos_entrada):
                if fila[entrada]:
                    entradas_existentes[i_entrada] = True

                    fila_entradas.update({entrada : fila[entrada]})

            #### Insertamos la fila en la tabla de transiciones
            self.tabla_transiciones.insertarFila(fila['estado_actual'], fila_entradas, fila['estado_actual'] in self.estados_aceptacion)
            ########################## Validamos que los simbolos de entrada existen en la fila
            for (i_existente, existente) in enumerate(entradas_existentes):
                if not existente:
                    print("Error en los simbolos de entrada en secuencia #{0}".format(str(i_existente + 1)))
                    return False

            #print("Entrada " + fila['estado_actual'] + "=> " + str(entradas_existentes))
        
        
        ######### Validdamos los otros existentes
        if not inicial_existente:
            print("El estado inicial {0} no fue encontrado en las secuencias ingresadas.".format(str(self.estado_inicial)))
            return False
        
        for (i_aceptacion, aceptacion) in enumerate(aceptacion_existente):
            if not aceptacion:
                print("El estado de aceptacion {0} no se encuentra en las secuencias ingresadas.".format(str(self.estados_aceptacion[i_aceptacion])))
                return False

        for (i_estado, estado) in enumerate(estados_existentes):
            if not estado:
                print("El estado {0} no fue encontrado en las secuencias ingresadas".format(str(self.estados[i_estado])))
                return False

        #print("Estados => " + str(estados_existentes))
        #print("Inicial => " + str(inicial_existente))
        #print("Aceptacion  => " + str(aceptacion_existente))


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

        # Tabla de transiciones
        __tabla_transiciones = []

        '''
        Constructor: Aqui seteamos la primera fila de la Tabla de Transiciones, la cual corresponde a los simbolos.
        @param simbolos_entrada Simbolos de entrada que se tienen para la Tabla.
        @param estado_inicial Estado correspondiente al que ira de primero en la Tabla de Transiciones.
        '''
        def __init__(self, simbolos_entrada, estado_inicial):
            self.__simbolos_entrada = simbolos_entrada
            self.__estado_inicial = estado_inicial

            entradas = ['CS']
            for entrada in self.__simbolos_entrada:
                entradas.append("{0}".format(str(entrada)))

            self.__tabla_transiciones.append(entradas)


        '''
        Insertamos los datos en los arrays de datos para posteriormente actualizar la Tabla de Transiciones.

        @param estado_actual Estado que tiene esa fila actualmente.
        @param transiciones Son todas las transiciones que posee el estado con el simbolo de entrada.
        @param aceptado Corresponde al estado que es aceptado por el automata finito.
        '''
        def insertarFila(self, estado_actual, transiciones, aceptado = False):
            self.estados_actuales.append(estado_actual)
            self.transiciones.append(transiciones)
            self.aceptados.append(aceptado)

            self.__actualizarTabla()

        '''
        Actualizamos la Tabla de Transiciones ubicando el estado inical en la primera fila (despues de los simbolos).
        Ademas, los simbolos para cada fila se ubican en el orden que el usuario los haya ingresado.
        '''
        def __actualizarTabla(self):
            nueva_fila = [self.estados_actuales[-1]]

            # Ubicacion de los simbolos en el orden que el usuario digito inicialmente.
            for entrada in self.__simbolos_entrada:
                nueva_fila.append((self.transiciones[-1])[entrada])

            nueva_fila.append(self.aceptados[-1])

            # Insercion de la fila en la tabla
            self.__tabla_transiciones.append(nueva_fila)

            # Modificacion del estado incial.
            if self.estados_actuales[-1] == self.__estado_inicial:
                self.__tabla_transiciones[-1], self.__tabla_transiciones[1] = self.__tabla_transiciones[1], self.__tabla_transiciones[-1]


        '''
        Permite obtener el total de transiciones que tiene el estado para X simbolo.
        @param index Numero de la fila.

        @return Integer Total de transiciones.
        '''
        def totalTransiciones(self, index):
            return len(self.transiciones[index])

        '''
        Mostramos la tabla.
        Se utiliza terminaltables para esto.
        '''
        def mostrar(self):
            #print(self.__tabla_transiciones)
            table = AsciiTable(self.__tabla_transiciones)
            print(table.table)
