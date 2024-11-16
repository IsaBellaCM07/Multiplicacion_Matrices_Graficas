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

    # Generar el diagrama de barras
    barras = plt.bar(algoritmos, tiempos_valores, color='darkorchid')

    # Agregar etiquetas encima de las barras con 5 decimales
    for barra, tiempo in zip(barras, tiempos_valores):
        plt.text(barra.get_x() + barra.get_width() / 2,  # Posición en x
                 barra.get_height() + (barra.get_height() * 0.01),  # Posición en y con un pequeño margen
                 f'{tiempo:.5f}',  # Texto con 5 decimales
                 ha='center', va='bottom', fontsize=10)

    # Configuración de los ejes y la gráfica
    plt.xticks(rotation=45, ha='right')  # Rotar etiquetas para mejor visibilidad
    plt.xlabel('Algoritmos')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.ylim(bottom=0)
    plt.title(f'Tiempo de ejecución para matrices de tamaño {tamano_matriz}x{tamano_matriz}')

    # Ajustar los márgenes para acomodar las etiquetas
    plt.subplots_adjust(bottom=0.2, top=0.9)  # Espacio adicional inferior y superior
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(archivo_salida)
    plt.close()

# Función para crear y guardar gráficos lineales comparativos
def crear_diagrama_lineal_comparativo(tiempos_python, tiempos_go, tamano_matriz, archivo_salida):
    plt.figure(figsize=(10, 6))

    algoritmos = list(tiempos_python.keys())
    tiempos_python_valores = [tiempos_python[alg] for alg in algoritmos]
    tiempos_go_valores = [tiempos_go[alg] for alg in algoritmos]

    # Generar líneas para Python y Go
    plt.plot(algoritmos, tiempos_python_valores, marker='o', linestyle='-', color='green', label='Python')
    plt.plot(algoritmos, tiempos_go_valores, marker='o', linestyle='-', color='purple', label='Go')

    # Configurar etiquetas
    plt.xticks(rotation=45, ha='right')  # Rotar etiquetas para mejor visibilidad
    plt.xlabel('Algoritmos')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.title(f'Comparación de tiempos para matrices de tamaño {tamano_matriz}x{tamano_matriz}')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Ajustar márgenes para acomodar etiquetas
    plt.subplots_adjust(bottom=0.2, top=0.9)
    plt.savefig(archivo_salida)
    plt.close()

# Función para crear y guardar los archivos CSV comparativos
def crear_csv_comparativo(tiempos_python, tiempos_go, archivo_salida, tamano_matriz):
    with open(archivo_salida, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Algoritmo", "Python", "Go"])  # Cabecera

        # Escribir los tiempos de ejecución para cada algoritmo
        for algoritmo in tiempos_python:
            python_tiempo = tiempos_python.get(algoritmo, 'N/A')
            go_tiempo = tiempos_go.get(algoritmo, 'N/A')
            writer.writerow([algoritmo, python_tiempo, go_tiempo])

# Directorios de entrada y salida
directorio_python = 'tiempos/tiempos_python'  # Ruta de los CSV generados por el proyecto Python
directorio_go = 'tiempos/tiempos_go'  # Ruta de los CSV generados por el proyecto Go
directorio_graficos_python = 'graficos/graficos_python'  # Carpeta donde se guardarán los gráficos de Python
directorio_graficos_go = 'graficos/graficos_go'  # Carpeta donde se guardarán los gráficos de Go
directorio_graficos_comparativos = 'graficos/graficos_comparativos'  # Carpeta de gráficos comparativos
directorio_comparativos = 'tiempos/tiempos_comparativos'  # Carpeta donde se guardarán los CSV comparativos

# Tamaños de matrices
tamano_matriz = [2 ** i for i in range(1, 9)]  # Tamaños: 2^1, 2^2, ..., 2^8

# Crear carpetas de gráficos y comparativos si no existen
os.makedirs(directorio_graficos_python, exist_ok=True)
os.makedirs(directorio_graficos_go, exist_ok=True)
os.makedirs(directorio_graficos_comparativos, exist_ok=True)
os.makedirs(directorio_comparativos, exist_ok=True)

# Procesar los archivos CSV para generar gráficos y CSV comparativos
for n in tamano_matriz:
    archivo_csv_python = os.path.join(directorio_python, f"tiempos_ejecucion_{n}.csv")
    archivo_csv_go = os.path.join(directorio_go, f"tiempos_{n}.csv")

    if os.path.exists(archivo_csv_python) and os.path.exists(archivo_csv_go):
        tiempos_python = leer_tiempos_csv(archivo_csv_python)
        tiempos_go = leer_tiempos_csv(archivo_csv_go)

        # Generar gráficos para Python y Go
        archivo_salida_python = os.path.join(directorio_graficos_python, f"grafico_python_{n}.png")
        crear_diagrama_barras(tiempos_python, archivo_salida_python, n)

        archivo_salida_go = os.path.join(directorio_graficos_go, f"grafico_go_{n}.png")
        crear_diagrama_barras(tiempos_go, archivo_salida_go, n)

        # Crear archivo CSV comparativo
        archivo_comparativo = os.path.join(directorio_comparativos, f"tiempo_comparativo_{n}.csv")
        crear_csv_comparativo(tiempos_python, tiempos_go, archivo_comparativo, n)

        # Generar gráfico comparativo lineal
        archivo_grafico_comparativo = os.path.join(directorio_graficos_comparativos, f"grafico_comparativo_{n}.png")
        crear_diagrama_lineal_comparativo(tiempos_python, tiempos_go, n, archivo_grafico_comparativo)

print("Gráficos de barras y lineales comparativos generados exitosamente.")
