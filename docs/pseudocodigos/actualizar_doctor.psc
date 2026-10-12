Algoritmo ActualizarDoctor
	Definir ids, nombres, especialidades Como Cadena
	Definir idBuscado, nombreNuevo, especialidadNueva Como Cadena
	Definir cantidad, i, posicion Como Entero
	Dimension ids[100]
	Dimension nombres[100]
	Dimension especialidades[100]
	cantidad <- 0 // Cargar doctores existentes.
	Escribir "ID del doctor a actualizar:"
	Leer idBuscado
	posicion <- 0
	Si cantidad > 0 Entonces
		Para i <- 1 Hasta cantidad Hacer
			Si ids[i] = idBuscado Entonces
				posicion <- i
			FinSi
		FinPara
	FinSi
	Si posicion = 0 Entonces
		Escribir "Error: doctor no encontrado."
	SiNo
		Escribir "Nuevo nombre:"
		Leer nombreNuevo
		Escribir "Nueva especialidad:"
		Leer especialidadNueva
		Si nombreNuevo = "" O especialidadNueva = "" Entonces
			Escribir "Error: nombre y especialidad son obligatorios."
		SiNo
			nombres[posicion] <- nombreNuevo
			especialidades[posicion] <- especialidadNueva
			Escribir "Doctor actualizado; guardar doctores.json."
		FinSi
	FinSi
FinAlgoritmo
