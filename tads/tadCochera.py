def crearCochera():
    return []

def agregarAuto(cochera, auto):
    cochera.append(auto)

def eliminarAuto(cochera, auto):
    cochera.remove(auto)

def recuperarAuto(cochera,i):
    return cochera[i-1]

def cantidadAutos(cochera):
    return len(cochera) 