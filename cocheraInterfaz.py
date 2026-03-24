# Importa módulos para la interfaz gráfica, manejo de tiempo y TADs del sistema de cocheras.
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tads.tadAutos import *
from tads.tadCochera import *
from tads.tadColaAux import*
from tads.tadColaTorres import*
from datetime import datetime, date, time, timedelta

# Crea instancias de los TADS Compuestos Cochera y Egreso y Cola.
cochera= crearCochera()
egreso= crearCochera()
colaAutos= crearCola()
icon = "assets\\3xhumed-Mega-Games-Pack-31-Cars-pixar-1.ico"


# ========================= Autos de prueba predefinidos =========================
autosPredefinidos = [("ABC123", (8,30), 1, 0, 0), ("DEF456", (9,15), 2, 0, 0), ("GHI789", (10,0), 3, 0, 0),
    ("JKL012", (11,45), 4, 0, 0), ("MNO345", (17,10), 5, 0, 0), ("PQR678", (19,0), 5, 0, 0), ("STU901", (7,45), 1, 0, 0),
    ("VWX234", (13,20), 6, 0, 0), ("YZA567", (18,30), 2, 0, 0), ("BCD890", (16,50), 7, 0, 0),
    ("ABT542", (16,50), 1, (21,50), 2500), ("JFK364", (11,50), 5, (15,50),  2000.00), ("AAA111", (9,42), 4, (18,30), 4500.00),
    ("JAJ900", (6,15), 10, (22,45), 8000), ("GDT234", (16,00), 1, (23,54), 3500.00), ("TTT213", (13,12), 2, (18,50), 2500.00),
    ("PAM910", (20,55), 3, (21,14), 500.00), ("GTR465", (16,30), 1, (18,26), 1500.00)]


# Carga de autos inicial.
def cargarAutosPredefinidos(cochera, egreso, autosPredefinidos, cantTorres):
    for patente, horaEntrada, torre, horaSalida, monto in autosPredefinidos:
        if 1 <= torre <= cantTorres:
            auto = crearAuto()
            horaEntradaDt = datetime.strptime(f"{horaEntrada[0]:02d}:{horaEntrada[1]:02d}", "%H:%M").time()
            if monto != 0:
                # Auto egresado
                horaSalidaDt = datetime.strptime(f"{horaSalida[0]:02d}:{horaSalida[1]:02d}", "%H:%M").time()
                cargarAuto(auto, patente, horaEntradaDt, torre, horaSalidaDt, monto)
                agregarAuto(egreso, auto)
            else:
                # Auto estacionado
                cargarAuto(auto, patente, horaEntradaDt, torre, horaSalida, monto)
                agregarAuto(cochera, auto)


# Convierte las entradas de usuario en int o float si se ingresó un valor.
def convertirEntrys(entradaPatente, entradaHora, entradaMinutos, entradaTorre, auto = None):
    if auto is None:
        # Cuando ingreso el auto, todavía no está cargado en la cochera.
        if not entradaHora.isdigit() or not entradaMinutos.isdigit():
            messagebox.showerror("Error", "Ingrese una hora válida.")
            return None, None, None
        
        if not entradaTorre.isdigit():
            messagebox.showerror("Error", f"Ingrese una torre válida (Número de 1 a {cantTorres}).")
            return None, None, None
        
        try:
            horaEntrada = int(entradaHora)
            minEntrada = int(entradaMinutos)
            horaDt = datetime.strptime(f"{horaEntrada:02d}:{minEntrada:02d}", "%H:%M").time()
        except ValueError:
            messagebox.showerror("Error", "La hora ingresada no es válida. Debe estar entre 00:00 y 23:59")
            return None, None, None 
        
        patente = entradaPatente
        torre = int(entradaTorre)

        return patente, horaDt, torre
    
    else:
        # Cuando modifico el auto, ya está cargado en la cochera.
        if not entradaPatente:
            nuevaPatente = verPatente(auto)
        else:
            nuevaPatente = entradaPatente
   
        horaEntrada = verHoraEntrada(auto)
        horaActual = horaEntrada.hour
        minActual = horaEntrada.minute

        # Si alguno de los dos campos está vacío, uso el valor previo para ese campo
        # Si ambos están vacíos, uso la hora completa previa
        if not entradaHora:
            nuevaHora = horaActual
        else:
            nuevaHora = entradaHora

        if not entradaMinutos:
            nuevoMin = minActual
        else:
            nuevoMin = entradaMinutos

        # Verifico que si no están vacíos, sean dígitos
        if (entradaHora and not entradaHora.isdigit()) or (entradaMinutos and not entradaMinutos.isdigit()):
            messagebox.showerror("Error", "Ingrese una hora válida (solo números).")
            return None, None, None

        try:
            nuevaHs = int(nuevaHora)
            nuevoMin = int(nuevoMin)
            horaDt = datetime.strptime(f"{nuevaHs:02d}:{nuevoMin:02d}", "%H:%M").time()
        except ValueError:
            messagebox.showerror("Error", "La hora ingresada no es válida. Debe estar entre 00:00 y 23:59")
            return None, None, None

        if not entradaTorre:
            nuevaTorre = verTorre(auto)
        elif entradaTorre.isdigit():
            nuevaTorre = int(entradaTorre)
        else:
            messagebox.showerror("Error", f"Ingrese una torre válida (Número de 1 a {cantTorres}).")
            return None, None, None
        
        return nuevaPatente, horaDt, nuevaTorre


def convertirEntrysSalida(horaSalida, minSalida):
    if not horaSalida.isdigit() or not minSalida.isdigit():
        messagebox.showerror("Error", "Ingrese una hora válida (formato 0-23 para horas y 0-59 para minutos).")
        return None
    try:
        horaS = int(horaSalida)
        minS = int(minSalida)
        horaDt = datetime.strptime(f"{horaS:02d}:{minS:02d}", "%H:%M").time()
    except ValueError:
        messagebox.showerror("Error", "La hora ingresada no es válida. Debe estar entre 00:00 y 23:59")
        return None
    return horaDt

