# Plan de Implementación Académico (Programación I)

Este plan actualiza y alinea todo el código del backend y de la interfaz gráfica en Tkinter para cumplir estrictamente con los parámetros y la estructura académica de la asignatura Programación I, garantizando que el código parezca desarrollado por un estudiante pero manteniendo el 100% de la funcionalidad, seguridad y validaciones.

---

## 1. Parámetros Académicos y Cómo se Reflejarán en el Código

| Parámetro Requerido | Implementación en el Código | Ubicación Principal |
|---|---|---|
| **Variables y constantes** | Definición explícita de constantes en mayúsculas (`ARCHIVO_PACIENTES = "pacientes.json"`, `FORMATO_FECHA = "%Y-%m-%d"`, etc.) y variables con nombres descriptivos simples (`contador`, `encontrado`, `indice`). | `services/`, `models/`, `ui/` |
| **Tipos de datos** | Cadenas de texto (`str`), enteros (`int`), booleanos (`bool`), listas (`list`), diccionarios (`dict`) y objetos/clases. | En todo el proyecto |
| **Operadores aritméticos, relacionales y lógicos** | Aritméticos (`+`, `-`, incremento `contador += 1`), relacionales (`==`, `!=`, `<`, `>`), lógicos (`and`, `or`, `not`). | Validaciones, filtros, conteos en reportes e inicio |
| **Estructuras condicionales** | Bloques limpios de `if`, `elif`, `else` para la toma de decisiones y validaciones. | En formularios, filtros y servicios |
| **Estructuras repetitivas (`for` y `while`)** | Búsquedas y recorridos mediante bucles `for` y bucles `while` (por ejemplo, búsqueda secuencial con índice `i = 0; while i < len(lista): ... i += 1`). | `services/citas_service.py`, `services/pacientes_service.py`, etc. |
| **Funciones con parámetros y retorno** | Funciones modulares con argumentos claros y sentencias `return` explícitas. | En todos los servicios y controladores |
| **Uso de listas para almacenar información** | Listas de objetos y diccionarios cargadas desde JSON, agregando elementos con `.append()` y manipulándolas. | `almacenamiento.py`, servicios |
| **Recorridos y búsquedas en listas** | Algoritmos de búsqueda lineal legibles para estudiante (con bandera `encontrado = False` o retorno directo). | `buscar_citas`, `obtener_pacientes`, etc. |
| **Validación de datos de entrada** | Validación de campos obligatorios, cadenas no vacías, formato de fecha (`AAAA-MM-DD`) y hora (`HH:MM`). | `validaciones.py`, formularios |
| **Menú principal interactivo** | Barra lateral y/o barra de menú con las opciones del sistema, permitiendo cambiar de vistas interactivamente. | `ui/ventana_principal.py` |
| **Modularización del código mediante funciones** | Separación limpia en modelos (`models/`), lógica de negocio (`services/`), vistas y formularios (`ui/`). | En toda la arquitectura |
| **Comentarios explicativos en el código** | Comentarios en español claros y didácticos que expliquen paso a paso qué hace cada bloque (estilo estudiante). | En todos los archivos `.py` |
| **Organización adecuada del programa** | Estructura de carpetas ordenada (`src/models/`, `src/services/`, `src/ui/`, `data/`). | Estructura modular del proyecto |

---

## 2. Alineación con la Estructura Funcional Requerida

El sistema cubrirá de forma explícita las operaciones solicitadas:

1. **Menú principal**:
   - Barra lateral interactiva y menú superior de opciones con acceso a cada módulo.
2. **Registrar información**:
   - Formulario para registrar nuevo paciente (nombre, identificación, teléfono).
   - Formulario para registrar nuevo doctor (nombre, especialidad).
   - Formulario para agendar nueva cita (selección de paciente, doctor, fecha y hora).
3. **Consultar información**:
   - Listado de pacientes en tabla.
   - Listado de doctores en tabla.
   - Listado de citas médicas en tabla con datos detallados.
   - Agenda del día actual en la pantalla de inicio.
4. **Buscar registros**:
   - Búsqueda y filtrado de citas por **Paciente**, **Doctor** y **Fecha**.
   - Búsqueda rápida de pacientes y doctores por texto/identificación.
5. **Modificar registros**:
   - Botón "Modificar / Editar" en pacientes, doctores y citas con carga de datos en formulario modal.
6. **Eliminar registros**:
   - Botón "Eliminar" con cuadro de diálogo de confirmación previa.
   - Regla de seguridad: Si un paciente o doctor tiene citas asociadas, el sistema bloquea la eliminación y explica el motivo.
   - Cancelación/eliminación de citas.
7. **Reportes**:
   - Reporte 1: Consultar agenda por fecha determinada.
   - Reporte 2: Consultar citas por doctor seleccionado.
   - Conteo y ordenamiento de resultados por fecha y hora.
8. **Salir del sistema**:
   - Botón visible "Salir" en el menú principal con mensaje de confirmación (`¿Desea salir del sistema?`).

---

## 3. Cambios Específicos por Archivo

### A. Backend

#### `src/services/almacenamiento.py`
- Reemplazar la escritura atómica avanzada (`NamedTemporaryFile`, `os.fsync`) por una apertura de archivo tradicional con `with open(..., "w", encoding="utf-8") as archivo: json.dump(...)`.
- Mantener la clase `ErrorAlmacenamiento` y capturar `json.JSONDecodeError` y `OSError`.
- Si el archivo no existe, retornar lista vacía `[]`.
- Añadir comentarios sencillos explicando lectura y escritura de archivos JSON.

