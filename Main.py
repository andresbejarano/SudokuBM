# -*- coding: cp1252 -*-
# Solucionador de Sudokus
# Codificado por:
#        -Andres Mauricio Bejarano Posada
#        -Leyla Mlayes Haddad
# Fecha: Segundo Semestre de 2007
# Materia: Inteligencia Artificial
# Profesor: Eduardo Zurek, Ph.D.
# Departamento de Ingeniería de Sistemas
# Universidad del Norte, Barranquilla, Colombia
# http://www.uninorte.edu.co
# http://www.eduardo-zurek.blogspot.com
#
# Este programa soluciona Sudokus de cualquier dificultad, para solucionarlos se
# basa en cuatro fases:
#
#  1. Proyección sobre cuadrantes: Los tablero de Sudokus normales están
#     compuestos por un tablero de 9 x 9 celdas, lo cual genera 9 cuadrantes
#     de 3 x 3 celdas cada uno. La proyección sobre cuadrantes consiste en
#     revisar, cuadrante por cuadrante, los valores que pueden ser colocados,
#     considerando los cuadrantes vecinos horizontales y verticales.
#
#       1   2   3   4   5   6   7   8   9    Un número que se encuentre en un
#     +---+---+---+---+---+---+---+---+---+  cuadrante no puede repetirse en
#   A | 1 |   | 9 |   |   |   | 2 |   | 8 |  dicho cuadrante, lo mismo sucede
#     +---+---+---+---+---+---+---+---+---+  si el número está en una fila o
#   B |   |   |   | 9 |   |   | 3 |   |   |  columna.
#     +---+---+---+---+---+---+---+---+---+
#   C |   | 4 |   | 6 |   |   | 5 | 1 |   |  Ejemplo:
#     +---+---+---+---+---+---+---+---+---+  
#   D |   |   | 3 | 7 | 2 |   |   |   | 6 |  Analizando el tercer cuadrante
#     +---+---+---+---+---+---+---+---+---+  (Filas A, B y C, columnas 7,8 y 9),
#   E |   |   |   |   |   |   |   |   |   |  el 9 no puede ir en las filas A y
#     +---+---+---+---+---+---+---+---+---+  B, luego la única posición del 9 en
#   F | 8 |   |   |   | 4 | 6 | 9 |   |   |  este cuadrante es en la celda C9.
#     +---+---+---+---+---+---+---+---+---+
#   G |   | 5 | 2 |   |   | 9 |   | 7 |   |  Este mismmo caso sucede en el
#     +---+---+---+---+---+---+---+---+---+  séptimo cuadrante (Filas G, H e I,
#   H |   |   | 1 |   |   | 7 |   |   |   |  columnas 1,2 y 3), el número 7 no
#     +---+---+---+---+---+---+---+---+---+  puede ir en las filas G y H, luego
#   I | 9 |   | 6 |   |   |   | 1 |   | 3 |  la única posición válida para este
#     +---+---+---+---+---+---+---+---+---+  número es la celda I2.
#
#
#  2. Proyección sobre filas y columnas: Hay ocasiones en que es posible
#     determinar la ubicación de un número verificando solamente las filas y
#     las columnas sin importar el cuadrante en que se encuentre o abarque. A
#     menudo se presentan casos en donde en una fila o columna solo falta un
#     número, si hacemos caso a la regla de que un número solo uede estar
#     contenido una sola vez en una fila o columna, podemos asegurar que valor
#     es el que debe ir en la posición vacia. Este caso se puede expandir al
#     caso de que hayan dos o más celdas vacias, haciendo proyección del Sudoku
#                                            sobre la fila o columna, es posible
#       1   2   3   4   5   6   7   8   9    determinar que valores se pueden
#     +---+---+---+---+---+---+---+---+---+  ubicar.
#   A |   | 1 |   |   | 3 |   | 9 |   |   |  
#     +---+---+---+---+---+---+---+---+---+  Ejemplo:
#   B | 3 | 8 |   |   | 2 | 9 | 1 |   |   |  
#     +---+---+---+---+---+---+---+---+---+  Ubicandonos en la fila H podemos
#   C |   |   | 4 |   | 1 | 8 | 7 | 2 | 3 |  observar que no podemos ubicar el
#     +---+---+---+---+---+---+---+---+---+  9 en las columnas 6 y 7, lo que
#   D | 4 |   |   | 9 |   | 3 |   | 1 |   |  nos garantiza que el 9 va ubicado
#     +---+---+---+---+---+---+---+---+---+  en la celda H1.
#   E | 1 |   |   |   |   |   |   |   | 4 |  
#     +---+---+---+---+---+---+---+---+---+  Otro caso lo podemos ver si
#   F | 8 |   |   | 2 | 4 | 1 |   |   | 7 |  analizamos la columna 7, no podemos
#     +---+---+---+---+---+---+---+---+---+  ubicar el 4 en las celdas D7, E7 y
#   G |   | 2 | 1 | 3 |   |   | 8 |   |   |  F7 ya que en dicho cuadrante se
#     +---+---+---+---+---+---+---+---+---+  encuentra el 4, lo que nos reduce
#   H |   | 4 | 8 | 1 | 5 |   |   | 3 | 2 |  el problema a revisar las celdas
#     +---+---+---+---+---+---+---+---+---+  H7 e I7, sin embargo, el 4 ya está
#   I |   | 3 | 6 |   |   | 2 |   | 7 | 1 |  en la fila H, luego podemos colocar
#     +---+---+---+---+---+---+---+---+---+  el número 4 en la celda I7.
#
#
#  3. Proyección expansiva: Una de las formas clásicas para resolver un Sudoku
#     es mirar los posibles números que una celda puede tomar. Esta técnica nos
#     permite identificar aquellas celdas donde solo existe la posibilidad de
#     que un solo número pueda ser ubicado. Lo que se hace es recorrer cuadrante
#     por cuadrante y verificar cuales son los posibles candidatos de las celdas
#     vacias. Cuando encontremos una celda con un solo candidato podemos 
#                                            asegurar que ese número es el que
#       1   2   3   4   5   6   7   8   9    va en dicha celda.
#     +---+---+---+---+---+---+---+---+---+  
#   A | 1 | 3 | 8 |   | 5 | 7 |   |   | 4 |  
#     +---+---+---+---+---+---+---+---+---+  
#   B |   | 7 | 4 | 1 | 6 | 3 |   | 8 |   |  Ejemplo:
#     +---+---+---+---+---+---+---+---+---+  
#   C |   |   |   |   | 8 | 4 | 1 | 7 | 3 |  Analizando el primer cuadrante,   
#     +---+---+---+---+---+---+---+---+---+  expandemos las celdas vacias, el   
#   D | 3 | 5 | 7 | 4 | 1 | 8 | 2 |   |   |  resultado nos arroja los   
#     +---+---+---+---+---+---+---+---+---+  siguientes candidatos:   
#   E |   |   |   | 3 | 2 | 9 |   | 4 |   |     
#     +---+---+---+---+---+---+---+---+---+     B1: 2,5,9
#   F | 4 | 9 | 2 | 5 | 7 | 6 | 3 | 1 | 8 |     C1: 2,5,6,9
#     +---+---+---+---+---+---+---+---+---+     C2: 2
#   G |   | 6 | 3 | 7 | 4 |   |   |   | 1 |     C3: 5,6,9
#     +---+---+---+---+---+---+---+---+---+     
#   H |   | 4 |   |   | 3 | 1 |   |   |   |  El resultado de la expansión nos
#     +---+---+---+---+---+---+---+---+---+  arroja que en la casilla C2 solo
#   I | 7 |   |   |   | 9 |   | 4 | 3 |   |  puede estar el 2, luego ese es el
#     +---+---+---+---+---+---+---+---+---+  número que va en dicha casilla
#
#
#  4. Multiplicidad mínima por suposición: En algunas ocasiones es imposible
#     solucionar un Sudoku usando solamente las técnicas antes listadas, un
#     ejemplo es cuando en cada casilla vacia se pueda colocar más de un número,
#     en estos casos se debe realizar suposiciones para poder seguir en la
#     solución, el problema radica en que si se escoge una celda con varias
#     posibilidades, el problema se multiplicará tantas veces como posibilidades
#     halla, por eso se escoge la celda con la menor cantidad de suposiciones
#     posibles, y se crean nuevos tableros tantas posibilidades hayan.
#
#       1   2   3   4   5   6   7   8   9    Ejemplo:
#     +---+---+---+---+---+---+---+---+---+  
#   A | 1 |   |   |   |   | 7 |   | 9 |   |  En este Sudoku, no se pueden
#     +---+---+---+---+---+---+---+---+---+  emplear las técnicas antes vistas,
#   B |   | 3 |   |   | 2 |   |   |   | 8 |  es necesario conocer aquellas
#     +---+---+---+---+---+---+---+---+---+  celdas donde se puedan ubicar la
#   C |   |   | 9 | 6 |   |   | 5 |   |   |  menor cantidad de números posibles,
#     +---+---+---+---+---+---+---+---+---+  en este caso, las únicas celdas con
#   D |   |   | 5 | 3 |   |   | 9 |   |   |  dos posibilidades son B3 y E3. La
#     +---+---+---+---+---+---+---+---+---+  escogencia de cual de las dos
#   E |   | 1 |   |   | 8 |   |   |   | 2 |  celdas se debe suponer puede llegar
#     +---+---+---+---+---+---+---+---+---+  a ser un problema de complejidad
#   F | 6 |   |   |   |   | 4 |   |   |   |  alta. 
#     +---+---+---+---+---+---+---+---+---+     
#   G | 3 |   |   |   |   |   |   | 1 |   |  La respuesta en este paso es que   
#     +---+---+---+---+---+---+---+---+---+  se van a generar dos nuevos   
#   H |   | 4 | 1 |   |   |   |   |   | 7 |  Sudokus, cada uno con uno de los
#     +---+---+---+---+---+---+---+---+---+  valores posibles en la celda
#   I |   |   | 7 |   |   |   | 3 |   |   |  escogida, y nuevamente se repite el
#     +---+---+---+---+---+---+---+---+---+  proceso desde la primera fase.
#
# Estas cuatro técnicas utilizadas se fusionan de tal forma que pueden dar
# solución a cualquier Sudoku. Por la estructura utilizada en cada fase, se
# plantea cada técnica a bases de busquedas cuyas soluciones cumplan el criterio
# establecido por las reglas de los Sudokus. Para la última fase se realizan
# tanto búsquedas como inferencias (la información obtenida es insuficiente
# para poder dar una solución concreta). lo ideal es que el programa no tenga
# que hacer uso de la última fase (pues aumenta la complejidad del problema),
# sin embargo, el uso correcto de esta técnica facilita enormemente la solución
# de este tipo de problemas ya que las inferencias estarán basadas en casos
# mínimos que generaran una cantidad de variantes mínimas del problema.
#
# Ejemplos de direcciones válidas para el ingreso del archivo:
#   Windows: C:\Documents and Settings\Usuario\Mis documentos\Sudoku1.txt
#   Linux: /home/Usuario/Archivos/Sudoku1.txt
#


