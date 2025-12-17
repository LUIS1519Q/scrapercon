import pandas as pd
import requests
import re
from collections import Counter

# ==========================================
# CONFIGURACIÓN GLOBAL
# ==========================================
URL = "https://books.toscrape.com/"  # <-- CAMBIA AQUÍ LA URL REAL
ARCHIVO_SALIDA = "datos_web_estatica.xlsx"

# ==========================================
# PASO 1: SCRAPING DE WEB ESTÁTICA
# ==========================================
def scrapear_web_estatica():
    """
    Descarga una página web estática y extrae su primera tabla HTML.
    """
    print(f"Conectando a {URL}...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    # Extrae todas las tablas HTML
    tablas = pd.read_html(response.text)

    print(f"Se encontraron {len(tablas)} tablas")

    # Tomamos la primera tabla (la principal)
    df = tablas[0]

    return df


# ==========================================
# PASO 2: GUARDAR Y ANALIZAR
# ==========================================
def analisis_y_guardado(df):
    """
    Guarda los datos en Excel y analiza las palabras más repetidas.
    """
    if df is None:
        print("No hay datos para procesar")
        return []

    # Guardar Excel
    df.to_excel(ARCHIVO_SALIDA, index=False)
    print(f"Archivo guardado como {ARCHIVO_SALIDA}")

    # Tomamos la primera columna como texto principal
    columna_texto = df.iloc[:, 0]

    print("\n--- Analizando palabras ---")

    texto = " ".join(columna_texto.astype(str))
    palabras = re.findall(r"\b[a-zA-Z]{4,}\b", texto.lower())

    conteo = Counter(palabras)
    top_palabras = conteo.most_common(5)

    print("Top 5 palabras más repetidas:")
    for palabra, freq in top_palabras:
        print(f"- {palabra}: {freq}")

    return [p[0] for p in top_palabras]


# ==========================================
# PASO 3: GENERAR FRASES EN ESPAÑOL
# ==========================================
def generar_nuevas_frases(palabras):
    """
    Genera 5 frases nuevas en español usando palabras frecuentes.
    """
    print("\n--- 5 Frases Nuevas (Español) ---")

    plantillas = [
        "El concepto de '{}' es fundamental en la sociedad actual.",
        "La historia demuestra que '{}' siempre ha sido importante.",
        "No puede existir progreso sin '{}'.",
        "Desde tiempos antiguos, '{}' ha guiado al ser humano.",
        "Reflexionar sobre '{}' nos ayuda a crecer."
    ]

    while len(palabras) < 5:
        palabras.append("conocimiento")

    for i in range(5):
        print(f"{i+1}. {plantillas[i].format(palabras[i])}")


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    df = scrapear_web_estatica()
    palabras_top = analisis_y_guardado(df)
    generar_nuevas_frases(palabras_top)
