Algoritmo CargarDatos
	Definir nombreArchivo Como Cadena
	Definir archivoExiste, jsonValido, esLista Como Logico
	Escribir "Nombre del archivo JSON que se cargara:"
	Leer nombreArchivo
	// PSeInt no lee JSON de forma nativa: estas condiciones representan
	// los resultados que entrega la operacion de lectura del sistema real.
	Escribir "¿El archivo existe? (Verdadero/Falso):"
	Leer archivoExiste
	Si No archivoExiste Entonces
		Escribir "El archivo no existe; devolver lista vacia."
	SiNo
		Escribir "¿El JSON es valido? (Verdadero/Falso):"
		Leer jsonValido
		Si jsonValido Entonces
			Escribir "¿El contenido es una lista? (Verdadero/Falso):"
			Leer esLista
			Si esLista Entonces
				Escribir "Devolver lista de registros cargados desde ", nombreArchivo
			SiNo
				Escribir "Error: el contenido JSON no es una lista; devolver lista vacia sin sobrescribir."
			FinSi
		SiNo
			Escribir "Error: JSON dañado; devolver lista vacia sin sobrescribir."
		FinSi
	FinSi
FinAlgoritmo
