# VISTA: Reportes
# Permite consultar la agenda por fecha y las citas por doctor

from datetime import datetime
import tkinter as tk
from tkinter import ttk

from services.almacenamiento import ErrorAlmacenamiento
from services.citas_service import (
    obtener_citas_del_dia,
    obtener_citas_detalladas,
    obtener_citas_por_doctor,
)
from services.doctores_service import obtener_doctores
from ui.widgets.mensajes import manejar_error, mostrar_advertencia


class ReportesView(ttk.Frame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.doctores_dict = {}

        self._crear_interfaz()
        self.actualizar()

    def _crear_interfaz(self):
        # Encabezado
        marco_header = ttk.Frame(self)
        marco_header.pack(fill=tk.X, padx=20, pady=(20, 10))

        lbl_titulo = ttk.Label(
            marco_header,
            text="Reportes y Consultas",
            font=("Arial", 16, "bold"),
        )
        lbl_titulo.pack(side=tk.LEFT)

        # Pestanas con Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 15))

        # Pestana 1: Agenda por fecha
        self.tab_fecha = ttk.Frame(self.notebook, padding="15 15 15 15")
        self.notebook.add(self.tab_fecha, text="📅 Agenda por Fecha")
        self._crear_reporte_fecha()

        # Pestana 2: Citas por doctor
        self.tab_doctor = ttk.Frame(self.notebook, padding="15 15 15 15")
        self.notebook.add(self.tab_doctor, text="🩺 Citas por Doctor")
        self._crear_reporte_doctor()

    def _crear_reporte_fecha(self):
        # Controles superiores
        marco_controles = ttk.Frame(self.tab_fecha)
        marco_controles.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(marco_controles, text="Fecha (AAAA-MM-DD):").pack(side=tk.LEFT, padx=(0, 6))
        self.txt_fecha = ttk.Entry(marco_controles, width=14)
        self.txt_fecha.pack(side=tk.LEFT, padx=(0, 6))
        self.txt_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))

        btn_hoy = ttk.Button(marco_controles, text="Hoy", width=5, command=self._set_fecha_hoy)
        btn_hoy.pack(side=tk.LEFT, padx=(0, 10))

        btn_consultar = ttk.Button(
            marco_controles,
            text="🔍 Consultar Agenda",
            command=self._consultar_por_fecha,
        )
        btn_consultar.pack(side=tk.LEFT)

        self.lbl_resumen_fecha = ttk.Label(marco_controles, text="", font=("Arial", 9, "bold"))
        self.lbl_resumen_fecha.pack(side=tk.RIGHT)

        # Tabla de resultados
        marco_tabla = ttk.Frame(self.tab_fecha)
        marco_tabla.pack(fill=tk.BOTH, expand=True)

        columnas = ("fecha", "hora", "paciente", "doctor")
        self.tabla_fecha = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse",
        )

        self.tabla_fecha.heading("fecha", text="Fecha")
        self.tabla_fecha.heading("hora", text="Hora")
        self.tabla_fecha.heading("paciente", text="Paciente")
        self.tabla_fecha.heading("doctor", text="Doctor")

        self.tabla_fecha.column("fecha", width=120, anchor=tk.CENTER)
        self.tabla_fecha.column("hora", width=100, anchor=tk.CENTER)
        self.tabla_fecha.column("paciente", width=300, anchor=tk.W)
        self.tabla_fecha.column("doctor", width=300, anchor=tk.W)

        scroll = ttk.Scrollbar(marco_tabla, orient=tk.VERTICAL, command=self.tabla_fecha.yview)
        self.tabla_fecha.configure(yscrollcommand=scroll.set)

        self.tabla_fecha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _crear_reporte_doctor(self):
        # Controles superiores
        marco_controles = ttk.Frame(self.tab_doctor)
        marco_controles.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(marco_controles, text="Seleccione Doctor:").pack(side=tk.LEFT, padx=(0, 6))
        self.combo_doctor = ttk.Combobox(marco_controles, state="readonly", width=32)
        self.combo_doctor.pack(side=tk.LEFT, padx=(0, 10))

        btn_consultar = ttk.Button(
            marco_controles,
            text="🔍 Consultar Citas",
            command=self._consultar_por_doctor,
        )
        btn_consultar.pack(side=tk.LEFT)

        self.lbl_resumen_doctor = ttk.Label(marco_controles, text="", font=("Arial", 9, "bold"))
        self.lbl_resumen_doctor.pack(side=tk.RIGHT)

        # Tabla de resultados
        marco_tabla = ttk.Frame(self.tab_doctor)
        marco_tabla.pack(fill=tk.BOTH, expand=True)

        columnas = ("fecha", "hora", "paciente", "doctor")
        self.tabla_doctor = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse",
        )

        self.tabla_doctor.heading("fecha", text="Fecha")
        self.tabla_doctor.heading("hora", text="Hora")
        self.tabla_doctor.heading("paciente", text="Paciente")
        self.tabla_doctor.heading("doctor", text="Doctor")

        self.tabla_doctor.column("fecha", width=120, anchor=tk.CENTER)
        self.tabla_doctor.column("hora", width=100, anchor=tk.CENTER)
        self.tabla_doctor.column("paciente", width=300, anchor=tk.W)
        self.tabla_doctor.column("doctor", width=300, anchor=tk.W)

        scroll = ttk.Scrollbar(marco_tabla, orient=tk.VERTICAL, command=self.tabla_doctor.yview)
        self.tabla_doctor.configure(yscrollcommand=scroll.set)

        self.tabla_doctor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _set_fecha_hoy(self):
        hoy = datetime.now().strftime("%Y-%m-%d")
        self.txt_fecha.delete(0, tk.END)
        self.txt_fecha.insert(0, hoy)

    def actualizar(self):
        # Recarga la lista de doctores en el combobox de reportes.
        try:
            doctores = obtener_doctores()
            self.doctores_dict = {}
            for d in doctores:
                etiqueta = f"{d.nombre} ({d.especialidad})"
                self.doctores_dict[etiqueta] = d.id

            nombres = list(self.doctores_dict.keys())
            self.combo_doctor.config(values=nombres)
            if len(nombres) > 0 and self.combo_doctor.get() == "":
                self.combo_doctor.current(0)
        except Exception:
            self.doctores_dict = {}

    def _consultar_por_fecha(self):
        fecha = self.txt_fecha.get().strip()

        try:
            citas = obtener_citas_del_dia(fecha)
            detalles = obtener_citas_detalladas(citas)

            for item in self.tabla_fecha.get_children():
                self.tabla_fecha.delete(item)

            contador = 0
            for c in detalles:
                self.tabla_fecha.insert(
                    "",
                    tk.END,
                    values=(c["fecha"], c["hora"], c["paciente_nombre"], c["doctor_nombre"]),
                )
                contador = contador + 1

            self.lbl_resumen_fecha.config(
                text=f"Total: {contador} cita(s) encontrada(s)."
            )

        except (ValueError, ErrorAlmacenamiento) as error:
            manejar_error(error, titulo="Error al consultar agenda", parent=self)
        except Exception as error:
            manejar_error(error, titulo="Error inesperado", parent=self)

    def _consultar_por_doctor(self):
        seleccion = self.combo_doctor.get()
        if seleccion == "":
            mostrar_advertencia(
                "Aviso",
                "Por favor, selecciona un doctor de la lista.",
                parent=self,
            )
            return

        doctor_id = self.doctores_dict.get(seleccion)
        if doctor_id is None:
            return

        try:
            citas = obtener_citas_por_doctor(doctor_id)
            detalles = obtener_citas_detalladas(citas)

            for item in self.tabla_doctor.get_children():
                self.tabla_doctor.delete(item)

            contador = 0
            for c in detalles:
                self.tabla_doctor.insert(
                    "",
                    tk.END,
                    values=(c["fecha"], c["hora"], c["paciente_nombre"], c["doctor_nombre"]),
                )
                contador = contador + 1

            self.lbl_resumen_doctor.config(
                text=f"Total: {contador} cita(s) del doctor."
            )

        except (ValueError, ErrorAlmacenamiento) as error:
            manejar_error(error, titulo="Error al consultar citas del doctor", parent=self)
        except Exception as error:
            manejar_error(error, titulo="Error inesperado", parent=self)
