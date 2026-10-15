# PROYECTO FINAL - PROGRAMACIÓN I
# Sistema de Gestión de Citas Médicas
# Punto de entrada principal del programa


import os
import sys
from pathlib import Path

# Configuramos la ruta para que Python encuentre los modulos dentro de src/
RUTA_SRC = Path(__file__).resolve().parent
if str(RUTA_SRC) not in sys.path:
    sys.path.insert(0, str(RUTA_SRC))

# Importamos la ventana principal
from ui.ventana_principal import VentanaPrincipal


def main():
    # Inicializamos la aplicacion grafica
    app = VentanaPrincipal()
    # Iniciamos el bucle principal de eventos de Tkinter
    app.mainloop()


if __name__ == "__main__":
    main()
