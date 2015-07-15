#!/usr/bin/python
# -*- coding: utf8 -*-
# Autores:
#   Bruno Faúndez Valenzuela
#   Jorge Martínez Martínez
#   Maximiliano Tapia Quiroz
# Descripción del código:
#   Este código implementa una clase para una Máquina de Turing y ejecuta pruebas
#   sobre cadenas para validarlas mediante la ejecución de transiciones que alcancen
#   un estado final.
# Licencia:
#   Este código se entrega con una licencia GNU GPL versión 3 que se adjunta
#   en un archivo LICENSE.
#   Se puede encontrar una copia de la licencia en http://www.gnu.org/licenses/gpl.html


import sys
from operator import itemgetter

# Nombre del archivo que especifica la Máquina de Turing y los casos a evaluar
inputFile = "entrada-prueba.txt"

class TuringMachine:
    def __init__(self, nstates, nsymbols, symbols):
        '''
        Clase para procesar una máquina de Turing.
        La máquina se inicializa con su cabezal en la posición en 0 y en el estado 0.
        La máquina se inicializa con una cinta vacía. La cinta se asigna con el método setTape().
        Parámetros:
            nstates: número de estados de la máquina sin contar el estado de término
            nsymbolos: número de símbolos del alfabeto de la máquina
            symbols: lista de símbolos de la máquina
        '''
        self.nstates = nstates
        self.nsymbols = nsymbols
        self.symbols = symbols
        self.transitions = []
        self.tape = []
        self.head = 0
        self.state = 0

    def setTape(self, tape):
        '''
        Se recibe una lista de caracteres y se asignan como cinta de la máquina.
        Se reinician la posición del cabezal y el estado.
        Parámetros:
            tape: lista con los caracteres de la cinta
        '''
        self.tape = tape.rstrip()
        self.head = 0
        self.state = 0

    def addTransition(self, transition):
        '''
        Se recibe una lista de caracteres representando una transición a añadir a la máquina.
        La lista de caracteres se añade a la lista transitions.
        Parámetros:
            transition: lista de caracteres representando una transición
        '''
        self.transitions.append(transition)
        self.sortTransitions()

    def sortTransitions(self):
        '''
        La lista de transiciones se ordena en base a los dos primeros campos: el estado y el símbolo leído.
        Parámetros:
            Este método no recibe ningún parámetro externo.
        '''
        self.transitions = sorted(self.transitions, key=itemgetter(0,1))

    def printTransitions(self):
        '''
        Se imprime la tabla de transiciones.
        Primero se imprime un formato y luego se imprimen las transiciones disponibles para cada estado.
        Parámetros:
            Este método no recibe ningún parámetro externo.
        '''
        print "> Tabla de Transiciones"
        fmt = '{:5s}  |' + '{:16s}\t|' * (self.nsymbols)
        print fmt.format("", *[' '*7+s for s in self.symbols])
        for i in range(self.nstates):
            tmp = []
            for j in range(self.nsymbols):
                transition = self.transitions[i*self.nsymbols+j][2:5]
                transition = ['%2s' % (t) for t in transition]
                tmp.append(transition)
            print fmt.format(str(i), *tmp)

    def checkAccepted(self):
        '''
        Se retorna True o False si la cadena es aceptada o rechazada por la Máquina de Turing. Se verifica el caracter de la cinta apuntado por el cabezal.
        Parámetros:
            Este método no recibe ningún parámetro externo.
        '''
        print ">>> Cinta resultante: %s\n>>> Posición del cabezal: %d" % (self.tape, self.head)
        if self.tape[self.head] == self.symbols[0]:
            return False
        else:
            return True

    def evaluate(self):
        '''
        Se evalúa la cinta, ejecutando todas las transiciones de la máquina. La función finaliza cuando se alcanza el estado -1.
        Parámetros:
            Este método no recibe ningún parámetro externo.
        '''
        while self.state != -1:
            # Se lee el caracter en la posición del cabezal y se obtiene su posición en la lista de símbolos de la máquina.
            tape = list(self.tape)
            char = tape[self.head]
            char_id = self.symbols.index(char)

            # Se obtiene la transición correspondiente al estado actual y al símbolo leído.
            transition = self.transitions[self.state*self.nsymbols+char_id][2:5]

            # Se escribe en la cinta el caracter correspondiente a la transición
            l_tape = list(self.tape)
            l_tape[self.head] = transition[0]
            self.tape = l_tape

            # Se ejecuta el movimiento correspondiente al cabeza.
            # Si se requiere extender la cinta, se le añaden caracteres vacíos antes del comienzo o después del final.
            mov = transition[1]
            if mov == 'd':
                self.head += 1
                if self.head == len(self.tape):
                    # Se añade un elemento por la derecha
                    self.tape.append(self.symbols[0])
            elif mov == 'i':
                self.head -= 1
                if self.head == -1:
                    # Se añade un elemento por la izquierda
                    self.tape = self.symbols[0] + self.tape
                    self.head = 0
            elif mov == 'q':
                pass

            # Se actualiza el estado actual de la máquina
            self.state = int(transition[2])

        # Habiendo llegado al estado de aceptación, se verifica si el
        # lenguaje es aceptado y se retorna el valor de aceptación
        return self.checkAccepted()

    def __str__(self):
        return "[Máquina de Turing]\n> Estados: %d\n> Símbolos: %d\n>> %s" % (self.nstates, self.nsymbols, self.symbols)

if __name__ == "__main__":
    '''
    Se lee el archivo de entrada especificado en la variable fileInput
    Se extraen los valores n y m para la cantidad de Estados y Símbolos respectivamente
    Se leen los símbolos
    '''
    file = open(inputFile, "r")
    buffer = file.readline().split()
    (n, m) = (int(buffer[0]), int(buffer[1]))
    symbols = file.readline().split()

    '''
    Se genera un objeto TuringMachine para encapsular las operaciones sobre la cinta
    y se imprime la configuración inicial de la máquina
    La máquina se inicializa con una cinta vacía
    '''
    machine = TuringMachine(n, m, symbols)
    print machine

    # Se añaden las m * n transiciones a la máquina y se imprime la tabla de transiciones
    for i in range(n*m):
        machine.addTransition(file.readline().split())
    machine.printTransitions()

    # Se lee la cantidad de casos a evaluar
    ntapes = int(file.readline())
    print "\n> %d casos disponibles" % (ntapes)
    for i in range(ntapes):
        # Se lee la cadena a validar y se imprime como una lista de caracteres
        tape = file.readline().rstrip()
        print ">> Caso %d" % (i+1)
        print ">>> Cadena de entrada: %s" % (list(tape))

        # Se le asigna la cinta a la máquina y se evalúa el lenguaje
        machine.setTape(tape)
        ret = machine.evaluate()

        # Se imprime el resultado de la evaluación de la cadena
        if ret:
            print ">>> [La cadena es aceptada]\n"
        else:
            print ">>> [La cadena no es aceptada]\n"

    file.close()
