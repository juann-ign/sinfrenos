#TADColaTorres


def crearCola():
    cola=[]     #crea una cola vacia
    return cola             

def EsVacia(cola):
    return len(cola) == 0 #return true si la cola esta vacia

def encolar(cola, auto):
    cola.append(auto)   #agrega un auto al final de la cola

def desencolar(cola):
    return cola.pop(0)   #retorna y elimina el primer auto de la cola
    

def tamCola(cola):
    return len(cola)    #retorna el tamanio de la cola
