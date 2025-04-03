#importar libreria GUI
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook
import Util
import csv
from datetime import datetime
import matplotlib.pyplot as plt

iconos = ["./iconos/Grafica.png", "./iconos/Datos.png"]
textos = ["Gráfica Fecha vs Cambio", "Calculas Estadísticas"]

def obtenerMonedas():
    #abrir el archivo CSV
    with open("./datos/Cambios Monedas.csv") as archivo:
        lectorArchivo = csv.reader(archivo)
        next(lectorArchivo) #omitir linea de encabezados
        return sorted(set(map(lambda linea: linea[0], lectorArchivo)))
        
    #No funcional
    monedas = set() #el uso de SET evita duplicados
    #abrir el archivo CSV
    with open("./datos/Cambios Monedas.csv") as archivo:
        lectorArchivo = csv.reader(archivo)
        next(lectorArchivo) #omitir linea de encabezados
        for linea in lectorArchivo:
            moneda, strfecha, strcambio = linea
            monedas.add(moneda)
    return list(monedas)

def obtenerDatos():
    #abrir el archivo CSV
    with open("./datos/Cambios Monedas.csv") as archivo:
        lectorArchivo = csv.reader(archivo)
        next(lectorArchivo) #omitir linea de encabezados
        return [
            { "moneda": linea[0] , "fecha": datetime.strptime(linea[1], "%d/%m/%Y") , "cambio": float(linea[2]) } for linea in lectorArchivo
            ]

def filtrarDatos(datos, moneda, desde, hasta):
    return list(filter(lambda dato: dato["moneda"]==moneda and desde<=dato["fecha"] and dato["fecha"] <=hasta , datos))

def extraerDatos(datos):
    datosOrdenados = sorted(datos, key=lambda dato: dato["fecha"])
    fechas = list(map(lambda dato: dato["fecha"], datosOrdenados))
    cambios = list(map(lambda dato: dato["cambio"], datosOrdenados))
    return fechas, cambios

def mostrarGrafica():
    if cmbMoneda.current() >= 0:
        #obtener datos de entrada
        moneda = monedas[cmbMoneda.current()]
        desde = datetime.strptime(cldDesde.get(), "%d/%m/%Y")
        hasta = datetime.strptime(cldHasta.get(), "%d/%m/%Y")
        
        datos = obtenerDatos()
        datosFiltrados = filtrarDatos(datos, moneda, desde, hasta)
        fechas, cambios = extraerDatos(datosFiltrados)

        #graficar
        plt.title("Cambios de monedas")
        plt.clf() #limpiar la grafica
        plt.ylabel("Valor Cambio")
        plt.xlabel("Fecha")

        plt.plot(fechas, cambios, label=f"Cambio de {moneda}")
        plt.grid()
        plt.legend()

        plt.savefig("graficaCambiosMoneda.png")
        

def mostrarEstadisticas():
    messagebox.showinfo("", "Hizo clic en ESTADISTICAS")

ventana = Tk()
ventana.title("Cambios de Moneda")
ventana.geometry("400x300")

botones = Util.agregarBarra(ventana, iconos, textos)
botones[0].configure(command=mostrarGrafica)
botones[1].configure(command=mostrarEstadisticas)

frmMoneda = Frame(ventana)
frmMoneda.pack(side=TOP, fill=X)

Util.agregarEtiqueta(frmMoneda, "Moneda", 0, 0)
monedas = obtenerMonedas()
cmbMoneda = Util.agregarLista(frmMoneda, monedas, 0, 1)

cldDesde = Util.agregarCalendario(frmMoneda, 0, 2)
cldHasta = Util.agregarCalendario(frmMoneda, 0, 3)

nb = Notebook(ventana)
nb.pack(fill=BOTH, expand=YES)
pestañas = ["Gráfica", "Estadisticas"]
for p in pestañas:
    frm = Frame(ventana)
    nb.add(frm, text=p)
