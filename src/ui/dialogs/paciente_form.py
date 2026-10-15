# DIALOGO: Formulario de Paciente
# Permite registrar o modificar un paciente

import tkinter as tk
from tkinter import ttk

from services.almacenamiento import ErrorAlmacenamiento
from services.pacientes_service import actualizar_paciente, registrar_paciente
from ui.widgets.mensajes import manejar_error, mostrar_info


class PacienteFormDialog(tk.Toplevel):
    def __init__(self, parent, paciente=None, on_guardar=None):
        super().__init__(parent)
        self.parent = parent
        self.paciente = paciente
        self.on_guardar = on_guardar

        # Determinamos si estamos creando o modificando
        self.es_edicion = self.paciente is not None

        if self.es_edicion:
            self.title("Modificar Paciente")
        else:
            self.title("Registrar Paciente")

        self.geometry("430x250")
        self.resizable(False, False)

        # Hace que la ventana sea modal
        self.transient(parent)
        self.grab_set()

        self._crear_widgets()

    def _crear_widgets(self):
        # Marco principal
        marco = ttk.Frame(self, padding="20 15 20 15")
        marco.pack(fill=tk.BOTH, expand=True)

        # Titulo
        texto_encabezado = "Modificar datos del paciente" if self.es_edicion else "Registrar nuevo paciente"
        lbl_titulo = ttk.Label(marco, text=texto_encabezado, font=("Arial", 11, "bold"))
        lbl_titulo.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))

        # Campo: Nombre
        ttk.Label(marco, text="Nombre completo *:").grid(row=1, column=0, sticky=tk.W, pady=6)
        self.txt_nombre = ttk.Entry(marco, width=30)
        self.txt_nombre.grid(row=1, column=1, sticky=tk.W, pady=6, padx=(10, 0))

        # Campo: Identificacion
        ttk.Label(marco, text="Identificación / Cédula *:").grid(row=2, column=0, sticky=tk.W, pady=6)
        self.txt_identificacion = ttk.Entry(marco, width=30)
        self.txt_identificacion.grid(row=2, column=1, sticky=tk.W, pady=6, padx=(10, 0))

        # Campo: Telefono
        ttk.Label(marco, text="Teléfono (opcional):").grid(row=3, column=0, sticky=tk.W, pady=6)
        self.txt_telefono = ttk.Entry(marco, width=30)
        self.txt_telefono.grid(row=3, column=1, sticky=tk.W, pady=6, padx=(10, 0))

        # Si estamos editando, rellenamos los datos actuales
        if self.es_edicion:
            self.txt_nombre.insert(0, self.paciente.nombre)
            self.txt_identificacion.insert(0, self.paciente.identificacion)
            if self.paciente.telefono:
                self.txt_telefono.insert(0, self.paciente.telefono)

        # Botones
        marco_botones = ttk.Frame(marco)
        marco_botones.grid(row=4, column=0, columnspan=2, sticky=tk.E, pady=(20, 0))

        btn_cancelar = ttk.Button(marco_botones, text="Cancelar", command=self.destroy)
        btn_cancelar.pack(side=tk.RIGHT, padx=(8, 0))

        btn_guardar = ttk.Button(marco_botones, text="Guardar", command=self._guardar)
        btn_guardar.pack(side=tk.RIGHT)

        # Colocar foco en el primer campo
        self.txt_nombre.focus_set()

    def _guardar(self):
        nombre = self.txt_nombre.get()
        identificacion = self.txt_identificacion.get()
        telefono = self.txt_telefono.get()

        try:
            if not self.es_edicion:
                # Caso registrar nuevo
                registrar_paciente(nombre, identificacion, telefono)
                mostrar_info("Éxito", "Paciente registrado correctamente.", parent=self)
            else:
                # Caso modificar existente
                actualizar_paciente(self.paciente.id, nombre, identificacion, telefono)
                mostrar_info("Éxito", "Paciente modificado correctamente.", parent=self)

            # Notificamos a la vista para que actualice la tabla
            if self.on_guardar:
                self.on_guardar()

            self.destroy()

        except (ValueError, ErrorAlmacenamiento) as error:
            manejar_error(error, titulo="Error al guardar paciente", parent=self)
        except Exception as error:
            manejar_error(error, titulo="Error inesperado", parent=self)
