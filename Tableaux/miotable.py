# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 18:03:56 2020

@author: Daniel
"""
#-*-coding: utf-8-*-
from random import choice
##############################################################################
# Variables globales
##############################################################################

# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listaHojas = []

##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
    def __init__(self, label, left, right):
        self.left = left
        self.right = right
        self.label = label

def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula
    if f.right == None:
        return f.label
    elif f.label == '-':
        return f.label + Inorder(f.right)
    else:
        return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def StringtoTree(A):
    # Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
    # Input: A, lista de caracteres con una formula escrita en notacion polaca inversa
             # letrasProposicionales, lista de letras proposicionales
    # Output: formula como tree

# OJO: DEBE INCLUIR SU CÓDIGO DE STRING2TREE EN ESTA PARTE!!!!!

    p = letrasProposicionales[0] # ELIMINE ESTA LINEA LUEGO DE INCLUIR EL CODIGO DE STRING2TREE
    return Tree(p, None, None) # ELIMINE ESTA LINEA LUEGO DE INCLUIR EL CODIGO DE STRING2TREE

##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
    cadena = "{"
    primero = True
    for f in H:
        if primero == True:
            primero = False
        else:
            cadena += ", "
            cadena += Inorder(f)
        return cadena + "}"

def par_complementario(l):
    # Esta función determina si una lista de solo literales
# contiene un par complementario
# Input: l, una lista de literales
# Output: True/False
    lista_literales=[]
    for literal in l:
        if literal.label != '-':
            if literal.label in lista_literales:
                return True
            else:
                lista_literales.append(literal.label)
        else:
            if literal.right.label in lista_literales:
                return True
            else:
                lista_literales.append(literal.right.label)
    return False        
            
def es_literal(f):
# Esta función determina si el árbol f es un literal
# Input: f, una fórmula como árbol
# Output: True/False
    if f.label in letrasProposicionales:
        return True
    elif f.label == '-':
        hoja = f.right
        if hoja.label in letrasProposicionales:
            return True
        else:
            return False
    else:
        return False


def no_literales(l):
# Esta función determina si una lista de fórmulas contiene
# solo literales
# Input: l, una lista de fórmulas como árboles
# Output: None/f, tal que f no es literal
    for formula in l:
        if es_literal(formula) == False:
            return 'f'
    return None
        
        

def clasifica_y_extiende(f):
# clasifica una fórmula como alfa o beta y extiende listaHojas
# de acuerdo a la regla respectiva
# Input: f, una fórmula como árbol
# Output: no tiene output, pues modifica la variable global listaHojas
    global listaHojas
    if es_literal(f) == False:
        if f.label == '-':
            if f.right.label == '-':
                listaHojas.remove(f)
                listaHojas.append(f.right.right)
                print("1ALPHA")
            elif f.right.label == 'O':
                listaHojas.remove(f)
                listaHojas.append([Tree('-',None,f.right.left),Tree('-',None,f.right.right)])
                print("3ALPHA")
            elif f.right.label == "->":
                listaHojas.remove(f)
                listaHojas.append([f.right.left,Tree('-',None,f.right.right)])
                print("4ALPHA")
            else:
                listaHojas.remove(f)
                listaHojas.append([Tree('-',None,f.right.left)])
                listaHojas.append([Tree('-',None,f.right.right)])
                print("1BETA")
        elif f.label == '&':
            listaHojas.remove(f)
            listaHojas.append([Tree('-',None,f.left),Tree('-',None,f.right)])
            print("2ALPHA")
        elif f.label == 'O':
            listaHojas.remove(f)
            listaHojas.append([f.left])
            listaHojas.append([f.right])
            print("2BETA")
        else:
            listaHojas.remove(f)
            listaHojas.append([Tree('-',None,f.left)])
            listaHojas.append([f.right])
            print("3BETA")
    else:
        print("Todos son literales")
        
def string2Tree(A, letrasProposicionales):
    # Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
    # Input: A, lista de caracteres con una formula escrita en notacion polaca inversa
             # letrasProposicionales, lista de letras proposicionales
    # Output: formula como tree
    conectivos = ['°', '^', '>']
    pila = []
    for c in A:
        if c in letrasProposicionales:
            pila.append(Tree(c, None, None))
        elif c == '~':
            formulaAux = Tree(c, None, pila[-1])
            del pila[-1]
            pila.append(formulaAux)
        elif c in conectivos:
            formulaAux = Tree(c, pila[-1], pila[-2])
            del pila[-1]
            del pila[-1]
            pila.append(formulaAux)
    return pila[-1]      

        
    



def Tableaux(f):

#Algoritmo de creacion de tableau a partir de lista_hojas
#Imput: - f, una fórmula como string en notación polaca inversa
#Output: interpretaciones: lista de listas de literales que hacen
# verdadera a f
    global listaHojas
    global listaInterpsVerdaderas
    A = string2Tree(f,letrasProposicionales)
    listaHojas = [[A]]
    while len(listaHojas) > 0 :
            hojas = choice(listaHojas)
            if not no_literales(hojas) :
                    for tree in hojas:
                            clasifica_y_extiende(tree)
            else:
                    if par_complementario(hojas):
                            listaHojas.remove(hojas)
                    else:
                            listaInterpsVerdaderas.append(hojas)
                            listaHojas.remove(hojas)

    return listaInterpsVerdaderas
