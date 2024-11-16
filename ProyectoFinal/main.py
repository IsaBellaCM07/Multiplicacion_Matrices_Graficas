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

# Función para crear y guardar gráficos lineales comparativos
def crear_diagrama_lineal_comparativo(tiempos_python, tiempos_go, archivo_salida):
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
    plt.ylabel('Tiempo promedio de ejecución (segundos)')
    plt.title('Comparación de tiempos promedio entre Python y Go')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Ajustar márgenes para acomodar etiquetas
    plt.subplots_adjust(bottom=0.2, top=0.9)
    plt.savefig(archivo_salida)
    plt.close()

# Función para crear y guardar el archivo CSV comparativo
def crear_csv_comparativo_promedio(tiempos_python, tiempos_go, archivo_salida):
    with open(archivo_salida, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Algoritmo", "Python", "Go"])  # Cabecera

        # Escribir los tiempos promedio para cada algoritmo
        for algoritmo in tiempos_python:
            python_tiempo = tiempos_python.get(algoritmo, 'N/A')
            go_tiempo = tiempos_go.get(algoritmo, 'N/A')
            writer.writerow([algoritmo, python_tiempo, go_tiempo])

# Directorios de entrada y salida
directorio_python = 'tiempos/tiempos_python'
directorio_go = 'tiempos/tiempos_go'
directorio_comparativos = 'tiempos/tiempos_comparativos'
directorio_graficos_comparativos = 'graficos/graficos_comparativos'

# Crear carpetas si no existen
os.makedirs(directorio_comparativos, exist_ok=True)
os.makedirs(directorio_graficos_comparativos, exist_ok=True)

# Archivos CSV de promedio
archivo_promedio_python = os.path.join(directorio_python, "tiempos_ejecucion_promedio.csv")
archivo_promedio_go = os.path.join(directorio_go, "tiempo_promedio.csv")

# Procesar y generar comparativo
if os.path.exists(archivo_promedio_python) and os.path.exists(archivo_promedio_go):
    tiempos_python = leer_tiempos_csv(archivo_promedio_python)
    tiempos_go = leer_tiempos_csv(archivo_promedio_go)

    # Crear archivo CSV comparativo de tiempos promedio
    archivo_comparativo_promedio = os.path.join(directorio_comparativos, "tiempo_comparativo_promedio.csv")
    crear_csv_comparativo_promedio(tiempos_python, tiempos_go, archivo_comparativo_promedio)

    # Crear gráfico lineal comparativo de tiempos promedio
    archivo_grafico_promedio = os.path.join(directorio_graficos_comparativos, "grafico_comparativo_promedio.png")
    crear_diagrama_lineal_comparativo(tiempos_python, tiempos_go, archivo_grafico_promedio)

    print("Archivo CSV y gráfico comparativo de tiempos promedio generados exitosamente.")
else:
    print("No se encontraron los archivos de tiempo promedio para Python o Go.")