from Classes import *

FileName = raw_input("Ingrese la direccion del archivo: ")
Sudokus = [Board(FileName)]
loop = 1
clear = 0
swIV = 1
Solve = 0
print "Calculando, por favor espere..."

while loop == 1 and clear == 0:
    loop = 0
    if swIV == 1:
        if len(Sudokus) == 0:
            loop = 0
            clear = 1
            Solve = 0
        else:
            Sudoku = Sudokus.pop()
            print Sudoku
            Solver = Agent(Sudoku)
            swIV = 0
    #Fase I: Proyeccion sobre cuadrantes
    for i in range(9):
        Solver.loadQuadrant(i + 1)
        for j in range(9):
            if Solver.isElementInQuadrant(str(j + 1)) == 0:
                Solver.proyectQuadrant(str(j + 1))
                if Solver.countQuadrantDash() == 1:
                    Solver.writeNumberInQuadrant(str(j + 1))
                    loop = 1
                Solver.clearQuadrant()
            Solver.applyQuadrant()



    clear = Sudoku.isSolved()
    if clear == 0:
        #Fase II-A: Proyeccion sobre filas
        for i in range(9):
            Solver.loadRow(i)
            for j in range(9):
                if Solver.isElementInVector(str(j + 1)) == 0:
                    Solver.proyectRow(str(j + 1))
                    if Solver.countVectorDash() == 1:
                        Solver.writeNumberInVector(str(j + 1),0)
                        loop = 1
                    Solver.clearVector()
                Solver.applyRow()
    else:
        Solve = 1



    clear = Sudoku.isSolved()
    if clear == 0:
        #Fase II-B: Proyeccion sobre columnas
        for i in range(9):
            Solver.loadColumn(i)
            for j in range(9):
                if Solver.isElementInVector(str(j + 1)) == 0:
                    Solver.proyectColumn(str(j + 1))
                    if Solver.countVectorDash() == 1:
                        Solver.writeNumberInVector(str(j + 1),1)
                        loop = 1
                    Solver.clearVector()
                Solver.applyColumn()
    else:
        Solve = 1



    clear = Sudoku.isSolved()
    if clear == 0:
        #Fase III: Proyeccion expansiva
        for i in range(9):
            Solver.loadQuadrant(i + 1)
            for j in range(9):
                if Solver.isElementInQuadrant(str(j + 1)) == 0:
                    Solver.expand(str(j + 1))
            for j in range(3):
                for k in range(3):
                    if len(Solver.getQuadrantValueAt(j,k)) == 2:
                        Solver.setQuadrantValueAt(j,k,Solver.getQuadrantValueAt(j,k)[1])
                        loop = 1
            Solver.clearQuadrant()
            Solver.applyQuadrant()
    else:
        Solve = 1



    clear = Sudoku.isSolved()
    if loop == 0 and clear == 0:
        #Fase IV: Multiplicidad minima por supocision
        loop = 1
        swIV = 1
        row = 0
        column = 0
        cant = 9
        for i in range(9):
            Solver.loadQuadrant(i + 1)
            for j in range(9):
                if Solver.isElementInQuadrant(str(j + 1)) == 0:
                    Solver.expand(str(j + 1))
            for j in range(3):
                for k in range(3):
                    if len(Solver.getQuadrantValueAt(j,k)) > 2 and len(Solver.getQuadrantValueAt(j,k)) < cant:
                        serie = Solver.getQuadrantValueAt(j,k)
                        cant = len(serie)
                        row = j
                        column = k
                        if i == 1:
                            column = column + 3
                        elif i == 2:
                            column = column + 6
                        elif i == 3:
                            row = row + 3
                        elif i == 4:
                            row = row + 3
                            column = column + 3
                        elif i == 5:
                            row = row + 3
                            column = column + 6
                        elif i == 6:
                            row = row + 6
                        elif i == 7:
                            row = row + 6
                            column = column + 3
                        elif i == 8:
                            row = row + 6
                            column = column + 6
        if cant < 9:
            i = 1
            while i < cant:
                Copia = Sudoku.copy()
                Copia.setValueAt(row,column,serie[i])
                Copia.inputStackValue(row,column,int(serie[i]))
                Sudokus.append(Copia)
                i = i + 1

if Solve == 0:
    print "El Sudoku ingresado no tiene solucion."
else:
    Sudoku.printMatrix()
    Sudoku.printSolution()
    cadena = "La solucion paso a paso esta registrada en el archivo "
    cadena = cadena + FileName[0:len(FileName) - 4] + "Solution.txt"
    print cadena
