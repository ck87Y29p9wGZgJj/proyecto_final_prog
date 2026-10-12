Algoritmo EliminarPaciente
	Definir ids, pacienteIdsCita Como Cadena
	Definir idBuscado Como Cadena
	Definir cantidadPacientes, cantidadCitas, i, posicion Como Entero
	Definir tieneCitas Como Logico
	Dimension ids[100]
	Dimension pacienteIdsCita[100]
	cantidadPacientes <- 0 // Cargar pacientes.
	cantidadCitas <- 0 // Cargar citas.
	Escribir "ID del paciente que desea eliminar:"
	Leer idBuscado
	posicion <- 0
	Si cantidadPacientes > 0 Entonces
		Para i <- 1 Hasta cantidadPacientes Hacer
			Si ids[i] = idBuscado Entonces
				posicion <- i
			FinSi
		FinPara
	FinSi
	Si posicion = 0 Entonces
		Escribir "Error: paciente no encontrado."
	SiNo
		tieneCitas <- Falso
		Si cantidadCitas > 0 Entonces
			Para i <- 1 Hasta cantidadCitas Hacer
				Si pacienteIdsCita[i] = idBuscado Entonces
					tieneCitas <- Verdadero
				FinSi
			FinPara
		FinSi
		Si tieneCitas Entonces
			Escribir "No se puede eliminar: cancele o reasigne sus citas primero."
		SiNo
			Si posicion < cantidadPacientes Entonces
				Para i <- posicion Hasta cantidadPacientes - 1 Hacer
					ids[i] <- ids[i + 1]
				FinPara
			FinSi
			cantidadPacientes <- cantidadPacientes - 1
			Escribir "Paciente eliminado; guardar pacientes.json."
		FinSi
	FinSi
FinAlgoritmo
