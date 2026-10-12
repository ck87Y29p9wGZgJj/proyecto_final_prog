Algoritmo FlujoGeneral
	Definir archivosCorrectos, continuar, operacionValida Como Logico
	Definir opcion Como Entero
	Escribir "Cargar pacientes.json, doctores.json y citas.json."
	Escribir "¿Los archivos se pudieron leer correctamente? (Verdadero/Falso):"
	Leer archivosCorrectos
	Si No archivosCorrectos Entonces
		Escribir "Advertencia: revisar archivos; continuar con las listas que se pudieron cargar."
	FinSi
	continuar <- Verdadero
	Mientras continuar Hacer
		Escribir "Seleccione una operacion:"
		Escribir "1. Gestion de pacientes"
		Escribir "2. Gestion de doctores"
		Escribir "3. Gestion de citas"
		Escribir "4. Busqueda"
		Escribir "5. Reportes"
		Escribir "0. Cerrar aplicacion"
		Leer opcion
		Si opcion = 0 Entonces
			continuar <- Falso
		SiNo
			operacionValida <- opcion >= 1 Y opcion <= 5
			Si operacionValida Entonces
				Escribir "Ejecutar la funcion correspondiente a la opcion."
				Escribir "Si hubo cambios, guardar la coleccion correspondiente en JSON."
			SiNo
				Escribir "Opcion no valida."
			FinSi
		FinSi
	FinMientras
	Escribir "Fin: los datos guardados permanecen en los archivos JSON."
FinAlgoritmo
