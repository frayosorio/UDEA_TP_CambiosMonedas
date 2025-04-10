#importar libreria GUI
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook
import Util
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from functools import reduce
import math

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

        #guardar la grafica
        nombreArchivo="graficaCambiosMoneda.png"
        plt.savefig(nombreArchivo)
        #cargar la grafica
        imgGrafica = PhotoImage(file = nombreArchivo)

        #crear LABEL para mostrar la grafica en el primer panel
        lblGrafica=Label(paneles[0])
        lblGrafica.config(image=imgGrafica)
        lblGrafica.image=imgGrafica

        lblGrafica.place(x=0, y=0)

        #redimensionar la ventana
        ventana.minsize(imgGrafica.width(), imgGrafica.height()+100)

        #seleccionar el panel respectivo
        nb.select(0)

def extraerCambios(datos):
    return list(map(lambda dato: dato["cambio"], datos))
        
#calculos de las estadisticas
def calcularPromedio(cambios):
    return reduce(lambda suma, cambio: suma + cambio, cambios) / len(cambios) if cambios else 0

    #funcional Pythonica
    return sum(cambios) / len(cambios) if cambios else 0

    #No funcional
    suma = 0
    if cambios:
        for cambio in cambios:
            suma += cambio
    return suma / len(cambios)

def calcularDesviacionEstandar(cambios):
    promedio = calcularPromedio(cambios)
    return math.sqrt(reduce(lambda suma, cambio: suma + (cambio-promedio)**2, cambios, 0) / len(cambios) if cambios else 0)

    #No funcional
    desviacion = 0
    if cambios:
        promedio = calcularPromedio(cambios)
        suma = 0
        for cambio in cambios:
            suma += (cambio-promedio)**2
        desviacion = math.sqrt(suma / len(cambios))
    return desviacion

def calcularMaximo(cambios):
    return reduce(lambda maximo, cambio: cambio if cambio>maximo else maximo, cambios) if cambios else 0

def calcularMinimo(cambios):
    return reduce(lambda minimo, cambio: cambio if cambio<minimo else minimo ,cambios) if cambios else 0

def calcularModa(cambios):
    #hallar la frecuencia de cada dato
    frecuencias = reduce(lambda diccionarios, cambio: {**diccionarios, cambio: diccionarios.get(cambio, 0) + 1}, cambios, {}) 
    #hallar la mayor frecuencia
    frecuenciaMaxima = reduce(lambda maximo, frecuencia: frecuencia if frecuencia[1]>maximo[1] else maximo, frecuencias.items())
    return frecuenciaMaxima[0] if frecuenciaMaxima[1] > 1 else None

    #funcional Pythonica
    try:
        return mode(cambios) if cambios else 0
    except statistics.StatisticsError:
        return None

def calcularEstadisticas(moneda, desde, hasta):
    datos = obtenerDatos()
    datosFiltrados = filtrarDatos(datos, moneda, desde, hasta)
    cambios = extraerCambios(datosFiltrados)

    moda = calcularModa(cambios)
    return {
        "Promedio:" : calcularPromedio(cambios),
        "Desviación estandar:": calcularDesviacionEstandar(cambios),
        "Máximo:": calcularMaximo(cambios),
        "Mínimo:": calcularMinimo(cambios),
        "Moda:": moda if moda else "No hay moda"
        }

def mostrarEstadisticas():
    if cmbMoneda.current() >= 0:
        #obtener datos de entrada
        moneda = monedas[cmbMoneda.current()]
        desde = datetime.strptime(cldDesde.get(), "%d/%m/%Y")
        hasta = datetime.strptime(cldHasta.get(), "%d/%m/%Y")
        
        estadisticas = calcularEstadisticas(moneda, desde, hasta)
        #mostrar resultados
        for i, (clave, valor) in enumerate(estadisticas.items()):
            Util.agregarEtiqueta(paneles[1], clave, i, 0)
            Util.agregarEtiqueta(paneles[1], valor, i, 1)

        #seleccionar el panel respectivo
        nb.select(1)
        return
        

        #No funcional
        #mostrar el promedio
        Util.agregarEtiqueta(paneles[1], "Promedio:", 0, 0)
        Util.agregarEtiqueta(paneles[1], calcularPromedio(cambios), 0, 1)

        #mostrar la desviación estandar
        Util.agregarEtiqueta(paneles[1], "Desviación estandar:", 1, 0)
        Util.agregarEtiqueta(paneles[1], calcularDesviacionEstandar(cambios), 1, 1)

        #mostrar el máximo
        Util.agregarEtiqueta(paneles[1], "Máximo:", 2, 0)
        Util.agregarEtiqueta(paneles[1], calcularMaximo(cambios), 2, 1)

        #mostrar el mínimo
        Util.agregarEtiqueta(paneles[1], "Mínimo:", 3, 0)
        Util.agregarEtiqueta(paneles[1], calcularMinimo(cambios), 3, 1)

        #mostrar la moda
        moda = calcularModa(cambios)
        Util.agregarEtiqueta(paneles[1], "Moda:", 4, 0)
        Util.agregarEtiqueta(paneles[1],  moda if moda else "No hay moda"  , 4, 1)


        

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
paneles = []
for p in pestañas:
    frm = Frame(ventana)
    paneles.append(frm)
    nb.add(frm, text=p)