def convertirEntrysLimpieza(entradaTorre):
    if entradaTorre.isdigit():
        torre = int(entradaTorre)
        return torre
    else:
        messagebox.showerror("Error", f"Ingrese una torre válida (Número de 1 a {cantTorres}).")
        return None

# ------------------- Verificación de Errores -----------------------------

# Verifica que la patente ingresada por el usuario tenga un fórmato válido.
def contieneNumLet(patente):
    if not patente:
        return False
    tieneLetra = False
    tieneNumero = False
    esAlfanumerica = patente.isalnum()
    for caracter in patente: # Este for recorre todos los caracteres del string ingresado como patente y verifica que tenga tanto letras como números.
        if caracter.isalpha():
            tieneLetra = True
        elif caracter.isdigit():
            tieneNumero = True
    if not (esAlfanumerica and tieneLetra and tieneNumero):  # Si no cumple con las 3 condiciones, muestra un mensaje de error y permite ingresar nuevamente la patente.
        messagebox.showerror("Error", "La patente debe contener letras y números (Ejemplo: ABD832)")
        return False
    else:
        return True

# Verifica que la patente ingresada por el usuario tenga un fórmato válido.
def patenteValida(cochera, patente):
    if patente is not None:
        # Verifica si la patente es alfanumérica y contiene tanto letras como números.
        if not contieneNumLet(patente):
            return False  
        
        # Verifica si el auto ya está en la cochera
        tam = cantidadAutos(cochera)
        for au in range(1, tam+1):
            auto = recuperarAuto(cochera, au)
            if verPatente(auto) == patente:
                messagebox.showerror("Vehículo ya ingresado", f"El vehículo con patente '{patente}' ya se encuentra en el estacionamiento.")
                return False
        return True
    else:
        return False


# Verifica que el formato de horario ingresado por el usuario sea correcto.
def horaValida(horaEntrada):
    hora = horaEntrada.hour
    minutos = horaEntrada.minute
    if horaEntrada is not None:
        if not (0 <= hora < 24 and 0 <= minutos < 60):
            messagebox.showerror("Error", "Ingrese una hora válida (formato 0-23 para horas y 0-59 para minutos).")
            return False
        else:
            return True
    else:
        return False


# Funcion que valida el número de torre ingresado por el usuario.
def torreValida(torre, cantTorres):
    if torre is not None:
        # Validar que la torre exista según la cantidad de torres que ingresó el usuario.
        if not (1 <= torre <= cantTorres):
            messagebox.showerror("Error", f"La torre debe estar entre 1 y {cantTorres}.")
            return False
        else:
            return True
    else:
        return False

#
def habilitarBotonCarga(pat, btn, hs=None, m=None, tt=None):
    entradaPatente = pat.get().strip()
    if not entradaPatente:  # Si la patente está vacía, el botón se desactiva
        btn.config(state="disabled")
        return
    if hs and m and tt:  # Solo se activa si todos los campos de hora/tipo están llenos
        entradaHora = hs.get().strip()
        entradaMin = m.get().strip()
        entradaTorre = tt.get().strip()

        if not (entradaHora and entradaMin and entradaTorre):  # Si alguno está vacío, botón desactivado
            btn.config(state="disabled")
        else:
            btn.config(state="normal")
    else:
        # Solo se verifica la patente.
        btn.config(state="normal")


def habilitarBotonModificacion(pat, btn, hs, m, tt):
    entradaPatente = pat.get().strip()
    entradaHora = hs.get().strip()
    entradaMin = m.get().strip()
    entradaTorre = tt.get().strip()

    if ((entradaPatente) or (entradaHora) or (entradaMin) or (entradaTorre)):
        btn.config(state="normal")
    else:
        btn.config(state="disabled")


def habilitarBotonLimpieza(torre, btn):
    entradaTorre = torre.get().strip()
    if entradaTorre:
        btn.config(state = 'normal')
    else:
        btn.config(state = 'disabled')


# ----------------------------- Implemementación de funcionalidades del sistema -----------------------------

#   a. Registro y modificación de vehículos ingresados.
    #    Alta de vehículos.
def ingreauto(cochera, ventanaPrincipal, cantTorres):
    # Oculta el menú principal
    ventanaPrincipal.withdraw()

    # Crea la ventana para ingresar auto.
    ingreVehiculo=tk.Toplevel()  # Ventana secundaria.
    ingreVehiculo.title("Ingresar vehículo")
    ingreVehiculo.geometry("400x200")

    def cargarAu():
        entradaPatente = pat.get().strip().upper()
        entradaHora = hs.get()
        entradaMinutos = m.get()
        entradaTorre = tt.get()

        patente, horaEntrada, torre = convertirEntrys(entradaPatente, entradaHora, entradaMinutos, entradaTorre)

        # Verificación de errores: si alguna falla, salimos sin agregar el auto
        if not (patenteValida(cochera, patente) and torreValida(torre, cantTorres)):
            return  #  No se carga el auto ni se cierra la ventana
        
        # Si pasó todas las validaciones, se crea y carga el auto
        auto = crearAuto()
        cargarAuto(auto, patente, horaEntrada, torre, 0, 0)
        agregarAuto(cochera, auto)
        
        messagebox.showinfo("Vehículo cargado", f"Patente: {verPatente(auto)}\nHora de entrada: {verHoraEntrada(auto).strftime("%H:%M")}  \nTorre: {verTorre(auto)}")
        print("Vehículo agregado:", verPatente(auto), "- Torre:", verTorre(auto))

        ingreVehiculo.destroy()
        ventanaPrincipal.deiconify()  # Mostrar el menú principal nuevamente.

    # Función envolvente para pasar los parámetros
    def validarBoton(_=None):
        habilitarBotonCarga(pat, btnCargado, hs, m, tt)
    
    #Ingresa los datos
    et1 = tk.Label(ingreVehiculo, text="Ingrese la patente")
    et1.pack()

    pat = tk.Entry(ingreVehiculo)
    pat.pack()
    pat.bind('<KeyRelease>', validarBoton)

    et2 = tk.Label(ingreVehiculo, text="Ingrese la hora de entrada (hh:mm)")
    et2.pack()

    hs=tk.Entry(ingreVehiculo)
    hs.pack()
    hs.bind('<KeyRelease>', validarBoton)

    m=tk.Entry(ingreVehiculo)
    m.pack()
    m.bind('<KeyRelease>', validarBoton)

    et3=tk.Label(ingreVehiculo, text = f"Ingrese la torre (1-{cantTorres})")
    et3.pack()

    tt=tk.Entry(ingreVehiculo)
    tt.pack()
    tt.bind('<KeyRelease>', validarBoton)

    btnCargado=tk.Button(ingreVehiculo, text = "Cargar vehículo", command = cargarAu, state = "disabled")
    btnCargado.pack()

    ingreVehiculo.bind('<Return>', lambda event: cargarAu() if btnCargado['state'] == 'normal' else None)

    def cerrarVentana():
        ingreVehiculo.destroy()
        ventanaPrincipal.deiconify()    # Restaurar el menú si se cerró manualmente.

    ingreVehiculo.protocol("WM_DELETE_WINDOW", cerrarVentana)

    ingreVehiculo.mainloop()

    #   Modificación de vehículos.
