# VISTA: Pacientes
# Permite consultar, registrar, modificar, eliminar y buscar pacientes

import tkinter as tk
from tkinter import ttk

from services.almacenamiento import ErrorAlmacenamiento
from services.pacientes_service import eliminar_paciente, obtener_pacientes
from ui.dialogs.paciente_form import PacienteFormDialog
from ui.widgets.mensajes import confirmar_accion, manejar_error, mostrar_advertencia, mostrar_info


class PacientesView(ttk.Frame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador

        # Diccionario para acceder a los pacientes por su ID
        self.pacientes_guardados = {}

        self._crear_interfaz()
        self.actualizar()

    def _crear_interfaz(self):
        # Encabezado
        marco_header = ttk.Frame(self)
        marco_header.pack(fill=tk.X, padx=20, pady=(20, 10))

        lbl_titulo = ttk.Label(
            marco_header,
            text="Gestión de Pacientes",
            font=("Arial", 16, "bold"),
        )
        lbl_titulo.pack(side=tk.LEFT)

        # Barra de botones para operaciones
        marco_acciones = ttk.Frame(self)
        marco_acciones.pack(fill=tk.X, padx=20, pady=(5, 10))

        btn_nuevo = ttk.Button(
            marco_acciones,
            text="➕ Registrar Paciente",
            command=self._nuevo_paciente,
        )
        btn_nuevo.pack(side=tk.LEFT, padx=(0, 6))

        btn_editar = ttk.Button(
            marco_acciones,
            text="✏️ Modificar",
            command=self._editar_paciente,
        )
        btn_editar.pack(side=tk.LEFT, padx=(0, 6))

        btn_eliminar = ttk.Button(
            marco_acciones,
            text="🗑️ Eliminar",
            command=self._eliminar_paciente,
        )
        btn_eliminar.pack(side=tk.LEFT, padx=(0, 6))

        btn_actualizar = ttk.Button(
            marco_acciones,
            text="🔄 Actualizar lista",
            command=self.actualizar,
        )
        btn_actualizar.pack(side=tk.LEFT)

        # Busqueda de registros
        marco_buscar = ttk.Frame(marco_acciones)
        marco_buscar.pack(side=tk.RIGHT)

        ttk.Label(marco_buscar, text="Buscar paciente:").pack(side=tk.LEFT, padx=(0, 5))
        self.txt_buscar = ttk.Entry(marco_buscar, width=18)
        self.txt_buscar.pack(side=tk.LEFT)
        self.txt_buscar.bind("<KeyRelease>", lambda event: self._buscar_en_tabla())

        # Tabla de pacientes
        marco_tabla = ttk.Frame(self)
        marco_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 10))

        columnas = ("nombre", "identificacion", "telefono")
        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse",
        )

        self.tabla.heading("nombre", text="Nombre del Paciente")
        self.tabla.heading("identificacion", text="Identificación / Cédula")
        self.tabla.heading("telefono", text="Teléfono")

        self.tabla.column("nombre", width=300, anchor=tk.W)
        self.tabla.column("identificacion", width=180, anchor=tk.CENTER)
        self.tabla.column("telefono", width=180, anchor=tk.CENTER)

        scroll = ttk.Scrollbar(marco_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Doble clic para modificar rapido
        self.tabla.bind("<Double-1>", lambda event: self._editar_paciente())

        # Barra inferior de estado y conteo
        self.lbl_estado = ttk.Label(self, text="", font=("Arial", 9))
        self.lbl_estado.pack(fill=tk.X, padx=20, pady=(0, 15))

    def actualizar(self):
        # Carga los pacientes desde el servicio y los muestra en la tabla.
        try:
            pacientes = obtener_pacientes()
            self.pacientes_guardados = {}

            # Almacenamos en el diccionario con su id
            for p in pacientes:
                self.pacientes_guardados[p.id] = p

            self._mostrar_pacientes(pacientes)

            # Conteo aritmetico
            total = len(pacientes)
            self.lbl_estado.config(text=f"Total de registros: {total} paciente(s).")

        except (ValueError, ErrorAlmacenamiento) as error:
            manejar_error(error, titulo="Error al cargar pacientes", parent=self)
        except Exception as error:
            manejar_error(error, titulo="Error inesperado", parent=self)

    def _mostrar_pacientes(self, lista):
        # Llena la tabla con los pacientes recibidos.
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for p in lista:
            tel = p.telefono if p.telefono != "" else "(Sin teléfono)"
            # Guardamos el id del paciente como identificador de la fila
            self.tabla.insert(
                "",
                tk.END,
                iid=p.id,
                values=(p.nombre, p.identificacion, tel),
            )

    def _buscar_en_tabla(self):
        # Filtra los pacientes mostrados segun el texto ingresado.
        texto = self.txt_buscar.get().strip().lower()
        if texto == "":
            self._mostrar_pacientes(list(self.pacientes_guardados.values()))
            return

        coincidencias = []
        for p in self.pacientes_guardados.values():
            if texto in p.nombre.lower() or texto in p.identificacion.lower() or texto in p.telefono.lower():
                coincidencias.append(p)

        self._mostrar_pacientes(coincidencias)

    def _obtener_seleccionado(self):
        # Obtiene el objeto Paciente seleccionado en la tabla.
        seleccion = self.tabla.selection()
        if len(seleccion) == 0:
            mostrar_advertencia(
                "Aviso",
                "Por favor, selecciona un paciente de la lista.",
                parent=self,
            )
            return None

        paciente_id = seleccion[0]
        return self.pacientes_guardados.get(paciente_id)

    def _nuevo_paciente(self):
        PacienteFormDialog(self, on_guardar=self.actualizar)

    def _editar_paciente(self):
        paciente = self._obtener_seleccionado()
        if paciente is not None:
            PacienteFormDialog(self, paciente=paciente, on_guardar=self.actualizar)

    def _eliminar_paciente(self):
        paciente = self._obtener_seleccionado()
        if paciente is None:
            return

        # Confirmamos la eliminacion
        mensaje = f"¿Está seguro de eliminar al paciente '{paciente.nombre}'?"
        if not confirmar_accion("Confirmar eliminación", mensaje, parent=self):
            return

        try:
            eliminar_paciente(paciente.id)
            mostrar_info("Éxito", "El paciente ha sido eliminado.", parent=self)
            self.actualizar()
        except (ValueError, ErrorAlmacenamiento) as error:
            manejar_error(error, titulo="No se pudo eliminar el paciente", parent=self)
        except Exception as error:
            manejar_error(error, titulo="Error inesperado", parent=self)
