import uuid
from models.cita import Cita
from services.almacenamiento import cargar_datos, guardar_datos
from services.doctores_service import obtener_doctores
from services.pacientes_service import obtener_pacientes

ARCHIVO = "citas.json"

def obtener_citas():
    datos = cargar_datos(ARCHIVO)
    return [Cita.from_dict(d) for d in datos]

def _guardar_todas(citas):
    datos = [c.to_dict() for c in citas]
    return guardar_datos(ARCHIVO, datos)

def registrar_cita(paciente_id, doctor_id, fecha, hora):
    if not fecha or not hora:
        raise ValueError("La fecha y la hora son obligatorias.")

    # Validar que paciente y doctor existan
    pacientes = obtener_pacientes()
    if not any(p.id == paciente_id for p in pacientes):
        raise ValueError("El paciente seleccionado no existe.")
        
    doctores = obtener_doctores()
    if not any(d.id == doctor_id for d in doctores):
        raise ValueError("El doctor seleccionado no existe.")
        
    citas = obtener_citas()
    
    # Regla principal: El doctor no puede tener otra cita en la misma fecha y hora
    for c in citas:
        if c.doctor_id == doctor_id and c.fecha == fecha and c.hora == hora:
            raise ValueError("Horario no disponible: el doctor ya tiene una cita reservada para esta fecha y hora exacta.")
            
    nuevo_id = str(uuid.uuid4())
    nueva_cita = Cita(nuevo_id, paciente_id, doctor_id, fecha, hora)
    citas.append(nueva_cita)
    
    _guardar_todas(citas)
    return nueva_cita

def eliminar_cita(id_cita):
    citas = obtener_citas()
    citas_nuevas = [c for c in citas if c.id != id_cita]
    
    if len(citas) == len(citas_nuevas):
        raise ValueError("Cita no encontrada.")
        
    _guardar_todas(citas_nuevas)
    return True

def obtener_citas_del_dia(fecha_hoy):
    return [c for c in obtener_citas() if c.fecha == fecha_hoy]

def obtener_citas_por_doctor(doctor_id):
    return [c for c in obtener_citas() if c.doctor_id == doctor_id]
