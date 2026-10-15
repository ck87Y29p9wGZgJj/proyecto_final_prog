# SERVICIO: Citas
# Operaciones para agendar, editar, cancelar y buscar citas medicas

import uuid

from models.cita import Cita
from services.almacenamiento import cargar_modelos, guardar_datos
from services.doctores_service import obtener_doctores
from services.pacientes_service import obtener_pacientes
from services.validaciones import texto_obligatorio, validar_fecha, validar_hora

# Constante con el nombre del archivo
ARCHIVO_CITAS = "citas.json"


def obtener_citas():
    # Devuelve la lista de todas las citas guardadas.
    return cargar_modelos(ARCHIVO_CITAS, Cita)


def _guardar_todas(citas):
    # Convierte la lista de objetos Cita a diccionarios y los guarda en el JSON.
    lista_diccionarios = []
    for c in citas:
        lista_diccionarios.append(c.to_dict())
    guardar_datos(ARCHIVO_CITAS, lista_diccionarios)


def _validar_existencia_paciente_y_doctor(paciente_id, doctor_id):
    # Comprueba que tanto el paciente como el doctor existan en el sistema.
    pacientes = obtener_pacientes()
    doctores = obtener_doctores()

    # Buscamos si existe el paciente
    paciente_encontrado = False
    for p in pacientes:
        if p.id == paciente_id:
            paciente_encontrado = True
            break
    if not paciente_encontrado:
        raise ValueError("El paciente seleccionado no existe.")

    # Buscamos si existe el doctor
    doctor_encontrado = False
    for d in doctores:
        if d.id == doctor_id:
            doctor_encontrado = True
            break
    if not doctor_encontrado:
        raise ValueError("El doctor seleccionado no existe.")


def _validar_disponibilidad_horario(citas, doctor_id, fecha, hora, excluir_id=None):
    # Verifica que el doctor no tenga otra cita agendada en la misma fecha y hora.
    # Si se pasa excluir_id (al editar), no se compara contra la misma cita.
    for cita in citas:
        # Si estamos editando, ignoramos la misma cita
        if cita.id != excluir_id:
            # Comparamos doctor, fecha y hora con operadores logicos
            if cita.doctor_id == doctor_id and cita.fecha == fecha and cita.hora == hora:
                raise ValueError(
                    "Horario no disponible: el doctor ya tiene una cita en esa fecha y hora."
                )


def registrar_cita(paciente_id, doctor_id, fecha, hora):
    # Agenda una nueva cita médica.
    # Validaciones de entrada
    paciente_id = texto_obligatorio(paciente_id, "El paciente")
    doctor_id = texto_obligatorio(doctor_id, "El doctor")
    fecha = validar_fecha(fecha)
    hora = validar_hora(hora)

    # Validamos que el paciente y doctor existan
    _validar_existencia_paciente_y_doctor(paciente_id, doctor_id)

    citas = obtener_citas()

    # Validamos que el doctor este disponible en ese horario
    _validar_disponibilidad_horario(citas, doctor_id, fecha, hora)

    # Creamos la nueva cita
    nuevo_id = str(uuid.uuid4())
    nueva_cita = Cita(nuevo_id, paciente_id, doctor_id, fecha, hora)

    # Agregamos y guardamos
    citas.append(nueva_cita)
    _guardar_todas(citas)

    return nueva_cita


def actualizar_cita(id_cita, paciente_id, doctor_id, fecha, hora):
    # Edita una cita existente.
    id_cita = texto_obligatorio(id_cita, "El identificador de la cita")
    paciente_id = texto_obligatorio(paciente_id, "El paciente")
    doctor_id = texto_obligatorio(doctor_id, "El doctor")
    fecha = validar_fecha(fecha)
    hora = validar_hora(hora)

    citas = obtener_citas()

    # Buscamos la cita por su id
    cita_encontrada = None
    for c in citas:
        if c.id == id_cita:
            cita_encontrada = c
            break

    if cita_encontrada is None:
        raise ValueError("Cita no encontrada.")

    _validar_existencia_paciente_y_doctor(paciente_id, doctor_id)
    _validar_disponibilidad_horario(citas, doctor_id, fecha, hora, excluir_id=id_cita)

    # Actualizamos los datos
    cita_encontrada.paciente_id = paciente_id
    cita_encontrada.doctor_id = doctor_id
    cita_encontrada.fecha = fecha
    cita_encontrada.hora = hora

    _guardar_todas(citas)
    return cita_encontrada