def modAuto(cochera, ventanaPrincipal, cantTorres):
    # Oculta el menú principal
    ventanaPrincipal.withdraw()

    # ========== VENTANA 1: Ingreso de patente ==========
    ventanaPatente = tk.Toplevel()
    ventanaPatente.title("Modificar datos del vehículo")
    ventanaPatente.geometry("400x150")

    # Función envolvente para pasar los parámetros
    def validarBoton(_=None):
        habilitarBotonCarga(entryPatente, botonBusqueda)
    
    tk.Label(ventanaPatente, text="Ingrese la patente del vehículo a modificar:").pack()
    entryPatente = tk.Entry(ventanaPatente)
    entryPatente.pack(pady=10)
    entryPatente.focus_set()
    entryPatente.bind('<KeyRelease>', validarBoton)

    def buscarAuto():
        pat = entryPatente.get().strip().upper()
        if not contieneNumLet(pat):
            return

        autoEncontrado = None
        tam = cantidadAutos(cochera)
        for i in range(1, tam + 1):
            auto = recuperarAuto(cochera, i)
            if verPatente(auto) == pat:
                autoEncontrado = auto
                break

        if autoEncontrado is None:
            messagebox.showerror("No encontrado", f"No se encontró el vehículo con patente {pat}")
            return

        ventanaPatente.destroy()
        ventanaEdicion(autoEncontrado)

    botonBusqueda = tk.Button(ventanaPatente, text="Buscar", command=buscarAuto, state = "disabled")
    botonBusqueda.pack()

    ventanaPatente.bind('<Return>', lambda event: buscarAuto() if botonBusqueda['state'] == 'normal' else None)

    def cerrarVentana1():
        ventanaPatente.destroy()
        ventanaPrincipal.deiconify()

    ventanaPatente.protocol("WM_DELETE_WINDOW", cerrarVentana1)

    # ========== VENTANA 2: Edición unificada ==========
    def ventanaEdicion(auto):
        win = tk.Toplevel()
        win.title("Modificar datos del vehículo")
        win.geometry("400x300")

        # Función envolvente para pasar los parámetros
        def validarBotonMod(_=None):
            habilitarBotonModificacion(patNueva, botonConfirmar, entradaH, entradaM, entradaTorre,)

        # Frame principal con alineación vertical
        contenedor = tk.Frame(win)
        contenedor.pack(padx=20, pady=20, anchor='w')  # Anchor 'w' alinea todo a la izquierda

        # === Patente actual ===
        tk.Label(contenedor, text=f"Patente: {verPatente(auto)}").pack(anchor="w")

        # === Patente nueva ===
        framePat = tk.Frame(contenedor)
        framePat.pack(anchor="w", pady=5)
        tk.Label(framePat, text="Nueva patente: ").pack(side="left")
        patNueva = tk.Entry(framePat)
        patNueva.pack(side="left")
        patNueva.bind('<KeyRelease>', validarBotonMod)

        # === Hora actual ===
        tk.Label(contenedor, text=f"Hora de entrada: {verHoraEntrada(auto).strftime("%H:%M")}").pack(anchor="w")

        # === Hora nueva ===
        frameHora = tk.Frame(contenedor)
        frameHora.pack(anchor="w", pady=5)
        tk.Label(frameHora, text="Nueva hora de entrada: ").pack(side="left")
        entradaH = tk.Entry(frameHora, width=3)
        entradaH.pack(side="left")
        entradaH.bind('<KeyRelease>', validarBotonMod) 

        entradaH.pack(side="left", padx=(5, 2))
        entradaM = tk.Entry(frameHora, width=3)
        entradaM.pack(side="left")
        entradaM.bind('<KeyRelease>', validarBotonMod) 

        # === Torre actual ===
        tk.Label(contenedor, text=f"Torre: {verTorre(auto)}").pack(anchor="w")

        # === Torre nueva ===
        frameTorre = tk.Frame(contenedor)
        frameTorre.pack(anchor="w", pady=5)
        tk.Label(frameTorre, text="Nueva torre: ").pack(side="left")
        entradaTorre = tk.Entry(frameTorre)
        entradaTorre.pack(side="left")
        entradaTorre.bind('<KeyRelease>', validarBotonMod) 

        def confirmarCambios():
            nuevaPat = patNueva.get().strip().upper()
            nuevaH = entradaH.get().strip()
            nuevaM = entradaM.get().strip()
            nuevaT = entradaTorre.get().strip()

            # Llamada a función que convierte los entrys en enteros.
            nuevaPat, nuevaHoraEntrada, nuevaTorre = convertirEntrys(nuevaPat, nuevaH, nuevaM, nuevaT, auto)

            # Verificación de errores: si alguna falla, salimos sin agregar el auto
            if not (contieneNumLet(nuevaPat) and torreValida(nuevaTorre, cantTorres)):
                return  # No se carga el auto ni se cierra la ventana
            
            mensajesIgualdad = []
            cambios = {}

            # Patente
            actualPat = verPatente(auto)
            if nuevaPat == "":
                nuevaPat = actualPat  # Mantener sin cambio
            elif nuevaPat == actualPat:
                mensajesIgualdad.append("La patente nueva es igual a la actual.")
            else:
                cambios["patente"] = nuevaPat

            # Hora de entrada
            actualHora = verHoraEntrada(auto)
            if nuevaHoraEntrada == "":
                nuevaHoraEntrada = actualHora
            elif nuevaHoraEntrada == actualHora:
                mensajesIgualdad.append("La hora de entrada nueva es igual a la actual.")
            else:
                cambios["hora"] = nuevaHoraEntrada

            # Torre
            actualTorre = verTorre(auto)
            if nuevaTorre == "":
                nuevaTorre = actualTorre
            elif nuevaTorre == actualTorre:
                mensajesIgualdad.append("La torre nueva es igual a la actual.")
            else:
                cambios["torre"] = nuevaTorre

            # Si no hubo cambios reales
            if not cambios:
                if mensajesIgualdad:
                    messagebox.showerror("Sin cambios", "\n".join(mensajesIgualdad) + "\n\nModifique algún campo o deje los campos iguales en blanco.")
                else:
                    messagebox.showinfo("Sin cambios", "No se ingresaron datos nuevos.")
                return

            # Mostrar advertencias por campos iguales (solo si hubo cambios)
            if mensajesIgualdad:
                continuar = messagebox.askyesno("Advertencia", "\n".join(mensajesIgualdad) + "\n\n¿Desea continuar con los cambios ingresados?")
                if not continuar:
                    return

            # Aplicar modificaciones
            if "patente" in cambios:
                modPatente(auto, cambios["patente"])
            if "hora" in cambios:
                modHoraEntrada(auto, cambios["hora"])
            if "torre" in cambios:
                modTorre(auto, cambios["torre"])

            messagebox.showinfo("Vehículo modificado", f"Patente: {verPatente(auto)}\nHora de entrada: {verHoraEntrada(auto).strftime('%H:%M')}\nTorre: {verTorre(auto)}")
            print("Vehículo modificado:", verPatente(auto), "- Torre:", verTorre(auto))
            win.destroy()
            ventanaPrincipal.deiconify()

        botonConfirmar = tk.Button(win, text="Confirmar cambios", command=confirmarCambios, state = "disabled")
        botonConfirmar.pack(pady=15)

        win.bind('<Return>', lambda event: confirmarCambios() if botonConfirmar['state'] == 'normal' else None)

        def cerrar():
            win.destroy()
            ventanaPrincipal.deiconify()

        win.protocol("WM_DELETE_WINDOW", cerrar)

    ventanaPatente.mainloop()
    

