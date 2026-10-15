# VISTA: Citas Médicas
# Permite agendar, modificar, cancelar y buscar citas

from datetime import datetime
import tkinter as tk
from tkinter import ttk

from services.almacenamiento import ErrorAlmacenamiento
from services.citas_service import (
    buscar_citas,
    eliminar_cita,
    obtener_citas,
    obtener_citas_detalladas,
)
from services.doctores_service import obtener_doctores
from services.pacientes_service import obtener_pacientes
from ui.dialogs.cita_form import CitaFormDialog
from ui.widgets.mensajes import (
    confirmar_accion,
    manejar_error,
    mostrar_advertencia,
    mostrar_info,
)


class CitasView(ttk.Frame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador

        self.citas_guardadas = {}
        self.citas_detalladas_map = {}

        self._crear_interfaz()
        self.actualizar()

    def _crear_interfaz(self):
        # Encabezado
        marco_header = ttk.Frame(self)
        marco_header.pack(fill=tk.X, padx=20, pady=(20, 10))

        lbl_titulo = ttk.Label(
            marco_header,
            text="Gestión de Citas Médicas",
            font=("Arial", 16, "bold"),
        )
        lbl_titulo.pack(side=tk.LEFT)

        # Botones de operaciones principales
        marco_acciones = ttk.Frame(self)
        marco_acciones.pack(fill=tk.X, padx=20, pady=(5, 10))

        btn_agendar = ttk.Button(
            marco_acciones,
            text="➕ Agendar Cita",
            command=self._agendar_cita,
        )
        btn_agendar.pack(side=tk.LEFT, padx=(0, 6))

        btn_editar = ttk.Button(
            marco_acciones,
            text="✏️ Modificar",
            command=self._editar_cita,
        )
        btn_editar.pack(side=tk.LEFT, padx=(0, 6))

        btn_cancelar = ttk.Button(
            marco_acciones,
            text="❌ Cancelar Cita",
            command=self._cancelar_cita,
        )
        btn_cancelar.pack(side=tk.LEFT, padx=(0, 6))

        btn_actualizar = ttk.Button(
            marco_acciones,
            text="🔄 Actualizar lista",
            command=self.actualizar,
        )
        btn_actualizar.pack(side=tk.LEFT)

        # Panel de Busqueda y Filtros
        marco_busqueda = ttk.LabelFrame(self, text=" Buscar registros de citas ", padding="10 8 10 8")
        marco_busqueda.pack(fill=tk.X, padx=20, pady=(5, 10))

        ttk.Label(marco_busqueda, text="Buscar por:").grid(row=0, column=0, padx=(0, 6), sticky=tk.W)

        self.tipo_criterio = tk.StringVar(value="Todos")
        self.combo_criterio = ttk.Combobox(
            marco_busqueda,
            textvariable=self.tipo_criterio,
            values=["Todos", "Fecha", "Paciente", "Doctor"],
            state="readonly",
            width=12,
        )
        self.combo_criterio.grid(row=0, column=1, padx=(0, 10), sticky=tk.W)
        self.combo_criterio.bind("<<ComboboxSelected>>", lambda event: self._cambiar_criterio())

        # Contenedor para el campo de valor del filtro
        self.marco_campo_valor = ttk.Frame(marco_busqueda)
        self.marco_campo_valor.grid(row=0, column=2, padx=(0, 10), sticky=tk.W)

        self.txt_fecha_filtro = ttk.Entry(self.marco_campo_valor, width=14)
        self.btn_hoy_filtro = ttk.Button(
            self.marco_campo_valor,
            text="Hoy",
            width=5,
            command=self._colocar_fecha_hoy,
        )

        self.combo_paciente_filtro = ttk.Combobox(self.marco_campo_valor, state="readonly", width=28)
        self.combo_doctor_filtro = ttk.Combobox(self.marco_campo_valor, state="readonly", width=28)

        # Boton buscar
        self.btn_filtrar = ttk.Button(
            marco_busqueda,
            text="🔍 Buscar",
            command=self._realizar_busqueda,
        )
        self.btn_filtrar.grid(row=0, column=3, padx=(0, 6), sticky=tk.W)

        # Boton limpiar
        self.btn_limpiar = ttk.Button(
            marco_busqueda,
            text="Mostrar todas",
            command=self.actualizar,
        )
        self.btn_limpiar.grid(row=0, column=4, sticky=tk.W)

        self._cambiar_criterio()

        # Tabla de citas
        marco_tabla = ttk.Frame(self)
        marco_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 10))

        columnas = ("fecha", "hora", "paciente", "doctor")
        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse",
        )

        self.tabla.heading("fecha", text="Fecha (AAAA-MM-DD)")
        self.tabla.heading("hora", text="Hora")
        self.tabla.heading("paciente", text="Paciente")
        self.tabla.heading("doctor", text="Doctor")

        self.tabla.column("fecha", width=140, anchor=tk.CENTER)
        self.tabla.column("hora", width=100, anchor=tk.CENTER)
        self.tabla.column("paciente", width=280, anchor=tk.W)
        self.tabla.column("doctor", width=280, anchor=tk.W)

        scroll = ttk.Scrollbar(marco_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tabla.bind("<Double-1>", lambda event: self._editar_cita())

        # Barra de estado inferior
        self.lbl_estado = ttk.Label(self, text="", font=("Arial", 9))
        self.lbl_estado.pack(fill=tk.X, padx=20, pady=(0, 15))

    def _colocar_fecha_hoy(self):
        hoy = datetime.now().strftime("%Y-%m-%d")
        self.txt_fecha_filtro.delete(0, tk.END)
        self.txt_fecha_filtro.insert(0, hoy)

    def _cambiar_criterio(self):
        criterio = self.tipo_criterio.get()

        # Ocultamos los componentes anteriores
        self.txt_fecha_filtro.pack_forget()
        self.btn_hoy_filtro.pack_forget()
        self.combo_paciente_filtro.pack_forget()
        self.combo_doctor_filtro.pack_forget()

        if criterio == "Fecha":
            self.txt_fecha_filtro.pack(side=tk.LEFT, padx=(0, 4))
            self.btn_hoy_filtro.pack(side=tk.LEFT)
            if self.txt_fecha_filtro.get() == "":
                self._colocar_fecha_hoy()
            self.btn_filtrar.config(state="normal")

        elif criterio == "Paciente":
            self._cargar_pacientes_en_filtro()
            self.combo_paciente_filtro.pack(side=tk.LEFT)
            self.btn_filtrar.config(state="normal")

        elif criterio == "Doctor":
            self._cargar_doctores_en_filtro()
            self.combo_doctor_filtro.pack(side=tk.LEFT)
            self.btn_filtrar.config(state="normal")

        else:
            self.btn_filtrar.config(state="disabled")

    def _cargar_pacientes_en_filtro(self):
        try:
            pacientes = obtener_pacientes()
            self.pacientes_filtro_dict = {}
            for p in pacientes:
                etiqueta = f"{p.nombre} ({p.identificacion})"
                self.pacientes_filtro_dict[etiqueta] = p.id

            nombres = list(self.pacientes_filtro_dict.keys())
            self.combo_paciente_filtro.config(values=nombres)
            if len(nombres) > 0:
                self.combo_paciente_filtro.current(0)
        except Exception:
            self.pacientes_filtro_dict = {}

    def _cargar_doctores_en_filtro(self):
        try:
            doctores = obtener_doctores()
            self.doctores_filtro_dict = {}
            for d in doctores:
                etiqueta = f"{d.nombre} ({d.especialidad})"
                self.doctores_filtro_dict[etiqueta] = d.id

            nombres = list(self.doctores_filtro_dict.keys())
            self.combo_doctor_filtro.config(values=nombres)
            if len(nombres) > 0:
                self.combo_doctor_filtro.current(0)
        except Exception:
            self.doctores_filtro_dict = {}

    def actualizar(self):
        # Consulta todas las citas médicas y actualiza la tabla.
        try:
            citas = obtener_citas()
            self.citas_guardadas = {}
            for c in citas:
                self.citas_guardadas[c.id] = c

            detalladas = obtener_citas_detalladas(citas)
            self._mostrar_en_tabla(detalladas)

            total = len(detalladas)
            self.lbl_estado.config(text=f"Total de registros: {total} cita(s) médica(s).")

            # Reiniciamos selector
            self.tipo_criterio.set("Todos")
            self._cambiar_criterio()

        except (ValueError, ErrorAlmacenamiento) as error:
            manejar_error(error, titulo="Error al cargar citas", parent=self)
        except Exception as error:
            manejar_error(error, titulo="Error inesperado", parent=self)

    def _realizar_busqueda(self):
        criterio = self.tipo_criterio.get()
        if criterio == "Todos":
            self.actualizar()
            return

        try:
            if criterio == "Fecha":
                fecha_ingresada = self.txt_fecha_filtro.get()
                citas_resultado = buscar_citas("fecha", fecha_ingresada)
                mensaje_filtro = f"fecha '{fecha_ingresada}'"

            elif criterio == "Paciente":
                etiqueta_p = self.combo_paciente_filtro.get()
                p_id = self.pacientes_filtro_dict.get(etiqueta_p, etiqueta_p)
                citas_resultado = buscar_citas("paciente_id", p_id)
                mensaje_filtro = f"paciente '{etiqueta_p}'"

            elif criterio == "Doctor":
                etiqueta_d = self.combo_doctor_filtro.get()
                d_id = self.doctores_filtro_dict.get(etiqueta_d, etiqueta_d)
                citas_resultado = buscar_citas("doctor_id", d_id)
                mensaje_filtro = f"doctor '{etiqueta_d}'"

            else:
                return

            detalladas = obtener_citas_detalladas(citas_resultado)
            self._mostrar_en_tabla(detalladas)

            total_encontradas = len(detalladas)
            self.lbl_estado.config(
                text=f"Búsqueda por {mensaje_filtro}: {total_encontradas} cita(s) encontrada(s)."
            )

        except (ValueError, ErrorAlmacenamiento) as error:
            manejar_error(error, titulo="Error en la búsqueda de citas", parent=self)
        except Exception as error:
            manejar_error(error, titulo="Error inesperado", parent=self)

    def _mostrar_en_tabla(self, lista_detallada):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        self.citas_detalladas_map = {}
        for fila in lista_detallada:
            self.citas_detalladas_map[fila["id"]] = fila
            self.tabla.insert(
                "",
                tk.END,
                iid=fila["id"],
                values=(
                    fila["fecha"],
                    fila["hora"],
                    fila["paciente_nombre"],
                    fila["doctor_nombre"],
                ),
            )

    def _obtener_seleccionada(self):
        seleccion = self.tabla.selection()
        if len(seleccion) == 0:
            mostrar_advertencia(
                "Aviso",
                "Por favor, selecciona una cita de la lista.",
                parent=self,
            )
            return None

        cita_id = seleccion[0]
        cita = self.citas_guardadas.get(cita_id)
        if cita is None:
            # Reintentamos cargarla si se hizo una busqueda filtrada
            todas = obtener_citas()
            for c in todas:
                self.citas_guardadas[c.id] = c
            cita = self.citas_guardadas.get(cita_id)

        return cita

    def _agendar_cita(self):
        CitaFormDialog(self, on_guardar=self.actualizar)

    def _editar_cita(self):
        cita = self._obtener_seleccionada()
        if cita is not None:
            CitaFormDialog(self, cita=cita, on_guardar=self.actualizar)

    def _cancelar_cita(self):
        cita = self._obtener_seleccionada()
        if cita is None:
            return

        detalles = self.citas_detalladas_map.get(cita.id, {})
        paciente = detalles.get("paciente_nombre", "el paciente")
        doctor = detalles.get("doctor_nombre", "el doctor")

        mensaje = (
            f"¿Está seguro de cancelar la cita médica?\n\n"
            f"Fecha: {cita.fecha} a las {cita.hora}\n"
            f"Paciente: {paciente}\n"
            f"Doctor: {doctor}"
        )

        if not confirmar_accion("Confirmar cancelación", mensaje, parent=self):
            return

        try:
            eliminar_cita(cita.id)
            mostrar_info("Éxito", "La cita médica ha sido cancelada.", parent=self)
            self.actualizar()
        except (ValueError, ErrorAlmacenamiento) as error:
            manejar_error(error, titulo="No se pudo cancelar la cita", parent=self)
        except Exception as error:
            manejar_error(error, titulo="Error inesperado", parent=self)
