from terminaltables import AsciiTable
import sys

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

    __filas_transiciones = []
    __es_deterministico = True 


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
        self.__filas_transiciones = []
        for index in range(len(estados)):
            self.__filas_transiciones.append(tokenizerTransiciones(input("Fila[{0}] >> ".format(index + 1))))
            self.__filas_transiciones[-1].update({'aceptacion' : self.__filas_transiciones[-1]['estado_actual'] in self.estados_aceptacion})
            
        # Validamos si el automata es valido.
        if self.__automataValido():
            print(self.tipoAutomata())
            print('Sin simplificar =>')
            self.tabla_transiciones.mostrar()
            # Se intenta simplificar si se puede.
            self.__simplificarAutomata()
            # Se valida el automata simplificado.
            if self.__automataValido():
                print('Simplificado =>')
                self.tabla_transiciones.mostrar()

    '''
    Permite conocer si el automata es valido o no en cuanto a ingreso de datos por parte del usuario.

    @return Boolean True si el automata es valido y False en caso contrario.
    '''
    def __automataValido(self):
        ################ 
        inicial_existente = False
        aceptacion_existente = []
        estados_existentes = []
        
        self.tabla_transiciones.limpiarTabla()

        ################ Total de filas congruente con los estados
        if len(self.estados) != len(self.__filas_transiciones):
            sys.exit("El total de Transiciones no tienen el mismo tamano que el total de Estados.")

        ################## Seteo de los estados de aceptacion en falso para empezar a validar
        for aceptacion in self.estados_aceptacion:
            aceptacion_existente.append(False)

        ################## Seteo de los estados existentes en falso para empezar a validar
        for estados in self.estados:
            estados_existentes.append(False)

        for (i_fila, fila) in enumerate(self.__filas_transiciones):
            ################### Estados existentes
            for (i_estado, estado) in enumerate(self.estados):
                if fila['estado_actual'] == estado:
                    estados_existentes[i_estado] = True

                ################# Total de simbolos por fila
                if len(self.simbolos_entrada) != (len(fila) - 2):
                    sys.exit("La entrada #{0} no posee todos los simbolos de entrada.".format(str(i_estado + 1)))

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

                    if not type(fila[entrada]) == str:
                        for estado_entrada in fila[entrada]:
                            if not estado_entrada in self.estados:
                                sys.exit("La transicion '{0}' del estado '{1}' con la entrada '{2}' es invalido.".format(str(estado_entrada), str(fila['estado_actual']), str(entrada)))
                    else:
                        if not fila[entrada] in self.estados:
                            sys.exit("La transicion '{0}' del estado '{1}' con la entrada '{2}' es invalido.".format(str(fila[entrada]), str(fila['estado_actual']), str(entrada)))
               
                    fila_entradas.update({entrada : fila[entrada]})
                    
                    #### Validamos que tipo de automata es.
                    if self.__es_deterministico:
                        self.__es_deterministico = len(fila[entrada]) == 1

            #### Insertamos la fila en la tabla de transiciones
            self.tabla_transiciones.insertarFila(fila['estado_actual'], fila_entradas, fila['aceptacion'])
            ########################## Validamos que los simbolos de entrada existen en la fila
            for (i_existente, existente) in enumerate(entradas_existentes):
                if not existente:
                    sys.exit("Error en los simbolos de entrada en secuencia #{0}".format(str(i_existente + 1)))

            #print("Entrada " + fila['estado_actual'] + "=> " + str(entradas_existentes))
        
        
        ######### Validdamos los otros existentes
        if not inicial_existente:
            sys.exit("El estado inicial {0} no fue encontrado en las secuencias ingresadas.".format(str(self.estado_inicial)))
        
        for (i_aceptacion, aceptacion) in enumerate(aceptacion_existente):
            if not aceptacion:
                sys.exit("El estado de aceptacion {0} no se encuentra en las secuencias ingresadas.".format(str(self.estados_aceptacion[i_aceptacion])))

        for (i_estado, estado) in enumerate(estados_existentes):
            if not estado:
                sys.exit("El estado {0} no fue encontrado en las secuencias ingresadas".format(str(self.estados[i_estado])))

        #print("Estados => " + str(estados_existentes))
        #print("Inicial => " + str(inicial_existente))
        #print("Aceptacion  => " + str(aceptacion_existente))


        return True

    '''
    Retorna el tipo de automata que se tiene.
    
    @return String Con el tipo de automata ingresado.
    '''
    def tipoAutomata(self):
        return "Deterministico" if self.__es_deterministico else "No Deterministico"

    def __simplificarAutomata(self):
        self.__eliminarEstadosRaros()
        self.__metodoParticiones()

    '''
    Elimina los Estados Extranos. Esos estados a los que no se llega mediante ninguna transicion.
    '''
    def __eliminarEstadosRaros(self):
        # Inicialmente se crea un diccionario con la clave estado y el valor de Falso.
        estados_validos = {}
        for estado in self.estados:
            estados_validos.update({estado : False})

        ## El primer for es del estado que comprobaremos vs los demas.
        for comprobar in self.__filas_transiciones:
            # Si ese estado que comprobaremos es el estado inicial, automaticamente lo aceptamos.
            if comprobar['estado_actual'] in self.estado_inicial:
                estados_validos[comprobar['estado_actual']] = True
            else :
                # El estado a comprobar vs los demas.
                for fila in self.__filas_transiciones:
                    # Si el estado a comprobar es igual al de la fila, no lo tomamos.
                    if comprobar['estado_actual'] != fila['estado_actual']:
                        # Recorremos los simbolos de cada entrada
                        for entrada in self.simbolos_entrada:
                            for transicion in fila[entrada]: 
                                # Si el estado valido no se ha visitado antes y es igual al de la transicion, lo marcamos
                                # como valido. Esto significa que si lo encontro una vez no lo vuelva a poner en true.       
                                if not estados_validos[transicion] and comprobar['estado_actual'] == transicion:
                                    estados_validos[transicion] = True

        # Finalmente, recorremos las filas entradas de nuevo con el motivo de quitar aquellos estados raros.
        for (i_fila, fila) in enumerate(self.__filas_transiciones):
            # Si el estado es falso, es decir, que no existe, entramos al if.
            if not estados_validos[fila['estado_actual']]:
                # Si es un estado de aceptacion, y unicamente se tiene uno como valido, retornamos un error.
                if fila['estado_actual'] in self.estados_aceptacion and len(self.estados_aceptacion) == 1:
                    sys.exit("No se llega jamas al estado de aceptacion.")
                else:
                    # Quitamos los extranos de la fila de transiciones.
                    self.__filas_transiciones.pop(i_fila)
                    # Tambien eliminamos ese estado.
                    self.estados.pop(self.estados.index(fila['estado_actual']))
                    # Si se tienen varios estados de aceptacion y uno de ellos es extrano, lo quitamos.
                    if fila['estado_actual'] in self.estados_aceptacion:
                        self.estados_aceptacion.pop(self.estados_aceptacion.index(fila['estado_actual']))

    def __metodoParticiones(self):
        separador = ''     

        ###################
        def buscarGrupo(grupo):
            def pertenece(index, item_pos, relaciones, comparar):
                for (index_relacion, relacion) in enumerate(relaciones):
                    for (index_item, item) in enumerate(relacion):
                        if index_relacion != index and item_pos == index_item:
                            return item == comparar
                        
            ####################
            def unirEquivalentes(particiones):
                nuevas_filas_transiciones = []
                estados_actuales = []
                transiciones_totales = []
                                
                a_unir = (list(filter(lambda x: x['pertenece'], particiones)))
                independientes = (list(filter(lambda x: not x['pertenece'], particiones)))
                
                # Unidos
                if len(a_unir):
                    transiciones = []
                    for elemento in a_unir:
                        estados_actuales.append(elemento['estado_actual'])
        
                        for entrada in self.simbolos_entrada:
                            transiciones.append({entrada: elemento[entrada]})
        
                    transiciones_simbolos = {}
                    for entrada in self.simbolos_entrada:
                        transiciones_por_simbolo = []
                        for (index_transicion, transicion) in enumerate(transiciones):
                            if entrada in transicion.keys():
                                transiciones_por_simbolo.append(transicion[entrada])
                        transiciones_simbolos.update({entrada: separador.join(sorted(set(transiciones_por_simbolo)))})
        
                    for fila in self.__filas_transiciones:
                        if len(a_unir):
                            if a_unir[0]['estado_actual'] == fila['estado_actual']:
                                aceptacion = fila['aceptacion']
                                break
        
                    nuevas_filas_transiciones.append({'estado_actual' : separador.join(estados_actuales), 'aceptacion' : aceptacion})
                    nuevas_filas_transiciones[-1].update(transiciones_simbolos)
        
                    
                #Independientes
                for independiente in independientes:
                    nueva_fila = {'estado_actual' : independiente['estado_actual']}
                    for entrada in self.simbolos_entrada:
                        nueva_fila.update({entrada : independiente[entrada]})
                    for fila in self.__filas_transiciones:
                        if independiente['estado_actual'] == fila['estado_actual']:
                            nueva_fila.update({'aceptacion' : fila['aceptacion']})
                            
                    nuevas_filas_transiciones.append(nueva_fila)
                    
                
                return nuevas_filas_transiciones
                
            ##################
            particiones = []
            relaciones = []
            buscar = list(map(lambda y : y['estado_actual'], grupo))
        
            for entrada in self.simbolos_entrada:
                filas_agrupadas = list(map(lambda x : list(map(lambda y : 
                                                        {'estado_actual': x['estado_actual'], entrada: y, 
                                                        'pertenece': y in buscar,}, x[entrada]))[0], grupo))
        
                
                particiones.append(filas_agrupadas)
                
                
            for particion in particiones:
                relaciones.append(list(map(lambda x: x['pertenece'], particion)))
        
            nuevas_particiones = []
            for (index_relacion, relacion) in enumerate(relaciones[0: -1]):
                for (index_item, item) in enumerate(relacion):
                    for particion in particiones:
                        particion[index_item]['pertenece'] = pertenece(index_relacion, index_item, relaciones, item)
                        if len(nuevas_particiones) > index_item:
                            if nuevas_particiones[index_item]['estado_actual'] == particion[index_item]['estado_actual']:
                                for entrada in self.simbolos_entrada:
                                    if entrada in particion[index_item].keys():
                                        nuevas_particiones[index_item].update({entrada: particion[index_item][entrada]})
                        else:
                            nuevas_particiones.append(particion[index_item])
            particiones = nuevas_particiones
            
            return unirEquivalentes(particiones)
            
        aceptados = list(filter(lambda x : x['aceptacion'], self.__filas_transiciones))
        no_aceptados = list(filter(lambda x : not x['aceptacion'], self.__filas_transiciones))
        
        nuevas_filas_estado = buscarGrupo(aceptados) + buscarGrupo(no_aceptados)
        
        
        for nueva_fila in nuevas_filas_estado:
            for fila in nuevas_filas_estado:
                for entrada in self.simbolos_entrada:
                    if fila[entrada] in nueva_fila['estado_actual']:
                        fila[entrada] = nueva_fila['estado_actual']
                        
                    if fila['estado_actual'] in nueva_fila['estado_actual']:
                        fila['estado_actual'] = nueva_fila['estado_actual']
                        
                    if fila['estado_actual'] in nueva_fila[entrada]:
                        fila['estado_actual'] = nueva_fila[entrada]

                    if separador.join(sorted(list(fila[entrada]) + list(set(nueva_fila['estado_actual']) - set(fila[entrada])))) == nueva_fila['estado_actual']:
                        fila[entrada] = nueva_fila['estado_actual']


            for (index_aceptacion, aceptacion) in enumerate(self.estados_aceptacion):
                if aceptacion in nueva_fila['estado_actual']:
                    self.estados_aceptacion[index_aceptacion] = nueva_fila['estado_actual']
                
            if self.estado_inicial in nueva_fila['estado_actual']:
                self.estado_inicial = nueva_fila['estado_actual']



        filas_estado_sin_duplicados = nuevas_filas_estado

        for (index_nueva, nueva_fila) in enumerate(nuevas_filas_estado):
            for (index_duplicado, duplicado) in enumerate(nuevas_filas_estado):
                if nueva_fila == duplicado and index_duplicado != index_nueva:
                    filas_estado_sin_duplicados.pop(index_duplicado)

        self.__filas_transiciones = filas_estado_sin_duplicados

        estados = []
        for fila in filas_estado_sin_duplicados:
            estados.append(fila['estado_actual'])

        self.estados = estados


    '''
    #Ejemplo
    0, a=0, b=3
    1, a=2, b=5
    2, a=2, b=7
    3, a=6, b=7
    4, a=1, b=6
    5, a=6, b=5
    6, a=6, b=3
    7, a=6, b=3

    ini: 0
    acep: 4,6

    # ND
    a, 0=a;c, 1=c
    b, 0=c, 1=b
    c, 0=b, 1=a;c
    d, 0=a;c, 1=d;b

    # D
    a, 0=a, 1=c
    b, 0=c, 1=b
    c, 0=b, 1=a
    d, 0=a, 1=d


    # D
    a, 0=a, 1=b
    b, 0=b, 1=a
    c, 0=c, 1=a
    '''
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
            self.__tablaPorDefecto()

        '''
        Inserta los datos por defecto que tendra la tabla de transiciones
        '''
        def __tablaPorDefecto(self):
            entradas = ['Estado']
            for entrada in self.__simbolos_entrada:
                entradas.append(str(entrada))
            entradas.append('Aceptacion')

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
            table = AsciiTable(self.__tabla_transiciones)
            print(str(table.table))

        '''
        Obtener la tabla de transiciones.

        @return Tabla de transiciones.
        '''
        def datosTransiciones(self):
            return self.__tabla_transiciones

        '''
        Limpia los datos de la tabla y la reestablece al estado por defecto
        '''
        def limpiarTabla(self):
            self.__tabla_transiciones.clear()
            self.__tablaPorDefecto()
