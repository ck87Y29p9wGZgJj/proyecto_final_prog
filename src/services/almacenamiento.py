import json
from pathlib import Path

# Obtener la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

def cargar_datos(nombre_archivo):
    ruta = DATA_DIR / nombre_archivo
    if not ruta.exists():
        return []
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: El archivo {nombre_archivo} está dañado. Iniciando con lista vacía.")
        return []
    except Exception as e:
        print(f"Error inesperado al leer {nombre_archivo}: {e}")
        return []

def guardar_datos(nombre_archivo, datos):
    ruta = DATA_DIR / nombre_archivo
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar los datos en {nombre_archivo}: {e}")
        return False
