import uuid
from models.doctor import Doctor
from services.almacenamiento import cargar_datos, guardar_datos

ARCHIVO = "doctores.json"

def obtener_doctores():
    datos = cargar_datos(ARCHIVO)
    return [Doctor.from_dict(d) for d in datos]

def _guardar_todos(doctores):
    datos = [d.to_dict() for d in doctores]
    return guardar_datos(ARCHIVO, datos)

def registrar_doctor(nombre, especialidad):
    if not nombre or not especialidad:
        raise ValueError("El nombre y la especialidad son obligatorios.")

    doctores = obtener_doctores()
    
    nuevo_id = str(uuid.uuid4())
    nuevo_doctor = Doctor(nuevo_id, nombre, especialidad)
    doctores.append(nuevo_doctor)
    
    _guardar_todos(doctores)
    return nuevo_doctor

def actualizar_doctor(id_doctor, nombre, especialidad):
    if not nombre or not especialidad:
        raise ValueError("El nombre y la especialidad son obligatorios.")

    doctores = obtener_doctores()
    for d in doctores:
        if d.id == id_doctor:
            d.nombre = nombre
            d.especialidad = especialidad
            _guardar_todos(doctores)
            return d
            
    raise ValueError("Doctor no encontrado.")

def eliminar_doctor(id_doctor):
    doctores = obtener_doctores()
    doctores_nuevos = [d for d in doctores if d.id != id_doctor]
    
    if len(doctores) == len(doctores_nuevos):
        raise ValueError("Doctor no encontrado.")
    
    # Pendiente: Validar que no tenga citas asignadas antes de borrarlo
    _guardar_todos(doctores_nuevos)
    return True