#  b. Registro de salida y cálculo de monto a cobrar.
    #   Baja de vehículos.
def retirarVehiculo(cochera, egreso, ventanaPrincipal):
    # Oculta el menú principal
    ventanaPrincipal.withdraw()

    # Creo la ventana para retirar a un vehiculo del estacionamiento
    retirarAuto = tk.Toplevel()
    retirarAuto.title("Retirar vehículo")
    retirarAuto.geometry("300x200")

    # Función envolvente para pasar los parámetros
    def validarBoton(_=None):
        habilitarBotonCarga(entryPatente, botonBusqueda)
    
    tk.Label(retirarAuto, text="Ingrese la patente del vehículo a retirar:").pack()
    entryPatente = tk.Entry(retirarAuto)
    entryPatente.pack(pady=10)
    entryPatente.focus_set()
    entryPatente.bind('<KeyRelease>', validarBoton)
    
    def buscarVehiculo():
        pat = entryPatente.get().strip().upper()
        if not contieneNumLet(pat):
            return

        autoEncontrado = None
        tam = cantidadAutos(cochera)
        for i in range(1, tam + 1):
            auto = recuperarAuto(cochera, i)
            if verPatente(auto) == pat:
                autoEncontrado = auto
                break

        if autoEncontrado is None:
            messagebox.showerror("No encontrado", f"No se encontró el vehículo con patente {pat}")
            return

        retirarAuto.destroy()
        ingresarHoraSalida(autoEncontrado)

    botonBusqueda = tk.Button(retirarAuto, text="Buscar", command=buscarVehiculo, state = "disabled")
    botonBusqueda.pack()

    retirarAuto.bind('<Return>', lambda event: buscarVehiculo() if botonBusqueda['state'] == 'normal' else None)

    def cerrarVentana1():
        retirarAuto.destroy()
        ventanaPrincipal.deiconify()

    retirarAuto.protocol("WM_DELETE_WINDOW", cerrarVentana1)

    def ingresarHoraSalida(auto):
        win = tk.Toplevel()
        win.title("Registrar hora de salida del vehículo")
        win.geometry("400x300")

        # Frame principal con alineación vertical
        contenedor = tk.Frame(win)
        contenedor.pack(padx=20, pady=20, anchor='w')  # Anchor 'w' alinea todo a la izquierda

        # === Hora de salida ===
        frameHora = tk.Frame(contenedor)
        frameHora.pack(anchor="w", pady=5)
        tk.Label(frameHora, text="Hora de salida: ").pack(side="left")
        
        entradaH = tk.Entry(frameHora, width=3)
        entradaH.pack(side="left")

        entradaM = tk.Entry(frameHora, width=3)
        entradaM.pack(side="left")

        def confirmarCambios():
            horaS = entradaH.get().strip()
            minS = entradaM.get().strip()

            horaEntrada = verHoraEntrada(auto)
            horaSalida = convertirEntrysSalida(horaS, minS)
            if horaSalida is None:
                return # Detiene el proceso si no se ingresa una hora valida.
            
            # Combina ambas horas con la fecha actual para poder restarlas.
            fecha = date.today()
            entradaDt = datetime.combine(fecha, horaEntrada)
            salidaDt = datetime.combine(fecha, horaSalida)
            
            if salidaDt <= entradaDt:
                messagebox.showerror("Error", "La hora de salida debe ser mayor a la hora de entrada.")
                return
            
            duracion = salidaDt - entradaDt
            duracionHs = duracion.total_seconds() / 3600 # 1.5 horas por ejemplo
            montoAuto = duracionHs * mon 

            if verTorre(auto) == 3:
                montoAuto *= 0.85  # Aplica descuento a los autos estacionados en la torre 3.
            
            # Redondea a 2 decimales.
            montoAuto = round(montoAuto, 2)
            # Guarda en el TAD Auto la hora de salida y el monto a pagar.
            modHoraSalida(auto, horaSalida)
            modMonto(auto, montoAuto)

            messagebox.showinfo("Vehículo retirado", f"Patente: {verPatente(auto)}\nHora de entrada: {verHoraEntrada(auto).strftime('%H:%M')}\nTorre: {verTorre(auto)}\nHora de salida: {verHoraSalida(auto).strftime('%H:%M')}\nMonto a pagar: {verMonto(auto)}")
            print("Vehículo retirado:", verPatente(auto), "- Tor:", verTorre(auto))
            eliminarAuto(cochera, auto)
            agregarAuto(egreso, auto)
            
            win.destroy()
            ventanaPrincipal.deiconify()
     
            # Validaciones y modificaciones
        botonConfirmar = tk.Button(win, text="Confirmar cambios", command = confirmarCambios, state = "normal")
        botonConfirmar.pack(pady = 15)
        win.bind('<Return>', lambda event: confirmarCambios() if botonConfirmar['state'] == 'normal' else None)
        
        def cerrar():
            win.destroy()
            ventanaPrincipal.deiconify()
        win.protocol("WM_DELETE_WINDOW", cerrar)
    retirarAuto.mainloop()
 

