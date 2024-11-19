import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox

# Función para descargar y procesar los datos
def obtener_datos():
    activos = entry_activos.get().split(',')
    fecha_inicio = entry_inicio.get()
    fecha_fin = entry_fin.get()

    if not activos or len(activos) < 2:
        messagebox.showerror("Error", "Por favor ingrese al menos dos activos separados por coma.")
        return

    try:
        # Descargar datos
        datos = yf.download(activos, start=fecha_inicio, end=fecha_fin)['Adj Close']
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al descargar los datos: {e}")
        return

    if datos.empty:
        messagebox.showerror("Error", "No se encontraron datos para los activos ingresados o las fechas seleccionadas.")
        return

    # Cálculo de los rendimientos
    rendimientos = datos.pct_change().dropna()

    # Peso de los activos (puede ser modificado)
    pesos = np.array([1 / len(activos)] * len(activos))

    # Cálculo de la volatilidad del portafolio
    var_portafolio = np.dot(pesos.T, np.dot(rendimientos.cov() * 252, pesos))
    volatilidad_portafolio = np.sqrt(var_portafolio)

    # Mostrar resultado en la interfaz gráfica
    label_volatilidad.config(text=f"Volatilidad del portafolio: {volatilidad_portafolio:.2%}")

    # Mostrar gráfico de rendimientos acumulados
    rendimientos_acumulados = (1 + rendimientos).cumprod() - 1
    plt.figure(figsize=(10, 6))

    for activo in rendimientos_acumulados.columns:
        plt.plot(rendimientos_acumulados.index, rendimientos_acumulados[activo], label=activo)

    plt.title('Rendimientos Acumulativos de los Activos')
    plt.xlabel('Fecha')
    plt.ylabel('Rendimiento Acumulado')
    plt.legend()
    plt.grid(True)
    plt.show()

# Configuración de la interfaz gráfica
ventana = Tk()
ventana.title("Calculadora de Volatilidad de Portafolio")

# Etiquetas y campos de entrada
label_activos = Label(ventana, text="Ingrese los activos (separados por coma):")
label_activos.pack()

entry_activos = Entry(ventana, width=50)
entry_activos.pack()

label_inicio = Label(ventana, text="Fecha de inicio (YYYY-MM-DD):")
label_inicio.pack()

entry_inicio = Entry(ventana, width=20)
entry_inicio.pack()

label_fin = Label(ventana, text="Fecha de fin (YYYY-MM-DD):")
label_fin.pack()

entry_fin = Entry(ventana, width=20)
entry_fin.pack()

# Botón para calcular
boton_calcular = Button(ventana, text="Calcular Volatilidad", command=obtener_datos)
boton_calcular.pack()

# Etiqueta para mostrar la volatilidad
label_volatilidad = Label(ventana, text="Volatilidad del portafolio:")
label_volatilidad.pack()

# Iniciar la ventana
ventana.mainloop()
