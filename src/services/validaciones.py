# SERVICIO: Validaciones
# Funciones para validar datos de entrada

from datetime import datetime

# Constantes con los formatos estandar
FORMATO_FECHA = "%Y-%m-%d"
FORMATO_HORA = "%H:%M"


def texto_obligatorio(valor, nombre_campo):
    # Verifica que el campo sea texto y no este vacio.
    if valor is None:
        raise ValueError(f"{nombre_campo} es obligatorio.")

    if not isinstance(valor, str):
        raise ValueError(f"{nombre_campo} debe ser texto.")

    texto_limpio = valor.strip()
    if texto_limpio == "":
        raise ValueError(f"{nombre_campo} es obligatorio.")

    return texto_limpio


def texto_opcional(valor):
    # Limpia el texto opcional (como el telefono) o devuelve cadena vacia.
    if valor is None:
        return ""

    if not isinstance(valor, str):
        raise ValueError("El teléfono debe ser texto.")

    return valor.strip()


def validar_fecha(fecha):
    # Comprueba que la fecha tenga el formato AAAA-MM-DD y sea una fecha real.
    fecha_limpia = texto_obligatorio(fecha, "La fecha")

    try:
        # Intentamos convertir la cadena en un objeto datetime
        fecha_obj = datetime.strptime(fecha_limpia, FORMATO_FECHA)
    except ValueError:
        raise ValueError("La fecha debe existir y tener el formato AAAA-MM-DD.")

    # Nos aseguramos de que coincida exactamente (ejemplo: no permitir 2026-02-30)
    if fecha_obj.strftime(FORMATO_FECHA) != fecha_limpia:
        raise ValueError("La fecha debe tener el formato AAAA-MM-DD.")

    return fecha_limpia


def validar_hora(hora):
    # Comprueba que la hora tenga el formato HH:MM en 24 horas.
    hora_limpia = texto_obligatorio(hora, "La hora")

    try:
        # Intentamos convertir a formato de hora
        hora_obj = datetime.strptime(hora_limpia, FORMATO_HORA)
    except ValueError:
        raise ValueError("La hora debe existir y tener el formato HH:MM (24 horas).")

    if hora_obj.strftime(FORMATO_HORA) != hora_limpia:
        raise ValueError("La hora debe tener el formato HH:MM (24 horas).")

    return hora_limpia
