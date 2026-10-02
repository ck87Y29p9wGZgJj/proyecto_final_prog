import uuid
from models.paciente import Paciente
from services.almacenamiento import cargar_datos, guardar_datos

ARCHIVO = "pacientes.json"

def obtener_pacientes():
    datos = cargar_datos(ARCHIVO)
    return [Paciente.from_dict(d) for d in datos]

def _guardar_todos(pacientes):
    datos = [p.to_dict() for p in pacientes]
    return guardar_datos(ARCHIVO, datos)

def registrar_paciente(nombre, identificacion, telefono):
    if not nombre or not identificacion:
        raise ValueError("El nombre y la identificación son obligatorios.")

    pacientes = obtener_pacientes()
    
    if any(p.identificacion == identificacion for p in pacientes):
        raise ValueError(f"Ya existe un paciente con la identificación {identificacion}.")
        
    nuevo_id = str(uuid.uuid4())
    nuevo_paciente = Paciente(nuevo_id, nombre, identificacion, telefono)
    pacientes.append(nuevo_paciente)
    
    _guardar_todos(pacientes)
    return nuevo_paciente

def actualizar_paciente(id_paciente, nombre, identificacion, telefono):
    if not nombre or not identificacion:
        raise ValueError("El nombre y la identificación son obligatorios.")

    pacientes = obtener_pacientes()
    for p in pacientes:
        if p.id == id_paciente:
            # Si cambia la identificación, revisar que no choque con otro paciente
            if p.identificacion != identificacion and any(otro.identificacion == identificacion for otro in pacientes):
                raise ValueError("La nueva identificación ya está registrada en otro paciente.")
                
            p.nombre = nombre
            p.identificacion = identificacion
            p.telefono = telefono
            _guardar_todos(pacientes)
            return p
            
    raise ValueError("Paciente no encontrado.")

def eliminar_paciente(id_paciente):
    pacientes = obtener_pacientes()
    pacientes_nuevos = [p for p in pacientes if p.id != id_paciente]
    
    if len(pacientes) == len(pacientes_nuevos):
        raise ValueError("Paciente no encontrado.")
    
    # Pendiente: Validar que no tenga citas asignadas antes de borrarlo (se hará al integrar citas)
    _guardar_todos(pacientes_nuevos)
    return True
