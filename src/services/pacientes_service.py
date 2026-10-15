# SERVICIO: Pacientes
# Operaciones para registrar, editar, listar y eliminar pacientes

import uuid

from models.paciente import Paciente
from services.almacenamiento import cargar_modelos, guardar_datos
from services.validaciones import texto_obligatorio, texto_opcional

# Constante con el nombre del archivo
ARCHIVO_PACIENTES = "pacientes.json"


def obtener_pacientes():
    # Carga y devuelve la lista de todos los pacientes registrados.
    return cargar_modelos(ARCHIVO_PACIENTES, Paciente)


def _guardar_todos(pacientes):
    # Convierte la lista de objetos Paciente a diccionarios y los guarda.
    lista_diccionarios = []
    for p in pacientes:
        lista_diccionarios.append(p.to_dict())
    guardar_datos(ARCHIVO_PACIENTES, lista_diccionarios)


def registrar_paciente(nombre, identificacion, telefono=""):
    # Registra un nuevo paciente validando que la identificacion no se repita.
    # Validamos las entradas
    nombre = texto_obligatorio(nombre, "El nombre")
    identificacion = texto_obligatorio(identificacion, "La identificación")
    telefono = texto_opcional(telefono)

    pacientes = obtener_pacientes()

    # Verificamos si la identificacion ya existe utilizando un bucle while
    indice = 0
    while indice < len(pacientes):
        if pacientes[indice].identificacion == identificacion:
            raise ValueError("Ya existe un paciente con esa identificación.")
        indice += 1

    # Generamos un id unico para el paciente
    nuevo_id = str(uuid.uuid4())
    nuevo_paciente = Paciente(nuevo_id, nombre, identificacion, telefono)

    # Agregamos a la lista y guardamos
    pacientes.append(nuevo_paciente)
    _guardar_todos(pacientes)

    return nuevo_paciente


def actualizar_paciente(id_paciente, nombre, identificacion, telefono=""):
    # Modifica la informacion de un paciente existente.
    id_paciente = texto_obligatorio(id_paciente, "El identificador del paciente")
    nombre = texto_obligatorio(nombre, "El nombre")
    identificacion = texto_obligatorio(identificacion, "La identificación")
    telefono = texto_opcional(telefono)

    pacientes = obtener_pacientes()

    # Buscamos al paciente por su id
    paciente_a_modificar = None
    for p in pacientes:
        if p.id == id_paciente:
            paciente_a_modificar = p
            break

    if paciente_a_modificar is None:
        raise ValueError("Paciente no encontrado.")

    # Verificamos que la nueva identificacion no le pertenezca a otro paciente
    for otro in pacientes:
        if otro.id != id_paciente and otro.identificacion == identificacion:
            raise ValueError("La identificación ya está registrada en otro paciente.")

    # Actualizamos los campos
    paciente_a_modificar.nombre = nombre
    paciente_a_modificar.identificacion = identificacion
    paciente_a_modificar.telefono = telefono

    _guardar_todos(pacientes)
    return paciente_a_modificar


def eliminar_paciente(id_paciente):
    # Elimina un paciente si existe y no tiene citas medicas agendadas.
    id_paciente = texto_obligatorio(id_paciente, "El identificador del paciente")
    pacientes = obtener_pacientes()

    # Buscamos el paciente
    paciente_a_eliminar = None
    for p in pacientes:
        if p.id == id_paciente:
            paciente_a_eliminar = p
            break

    if paciente_a_eliminar is None:
        raise ValueError("Paciente no encontrado.")

    # Importamos localmente para evitar dependencias circulares
    from services.citas_service import obtener_citas

    citas = obtener_citas()
    # Comprobamos si tiene citas asociadas
    for cita in citas:
        if cita.paciente_id == id_paciente:
            raise ValueError("No se puede eliminar el paciente porque tiene citas asociadas.")

    # Si no tiene citas, procedemos a eliminarlo
    pacientes.remove(paciente_a_eliminar)
    _guardar_todos(pacientes)

    return True