#  c. Listado completo de vehículos.
def imprimirVehiculos(cochera, egreso):
    # Ventana principal de listado
    listado = tk.Tk()
    listado.title("Listado de vehículos")
    listado.geometry("400x400")

    # Pestañas con Notebook
    notebook = ttk.Notebook(listado)
    notebook.pack(expand=True, fill='both')

    # Función interna que carga autos en un frame
    def agregarListadoAutos(frame, coleccion):
        headers = ["Patente", "Hora entrada", "Torre", "Hora salida", "Monto"]
        for col, header in enumerate(headers):
            tk.Label(frame, text = header, font=('Arial', 10, 'bold')).grid(row=0, column=col, padx=5, pady=5)
            
        tam = cantidadAutos(coleccion)
        for i in range(1, tam + 1):
            auto = recuperarAuto(coleccion, i)

            pat = verPatente(auto)
            horaEntrada = verHoraEntrada(auto)
            torre = verTorre(auto)
            horaSalida = verHoraSalida(auto)
            monto = verMonto(auto)

            tk.Label(frame, text=pat).grid(row=i, column=0)
            tk.Label(frame, text=horaEntrada.strftime('%H:%M')).grid(row=i, column=1)
            tk.Label(frame, text=torre).grid(row=i, column=2)
            if horaSalida:
                tk.Label(frame, text=horaSalida.strftime('%H:%M')).grid(row = i, column = 3)
            else:
                tk.Label(frame, text="-").grid(row = i, column = 3)
            if monto:
                tk.Label(frame, text=f"${monto:.2f}").grid(row=i, column=4)
            else:
                tk.Label(frame, text = "-").grid(row=i, column=4)

    # Frame de autos estacionados
    frameEstacionados = tk.Frame(notebook)
    notebook.add(frameEstacionados, text="Estacionados")
    agregarListadoAutos(frameEstacionados, cochera)

    # Frame de autos egresados
    frameEgresados = tk.Frame(notebook)
    notebook.add(frameEgresados, text="Egresados")
    agregarListadoAutos(frameEgresados, egreso)

    listado.mainloop()


#  d. Informe de recaudación por torre.
def informeTorre(egreso, cantTorres):
    # Crea la ventana de recaudación
    recaudacion = tk.Toplevel()
    recaudacion.title("Informe de recaudación por torre")
    recaudacion.geometry("300x400")

    # Título
    titulo = tk.Label(recaudacion, text = "Recaudación por torre", font = ("Arial", 12, "bold"))
    titulo.pack(pady = 10)
    
    # Muestra la recaudación por torre
    montos = [0] * (cantTorres+1)  # índice 1 a n torres 

    total = cantidadAutos(egreso)
    for i in range(1, total+1):
        auto = recuperarAuto(egreso, i)
        torre = verTorre(auto) 
        monto = verMonto(auto)
        montos[torre] += monto

    frame = tk.Frame(recaudacion)
    frame.pack()

    # Headers
    tk.Label(frame, text = "Torre", font = ("Arial", 10, "bold")).grid(row = 0, column = 0, padx = 10, pady = 5)
    tk.Label(frame, text = "Recaudación", font = ("Arial", 10, "bold")).grid(row = 0, column = 1, padx = 10, pady = 5)

    # Datos por torre
    for i in range(1, cantTorres + 1):
        tk.Label(frame, text = f"{i}").grid(row = i, column = 0, padx = 10, pady = 2)
        tk.Label(frame, text = f"${round(montos[i], 2)}").grid(row = i, column = 1, padx = 10, pady = 2)
      
    print("\n--- Recaudación por torre ---")
    for i in range(1, cantTorres + 1):  # Torres 1 a n
        print(f"Torre {i}: ${round(montos[i], 2)}")


