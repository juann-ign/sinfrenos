from tadAutos import *
from tadCochera import *
import os
from datetime import datetime,time
from tadColaTorres import* 

cochera= crearCochera()
egreso= crearCochera()
precioEstadiaHora= 500
colaAutos= crearCola()

# AUTOS PRECARGADOS
autos_predefinidos = [  #tupla con los datos del auto
    ("ABC123", "08:30", 0, 1, 0),
    ("DEF456", "09:15", 0, 2, 0),
    ("GHI789", "10:00", 0, 3, 0),
    ("JKL012", "11:45", 0, 4, 0),
    ("MNO345", "17:10", 0, 5, 0),
    ("PQR678", "19:00", 0, 3, 0),
    ("STU901", "07:45", 0, 2, 0),
    ("VWX234", "13:20", 0, 1, 0),
    ("YZA567", "18:30", 0, 4, 0),
    ("BCD890", "16:50", 0, 5, 0),
]

for patente, horaEntrada, horaSalida, torre, monto in autos_predefinidos:   #usa un bucle para cargar cada auto en el tad
    auto = crearAuto()
    cargarAuto(auto, patente, horaEntrada, horaSalida, torre, monto)
    agreagarAuto(auto, cochera)


#almacenar hora
hora=datetime.now().time()


# PUNTO a)

#fucnion que permite ingresar nuevos vehiculos al estacionamiento
def nuevoVehiculo(cochera):
    patente= input("Ingrese la patente ")
    horaEntrada= input("Ingrese la hora de entrada ")
    torre= input("Ingrese la torre ")
    auto= crearAuto()
    cargarAuto(auto,patente, horaEntrada, torre)
    agreagarAuto(auto, cochera)

#funcion que permite modificar los datos de ingreso de un auto registrado
def modificarAuto(auto):
    print("1_ Modificar patente")
    print("2_ Modificar hora de entrada")
    print("3_ Modificar torre")
    
    opc=int(input()) #variable opcion para elegir que modificar
    if opc == 1:
        patente= input()
        modPatente(auto, patente)
    
    if opc == 2:
        HoraEntrada= input()
        modHoraEntrada(auto, HoraEntrada)
    
    if opc == 3:
        torre=input()
        modTorre(auto, torre)


#PUNTO B)

def retirarVehiculo(cochera, egreso):
    i=int(input("Ingrese el identificador del vehiculo que se retira "))
    auto=recuperarAuto(cochera, i)
    print("Vehiculo numero: # " + str(numeroAuto)) 
    print(verPatente(auto))
    print(verHoraEntrada(auto))
    print(verTorre(auto))
    horaSalida = input("Ingrese la hora de salida (HH:MM): ")
    modHoraSalida(auto, horaSalida)  # Guarda la hora de salida
    hEntrada = datetime.strptime(verHoraEntrada(auto), "%H:%M")
    hSalida = datetime.strptime(verHoraSalida(auto), "%H:%M")
    duracion = (hSalida.hour - hEntrada.hour)
    monto = duracion * precioEstadiaHora
    if int(verTorre(auto)) == 3:
        monto *= 0.85  # aplica descuento
    modMonto(auto, round(monto, 2))  # Guarda el monto en el vehículo
    print("Monto total a pagar: $" + str(round(monto, 2)))
    print("\n")
    eliminarAuto(auto,cochera)
    agreagarAuto(auto,egreso)
    print("El vehiculo se retiro")
    os.system ('pause')



#PUNTO C) 

def imprimirVehiculos(cochera, numeroAuto, egreso):
    print("------Autos estacionados-----")
    for auto in cochera:
        print("Vehiculo numero: # " + str(numeroAuto))
        print(verPatente(auto))
        print(verHoraEntrada(auto))
        print(verTorre(auto))
        print("Hora de salida: -")
        print("Monto: -")
        print("\n")
        numeroAuto+=1
    print("------Autos egresados------")
    for auto in egreso:
        print(verPatente(auto))
        print(verHoraEntrada(auto))
        print(verTorre(auto))
        print("Hora de salida: " + verHoraSalida(auto))
        print("Monto: $" + str(verMonto(auto)))
        print("\n")
    os.system('pause')

