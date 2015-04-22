# -*- coding: cp1252 -*-
# Archivo de clases
# Codificado por:
#           -Andres Mauricio Bejarano Posada
#           -Leyla Mlayes Haddad
#
# Para la solución de Sudokus desde el punto de vista de la Inteligencia
# Artificial, se requiere la implementación lógica de un entorno y un agente,
# para ello se codifican las clases Board (Entorno, que en nuestro caso es
# una matriz de 9 x 9) y Agent (Agente, el cual examina la posición de los
# números en la matriz para poder ubicar los números faltantes, cumpliendo con
# las reglas del juego del Sudoku).
#
# Tanto la clase Board como Agent solo poseen funciones de lectura, asignación
# y verificación, por lo tanto la lógica para la solución de Sudokus se
# encuentra en el programa principal (archivo main.py).
#
# Se utilizaron las siguientes convenciones de codificación para ambas clases:
#  1. Representación de datos booleanos: Todas las funciones booleanas son las
#     que inician con el prefijo "is". Estas devolveran 0 en caso de que la
#     respuesta sea false, y 1 en caso de que la respuesta sea true.
#  2. Dado que Python permite programar con el enfoque Orientado a Objetos,
#     utilizamos funciones para lectura y escritura sobre atributos de cada
#     clase, por tanto, todos los atributos se manejan de forma privada y todas
#     las funciones son del tipo público.
#  3. No se hace uso de librerias externas a las clásicas que vienen dentro del
#     paquete básico de Python, luego el programa debe funcionar correctamente
#     en cualquier computador que tenga instalado Python.
#


# Clase Board
#
# Hace de las veces del entorno. Es básicamente la representación lógica del
# Sudoku, por tanto se cuidó que solo tuviera las funciones que relacionan al
# agente con el tablero. Sus funciones fueron codificadas de tal forma que no
# fueran parte esencial de la lógica del programa (así como la solución de un
# Sudoku por una persona, la forma de llenar el tablero depende de la persona y
# no del Sudoku).
#
# Para poder generar el archivo con la solución paso a paso del Sudoku, se hace
# uso de una arreglo donde se van adicionando los valores a los que se le ha
# encontrado la ubicación exacta.

