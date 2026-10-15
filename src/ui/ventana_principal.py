# VENTANA PRINCIPAL
# Contenedor principal con menu de navegacion y vistas del sistema


import tkinter as tk
from tkinter import ttk

from ui.views.citas_view import CitasView
from ui.views.doctores_view import DoctoresView
from ui.views.inicio_view import InicioView
from ui.views.pacientes_view import PacientesView
from ui.views.reportes_view import ReportesView
from ui.widgets.mensajes import confirmar_accion


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestión de Citas Médicas")
        self.geometry("1020x660")
        self.minsize(880, 540)

        # Configurar estilos basicos
        self._configurar_estilos()

        # Construir menu superior y barra lateral
        self._crear_menu_superior()
        self._crear_layout()
        self._cargar_vistas()

        # Iniciar en la vista de Inicio
        self.mostrar_vista("inicio")

        # Confirmar salida al cerrar la ventana con la X
        self.protocol("WM_DELETE_WINDOW", self._salir_del_sistema)

    def _configurar_estilos(self):
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        # Configuracion visual de tablas y botones
        self.style.configure("Treeview", font=("Arial", 9), rowheight=24)
        self.style.configure("Treeview.Heading", font=("Arial", 9, "bold"))
        self.style.configure("TButton", font=("Arial", 9))
        self.style.configure("TLabel", font=("Arial", 9))

    def _crear_menu_superior(self):
        # Crea la barra de menus superior del sistema.
        barra_menu = tk.Menu(self)

        # Menu Archivo
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Inicio", command=lambda: self.mostrar_vista("inicio"))
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir del sistema", command=self._salir_del_sistema)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

        # Menu Modulos
        menu_modulos = tk.Menu(barra_menu, tearoff=0)
        menu_modulos.add_command(label="Pacientes", command=lambda: self.mostrar_vista("pacientes"))
        menu_modulos.add_command(label="Doctores", command=lambda: self.mostrar_vista("doctores"))
        menu_modulos.add_command(label="Citas Médicas", command=lambda: self.mostrar_vista("citas"))
        menu_modulos.add_command(label="Reportes", command=lambda: self.mostrar_vista("reportes"))
        barra_menu.add_cascade(label="Módulos", menu=menu_modulos)

        self.config(menu=barra_menu)

    def _crear_layout(self):
        # Configuramos la cuadricula principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Barra lateral izquierda
        self.sidebar = tk.Frame(self, bg="#2c3e50", width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Titulo en la barra lateral
        lbl_logo = tk.Label(
            self.sidebar,
            text="🏥 MediCitas",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
        )
        lbl_logo.pack(pady=(20, 5))

        lbl_sub = tk.Label(
            self.sidebar,
            text="Gestión de Citas",
            font=("Arial", 8),
            bg="#2c3e50",
            fg="#bdc3c7",
        )
        lbl_sub.pack(pady=(0, 20))

        # Botones de navegacion
        self.botones_menu = {}
        opciones = [
            ("inicio", "🏠 Inicio"),
            ("pacientes", "👥 Pacientes"),
            ("doctores", "🩺 Doctores"),
            ("citas", "📅 Citas"),
            ("reportes", "📊 Reportes"),
        ]

        for clave, texto in opciones:
            btn = tk.Button(
                self.sidebar,
                text=texto,
                font=("Arial", 10, "bold"),
                anchor="w",
                padx=15,
                pady=8,
                bg="#2c3e50",
                fg="#ecf0f1",
                activebackground="#34495e",
                activeforeground="#ffffff",
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda k=clave: self.mostrar_vista(k),
            )
            btn.pack(fill=tk.X, padx=10, pady=2)
            self.botones_menu[clave] = btn

        # Boton visible para Salir del sistema
        btn_salir = tk.Button(
            self.sidebar,
            text="🚪 Salir del sistema",
            font=("Arial", 9, "bold"),
            bg="#c0392b",
            fg="#ffffff",
            activebackground="#e74c3c",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            command=self._salir_del_sistema,
        )
        btn_salir.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=20)

        # Area central para mostrar las vistas
        self.area_central = ttk.Frame(self)
        self.area_central.grid(row=0, column=1, sticky="nsew")
        self.area_central.grid_rowconfigure(0, weight=1)
        self.area_central.grid_columnconfigure(0, weight=1)

    def _cargar_vistas(self):
        # Instancia los marcos de cada seccion dentro del area central.
        self.vistas = {}

        self.vistas["inicio"] = InicioView(self.area_central, controlador=self)
        self.vistas["pacientes"] = PacientesView(self.area_central, controlador=self)
        self.vistas["doctores"] = DoctoresView(self.area_central, controlador=self)
        self.vistas["citas"] = CitasView(self.area_central, controlador=self)
        self.vistas["reportes"] = ReportesView(self.area_central, controlador=self)

        # Colocamos todas en la misma posicion grid (para elevar la activa con tkraise)
        for vista in self.vistas.values():
            vista.grid(row=0, column=0, sticky="nsew")

    def mostrar_vista(self, clave_vista):
        # Cambia a la vista seleccionada y actualiza sus registros.
        if clave_vista not in self.vistas:
            return

        # Traemos la vista seleccionada al frente
        vista_activa = self.vistas[clave_vista]
        vista_activa.tkraise()

        # Si la vista tiene metodo actualizar, lo llamamos
        if hasattr(vista_activa, "actualizar"):
            vista_activa.actualizar()

        # Resaltamos visualmente el boton activo en el menu
        for clave, btn in self.botones_menu.items():
            if clave == clave_vista:
                btn.config(bg="#3498db", fg="#ffffff")
            else:
                btn.config(bg="#2c3e50", fg="#ecf0f1")

    def _salir_del_sistema(self):
        # Pide confirmacion antes de cerrar el programa.
        if confirmar_accion("Salir", "¿Desea salir del sistema?", parent=self):
            self.destroy()
