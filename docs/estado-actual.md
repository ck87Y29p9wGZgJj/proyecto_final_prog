# Documentación inicial del estado actual

**Proyecto:** Sistema de gestión de citas médicas para consultorios pequeños  
**Fecha de actualización:** 2 de octubre de 2026  
**Estado:** desarrollo inicial; la interfaz y varios flujos funcionales todavía están pendientes. Por ahora solo se ha implementado logica de backend

## Propósito de este documento

Este documento registra lo que existe actualmente en el código del proyecto. Esta documentación detalla las funciones que ya están implementadas. Conforme a que se hagan actualizaciones se va a editar esta documentación.

## Resumen del estado

El programa utiliza uv para manejar dependencias y un entorno virtual .venv. 

Acontinuacion se muestran las principales caracteristicas del programa:

El proyecto cuenta con modelos de datos para pacientes, doctores y citas; servicios básicos para operar esas entidades; y una capa común que lee y escribe archivos JSON en `data/`. La aplicación abre una ventana Tkinter de bienvenida, pero todavía no presenta pantallas para administrar los registros ni conecta la interfaz con los servicios.

Área y estado actual 

Modelos de paciente, doctor y cita: Implementados con conversión a y desde diccionarios. 

Persistencia JSON: Implementada para cargar y guardar colecciones. 

Pacientes: Consulta, registro, actualización y eliminación disponibles en el servicio. 

Doctores: Consulta, registro, actualización y eliminación disponibles en el servicio. 

Citas: Consulta, registro, eliminación, agenda por fecha y filtro por doctor disponibles en el servicio. 

Validación de horario: El servicio de citas evita duplicar el mismo doctor, fecha y hora exactos. 

Interfaz gráfica: Solo hay una ventana de bienvenida; la gestión visual está pendiente. 

Búsqueda por paciente o fecha: aun no existe una función específica de búsqueda; solo está disponible el filtro por doctor y la consulta por fecha del día. 

Edición de citas: No implementada. 

Pruebas automatizadas: No se encontraron archivos de pruebas en la estructura revisada. 

## Estructura actual

```
proyecto-final/
├── data/
│   ├── pacientes.json
│   ├── doctores.json
│   └── citas.json
├── docs/
│   └── estado-actual.md
├── src/
   ├── main.py
   ├── models/
   │   ├── paciente.py
   │   ├── doctor.py
   │   └── cita.py
   └── services/
       ├── almacenamiento.py
       ├── pacientes_service.py
       ├── doctores_service.py
       └── citas_service.py
```

## Componentes implementados

### Punto de entrada

`src/main.py` crea una ventana Tkinter titulada **Gestión de Citas Médicas**, con tamaño inicial de 800 × 600 píxeles y un texto de bienvenida. Inicia el ciclo de eventos de Tkinter. Por ahora no carga los datos ni ofrece botones o formularios para usar los servicios.

### Modelos

Los modelos representan los campos que se guardan en JSON y proporcionan `to_dict()` y `from_dict()` para convertir entre objetos Python y diccionarios:

- **Paciente:** `id`, `nombre`, `identificacion`, `telefono`.
- **Doctor:** `id`, `nombre`, `especialidad`.
- **Cita:** `id`, `paciente_id`, `doctor_id`, `fecha`, `hora`.

Los identificadores nuevos son UUID almacenados como texto. Las citas relacionan pacientes y doctores mediante sus identificadores.

### Persistencia

`src/services/almacenamiento.py` calcula la carpeta raíz del proyecto a partir de la ubicación del archivo y usa `data/` como directorio de almacenamiento. `cargar_datos(nombre_archivo)` devuelve una lista vacía si el archivo no existe. Si ocurre un error de lectura o el JSON no se puede interpretar, imprime un mensaje en la consola y también devuelve una lista vacía. `guardar_datos(nombre_archivo, datos)` crea el directorio si hace falta, escribe JSON con indentación y caracteres Unicode preservados, e informa éxito o fallo mediante un valor booleano.

Actualmente los servicios no comprueban ese valor booleano al guardar; por ello, un fallo de escritura podría no llegar a quien llamó la operación como una excepción. 

### Servicio de pacientes

`src/services/pacientes_service.py` permite:

- Obtener todos los pacientes.
- Registrar un paciente con UUID. Nombre e identificación son obligatorios y la identificación debe ser única.
- Actualizar nombre, identificación y teléfono. Al cambiar la identificación, se evita duplicar la de otro paciente.
- Eliminar un paciente existente.

La eliminación no comprueba si el paciente tiene citas asociadas; el propio código lo deja indicado como pendiente. El teléfono no se valida como obligatorio.

### Servicio de doctores

`src/services/doctores_service.py` permite obtener, registrar, actualizar y eliminar doctores. Nombre y especialidad son obligatorios al registrar o actualizar. No se comprueba si hay citas asociadas antes de eliminar un doctor, y tampoco se evita registrar nombres duplicados.

### Servicio de citas

`src/services/citas_service.py` permite:

- Obtener todas las citas.
- Registrar una cita si la fecha y hora tienen algún valor, y si existen el paciente y el doctor referenciados.
- Rechazar otra cita del mismo doctor cuando coinciden exactamente la fecha y la hora.
- Eliminar una cita existente.
- Obtener citas de una fecha recibida como argumento.
- Filtrar citas por identificador de doctor.

La validación compara los valores recibidos como texto. No valida un formato real de fecha u hora ni detecta intervalos superpuestos; la regla implementada cubre coincidencias exactas. No existe una operación para modificar una cita ni funciones de búsqueda por paciente.

## Formato de los datos

Los archivos contienen arreglos JSON. Cuando haya registros, se espera una estructura equivalente a la siguiente:

```json
{
  "id": "identificador-uuid",
  "nombre": "Nombre de ejemplo",
  "identificacion": "ID-001",
  "telefono": "809-555-0100"
}
```

Para doctores, los campos son `id`, `nombre` y `especialidad`. Para citas, son `id`, `paciente_id`, `doctor_id`, `fecha` y `hora`. El código no impone actualmente un formato de fecha u hora; la propuesta recomienda usar `AAAA-MM-DD` y `HH:MM`, respectivamente.

## Ejecución disponible

El punto de entrada puede iniciarse desde la carpeta raíz del proyecto con el comando: python src/main.py


Se requiere Python 3 con Tkinter disponible. La ventana actual solo muestra el mensaje de bienvenida. 


## Próximos pasos 

1. Crear las pantallas Tkinter de pacientes, doctores y citas, conectándolas con los servicios existentes.
2. Definir y validar formatos de fecha y hora antes de guardar citas.
3. Resolver la eliminación de pacientes o doctores con citas relacionadas para evitar referencias huérfanas.
4. Añadir edición de citas y búsquedas por paciente y fecha.
5. Crear los reportes visibles de citas del día y por doctor.
6. Manejar errores de persistencia de forma que la interfaz los pueda comunicar y los datos dañados no se sobrescriban silenciosamente.
7. Revisar y completar este documento cuando las funciones estén integradas; documentar las pruebas manuales realizadas y sus resultados.


