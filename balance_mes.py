import pandas as pd
from decimal import Decimal, InvalidOperation

def convertir_a_decimal(valor):
    """Convierte un valor a Decimal asegurando que los puntos sean solo decimales, no separadores de miles."""
    try:
        if isinstance(valor, str):
            valor = valor.strip()  # Eliminar espacios extra
            valor = valor.replace(".", "")  # Eliminar separadores de miles
            valor = valor.replace(",", ".")  # Convertir decimales de , a .
        
        # Si la celda está vacía o tiene valores no numéricos, devolver 0
        return Decimal(valor) if valor else Decimal("0")

    except (InvalidOperation, AttributeError):
        return Decimal("0")

def calcular_balance(nombre_csv):
    # Leer el archivo CSV como texto para evitar que pandas modifique los números
    df = pd.read_csv(nombre_csv, sep=";", dtype=str)

    # Convertir las columnas usando la función segura
    df["Débito"] = df["Débito"].apply(convertir_a_decimal)
    df["Ingreso"] = df["Ingreso"].apply(convertir_a_decimal)

    # Calcular sumas (sumar todo directamente ya que Débito es negativo)
    balance_final = sum(df["Débito"]) + sum(df["Ingreso"])

    # Mostrar resultados sin decimales
    print(f"Archivo procesado: {nombre_csv}")
    print(f"Total Débito: {int(sum(df['Débito'])):,}")  # Convertir a entero y formatear
    print(f"Total Ingreso: {int(sum(df['Ingreso'])):,}")  # Convertir a entero y formatear
    print(f"Balance Final: {int(balance_final):,}")  # Convertir a entero y formatear

# Ejecutar la función con el archivo CSV generado previamente
calcular_balance("05_2024.csv")
