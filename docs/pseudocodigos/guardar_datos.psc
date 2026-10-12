Algoritmo GuardarDatos
	Definir nombreArchivo Como Cadena
	Definir carpetaExiste, escrituraExitosa Como Logico
	Escribir "Nombre del archivo JSON:"
	Leer nombreArchivo
	Escribir "¿Existe la carpeta data? (Verdadero/Falso):"
	Leer carpetaExiste
	Si No carpetaExiste Entonces
		Escribir "Crear carpeta data/"
	FinSi
	Escribir "Convertir los registros a JSON y escribirlos con indentacion y Unicode."
	Escribir "¿La escritura fue exitosa? (Verdadero/Falso):"
	Leer escrituraExitosa
	Si escrituraExitosa Entonces
		Escribir "Datos guardados en ", nombreArchivo
	SiNo
		Escribir "Error al guardar; devolver Falso."
	FinSi
FinAlgoritmo