#   e. Estadísticas y limpieza por horario y torre.
    #   a) Contar vehículos ingresados en horas pico (7 a 10 hs y 17 a 20 hs).
def listarHoraPico(cochera):
    # Crear ventana
    ventana = tk.Toplevel()
    ventana.title("Ingresos en hora pico")
    ventana.geometry("480x300")

    # Título
    tk.Label(ventana, text="Vehículos ingresados en hora pico (07-10 y 18-21)", font=("Arial", 12, "bold")).pack(pady=5)

    # Contador de hora pico
    total = cantidadAutos(cochera)
    contador = 0
    autosHoraPico = []

    for i in range(1, total + 1):
        auto = recuperarAuto(cochera, i)
        hora = verHoraEntrada(auto).hour
        if (7 <= hora < 10) or (18 <= hora < 21):
            autosHoraPico.append(auto)
            contador += 1

    # Mostrar contador
    tk.Label(ventana, text=f"Han ingresado {contador} vehículos en hora pico", font=("Arial", 11)).pack()

    # Encabezados
    encabezado = tk.Frame(ventana)
    encabezado.pack(pady=5)
    tk.Label(encabezado, text="Patente", width=15, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=0)
    tk.Label(encabezado, text="Hora de entrada", width=15, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=1)
    tk.Label(encabezado, text="Torre", width=10, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=2)

    # Listado
    cuerpo = tk.Frame(ventana)
    cuerpo.pack()

    if contador == 0:
        tk.Label(cuerpo, text="No hubo ingresos en hora pico.").pack()
    else:
        for fila, auto in enumerate(autosHoraPico, start=1):
            patente = verPatente(auto)
            horaEntrada = verHoraEntrada(auto).strftime('%H:%M')
            torre = verTorre(auto)

            tk.Label(cuerpo, text=patente, width=15, anchor="w").grid(row=fila, column=0)
            tk.Label(cuerpo, text=horaEntrada, width=15, anchor="w").grid(row=fila, column=1)
            tk.Label(cuerpo, text=torre, width=10, anchor="w").grid(row=fila, column=2)



    #    b) Eliminar vehículos de una torre ingresados después de las 18:00 
def limpiarPorTorreYHora(cochera, egreso, ventanaPrincipal, cantTorres):
    ventanaPrincipal.withdraw()
    limpiarVehiculo = tk.Toplevel()
    limpiarVehiculo.title("Limpiar vehículos de una torre")
    limpiarVehiculo.geometry("400x500")

    # === Variable para modo prueba ===
    modoPrueba = tk.BooleanVar()

    # === Función que activa/desactiva los entrys de manera manual ===
    def alternarModoPrueba():
        if modoPrueba.get():
            entryHs.config(state = "normal")
            entryMs.config(state = "normal")
        else:
            entryHs.delete(0, tk.END)
            entryMs.delete(0, tk.END)
            entryHs.config(state = "disabled")
            entryMs.config(state = "disabled")

    # === Checkbox para activar modo prueba ===
    tk.Checkbutton(limpiarVehiculo, text = "Modo prueba (ingresar hora de salida manual).", variable = modoPrueba, command = alternarModoPrueba).pack()

    # === Entrada de hora de salida (visible solo en modo prueba) ===
    frameHoraSalida = tk.Frame(limpiarVehiculo)
    tk.Label(frameHoraSalida, text="Hora de salida (hh mm): ").pack(side="left")

    entryHs = tk.Entry(frameHoraSalida, width=3)
    entryHs.pack(side="left")
    entryHs.config(state = "disabled")

    entryMs = tk.Entry(frameHoraSalida, width=3)
    entryMs.pack(side="left")
    entryMs.config(state = "disabled")

    frameHoraSalida.pack(pady=10)

    def limpiarTorre():
        entradaTorre = torreObjetivo.get()
        torre = convertirEntrysLimpieza(entradaTorre)
        if not torreValida(torre, cantTorres):
            return

        # Obtener hora de salida
        if modoPrueba.get():
            hsSalida = entryHs.get().strip()
            minSalida = entryMs.get().strip()
            horaSalida = convertirEntrysSalida(hsSalida, minSalida)
            if not horaSalida:
                return
        else:
            horaSalida = datetime.now().time()
        
        eliminados = 0
        i = 1
        while i <= cantidadAutos(cochera):
            auto = recuperarAuto(cochera, i)
            horaEntrada = verHoraEntrada(auto)
            if verTorre(auto) == torre and horaEntrada.hour >= 18: # PARA PROBAR LO SETEO EN 10
                # Calcular monto
                fecha = date.today()
                entradaDt = datetime.combine(fecha, horaEntrada)
                salidaDt = datetime.combine(fecha, horaSalida)

                if salidaDt <= entradaDt:
                    salidaDt += timedelta(days=1)  # Ajuste si necesario

                duracion = salidaDt - entradaDt
                duracionHs = duracion.total_seconds() / 3600
                montoAuto = duracionHs * mon ## MODIFICAR PRECESTADIA

                if verTorre(auto) == 3:
                    montoAuto *= 0.85

                montoAuto = round(montoAuto, 2)

                modHoraSalida(auto, horaSalida)
                modMonto(auto, montoAuto)

                eliminarAuto(cochera, auto)
                agregarAuto(egreso, auto)
                eliminados += 1
            else:
                i += 1

        messagebox.showinfo("Resultado", f"Se eliminaron {eliminados} vehículos de la torre {torre} ingresados después de las 18:00.")
        imprimirVehiculos(cochera, egreso)

    def validarBoton(_=None):
        habilitarBotonLimpieza(torreObjetivo, btnLimpiarVehiculo)

    et1 = tk.Label(limpiarVehiculo, text="Ingrese la torre que se desea limpiar")
    et1.pack()

    torreObjetivo = tk.Entry(limpiarVehiculo)
    torreObjetivo.pack()
    torreObjetivo.bind('<KeyRelease>', validarBoton)

    btnLimpiarVehiculo = tk.Button(limpiarVehiculo, text="Limpiar torre", command=limpiarTorre, state='disabled')
    btnLimpiarVehiculo.pack(pady=15)

    limpiarVehiculo.bind('<Return>', lambda event: limpiarTorre() if btnLimpiarVehiculo['state'] == 'normal' else None)

    def cerrarVentana():
        limpiarVehiculo.destroy()
        ventanaPrincipal.deiconify()

    limpiarVehiculo.protocol("WM_DELETE_WINDOW", cerrarVentana)
    limpiarVehiculo.mainloop()



