def crearCola():
    cola=[]
    return cola
def esVacia(cola):
    #Retorna V si la cola no tiene elementos
    return len(cola)==0
def encolar(cola,elem):
    #Agrega un elemento al final de la cola
    cola.append(elem)
def desencolar(cola):
    #Retorna y elemina el primer elemento de la cola
    return cola.pop(0)
def tamanioCola(cola):
    #Retorna la cantidad de elementos de la cola
    return len(cola)
def copiarCola(cola1,cola2):
    #Copia los datos de la cola 2 a la cola 1
    aux=crearCola()
    while not esVacia(cola2):
        elem=desencolar(cola2)
        encolar(aux,elem)
    while not esVacia(aux):
        elem=desencolar(aux)
        encolar(cola1,elem)
        encolar(cola2,elem)