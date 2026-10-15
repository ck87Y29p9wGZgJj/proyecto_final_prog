# MODULO: Mensajes
# Funciones auxiliares para mostrar alertas y confirmaciones


from tkinter import messagebox
from services.almacenamiento import ErrorAlmacenamiento


def mostrar_info(titulo, mensaje, parent=None):
    # Muestra una ventana emergente de informacion.
    messagebox.showinfo(titulo, mensaje, parent=parent)


def mostrar_error(titulo, mensaje, parent=None):
    # Muestra una ventana emergente de error.
    messagebox.showerror(titulo, mensaje, parent=parent)


def mostrar_advertencia(titulo, mensaje, parent=None):
    # Muestra una ventana de advertencia o aviso.
    messagebox.showwarning(titulo, mensaje, parent=parent)


def confirmar_accion(titulo, mensaje, parent=None):
    # Pide confirmacion al usuario y devuelve True si acepta o False si cancela.
    respuesta = messagebox.askyesno(titulo, mensaje, parent=parent)
    return respuesta


def manejar_error(error, titulo="Error", parent=None):
    # Atrapa y clasifica el error para mostrarselo claramente al usuario:
    # - ValueError: reglas de negocio, datos vacios o conflictos.
    # - ErrorAlmacenamiento: problemas con los archivos JSON.
    # - Otras excepciones no previstas.
    if isinstance(error, ValueError):
        mostrar_error(titulo, str(error), parent=parent)
    elif isinstance(error, ErrorAlmacenamiento):
        mensaje = f"Error en los archivos de datos:\n{error}"
        mostrar_error("Error de almacenamiento", mensaje, parent=parent)
    else:
        mensaje = f"Ocurrió un error inesperado:\n{error}"
        mostrar_error("Error", mensaje, parent=parent)
