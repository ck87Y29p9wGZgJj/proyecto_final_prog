Algoritmo EliminarDoctor
	Definir ids, doctorIdsCita Como Cadena
	Definir idBuscado Como Cadena
	Definir cantidadDoctores, cantidadCitas, i, posicion Como Entero
	Definir tieneCitas Como Logico
	Dimension ids[100]
	Dimension doctorIdsCita[100]
	cantidadDoctores <- 0 // Cargar doctores.
	cantidadCitas <- 0 // Cargar citas.
	Escribir "ID del doctor que desea eliminar:"
	Leer idBuscado
	posicion <- 0
	Si cantidadDoctores > 0 Entonces
		Para i <- 1 Hasta cantidadDoctores Hacer
			Si ids[i] = idBuscado Entonces
				posicion <- i
			FinSi
		FinPara
	FinSi
	Si posicion = 0 Entonces
		Escribir "Error: doctor no encontrado."
	SiNo
		tieneCitas <- Falso
		Si cantidadCitas > 0 Entonces
			Para i <- 1 Hasta cantidadCitas Hacer
				Si doctorIdsCita[i] = idBuscado Entonces
					tieneCitas <- Verdadero
				FinSi
			FinPara
		FinSi
		Si tieneCitas Entonces
			Escribir "No se puede eliminar: cancele o reasigne sus citas primero."
		SiNo
			Si posicion < cantidadDoctores Entonces
				Para i <- posicion Hasta cantidadDoctores - 1 Hacer
					ids[i] <- ids[i + 1]
				FinPara
			FinSi
			cantidadDoctores <- cantidadDoctores - 1
			Escribir "Doctor eliminado; guardar doctores.json."
		FinSi
	FinSi
FinAlgoritmo