#   f. Generación y visualización de cola por torre.
def colaPorTorre(cochera, egreso, ventanaPrincipal, cantTorres):
    # Oculta el menú principal
    ventanaPrincipal.withdraw()

    # Creo la ventana para retirar a un vehiculo del estacionamiento
    colaTorre = tk.Toplevel()
    colaTorre.title("Seleccionar torre a listar")
    colaTorre.geometry("300x200")

    # Función envolvente para pasar los parámetros
    def validarBoton(_=None):
        habilitarBotonLimpieza(entryTorre, botonBusqueda)
    
    tk.Label(colaTorre, text="Ingrese número de torre:").pack(pady = 10)
    entryTorre = tk.Entry(colaTorre)
    entryTorre.pack(pady=10)
    entryTorre.focus_set()
    entryTorre.bind('<KeyRelease>', validarBoton)
    
    def buscarTorre():
        entradaTorre = entryTorre.get().strip()
        torre = convertirEntrysLimpieza(entradaTorre)
        if not torreValida(torre, cantTorres):
            return
        
        colaTorre.destroy()
        mostrarColaVehiculos(torre)
    
    def mostrarColaVehiculos(torre,):
        # Ventana para visualizar la torre.
        mostrarC = tk.Toplevel()
        mostrarC.title(f"Cola de vehículos en la torre {torre}")
        mostrarC.geometry("400x400")

        # Esta función filtra autos de una colección según la torre.
        def filtrarPorTorre(coleccion, torre):
            cola = crearCola()
            for i in range(1, cantidadAutos(coleccion) + 1):
                auto = recuperarAuto(coleccion, i)
                if verTorre(auto) == torre:
                    encolar(cola, auto)
            return cola


        # Pestañas con Notebook
        notebook = ttk.Notebook(mostrarC)
        notebook.pack(expand = True, fill = 'both')

        # Función interna que carga autos en un frame
        def agregarAutosCola(frame, cola):
            headers = ["Patente", "Hora entrada", "Torre", "Hora salida", "Monto"]
            for col, header in enumerate(headers):
                tk.Label(frame, text = header, font=('Arial', 10, 'bold')).grid(row=0, column=col, padx=5, pady=5)
                
            aux = crearCola()
            i = 1
            while not esVacia(cola):
                auto = desencolar(cola)
                pat = verPatente(auto)
                horaEntrada = verHoraEntrada(auto)
                torre = verTorre(auto)
                horaSalida = verHoraSalida(auto)
                monto = verMonto(auto)

                tk.Label(frame, text=pat).grid(row=i, column=0)
                tk.Label(frame, text=horaEntrada.strftime('%H:%M')).grid(row=i, column=1)
                tk.Label(frame, text=torre).grid(row=i, column=2)
                tk.Label(frame, text=horaSalida.strftime('%H:%M') if horaSalida else "-").grid(row=i, column=3)
                tk.Label(frame, text=f"${monto:.2f}" if monto else "-").grid(row=i, column=4)

                encolar(aux, auto)
                i += 1
            
            while not esVacia(aux):
                encolar(cola, desencolar(aux))

        # Frame de autos estacionados
        colaEstacionados = filtrarPorTorre(cochera, torre)
        frameEstacionados = tk.Frame(notebook)
        notebook.add(frameEstacionados, text = "Estacionados")

        if esVacia(colaEstacionados):
            tk.Label(frameEstacionados, text = f"No hay vehículos estacionados en la torre {torre}.").pack(pady = 10)
        else:
            agregarAutosCola(frameEstacionados, colaEstacionados)


        # Frame de autos egresados
        colaEgresados = filtrarPorTorre(egreso, torre)
        frameEgresados = tk.Frame(notebook)
        notebook.add(frameEgresados, text="Egresados")

        if esVacia(colaEgresados):
            tk.Label(frameEgresados, text = f"No hay vehículos egresados de la torre {torre}.").pack(pady = 10)
        else:
            agregarAutosCola(frameEstacionados, colaEgresados)
       
        mostrarC.mainloop()

    botonBusqueda = tk.Button(colaTorre, text="Buscar", command=buscarTorre, state = "disabled")
    botonBusqueda.pack(pady = 10)

    colaTorre.bind('<Return>', lambda event: buscarTorre() if botonBusqueda['state'] == 'normal' else None)

    def cerrarVentana1():
        colaTorre.destroy()
        ventanaPrincipal.deiconify()

    colaTorre.protocol("WM_DELETE_WINDOW", cerrarVentana1)

    colaTorre.mainloop()


