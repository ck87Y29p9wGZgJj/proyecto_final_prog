# VISTA: Doctores
# Permite consultar, registrar, modificar, eliminar y buscar doctores

import tkinter as tk
from tkinter import ttk

from services.almacenamiento import ErrorAlmacenamiento
from services.doctores_service import eliminar_doctor, obtener_doctores
from ui.dialogs.doctor_form import DoctorFormDialog
from ui.widgets.mensajes import confirmar_accion, manejar_error, mostrar_advertencia, mostrar_info


class DoctoresView(ttk.Frame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador

        self.doctores_guardados = {}

        self._crear_interfaz()
        self.actualizar()

    def _crear_interfaz(self):
        # Encabezado
        marco_header = ttk.Frame(self)
        marco_header.pack(fill=tk.X, padx=20, pady=(20, 10))

        lbl_titulo = ttk.Label(
            marco_header,
            text="Gestión de Doctores",
            font=("Arial", 16, "bold"),
        )
        lbl_titulo.pack(side=tk.LEFT)

        # Botones de operaciones
        marco_acciones = ttk.Frame(self)
        marco_acciones.pack(fill=tk.X, padx=20, pady=(5, 10))

        btn_nuevo = ttk.Button(
            marco_acciones,
            text="➕ Registrar Doctor",
            command=self._nuevo_doctor,
        )
        btn_nuevo.pack(side=tk.LEFT, padx=(0, 6))

        btn_editar = ttk.Button(
            marco_acciones,
            text="✏️ Modificar",
            command=self._editar_doctor,
        )
        btn_editar.pack(side=tk.LEFT, padx=(0, 6))

        btn_eliminar = ttk.Button(
            marco_acciones,
            text="🗑️ Eliminar",
            command=self._eliminar_doctor,
        )
        btn_eliminar.pack(side=tk.LEFT, padx=(0, 6))

        btn_actualizar = ttk.Button(
            marco_acciones,
            text="🔄 Actualizar lista",
            command=self.actualizar,
        )
        btn_actualizar.pack(side=tk.LEFT)

        # Buscador rapido
        marco_buscar = ttk.Frame(marco_acciones)
        marco_buscar.pack(side=tk.RIGHT)

        ttk.Label(marco_buscar, text="Buscar doctor:").pack(side=tk.LEFT, padx=(0, 5))
        self.txt_buscar = ttk.Entry(marco_buscar, width=18)
        self.txt_buscar.pack(side=tk.LEFT)
        self.txt_buscar.bind("<KeyRelease>", lambda event: self._buscar_en_tabla())

        # Tabla de doctores
        marco_tabla = ttk.Frame(self)
        marco_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 10))

        columnas = ("nombre", "especialidad")
        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse",
        )

        self.tabla.heading("nombre", text="Nombre del Doctor")
        self.tabla.heading("especialidad", text="Especialidad")

        self.tabla.column("nombre", width=360, anchor=tk.W)
        self.tabla.column("especialidad", width=300, anchor=tk.W)

        scroll = ttk.Scrollbar(marco_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tabla.bind("<Double-1>", lambda event: self._editar_doctor())

        # Barra inferior de estado
        self.lbl_estado = ttk.Label(self, text="", font=("Arial", 9))
        self.lbl_estado.pack(fill=tk.X, padx=20, pady=(0, 15))

    def actualizar(self):
        # Consulta los doctores y actualiza la lista.
        try:
            doctores = obtener_doctores()
            self.doctores_guardados = {}

            for d in doctores:
                self.doctores_guardados[d.id] = d

            self._mostrar_doctores(doctores)

            total = len(doctores)
            self.lbl_estado.config(text=f"Total de registros: {total} doctor(es).")

        except (ValueError, ErrorAlmacenamiento) as error:
            manejar_error(error, titulo="Error al cargar doctores", parent=self)
        except Exception as error:
            manejar_error(error, titulo="Error inesperado", parent=self)

    def _mostrar_doctores(self, lista):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for d in lista:
            self.tabla.insert(
                "",
                tk.END,
                iid=d.id,
                values=(d.nombre, d.especialidad),
            )

    def _buscar_en_tabla(self):
        texto = self.txt_buscar.get().strip().lower()
        if texto == "":
            self._mostrar_doctores(list(self.doctores_guardados.values()))
            return

        coincidencias = []
        for d in self.doctores_guardados.values():
            if texto in d.nombre.lower() or texto in d.especialidad.lower():
                coincidencias.append(d)

        self._mostrar_doctores(coincidencias)

    def _obtener_seleccionado(self):
        seleccion = self.tabla.selection()
        if len(seleccion) == 0:
            mostrar_advertencia(
                "Aviso",
                "Por favor, selecciona un doctor de la lista.",
                parent=self,
            )
            return None

        doctor_id = seleccion[0]
        return self.doctores_guardados.get(doctor_id)

    def _nuevo_doctor(self):
        DoctorFormDialog(self, on_guardar=self.actualizar)

    def _editar_doctor(self):
        doctor = self._obtener_seleccionado()
        if doctor is not None:
            DoctorFormDialog(self, doctor=doctor, on_guardar=self.actualizar)

    def _eliminar_doctor(self):
        doctor = self._obtener_seleccionado()
        if doctor is None:
            return

        mensaje = f"¿Está seguro de eliminar al doctor '{doctor.nombre}'?"
        if not confirmar_accion("Confirmar eliminación", mensaje, parent=self):
            return

        try:
            eliminar_doctor(doctor.id)
            mostrar_info("Éxito", "El doctor ha sido eliminado.", parent=self)
            self.actualizar()
        except (ValueError, ErrorAlmacenamiento) as error:
            manejar_error(error, titulo="No se pudo eliminar el doctor", parent=self)
        except Exception as error:
            manejar_error(error, titulo="Error inesperado", parent=self)