class Board:

    # Constructor de la clase. Recibe por parámetro la dirección donde se
    # encuentra el archivo que contiene al Sudoku, y se llena con los datos
    # encontrados.
    def __init__(self,path):
        self.Matrix = [["*"]*9 for i in range(9)]
        self.Original = [["*"]*9 for i in range(9)]
        self.Stack = [[0]*3 for i in range(81)]
        self.Top = -1
        self.BlankSpaces = 81
        self.Path = path
        self.SolutionPath = path
        if self.SolutionPath[len(self.SolutionPath) - 4:len(self.SolutionPath)] == ".txt":
            self.SolutionPath = self.SolutionPath[0:len(self.SolutionPath) - 4]
        InfoFile = open(path,"r")
        for i in range(9):
          linea = InfoFile.readline()
          for j in range(9):
            self.Matrix[i][j] = linea[2 * j]
            self.Original[i][j] = linea[2 * j]
            if self.Matrix[i][j] != "*":
                self.BlankSpaces = self.BlankSpaces - 1
        InfoFile.close()

    # Devuelve una copia de si mismo a otro apuntador del tipo Board
    def copy(self):
        Copy = Board(self.Path)
        for i in range(9):
            for j in range(9):
                Copy.setValueAt(i,j,self.Matrix[i][j])
        for i in range(self.Top + 1):
            Copy.inputStackValue(self.Stack[i][0],self.Stack[i][1],self.Stack[i][2])
        return Copy

    # Retorna el número indicado por la fila y columna ingresadas
    def getValueAt(self,row,column):
        return self.Matrix[row][column]

    # Ingresa un nuevo valor en el arreglo para la generación del archivo con la
    # solución paso a paso
    def inputStackValue(self,row,column,value):
        self.Top = self.Top + 1
        self.Stack[self.Top][0] = row
        self.Stack[self.Top][1] = column
        self.Stack[self.Top][2] = value
        self.BlankSpaces = self.BlankSpaces - 1

    # Pregunta si el número ingresado se encuentra en la fila indicada
    def isElementInRow(self,row,element):
        sw = 0
        i = 0
        while i < 9 and sw == 0:
            if self.Matrix[row][i] == element:
                sw = 1
            else:
                i = i + 1
        return sw

    # Pregunta si el número ingresado se encuentra en la columna indicada
    def isElementInColumn(self,column,element):
        sw = 0
        i = 0
        while i < 9 and sw == 0:
            if self.Matrix[i][column] == element:
                sw = 1
            else:
                i = i + 1
        return sw

    # Indica si el Soduko está solucionado, su respuesta se basa en el número de
    # casillas en blanco que halla en el tablero
    def isSolved(self):
        sw = 1
        i = 0
        while i < 9 and sw == 1:
            j = 0
            while j < 9 and sw == 1:
                if self.Matrix[i][j] == "*":
                    sw = 0
                else:
                    j = j + 1
            i = i + 1
        return sw

    # Imprime el tablero por pantalla
    def printMatrix(self):
        t = ""
        for i in range(9):
            t = t + "+---+---+---+---+---+---+---+---+---+\n"
            for j in range(9):
                if self.Matrix[i][j] == "*":
                    t = t + "|   "
                else:
                    t = t + "| " + str(self.Matrix[i][j]) + " "
            t = t + "|\n"
        t = t + "+---+---+---+---+---+---+---+---+---+\n"
        print t

    # Genera el archivo con la solución paso a paso. Toda solución tendrá el
    # nombre del archivo original concatenado con la palabra "Solution".
    # Ejemplo: Si el nombre es Sudoku1.txt, el archivo generado será
    # Sudoku1Solution.txt
    # La solución se guardará en la misma carpeta donde se encuentre el Sudoku
    # leido.
    def printSolution(self):
        InfoFile = open(self.SolutionPath + "Solution.txt","w")
        InfoFile.write("Solucion paso a paso\n")
        InfoFile.write("Solucion realizada por el algoritmo codificado por:\n")
        InfoFile.write("   ->Andres Mauricio Bejarano Posada\n   ->Leyla Mlayes Haddad\n")
        Letters = ["A","B","C","D","E","F","G","H","I"]
        i = 0
        while i <= self.Top:
            InfoFile.write("\n\n\n------------------------------------------\n")
            InfoFile.write("Numero adicionado: " + str(self.Stack[i][2]) + "\n")
            InfoFile.write("Posicion: " + Letters[self.Stack[i][0]] + str(self.Stack[i][1] + 1) + "\n\n")
            self.Original[self.Stack[i][0]][self.Stack[i][1]] = str(self.Stack[i][2])
            InfoFile.write("     1   2   3   4   5   6   7   8   9\n")
            InfoFile.write("   +---+---+---+---+---+---+---+---+---+\n")
            for j in range(9):
                InfoFile.write(" " + Letters[j] + " ")
                for k in range(9):
                    if self.Original[j][k] == "*":
                        InfoFile.write("|   ")
                    else:
                        InfoFile.write("| " + str(self.Original[j][k]) + " ")
                InfoFile.write("|\n")
                InfoFile.write("   +---+---+---+---+---+---+---+---+---+\n")
            i = i + 1
        InfoFile.close()

    # Ingresa un valor en la fila y columna indicada
    def setValueAt(self,row,column,value):
        self.Matrix[row][column] = value



# Clase Agent
#
# Hace de agente racional en el problema de la solucion de un Sudoku. Sus
# funciones están codificadas para que pueda responder a las fases definidas
# en el programa principal.
#
# El agente puede ser instanciado con un Sudoku en cualquie fase de resolución,
# lo cual no limita el alcance del agente en las diferentes fases codificadas
# en el algoritmo principal. Esto se hace con el fin de un correcto
# funcionamiento de la fase de multiplicidad mínima por suposición.
#
# El agente trabaja basado en proyecciones y expansiones las cuales son armadas
# en el algoritmo principal. La clase Agent como tal trabaja la carga de
# cuadrantes, filas y columnas, además es la que examina las proyecciones y
# determina cuales son los valores que deben incluirse en nel Sudoku. Estas
# funciones deben indicarse en la fase exacta, pues el comportamiento de como
# debe pensar el agente no esta implícito en la definición del comportamiento,
# sino en la lógica del procedimiento contenido en el programa principal.

