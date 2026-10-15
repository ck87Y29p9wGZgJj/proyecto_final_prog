# VISTA: Inicio
# Muestra la agenda de citas del dia actual

from datetime import datetime
import tkinter as tk
from tkinter import ttk

from services.almacenamiento import ErrorAlmacenamiento
from services.citas_service import obtener_citas_del_dia, obtener_citas_detalladas
from ui.widgets.mensajes import manejar_error


class InicioView(ttk.Frame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador

        self._crear_interfaz()
        self.actualizar()

    def _crear_interfaz(self):
        # Marco del encabezado
        marco_header = ttk.Frame(self)
        marco_header.pack(fill=tk.X, padx=20, pady=(20, 10))

        lbl_titulo = ttk.Label(
            marco_header,
            text="Panel de Inicio - Agenda del Día",
            font=("Arial", 16, "bold"),
        )
        lbl_titulo.pack(side=tk.LEFT)

        btn_refrescar = ttk.Button(
            marco_header,
            text="🔄 Actualizar",
            command=self.actualizar,
        )
        btn_refrescar.pack(side=tk.RIGHT)

        # Informacion de la fecha actual
        self.lbl_fecha = ttk.Label(self, text="", font=("Arial", 10, "italic"))
        self.lbl_fecha.pack(anchor=tk.W, padx=20, pady=(0, 10))

        # Marco que contiene la tabla
        marco_tabla = ttk.LabelFrame(self, text=" Citas programadas para hoy ", padding="10 10 10 10")
        marco_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        columnas = ("hora", "paciente", "doctor")
        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse",
        )

        # Encabezados de columnas
        self.tabla.heading("hora", text="Hora")
        self.tabla.heading("paciente", text="Paciente")
        self.tabla.heading("doctor", text="Doctor")

        self.tabla.column("hora", width=120, anchor=tk.CENTER)
        self.tabla.column("paciente", width=320, anchor=tk.W)
        self.tabla.column("doctor", width=320, anchor=tk.W)

        # Barra de desplazamiento vertical
        scroll = ttk.Scrollbar(marco_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Mensaje de estado inferior
        self.lbl_total = ttk.Label(self, text="", font=("Arial", 9, "bold"))
        self.lbl_total.pack(anchor=tk.W, padx=20, pady=(0, 15))

    def actualizar(self):
        # Carga y muestra las citas programadas para hoy.
        hoy = datetime.now().strftime("%Y-%m-%d")
        self.lbl_fecha.config(text=f"Fecha del día: {hoy}")

        try:
            # Obtenemos las citas de hoy y sus datos detallados
            citas_hoy = obtener_citas_del_dia(hoy)
            citas_detalladas = obtener_citas_detalladas(citas_hoy)

            # Limpiamos los elementos previos de la tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            # Contador aritmetico de citas
            contador = 0
            for c in citas_detalladas:
                self.tabla.insert(
                    "",
                    tk.END,
                    values=(c["hora"], c["paciente_nombre"], c["doctor_nombre"]),
                )
                contador = contador + 1

            # Actualizamos la etiqueta con el total
            self.lbl_total.config(
                text=f"Total de citas para hoy: {contador}"
            )

        except (ValueError, ErrorAlmacenamiento) as error:
            manejar_error(error, titulo="Error al cargar agenda del día", parent=self)
        except Exception as error:
            manejar_error(error, titulo="Error inesperado", parent=self)