# main
def menu():
    print('¡Día iniciado!')
    global mon, cantTorres
    mon=float(monto.get())
    cantTorres = int(torres.get())
    cargarAutosPredefinidos(cochera, egreso, autosPredefinidos, cantTorres)

    inicio.destroy()

    root=tk.Tk()
    root.title("Estacionamiento")
    root.configure()
    root.geometry("600x720")
    root.iconbitmap(icon)
    root.configure(bg="#FFFFFF")

    
    #Botones por función
   # Título principal
    titulo = tk.Label(root, text="MENÚ PRINCIPAL",
                      font=("Arial", 16, "bold"),
                      bg="#FFFFFF", fg="#002F6C")
    titulo.pack(pady=(35, 30))

    # Frame contenedor de botones
    menu_frame = tk.Frame(root, bg="#FFFFFF")
    menu_frame.pack(pady=10)

    # Estilo de botones
    btn_config = {
        "bg": "#002F6C",
        "fg": "#FFFFFF",
        "font": ("Arial", 13, "bold"),
        "bd": 4,
        "height": 2,
        "width": 35,
        "master": menu_frame,
        "anchor": "center"
    }

    botones = [
        ("Ingresar vehículo", lambda: ingreauto(cochera, root, cantTorres)),
        ("Modificar vehículo", lambda: modAuto(cochera, root, cantTorres)),
        ("Retirar vehículo", lambda: retirarVehiculo(cochera, egreso, root)),
        ("Mostrar listado de vehículos", lambda: imprimirVehiculos(cochera, egreso)),
        ("Mostrar recaudación por torre", lambda: informeTorre(egreso, cantTorres)),
        ("Mostrar cantidad de autos en hora pico", lambda: listarHoraPico(cochera)),
        ("Limpiar torre pasadas las 18 hs", lambda: limpiarPorTorreYHora(cochera, egreso, root, cantTorres)),
        ("Mostrar cola de vehículos", lambda: colaPorTorre(cochera, egreso, root, cantTorres)),
    ]

    for texto, comando in botones:
        boton = tk.Button(text=texto, command=comando, **btn_config)
        boton.pack(pady=4)


def habilitarBtn(_=None):
    entradaMonto = monto.get().strip()
    entradaTorre = torres.get().strip()
    try:
        if entradaMonto and entradaTorre:
            float(entradaMonto)
            int(entradaTorre)
            btnIniciarDia.config(state='normal', bg="#00833B", fg="#FFFFFF")
        else:
            btnIniciarDia.config(state='disabled', bg="#CCCCCC", fg="#FFFFFF")
    except ValueError:
        btnIniciarDia.config(state='disabled', bg="#CCCCCC", fg="#FFFFFF")

def addPlaceholder(entry, placeholder):
    def onFocusIn(event):
        if entry.get() == placeholder:
            entry.delete(0, 'end')
            entry.config(fg='black')
    def onFocusOut(event):
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(fg='gray')
            entry.icursor(0)
    def onKeyRelease(event):
        texto = entry.get()
        if texto == '':
            entry.config(fg='gray')
            entry.delete(0, 'end')
            entry.insert(0, placeholder)
            entry.icursor(0)
        elif texto == placeholder:
            entry.config(fg='gray')
            entry.icursor(0)
        else:
            entry.config(fg='black')
    entry.insert(0, placeholder)
    entry.config(fg='gray')
    entry.bind('<FocusIn>', onFocusIn)
    entry.bind('<FocusOut>', onFocusOut)
    entry.bind('<KeyRelease>', onKeyRelease)

def onEnter(e):
    if btnIniciarDia['state'] == 'normal':
        btnIniciarDia.config(bg="#3BE975")

def onLeave(e):
    if btnIniciarDia['state'] == 'normal':
        btnIniciarDia.config(bg="#00833B")
    else:
        btnIniciarDia.config(bg="#CCCCCC")

inicio = tk.Tk()
inicio.title('Cochera')
inicio.geometry("400x380")
inicio.resizable(0, 0)
inicio.configure(bg="#FFFFFF")
inicio.iconbitmap(icon)

diaActual = datetime.now().strftime("%d/%m")
titulo = tk.Label(inicio, text=f"CONFIGURACIÓN DEL DÍA {diaActual}",
                  font=("Arial", 16, "bold"), bg="#FFFFFF", fg="#002F6C")
titulo.pack(pady=(30, 15))

form = tk.Frame(inicio, bg="#FFFFFF")
form.pack(pady=20)

# Monto
lblMonto = tk.Label(form, text="Monto",
                     font=("Arial", 10, "bold"), bg="#FFFFFF", fg="#333333", anchor="w")
lblMonto.pack(fill='x')

frameMonto = tk.Frame(form, bg="#FFFFFF", bd=1, relief='solid', highlightthickness=1, highlightbackground="#999999")
frameMonto.pack(fill='x', pady=(0, 15))

monto = tk.Entry(frameMonto, font=('Arial', 10), bd=0, width=24)
monto.pack(fill='x', padx=10, ipady=8,)
addPlaceholder(monto, " Ingresá el precio por hora")

# Torres
lblTorres = tk.Label(form, text="Torres",
                      font=("Arial", 10, "bold"), bg="#FFFFFF", fg="#333333", anchor="w")
lblTorres.pack(fill='x')

frameTorres = tk.Frame(form, bg="#FFFFFF", bd=1, relief='solid', highlightthickness=1, highlightbackground="#999999")
frameTorres.pack(fill='x', pady=(0, 15))

torres = tk.Entry(frameTorres, font=('Arial', 10), bd=0, width=24)
torres.pack(fill='x', padx=10, ipady=8)
addPlaceholder(torres, " Ingresá la cantidad de torres")

monto.bind('<KeyRelease>', lambda e: (habilitarBtn(), None))
torres.bind('<KeyRelease>', lambda e: (habilitarBtn(), None))

btnIniciarDia = tk.Button(inicio, text='INICIAR DÍA', command=menu,
                          state='disabled', bg="#CCCCCC", fg="#FFFFFF",
                          font=('Arial', 11, 'bold'), bd=0, height=2)
btnIniciarDia.pack(fill='x', padx=70)

btnIniciarDia.bind("<Enter>", onEnter)
btnIniciarDia.bind("<Leave>", onLeave)

inicio.bind('<Return>', lambda event: menu() if btnIniciarDia['state'] == 'normal' else None)

inicio.mainloop()