import pandas as pd
import re

def procesar_excel(nombre_archivo):
    # Leer el archivo Excel sin encabezados y asegurando que los valores se mantengan como texto
    df = pd.read_excel(nombre_archivo, engine='openpyxl', header=None, dtype=str)

    # Extraer el valor de la celda F4 y limpiar el nombre del archivo
    nombre_salida = str(df.iloc[3, 5]).strip()  # Convertir a string y limpiar espacios
    if nombre_salida.isnumeric():
        nombre_salida = f"archivo_{nombre_salida}"  # Evitar que sea solo un número
    nombre_salida = re.sub(r'[\/:*?"<>|]', '_', nombre_salida)  # Eliminar caracteres inválidos

    # Remover las primeras 8 filas y resetear el índice
    df = df.iloc[8:].reset_index(drop=True)

    # Ahora aseguramos que comenzamos en la fila 10 (índice 9 en Pandas)
    df = df.iloc[1:].reset_index(drop=True)  # Elimina una fila adicional para llegar a la fila 10

    # Seleccionar solo las columnas D y E (índices 3 y 4)
    df = df.iloc[:, [3, 4]]
    df.columns = ["Débito", "Ingreso"]  # Renombrar

    # Convertir celdas vacías a NaN para poder filtrar correctamente
    df = df.replace(r'^\s*$', pd.NA, regex=True)  

    # Encontrar la primera fila donde ambas columnas son NaN y detenerse ahí
    for index, row in df.iterrows():
        if pd.isna(row["Débito"]) and pd.isna(row["Ingreso"]):  # Ambas columnas vacías
            df = df.iloc[:index]  # Solo tomar filas hasta antes de la primera vacía
            break

    # Si después del filtrado no queda nada, avisar
    if df.empty:
        print("No se encontraron datos válidos después de la fila 10.")
        return

    # Guardar el resultado en CSV con formato adecuado (manteniendo los números con puntos y ceros intactos)
    nombre_csv = f"{nombre_salida}.csv"
    df.to_csv(nombre_csv, sep=";", index=False, encoding="utf-8", quotechar='"')

    print(f"Archivo guardado como: {nombre_csv}")

# Ejecutar la función con un archivo de prueba
procesar_excel("archivo.xlsx")