class Agent:

    # Constructor de la clase. Recibe por parámetro el Sudoku que va a resolver.
    def __init__(self,Board):
        self.Enviroment = Board
        self.Quadrant = [["-"]*3 for i in range(3)]
        self.Vector = ["-"]*9
        self.SelectedQuadrant = 0
        self.SelectedRow = 0
        self.SelectedColumn = 0

    #Carga el cuadrante indicado
    def loadQuadrant(self,Number):
        self.SelectedQuadrant = Number
        for i in range(3):
            for j in range(3):
                if Number == 1:
                    self.Quadrant[i][j] = self.Enviroment.getValueAt(i,j)
                elif Number == 2:
                    self.Quadrant[i][j] = self.Enviroment.getValueAt(i,j + 3)
                elif Number == 3:
                    self.Quadrant[i][j] = self.Enviroment.getValueAt(i,j + 6)
                elif Number == 4:
                    self.Quadrant[i][j] = self.Enviroment.getValueAt(i + 3,j)
                elif Number == 5:
                    self.Quadrant[i][j] = self.Enviroment.getValueAt(i + 3,j + 3)
                elif Number == 6:
                    self.Quadrant[i][j] = self.Enviroment.getValueAt(i + 3,j + 6)
                elif Number == 7:
                    self.Quadrant[i][j] = self.Enviroment.getValueAt(i + 6,j)
                elif Number == 8:
                    self.Quadrant[i][j] = self.Enviroment.getValueAt(i + 6,j + 3)
                else:
                    self.Quadrant[i][j] = self.Enviroment.getValueAt(i + 6,j + 6)

    #Indica si el numero ingresado se encuentra en el cuadrante
    def isElementInQuadrant(self,number):
        sw = 0
        for i in range(3):
            for j in range(3):
                if self.Quadrant[i][j] == number:
                    sw = 1
        return sw

    #Escribe el cuadrante por pantalla
    def printQuadrant(self):
        t = "|"
        for i in range(3):
            for j in range(3):
                t = t + str(self.Quadrant[i][j]) + "|"
            t = t + "\n"
        print t

    #Llena la fila indicada del cuadrante con afirmaciones (!)
    def fillQuadrantRow(self,Row):
        for i in range(3):
            if self.Quadrant[Row][i] == "*":
                self.Quadrant[Row][i] = "!"

    #Llena la columna indicada del cuadrante con admiraciones (!)
    def fillQuadrantColumn(self,Column):
        for i in range(3):
            if self.Quadrant[i][Column] == "*":
                self.Quadrant[i][Column] = "!"

    #Limpia el cuadrante de símbolos
    def clearQuadrant(self):
        for i in range(3):
            for j in range(3):
                if  self.Quadrant[i][j] == "!":
                    self.Quadrant[i][j] = "*"
                elif self.Quadrant[i][j][0] == "*" and len(self.Quadrant[i][j]) > 1:
                    self.Quadrant[i][j] = "*"

    #Cuenta los guiones que hayan en el cuadrante
    def countQuadrantDash(self):
        cont = 0
        for i in range(3):
            for j in range(3):
                if self.Quadrant[i][j] == "*":
                    cont = cont + 1
        return cont

    #Busca donde se encuentre el guion (-) y coloca el numero ingresado
    def writeNumberInQuadrant(self,Number):
        i = 0
        sw = 0
        while i < 3 and sw == 0:
            j = 0
            while j < 3 and sw == 0:
                if self.Quadrant[i][j] == "*":
                    self.Quadrant[i][j] = Number
                    sw = 1
                    if self.SelectedQuadrant == 1:
                        self.Enviroment.inputStackValue(i,j,int(Number))
                    elif self.SelectedQuadrant == 2:
                        self.Enviroment.inputStackValue(i,j + 3,int(Number))
                    elif self.SelectedQuadrant == 3:
                        self.Enviroment.inputStackValue(i,j + 6,int(Number))
                    elif self.SelectedQuadrant == 4:
                        self.Enviroment.inputStackValue(i + 3,j,int(Number))
                    elif self.SelectedQuadrant == 5:
                        self.Enviroment.inputStackValue(i + 3,j + 3,int(Number))
                    elif self.SelectedQuadrant == 6:
                        self.Enviroment.inputStackValue(i + 3,j + 6,int(Number))
                    elif self.SelectedQuadrant == 7:
                        self.Enviroment.inputStackValue(i + 6,j,int(Number))
                    elif self.SelectedQuadrant == 8:
                        self.Enviroment.inputStackValue(i + 6,j + 3,int(Number))
                    else:
                        self.Enviroment.inputStackValue(i + 6,j + 6,int(Number))
                else:
                    j = j + 1
            i = i + 1

    #Aplica los cambios hechos en el cuadrante al Sudoku
    def applyQuadrant(self):
        for i in range(3):
            for j in range(3):
                if self.SelectedQuadrant == 1:
                    self.Enviroment.setValueAt(i,j,self.Quadrant[i][j])
                elif self.SelectedQuadrant == 2:
                    self.Enviroment.setValueAt(i,j+3,self.Quadrant[i][j])
                elif self.SelectedQuadrant == 3:
                    self.Enviroment.setValueAt(i,j+6,self.Quadrant[i][j])
                elif self.SelectedQuadrant == 4:
                    self.Enviroment.setValueAt(i+3,j,self.Quadrant[i][j])
                elif self.SelectedQuadrant == 5:
                    self.Enviroment.setValueAt(i+3,j+3,self.Quadrant[i][j])
                elif self.SelectedQuadrant == 6:
                    self.Enviroment.setValueAt(i+3,j+6,self.Quadrant[i][j])
                elif self.SelectedQuadrant == 7:
                    self.Enviroment.setValueAt(i+6,j,self.Quadrant[i][j])
                elif self.SelectedQuadrant == 8:
                    self.Enviroment.setValueAt(i+6,j+3,self.Quadrant[i][j])
                else:
                    self.Enviroment.setValueAt(i+6,j+6,self.Quadrant[i][j])

    #Hace las proyecciones sobre el cuadrante con respecto al numero ingresado
    def proyectQuadrant(self,Number):
        for i in range(3):
            if self.SelectedQuadrant == 1:
                if self.Enviroment.isElementInRow(i,Number):
                    self.fillQuadrantRow(i)
                if self.Enviroment.isElementInColumn(i,Number):
                    self.fillQuadrantColumn(i)
            elif self.SelectedQuadrant == 2:
                if self.Enviroment.isElementInRow(i,Number):
                    self.fillQuadrantRow(i)
                if self.Enviroment.isElementInColumn(i+3,Number):
                    self.fillQuadrantColumn(i)
            elif self.SelectedQuadrant == 3:
                if self.Enviroment.isElementInRow(i,Number):
                    self.fillQuadrantRow(i)
                if self.Enviroment.isElementInColumn(i+6,Number):
                    self.fillQuadrantColumn(i)
            elif self.SelectedQuadrant == 4:
                if self.Enviroment.isElementInRow(i+3,Number):
                    self.fillQuadrantRow(i)
                if self.Enviroment.isElementInColumn(i,Number):
                    self.fillQuadrantColumn(i)
            elif self.SelectedQuadrant == 5:
                if self.Enviroment.isElementInRow(i+3,Number):
                    self.fillQuadrantRow(i)
                if self.Enviroment.isElementInColumn(i+3,Number):
                    self.fillQuadrantColumn(i)
            elif self.SelectedQuadrant == 6:
                if self.Enviroment.isElementInRow(i+3,Number):
                    self.fillQuadrantRow(i)
                if self.Enviroment.isElementInColumn(i+6,Number):
                    self.fillQuadrantColumn(i)
            elif self.SelectedQuadrant == 7:
                if self.Enviroment.isElementInRow(i+6,Number):
                    self.fillQuadrantRow(i)
                if self.Enviroment.isElementInColumn(i,Number):
                    self.fillQuadrantColumn(i)
            elif self.SelectedQuadrant == 8:
                if self.Enviroment.isElementInRow(i+6,Number):
                    self.fillQuadrantRow(i)
                if self.Enviroment.isElementInColumn(i+3,Number):
                    self.fillQuadrantColumn(i)
            else:
                if self.Enviroment.isElementInRow(i+6,Number):
                    self.fillQuadrantRow(i)
                if self.Enviroment.isElementInColumn(i+6,Number):
                    self.fillQuadrantColumn(i)

    # Carga la fila indicada en el vector
    def loadRow(self,Number):
        self.SelectedRow = Number
        for i in range(9):
            self.Vector[i] = self.Enviroment.getValueAt(Number,i)

    # Carga la columna indicada en el vector
    def loadColumn(self,Number):
        self.SelectedColumn = Number
        for i in range(9):
            self.Vector[i] = self.Enviroment.getValueAt(i,Number)

    # Indica si el elemento ingresado se encuentra en el vector
    def isElementInVector(self,Number):
        sw = 0
        i = 0
        while sw == 0 and i < 9:
            if self.Vector[i] == Number:
                sw = 1
            else:
                i = i+1
        return sw

    # Aplica el vector a la solución del Sudoku como fila
    def applyRow(self):
        for i in range(9):
            self.Enviroment.setValueAt(self.SelectedRow,i,self.Vector[i])

    # Aplica el vector a la solución del Sudoku como columna
    def applyColumn(self):
        for i in range(9):
            self.Enviroment.setValueAt(i,self.SelectedColumn,self.Vector[i])

    # Cuenta el número de "-" que hay en el vector
    def countVectorDash(self):
        cont = 0
        for i in range(9):
            if self.Vector[i] == "*":
                cont = cont + 1
        return cont

    # Limpia el vector
    def clearVector(self):
        for i in range(9):
            if self.Vector[i] == "!":
                self.Vector[i] = "*"

    # Ingresa el numero ingresado en el vector, si es 0 el vector se comporta
    # como una fila, si es 1 se comporta como una columna
    def writeNumberInVector(self,Number,value):
        sw = 0
        i = 0
        while sw == 0:
            if self.Vector[i] == "*":
                self.Vector[i] = Number
                sw = 1
                if value == 0:
                    self.Enviroment.inputStackValue(self.SelectedRow,i,int(Number))
                else:
                    self.Enviroment.inputStackValue(i,self.SelectedColumn,int(Number))
            else:
                i = i + 1

    # Llena el sector indicado con "!"
    def fillVector(self,Sector):
        if Sector == 1:
            for i in range(3):
                if self.Vector[i] == "*":
                    self.Vector[i] = "!"
        elif Sector == 2:
            for i in range(3):
                if self.Vector[i+3] == "*":
                    self.Vector[i+3] = "!"
        else:
            for i in range(3):
                if self.Vector[i+6] == "*":
                    self.Vector[i+6] = "!"

    # Realiza la proyección del Sudoku sobre la fila almacenada en el vector
    def proyectRow(self,Number):
        for i in range(9):
            if self.Vector[i] == "*" and self.Enviroment.isElementInColumn(i,Number):
                self.Vector[i] = "!"
        if self.SelectedRow == 0 or self.SelectedRow == 1 or self.SelectedRow == 2:
            for i in range(3):
                self.loadQuadrant(i+1)
                if self.isElementInQuadrant(Number):
                    self.fillVector(i+1)
        elif self.SelectedRow == 3 or self.SelectedRow == 4 or self.SelectedRow == 5:
            for i in range(3):
                self.loadQuadrant(i+4)
                if self.isElementInQuadrant(Number):
                    self.fillVector(i+1)
        else:
            for i in range(3):
                self.loadQuadrant(i+7)
                if self.isElementInQuadrant(Number):
                    self.fillVector(i+1)

    # Realiza la proyección del Sudoku sobre la columna almacenada en el vector
    def proyectColumn(self,Number):
        for i in range(9):
            if self.Vector[i] == "*" and self.Enviroment.isElementInRow(i,Number):
                self.Vector[i] = "!"
        if self.SelectedColumn == 0 or self.SelectedColumn == 1 or self.SelectedColumn == 2:
            for i in range(3):
                self.loadQuadrant(3*i+1)
                if self.isElementInQuadrant(Number):
                    self.fillVector(i+1)
        elif self.SelectedColumn == 3 or self.SelectedColumn == 4 or self.SelectedColumn == 5:
            for i in range(3):
                self.loadQuadrant(3*i+2)
                if self.isElementInQuadrant(Number):
                    self.fillVector(i+1)
        else:
            for i in range(3):
                self.loadQuadrant(3*i+3)
                if self.isElementInQuadrant(Number):
                    self.fillVector(i+1)

    # Expande el cuadrante de acuerdo al número ingresado
    def expand(self,Number):
        for i in range(3):
            for j in range(3):
                if self.Quadrant[i][j][0] == "*":
                    if self.SelectedQuadrant == 1:
                        if self.Enviroment.isElementInRow(i,Number) == 0 and self.Enviroment.isElementInColumn(j,Number) == 0:
                            self.Quadrant[i][j] = self.Quadrant[i][j] + Number
                    elif self.SelectedQuadrant == 2:
                        if self.Enviroment.isElementInRow(i,Number) == 0 and self.Enviroment.isElementInColumn(j+3,Number) == 0:
                            self.Quadrant[i][j] = self.Quadrant[i][j] + Number
                    elif self.SelectedQuadrant == 3:
                        if self.Enviroment.isElementInRow(i,Number) == 0 and self.Enviroment.isElementInColumn(j+6,Number) == 0:
                            self.Quadrant[i][j] = self.Quadrant[i][j] + Number
                    elif self.SelectedQuadrant == 4:
                        if self.Enviroment.isElementInRow(i+3,Number) == 0 and self.Enviroment.isElementInColumn(j,Number) == 0:
                            self.Quadrant[i][j] = self.Quadrant[i][j] + Number
                    elif self.SelectedQuadrant == 5:
                        if self.Enviroment.isElementInRow(i+3,Number) == 0 and self.Enviroment.isElementInColumn(j+3,Number) == 0:
                            self.Quadrant[i][j] = self.Quadrant[i][j] + Number
                    elif self.SelectedQuadrant == 6:
                        if self.Enviroment.isElementInRow(i+3,Number) == 0 and self.Enviroment.isElementInColumn(j+6,Number) == 0:
                            self.Quadrant[i][j] = self.Quadrant[i][j] + Number
                    elif self.SelectedQuadrant == 7:
                        if self.Enviroment.isElementInRow(i+6,Number) == 0 and self.Enviroment.isElementInColumn(j,Number) == 0:
                            self.Quadrant[i][j] = self.Quadrant[i][j] + Number
                    elif self.SelectedQuadrant == 8:
                        if self.Enviroment.isElementInRow(i+6,Number) == 0 and self.Enviroment.isElementInColumn(j+3,Number) == 0:
                            self.Quadrant[i][j] = self.Quadrant[i][j] + Number
                    else:
                        if self.Enviroment.isElementInRow(i+6,Number) == 0 and self.Enviroment.isElementInColumn(j+6,Number) == 0:
                            self.Quadrant[i][j] = self.Quadrant[i][j] + Number

    # Obtiene el valor del cuadrante en la fila y columna indicada
    def getQuadrantValueAt(self,row,column):
        return self.Quadrant[row][column]

    # Asigna un valor en el cuadrante con la fila y columna indicada
    def setQuadrantValueAt(self,row,column,Number):
        self.Quadrant[row][column] = Number
        if self.SelectedQuadrant == 1:
            self.Enviroment.inputStackValue(row,column,int(Number))
        elif self.SelectedQuadrant == 2:
            self.Enviroment.inputStackValue(row,column + 3,int(Number))
        elif self.SelectedQuadrant == 3:
            self.Enviroment.inputStackValue(row,column + 6,int(Number))
        elif self.SelectedQuadrant == 4:
            self.Enviroment.inputStackValue(row + 3,column,int(Number))
        elif self.SelectedQuadrant == 5:
            self.Enviroment.inputStackValue(row + 3,column + 3,int(Number))
        elif self.SelectedQuadrant == 6:
            self.Enviroment.inputStackValue(row + 3,column + 6,int(Number))
        elif self.SelectedQuadrant == 7:
            self.Enviroment.inputStackValue(row + 6,column,int(Number))
        elif self.SelectedQuadrant == 8:
            self.Enviroment.inputStackValue(row + 6,column + 3,int(Number))
        else:
            self.Enviroment.inputStackValue(row + 6,column + 6,int(Number))