#### `src/services/validaciones.py`
- Usar operadores lógicos y condicionales sencillos:
  ```python
  # Validar que el texto no sea vacio
  if valor is None or valor.strip() == "":
      raise ValueError(f"{nombre_campo} es obligatorio.")
  ```
- Validar formato de fecha y hora usando `datetime.strptime`.

#### `src/models/paciente.py`, `doctor.py`, `cita.py`
- Clases con `__init__`, `to_dict()` y `from_dict(data)`.
- Reemplazar comprensiones complejas por validaciones directas `if "nombre" not in data:` y comentarios explicativos.

#### `src/services/pacientes_service.py` y `doctores_service.py`
- Utilizar constantes: `ARCHIVO_PACIENTES = "pacientes.json"`, `ARCHIVO_DOCTORES = "doctores.json"`.
- Utilizar bucles tradicionales (`for` y `while`) para búsquedas y validación de duplicados:
  ```python
  # Verificar si la identificacion ya esta registrada usando un bucle while
  i = 0
  while i < len(pacientes):
      if pacientes[i].identificacion == identificacion:
          raise ValueError("Ya existe un paciente con esa identificación.")
      i += 1
  ```
- Mantener la verificación de citas asociadas antes de eliminar.

#### `src/services/citas_service.py`
- Usar constante `ARCHIVO_CITAS = "citas.json"`.
- Verificar disponibilidad del doctor mediante recorrido `for`:
  ```python
  for cita in citas:
      if cita.id != excluir_id:
          if cita.doctor_id == doctor_id and cita.fecha == fecha and cita.hora == hora:
              raise ValueError("Horario no disponible: el doctor ya tiene una cita en esa fecha y hora.")
  ```
- Simplificar `buscar_citas(criterio, valor)` con estructura `if/elif/else` clara.
- Enriquecer `obtener_citas_detalladas` con bucles comprensibles y comentarios didácticos.

---

### B. Frontend (Tkinter)

#### `src/ui/widgets/mensajes.py`
- Funciones modulares sencillas para `mostrar_info`, `mostrar_error`, `mostrar_advertencia`, `confirmar_accion` y `manejar_error`.

#### `src/ui/dialogs/` (`paciente_form.py`, `doctor_form.py`, `cita_form.py`)
- Diálogos modales sencillos y directos con `tk.Toplevel`.
- Etiquetas claras, campos `ttk.Entry` y `ttk.Combobox`.
- Botones "Guardar" y "Cancelar".
- Manejo de excepciones `(ValueError, ErrorAlmacenamiento)` sin cerrar el diálogo si hay error.

#### `src/ui/views/` (`inicio_view.py`, `pacientes_view.py`, `doctores_view.py`, `citas_view.py`, `reportes_view.py`)
- Nombres de botones explícitos:
  - Pacientes: `[➕ Registrar Paciente]`, `[✏️ Modificar]`, `[🗑️ Eliminar]`, `[🔄 Actualizar lista]`, `[🔍 Buscar]`.
  - Doctores: `[➕ Registrar Doctor]`, `[✏️ Modificar]`, `[🗑️ Eliminar]`, `[🔄 Actualizar lista]`, `[🔍 Buscar]`.
  - Citas: `[➕ Registrar / Agendar Cita]`, `[✏️ Modificar]`, `[❌ Cancelar Cita]`, `[🔄 Actualizar lista]`, panel `[🔍 Buscar registros]`.
  - Reportes: Consulta por fecha y consulta por doctor con conteo de registros (`contador = contador + 1`).
  - Inicio: Consulta de la agenda del día actual.

#### `src/ui/ventana_principal.py`
- Menú lateral con opciones:
  - 🏠 Inicio (Consultar agenda de hoy)
  - 👥 Pacientes (Registrar, Consultar, Modificar, Eliminar)
  - 🩺 Doctores (Registrar, Consultar, Modificar, Eliminar)
  - 📅 Citas (Registrar, Consultar, Buscar, Modificar, Eliminar)
  - 📊 Reportes (Consultas y estadísticas)
  - 🚪 Salir del sistema (con confirmación `confirmar_accion`)
- Barra de menú superior (Menú "Archivo" -> Salir, Menú "Operaciones" -> Registrar, Consultar, etc.).

#### `src/main.py`
- Archivo principal claro y bien estructurado que inicia la aplicación.

---

## 4. Plan de Verificación

1. **Verificación de Requisitos Académicos**:
   - Comprobar presencia de variables, constantes (`CONSTANTE = ...`), operadores aritméticos (`+`), relacionales y lógicos (`and`, `or`, `not`).
   - Comprobar presencia explícita de bucles `for` y `while`.
   - Comprobar presencia de condicionales `if`, `elif`, `else`.
   - Comprobar manejo de listas (`.append()`, `.remove()`, indexación).
   - Comprobar comentarios didácticos en todos los archivos.
2. **Verificación Funcional**:
   - Ejecutar script de prueba integral verificando alta, consulta, modificación, eliminación y validaciones de negocio.
   - Probar que no permita duplicar cédula de paciente.
   - Probar que no permita cita duplicada para el doctor en la misma fecha y hora.
   - Probar que bloquee eliminación de paciente o doctor con citas asociadas.
   - Probar reportes y persistencia en los archivos JSON de `data/`.
