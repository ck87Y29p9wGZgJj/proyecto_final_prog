# SERVICIO: Doctores
# Operaciones para registrar, editar, listar y eliminar doctores

import uuid

from models.doctor import Doctor
from services.almacenamiento import cargar_modelos, guardar_datos
from services.validaciones import texto_obligatorio

# Constante con el nombre del archivo
ARCHIVO_DOCTORES = "doctores.json"


def obtener_doctores():
    # Carga y devuelve la lista de todos los doctores registrados.
    return cargar_modelos(ARCHIVO_DOCTORES, Doctor)


def _guardar_todos(doctores):
    # Convierte la lista de objetos Doctor a diccionarios y los guarda.
    lista_diccionarios = []
    for doc in doctores:
        lista_diccionarios.append(doc.to_dict())
    guardar_datos(ARCHIVO_DOCTORES, lista_diccionarios)


def registrar_doctor(nombre, especialidad):
    # Registra un nuevo doctor en el sistema.
    # Validamos los campos obligatorios
    nombre = texto_obligatorio(nombre, "El nombre")
    especialidad = texto_obligatorio(especialidad, "La especialidad")

    doctores = obtener_doctores()

    # Generamos identificador unico
    nuevo_id = str(uuid.uuid4())
    nuevo_doctor = Doctor(nuevo_id, nombre, especialidad)

    # Agregamos a la lista y guardamos
    doctores.append(nuevo_doctor)
    _guardar_todos(doctores)

    return nuevo_doctor


def actualizar_doctor(id_doctor, nombre, especialidad):
    # Modifica los datos de un doctor existente.
    id_doctor = texto_obligatorio(id_doctor, "El identificador del doctor")
    nombre = texto_obligatorio(nombre, "El nombre")
    especialidad = texto_obligatorio(especialidad, "La especialidad")

    doctores = obtener_doctores()

    # Buscamos el doctor utilizando un bucle while
    doctor_encontrado = None
    indice = 0
    while indice < len(doctores):
        if doctores[indice].id == id_doctor:
            doctor_encontrado = doctores[indice]
            break
        indice += 1

    if doctor_encontrado is None:
        raise ValueError("Doctor no encontrado.")

    # Actualizamos los valores
    doctor_encontrado.nombre = nombre
    doctor_encontrado.especialidad = especialidad

    _guardar_todos(doctores)
    return doctor_encontrado


def eliminar_doctor(id_doctor):
    # Elimina un doctor si no tiene citas medicas programadas.
    id_doctor = texto_obligatorio(id_doctor, "El identificador del doctor")
    doctores = obtener_doctores()

    doctor_a_eliminar = None
    for doc in doctores:
        if doc.id == id_doctor:
            doctor_a_eliminar = doc
            break

    if doctor_a_eliminar is None:
        raise ValueError("Doctor no encontrado.")

    # Importacion local para evitar ciclos
    from services.citas_service import obtener_citas

    citas = obtener_citas()
    # Verificamos si tiene citas asociadas
    for cita in citas:
        if cita.doctor_id == id_doctor:
            raise ValueError("No se puede eliminar el doctor porque tiene citas asociadas.")

    # Eliminamos y guardamos cambios
    doctores.remove(doctor_a_eliminar)
    _guardar_todos(doctores)

    return True
