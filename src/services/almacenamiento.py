# MODULO: Almacenamiento
# Funciones para leer y guardar datos en archivos JSON


import json
import os
from pathlib import Path

# Carpeta principal del proyecto y subcarpeta data/
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent.parent
CARPETA_DATOS = CARPETA_PROYECTO / "data"


class ErrorAlmacenamiento(Exception):
    # Excepcion personalizada para errores al leer o escribir los archivos de datos.
    pass


def _obtener_ruta(nombre_archivo):
    #Obtiene la ruta completa hacia el archivo dentro de la carpeta data/.
    # Verificamos que sea un nombre de archivo .json
    if not nombre_archivo.endswith(".json"):
        raise ValueError("El archivo de datos debe tener extension .json")
    return CARPETA_DATOS / nombre_archivo


def cargar_datos(nombre_archivo):
    #Lee y carga la lista de datos desde un archivo JSON.
    ruta = _obtener_ruta(nombre_archivo)

    # Si el archivo no existe todavia, se devuelve una lista vacia
    if not ruta.exists():
        return []

    try:
        # Abrimos el archivo en modo lectura
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ErrorAlmacenamiento(
            f"No se pudieron leer los datos de {nombre_archivo}. Revisa el archivo antes de continuar."
        )

    # Validamos que el contenido sea una lista
    if not isinstance(datos, list):
        raise ErrorAlmacenamiento(f"El contenido de {nombre_archivo} no tiene el formato esperado.")

    # Validamos que cada elemento de la lista sea un diccionario
    for registro in datos:
        if not isinstance(registro, dict):
            raise ErrorAlmacenamiento(f"El contenido de {nombre_archivo} no tiene el formato esperado.")

    return datos


def cargar_modelos(nombre_archivo, modelo_clase):
    #Carga los diccionarios y los transforma en objetos del modelo especificado.
    lista_diccionarios = cargar_datos(nombre_archivo)
    lista_objetos = []

    try:
        # Recorremos cada diccionario para convertirlo en objeto
        for item in lista_diccionarios:
            objeto = modelo_clase.from_dict(item)
            lista_objetos.append(objeto)
    except (KeyError, TypeError, ValueError) as error:
        raise ErrorAlmacenamiento(
            f"Uno de los registros de {nombre_archivo} no tiene el formato esperado."
        )

    return lista_objetos


def guardar_datos(nombre_archivo, datos):
    #Guarda una lista de datos en el archivo JSON correspondiente.
    ruta = _obtener_ruta(nombre_archivo)

    # Validamos que sea una lista
    if not isinstance(datos, list):
        raise ValueError("Los datos a guardar deben ser una lista de registros.")

    try:
        # Nos aseguramos de que la carpeta data exista
        CARPETA_DATOS.mkdir(parents=True, exist_ok=True)

        # Abrimos el archivo en modo escritura y guardamos el JSON formateado
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
            archivo.write("\n")
    except (OSError, TypeError, ValueError) as error:
        raise ErrorAlmacenamiento(f"No se pudieron guardar los datos en {nombre_archivo}.")
