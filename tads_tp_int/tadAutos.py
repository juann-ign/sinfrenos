
def crearAuto():
    auto = ["", (0.0), 0, (0,0), 0.0]
    return auto

def cargarAuto(auto, patente, horaEntrada, torre, horaSalida, monto):
    auto[0] = patente
    auto[1] = horaEntrada
    auto[2] = torre
    auto[3] = horaSalida
    auto[4] = monto

def verPatente(auto):
    return auto[0]

def verHoraEntrada(auto):
    return auto[1]

def verTorre(auto):
    return auto[2]

def verHoraSalida(auto):
    return auto[3]

def verMonto(auto):
    return auto[4]

def modPatente(auto, patente):
    auto[0]= patente

def modHoraEntrada(auto, horaEntrada):
    auto[1]= horaEntrada

def modTorre(auto, torre):
    auto[2]= torre

def modHoraSalida(auto, horaSalida):
    auto[3]= horaSalida

def modMonto(auto, monto):
    auto[4]= monto