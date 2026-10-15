# DIALOGO: Formulario de Cita Medica
# Permite agendar o modificar una cita

from datetime import datetime
import tkinter as tk
from tkinter import ttk

from services.almacenamiento import ErrorAlmacenamiento
from services.citas_service import actualizar_cita, registrar_cita
from services.doctores_service import obtener_doctores
from services.pacientes_service import obtener_pacientes
from ui.widgets.mensajes import manejar_error, mostrar_advertencia, mostrar_info


class CitaFormDialog(tk.Toplevel):
    def __init__(self, parent, cita=None, on_guardar=None):
        super().__init__(parent)
        self.parent = parent
        self.cita = cita
        self.on_guardar = on_guardar

        self.es_edicion = self.cita is not None

        if self.es_edicion:
            self.title("Modificar Cita Médica")
        else:
            self.title("Registrar Cita Médica")

        self.geometry("460x320")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        # Diccionarios para mapear el texto del combo con el ID real
        self.pacientes_ids = {}
        self.doctores_ids = {}

        self._cargar_listas()
        self._crear_widgets()

    def _cargar_listas(self):
        try:
            pacientes = obtener_pacientes()
            for p in pacientes:
                texto = f"{p.nombre} (Cédula: {p.identificacion})"
                self.pacientes_ids[texto] = p.id

            doctores = obtener_doctores()
            for d in doctores:
                texto = f"{d.nombre} ({d.especialidad})"
                self.doctores_ids[texto] = d.id
        except Exception as error:
            manejar_error(error, titulo="Error al cargar listas de referencia", parent=self)

    def _crear_widgets(self):
        marco = ttk.Frame(self, padding="20 15 20 15")
        marco.pack(fill=tk.BOTH, expand=True)

        texto_encabezado = "Modificar cita médica" if self.es_edicion else "Agendar nueva cita médica"
        lbl_titulo = ttk.Label(marco, text=texto_encabezado, font=("Arial", 11, "bold"))
        lbl_titulo.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))

        # Seleccionar Paciente
        ttk.Label(marco, text="Paciente *:").grid(row=1, column=0, sticky=tk.W, pady=6)
        nombres_p = list(self.pacientes_ids.keys())
        self.combo_paciente = ttk.Combobox(marco, values=nombres_p, state="readonly", width=34)
        self.combo_paciente.grid(row=1, column=1, sticky=tk.W, pady=6, padx=(10, 0))

        # Seleccionar Doctor
        ttk.Label(marco, text="Doctor *:").grid(row=2, column=0, sticky=tk.W, pady=6)
        nombres_d = list(self.doctores_ids.keys())
        self.combo_doctor = ttk.Combobox(marco, values=nombres_d, state="readonly", width=34)
        self.combo_doctor.grid(row=2, column=1, sticky=tk.W, pady=6, padx=(10, 0))

        # Campo Fecha
        ttk.Label(marco, text="Fecha (AAAA-MM-DD) *:").grid(row=3, column=0, sticky=tk.W, pady=6)
        marco_fecha = ttk.Frame(marco)
        marco_fecha.grid(row=3, column=1, sticky=tk.W, pady=6, padx=(10, 0))

        self.txt_fecha = ttk.Entry(marco_fecha, width=18)
        self.txt_fecha.pack(side=tk.LEFT)

        btn_hoy = ttk.Button(marco_fecha, text="Hoy", width=5, command=self._poner_fecha_hoy)
        btn_hoy.pack(side=tk.LEFT, padx=(5, 0))

        # Campo Hora
        ttk.Label(marco, text="Hora (HH:MM, 24h) *:").grid(row=4, column=0, sticky=tk.W, pady=6)
        horas_comunes = [
            "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
            "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
            "14:00", "14:30", "15:00", "15:30", "16:00", "16:30",
            "17:00", "17:30", "18:00"
        ]
        self.combo_hora = ttk.Combobox(marco, values=horas_comunes, width=34)
        self.combo_hora.grid(row=4, column=1, sticky=tk.W, pady=6, padx=(10, 0))

        # Si estamos editando, precargamos los valores actuales
        if self.es_edicion:
            for texto, pid in self.pacientes_ids.items():
                if pid == self.cita.paciente_id:
                    self.combo_paciente.set(texto)
                    break

            for texto, did in self.doctores_ids.items():
                if did == self.cita.doctor_id:
                    self.combo_doctor.set(texto)
                    break

            self.txt_fecha.insert(0, self.cita.fecha)
            self.combo_hora.set(self.cita.hora)
        else:
            self._poner_fecha_hoy()
            if nombres_p:
                self.combo_paciente.current(0)
            if nombres_d:
                self.combo_doctor.current(0)
            self.combo_hora.set("09:00")

        # Botones
        marco_botones = ttk.Frame(marco)
        marco_botones.grid(row=5, column=0, columnspan=2, sticky=tk.E, pady=(20, 0))

        btn_cancelar = ttk.Button(marco_botones, text="Cancelar", command=self.destroy)
        btn_cancelar.pack(side=tk.RIGHT, padx=(8, 0))

        btn_guardar = ttk.Button(marco_botones, text="Guardar", command=self._guardar)
        btn_guardar.pack(side=tk.RIGHT)

        # Avisos si falta registrar pacientes o doctores
        if not self.pacientes_ids:
            mostrar_advertencia(
                "Aviso",
                "No hay pacientes registrados. Primero debes registrar pacientes.",
                parent=self,
            )
        elif not self.doctores_ids:
            mostrar_advertencia(
                "Aviso",
                "No hay doctores registrados. Primero debes registrar doctores.",
                parent=self,
            )

    def _poner_fecha_hoy(self):
        hoy = datetime.now().strftime("%Y-%m-%d")
        self.txt_fecha.delete(0, tk.END)
        self.txt_fecha.insert(0, hoy)

    def _guardar(self):
        texto_p = self.combo_paciente.get()
        texto_d = self.combo_doctor.get()
        fecha = self.txt_fecha.get()
        hora = self.combo_hora.get()

        # Obtenemos los identificadores correspondientes
        paciente_id = self.pacientes_ids.get(texto_p, texto_p)
        doctor_id = self.doctores_ids.get(texto_d, texto_d)

        try:
            if not self.es_edicion:
                registrar_cita(paciente_id, doctor_id, fecha, hora)
                mostrar_info("Éxito", "Cita médica agendada correctamente.", parent=self)
            else:
                actualizar_cita(self.cita.id, paciente_id, doctor_id, fecha, hora)
                mostrar_info("Éxito", "Cita médica modificada correctamente.", parent=self)

            if self.on_guardar:
                self.on_guardar()

            self.destroy()

        except (ValueError, ErrorAlmacenamiento) as error:
            manejar_error(error, titulo="Error al guardar la cita", parent=self)
        except Exception as error:
            manejar_error(error, titulo="Error inesperado", parent=self)