def eliminar_cita(id_cita):
    # Cancela o elimina una cita medica.
    id_cita = texto_obligatorio(id_cita, "El identificador de la cita")
    citas = obtener_citas()

    cita_a_eliminar = None
    for c in citas:
        if c.id == id_cita:
            cita_a_eliminar = c
            break

    if cita_a_eliminar is None:
        raise ValueError("Cita no encontrada.")

    citas.remove(cita_a_eliminar)
    _guardar_todas(citas)

    return True


def buscar_citas(criterio, valor):
    # Busca citas segun el criterio especificado:
    # - 'paciente' o 'paciente_id': busca por id del paciente
    # - 'doctor' o 'doctor_id': busca por id del doctor
    # - 'fecha': busca por fecha (AAAA-MM-DD)
    criterio_limpio = texto_obligatorio(criterio, "El criterio de búsqueda").lower()
    todas_las_citas = obtener_citas()
    resultados = []

    # Aplicamos condicionales segun el tipo de busqueda
    if criterio_limpio == "fecha":
        fecha_valida = validar_fecha(valor)
        for c in todas_las_citas:
            if c.fecha == fecha_valida:
                resultados.append(c)

    elif criterio_limpio == "paciente" or criterio_limpio == "paciente_id":
        valor_limpio = texto_obligatorio(valor, "El identificador a buscar")
        for c in todas_las_citas:
            if c.paciente_id == valor_limpio:
                resultados.append(c)

    elif criterio_limpio == "doctor" or criterio_limpio == "doctor_id":
        valor_limpio = texto_obligatorio(valor, "El identificador a buscar")
        for c in todas_las_citas:
            if c.doctor_id == valor_limpio:
                resultados.append(c)

    else:
        raise ValueError("Criterio no válido. Usa paciente, doctor o fecha.")

    # Ordenamos los resultados por fecha y hora
    resultados_ordenados = sorted(resultados, key=lambda x: (x.fecha, x.hora))
    return resultados_ordenados


def obtener_citas_del_dia(fecha_hoy):
    # Obtiene la lista de citas programadas para una fecha especifica.
    fecha_valida = validar_fecha(fecha_hoy)
    citas = obtener_citas()
    citas_hoy = []

    for c in citas:
        if c.fecha == fecha_valida:
            citas_hoy.append(c)

    # Ordenamos por hora
    citas_hoy.sort(key=lambda x: x.hora)
    return citas_hoy


def obtener_citas_por_doctor(doctor_id):
    # Obtiene todas las citas de un doctor especifico.
    doctor_id = texto_obligatorio(doctor_id, "El identificador del doctor")
    citas = obtener_citas()
    citas_doctor = []

    for c in citas:
        if c.doctor_id == doctor_id:
            citas_doctor.append(c)

    # Ordenamos por fecha y hora
    citas_doctor.sort(key=lambda x: (x.fecha, x.hora))
    return citas_doctor


def obtener_citas_detalladas(citas=None):
    # Prepara la informacion de las citas lista para mostrar en las tablas,
    # incluyendo los nombres legibles del paciente y del doctor.
    if citas is None:
        citas = obtener_citas()

    pacientes = obtener_pacientes()
    doctores = obtener_doctores()

    # Creamos diccionarios auxiliares id -> nombre
    nombres_pacientes = {}
    for p in pacientes:
        nombres_pacientes[p.id] = p.nombre

    nombres_doctores = {}
    for d in doctores:
        nombres_doctores[d.id] = d.nombre

    # Construimos la lista detallada
    lista_detallada = []
    for c in citas:
        nombre_p = nombres_pacientes.get(c.paciente_id, "Paciente no disponible")
        nombre_d = nombres_doctores.get(c.doctor_id, "Doctor no disponible")

        fila = {
            "id": c.id,
            "paciente_id": c.paciente_id,
            "paciente_nombre": nombre_p,
            "doctor_id": c.doctor_id,
            "doctor_nombre": nombre_d,
            "fecha": c.fecha,
            "hora": c.hora,
        }
        lista_detallada.append(fila)

    # Ordenamos por fecha y hora
    lista_detallada.sort(key=lambda x: (x["fecha"], x["hora"]))
    return lista_detallada
