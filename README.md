# Sistema de Gestión de Citas Médicas

Este proyecto lo hice para organizar las citas de un consultorio pequeño. Desde la aplicación se pueden guardar pacientes y doctores, agendar citas y consultar la agenda. Está programado en Python y usa Tkinter para las ventanas. La información queda guardada en archivos JSON dentro de `data/`.

## Cómo iniciar el programa

Se necesita Python 3 con Tkinter instalado. No hace falta instalar paquetes adicionales.

1. Abre una terminal en la carpeta del proyecto.
2. Ejecuta este comando:

   ```powershell
   python src/main.py
   ```

   Si en tu equipo usas el lanzador de Windows, también puedes probar `py src/main.py`.
3. Al abrirse la ventana, usa el menú de la izquierda o el menú superior para entrar a cada sección.

## Guía de las secciones

### Inicio

Muestra las citas programadas para la fecha actual, con la hora, el paciente y el doctor. El botón **Actualizar** vuelve a cargar la agenda.

### Pacientes

En esta sección puedes registrar, modificar y eliminar pacientes. Para registrar uno, pulsa **Registrar Paciente** y completa el nombre y la identificación; el teléfono es opcional. También puedes escribir en el campo de búsqueda para filtrar la tabla por nombre, identificación o teléfono.

Para modificar o eliminar un registro, selecciónalo primero en la tabla. Si haces doble clic sobre un paciente, se abre su formulario de modificación. No se puede borrar un paciente que tenga citas asociadas.

### Doctores

Aquí puedes registrar, modificar, buscar y eliminar doctores. El nombre y la especialidad son obligatorios. Selecciona un doctor en la tabla para modificarlo o eliminarlo. Si tiene citas asociadas, el sistema no permitirá eliminarlo.

### Citas

Antes de agendar una cita, registra al paciente y al doctor. Pulsa **Agendar Cita**, selecciona ambos y completa la fecha y la hora. La fecha se escribe como `AAAA-MM-DD` y la hora en formato de 24 horas, por ejemplo `14:30`.

La aplicación no permite asignar al mismo doctor dos citas con la misma fecha y hora exactas. En esta pantalla también puedes modificar o cancelar una cita. Para buscar, selecciona fecha, paciente o doctor en el filtro; **Mostrar todas** vuelve a cargar la lista completa.

### Reportes

La pestaña **Agenda por Fecha** permite consultar las citas de una fecha. La pestaña **Citas por Doctor** muestra las citas del doctor seleccionado. Las tablas incluyen fecha, hora, paciente y doctor.

## Datos guardados

Los registros se guardan localmente en:

- `data/pacientes.json`
- `data/doctores.json`
- `data/citas.json`

Al guardar un cambio, el archivo correspondiente se actualiza. Si vas a limpiar o reemplazar estos archivos, haz una copia primero: contienen los registros del consultorio.

## Carpetas del proyecto

- `src/models/`: clases que representan pacientes, doctores y citas.
- `src/services/`: reglas, validaciones y lectura o escritura de los datos.
- `src/ui/`: ventana principal, pantallas y formularios.
- `data/`: archivos JSON con los registros.
- `docs/`: estado del proyecto, pseudocódigos y diagramas usados para diseñarlo.

## Alcance

El programa trabaja en una sola computadora y no necesita conexión a internet. No incluye inicio de sesión, notificaciones ni una base de datos. Las reglas de las citas revisan coincidencias exactas de fecha y hora; no se definió duración para detectar citas que se solapan.
