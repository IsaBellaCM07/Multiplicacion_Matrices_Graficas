import os
import csv
import matplotlib.pyplot as plt

# Función para leer los archivos CSV
def leer_tiempos_csv(archivo_csv):
    tiempos = {}
    with open(archivo_csv, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la cabecera
        for row in reader:
            algoritmo, tiempo = row[0], float(row[1])
            tiempos[algoritmo] = tiempo  # Guardar el tiempo del algoritmo
    return tiempos

# Función para crear y guardar gráficos de barras
def crear_diagrama_barras(tiempos, archivo_salida, tamano_matriz):
    plt.figure(figsize=(10, 6))
    algoritmos = list(tiempos.keys())
    tiempos_valores = list(tiempos.values())

    barras = plt.bar(algoritmos, tiempos_valores, color='darkorchid')

    for barra, tiempo in zip(barras, tiempos_valores):
        plt.text(barra.get_x() + barra.get_width() / 2, barra.get_height() + (barra.get_height() * 0.01), f'{tiempo:.5f}', ha='center', va='bottom', fontsize=10)

    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Algoritmos')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.ylim(bottom=0)
    plt.title(f'Tiempo de ejecución para matrices de tamaño {tamano_matriz}x{tamano_matriz}')
    plt.subplots_adjust(bottom=0.2, top=0.9)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(archivo_salida)
    plt.close()

# Función para crear y guardar gráficos lineales comparativos
def crear_diagrama_lineal_comparativo(tiempos_python, tiempos_go, tamano_matriz, archivo_salida):
    plt.figure(figsize=(10, 6))

    algoritmos = list(tiempos_python.keys())
    tiempos_python_valores = [tiempos_python[alg] for alg in algoritmos]
    tiempos_go_valores = [tiempos_go[alg] for alg in algoritmos]

    plt.plot(algoritmos, tiempos_python_valores, marker='o', linestyle='-', color='green', label='Python')
    plt.plot(algoritmos, tiempos_go_valores, marker='o', linestyle='-', color='purple', label='Go')

    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Algoritmos')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.title(f'Comparación de tiempos para matrices de tamaño {tamano_matriz}x{tamano_matriz}')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.subplots_adjust(bottom=0.2, top=0.9)
    plt.savefig(archivo_salida)
    plt.close()

# Función para crear y guardar los archivos CSV comparativos
def crear_csv_comparativo(tiempos_python, tiempos_go, archivo_salida, tamano_matriz):
    with open(archivo_salida, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Algoritmo", "Python", "Go"])

        for algoritmo in tiempos_python:
            python_tiempo = tiempos_python.get(algoritmo, 'N/A')
            go_tiempo = tiempos_go.get(algoritmo, 'N/A')
            writer.writerow([algoritmo, python_tiempo, go_tiempo])

# Directorios
directorio_python = 'tiempos/tiempos_python'
directorio_go = 'tiempos/tiempos_go'
directorio_graficos_python = 'graficos/graficos_python'
directorio_graficos_go = 'graficos/graficos_go'
directorio_graficos_comparativos = 'graficos/graficos_comparativos'
directorio_comparativos = 'tiempos/tiempos_comparativos'

# Tamaños de matrices
tamano_matriz = [2 ** i for i in range(1, 9)]

# Crear directorios
os.makedirs(directorio_graficos_python, exist_ok=True)
os.makedirs(directorio_graficos_go, exist_ok=True)
os.makedirs(directorio_graficos_comparativos, exist_ok=True)
os.makedirs(directorio_comparativos, exist_ok=True)

# Procesar archivos para generar gráficos y CSV comparativos
for n in tamano_matriz:
    archivo_csv_python = os.path.join(directorio_python, f"tiempos_ejecucion_{n}.csv")
    archivo_csv_go = os.path.join(directorio_go, f"tiempos_{n}.csv")

    if os.path.exists(archivo_csv_python) and os.path.exists(archivo_csv_go):
        tiempos_python = leer_tiempos_csv(archivo_csv_python)
        tiempos_go = leer_tiempos_csv(archivo_csv_go)

        archivo_salida_python = os.path.join(directorio_graficos_python, f"grafico_python_{n}.png")
        crear_diagrama_barras(tiempos_python, archivo_salida_python, n)

        archivo_salida_go = os.path.join(directorio_graficos_go, f"grafico_go_{n}.png")
        crear_diagrama_barras(tiempos_go, archivo_salida_go, n)

        archivo_comparativo = os.path.join(directorio_comparativos, f"tiempo_comparativo_{n}.csv")
        crear_csv_comparativo(tiempos_python, tiempos_go, archivo_comparativo, n)

        archivo_grafico_comparativo = os.path.join(directorio_graficos_comparativos, f"grafico_comparativo_{n}.png")
        crear_diagrama_lineal_comparativo(tiempos_python, tiempos_go, n, archivo_grafico_comparativo)

# Procesar promedios
archivo_promedio_python = os.path.join(directorio_python, "tiempos_ejecucion_promedio.csv")
archivo_promedio_go = os.path.join(directorio_go, "tiempo_promedio.csv")
archivo_comparativo_promedio = os.path.join(directorio_comparativos, "tiempo_comparativo_promedio.csv")
archivo_grafico_comparativo_promedio = os.path.join(directorio_graficos_comparativos, "grafico_comparativo_promedio.png")

if os.path.exists(archivo_promedio_python) and os.path.exists(archivo_promedio_go):
    tiempos_promedio_python = leer_tiempos_csv(archivo_promedio_python)
    tiempos_promedio_go = leer_tiempos_csv(archivo_promedio_go)

    archivo_grafico_python_promedio = os.path.join(directorio_graficos_python, "grafico_python_promedio.png")
    crear_diagrama_barras(tiempos_promedio_python, archivo_grafico_python_promedio, "Promedio")

    archivo_grafico_go_promedio = os.path.join(directorio_graficos_go, "grafico_go_promedio.png")
    crear_diagrama_barras(tiempos_promedio_go, archivo_grafico_go_promedio, "Promedio")

    crear_csv_comparativo(tiempos_promedio_python, tiempos_promedio_go, archivo_comparativo_promedio, "Promedio")
    crear_diagrama_lineal_comparativo(tiempos_promedio_python, tiempos_promedio_go, "Promedio", archivo_grafico_comparativo_promedio)


print("Gráficos de barras, lineales comparativos y promedios generados exitosamente.")