#PUNTO D) 

def informeTorre(egreso):
    montos = [0, 0, 0, 0, 0, 0]  # índice 1 a 5 (posición 0 no se usa)

    for auto in egreso:
        torre = int(verTorre(auto)) 
        monto = verMonto(auto)
        montos[torre] += monto

    print("\n--- Recaudación por torre ---")
    for i in range(1, 6):  # Torres 1 a 5
        print("Torre " + str(i) + ": $" + str(round(montos[i], 2)))



# PUNTO E)

# a) – Contar vehículos ingresados en horas pico
def contarHorasPico(cochera):
    contador = 0
    for auto in cochera:
        hora_str = verHoraEntrada(auto)
        hora_dt = datetime.strptime(hora_str, "%H:%M").time()
        if time(7, 0) <= hora_dt <= time(10, 0) or time(17, 0) <= hora_dt <= time(20, 0):
            contador += 1
    return contador

# b) – Eliminar vehículos de una torre ingresados después de las 18:00
def limpiarPorTorreYHora(cochera, torre_objetivo):
    eliminados = 0
    i = 0
    while i < len(cochera):
        auto = cochera[i]
        hora_str = verHoraEntrada(auto)
        hora_dt = datetime.strptime(hora_str, "%H:%M").time()
        if verTorre(auto) == torre_objetivo and hora_dt > time(18, 0):
            eliminarAuto(auto, cochera)
            eliminados += 1
        else:
            i += 1
    return eliminados


#PUNTO F)
#preguntarle el miercoles al profe si podemos hacer una cola auxiliar

def crearColaPorTorre(cochera, torre_buscada):
    

    for auto in cochera:
        if verTorre(auto) == torre_buscada:
            encolar(colaAutos, auto)
            print("Auto agregado a la cola: ")
            print("Patente del vehiculo: ", verPatente(auto))
            print("Hora de entrada: ", verHoraEntrada(auto))
            print("Torre: ", verTorre(auto))
            print("-----------------------------")

    if EsVacia(colaAutos):
        print("No se encontraron autos para la torre:", torre_buscada)

    return colaAutos


menu=1
while(menu):
    numeroAuto=1
    print("1_ Registrar nuevo vehiculo ")
    print("2_ Gestionar vehiculos estacionados")
    print("3_ Registrar salida del vehiculo")
    print("4_ Mostrar listado completo de vehiculos")
    print("5_ Informe de recaudacion por torre")
    print("6_ Cantidad de vehiculos ingresados durante hora pico")
    print("7_ Vehiculos eliminados despues de las 18hs")
    print("8_ Vehiculos en una torre especifica")
    print("0_ Salir\n")
    opc=int(input())
    if opc == 1:
        nuevoVehiculo(cochera)
    if opc == 2:
        modificarAuto(cochera, numeroAuto, egreso)
    if opc == 3:
        retirarVehiculo(cochera, egreso)
    if opc == 4:
        imprimirVehiculos(cochera, numeroAuto, egreso)
    if opc == 5:
        print(informeTorre)
    if opc == 6:
        cantidad = contarHorasPico(cochera)
        print("Cantidad de vehículos ingresados en hora pico:", cantidad)
    if opc == 7:
        torre = input("Ingrese la torre a limpiar: ")
        eliminados = limpiarPorTorreYHora(cochera, torre)
        print("Se eliminaron " + str(eliminados) + " vehículos de la torre " + str(torre) + " que ingresaron después de las 18:00.")
    if opc == 8:
        print(colaAutos)
    if opc == 0:
        menu = 0
    os.system('cls')



