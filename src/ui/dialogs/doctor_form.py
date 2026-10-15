# DIALOGO: Formulario de Doctor
# Permite registrar o modificar un doctor

import tkinter as tk
from tkinter import ttk

from services.almacenamiento import ErrorAlmacenamiento
from services.doctores_service import actualizar_doctor, registrar_doctor
from ui.widgets.mensajes import manejar_error, mostrar_info


class DoctorFormDialog(tk.Toplevel):
    def __init__(self, parent, doctor=None, on_guardar=None):
        super().__init__(parent)
        self.parent = parent
        self.doctor = doctor
        self.on_guardar = on_guardar

        self.es_edicion = self.doctor is not None

        if self.es_edicion:
            self.title("Modificar Doctor")
        else:
            self.title("Registrar Doctor")

        self.geometry("420x220")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self._crear_widgets()

    def _crear_widgets(self):
        marco = ttk.Frame(self, padding="20 15 20 15")
        marco.pack(fill=tk.BOTH, expand=True)

        texto_encabezado = "Modificar datos del doctor" if self.es_edicion else "Registrar nuevo doctor"
        lbl_titulo = ttk.Label(marco, text=texto_encabezado, font=("Arial", 11, "bold"))
        lbl_titulo.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))

        # Campo: Nombre
        ttk.Label(marco, text="Nombre completo *:").grid(row=1, column=0, sticky=tk.W, pady=6)
        self.txt_nombre = ttk.Entry(marco, width=30)
        self.txt_nombre.grid(row=1, column=1, sticky=tk.W, pady=6, padx=(10, 0))

        # Campo: Especialidad
        ttk.Label(marco, text="Especialidad *:").grid(row=2, column=0, sticky=tk.W, pady=6)
        self.txt_especialidad = ttk.Entry(marco, width=30)
        self.txt_especialidad.grid(row=2, column=1, sticky=tk.W, pady=6, padx=(10, 0))

        # Si es edicion cargamos los datos
        if self.es_edicion:
            self.txt_nombre.insert(0, self.doctor.nombre)
            self.txt_especialidad.insert(0, self.doctor.especialidad)

        # Botones
        marco_botones = ttk.Frame(marco)
        marco_botones.grid(row=3, column=0, columnspan=2, sticky=tk.E, pady=(20, 0))

        btn_cancelar = ttk.Button(marco_botones, text="Cancelar", command=self.destroy)
        btn_cancelar.pack(side=tk.RIGHT, padx=(8, 0))

        btn_guardar = ttk.Button(marco_botones, text="Guardar", command=self._guardar)
        btn_guardar.pack(side=tk.RIGHT)

        self.txt_nombre.focus_set()

    def _guardar(self):
        nombre = self.txt_nombre.get()
        especialidad = self.txt_especialidad.get()

        try:
            if not self.es_edicion:
                registrar_doctor(nombre, especialidad)
                mostrar_info("Éxito", "Doctor registrado correctamente.", parent=self)
            else:
                actualizar_doctor(self.doctor.id, nombre, especialidad)
                mostrar_info("Éxito", "Doctor modificado correctamente.", parent=self)

            if self.on_guardar:
                self.on_guardar()

            self.destroy()

        except (ValueError, ErrorAlmacenamiento) as error:
            manejar_error(error, titulo="Error al guardar doctor", parent=self)
        except Exception as error:
            manejar_error(error, titulo="Error inesperado", parent=self)
