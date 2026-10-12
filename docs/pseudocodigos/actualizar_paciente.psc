Algoritmo ActualizarPaciente
	Definir ids, nombres, identificaciones, telefonos Como Cadena
	Definir idBuscado, nombreNuevo, identificacionNueva, telefonoNuevo Como Cadena
	Definir cantidad, i, posicion Como Entero
	Definir duplicada Como Logico
	Dimension ids[100]
	Dimension nombres[100]
	Dimension identificaciones[100]
	Dimension telefonos[100]
	cantidad <- 0 // Cargar aqui los pacientes existentes.
	Escribir "ID del paciente que desea actualizar:"
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
		Escribir "Error: paciente no encontrado."
	SiNo
		Escribir "Nuevo nombre:"
		Leer nombreNuevo
		Escribir "Nueva identificacion:"
		Leer identificacionNueva
		Escribir "Nuevo telefono (opcional):"
		Leer telefonoNuevo
		Si nombreNuevo = "" O identificacionNueva = "" Entonces
			Escribir "Error: los datos obligatorios no pueden estar vacios."
		SiNo
			duplicada <- Falso
			Si cantidad > 0 Entonces
				Para i <- 1 Hasta cantidad Hacer
					Si i <> posicion Y identificaciones[i] = identificacionNueva Entonces
						duplicada <- Verdadero
					FinSi
				FinPara
			FinSi
			Si duplicada Entonces
				Escribir "Error: identificacion duplicada."
			SiNo
				nombres[posicion] <- nombreNuevo
				identificaciones[posicion] <- identificacionNueva
				telefonos[posicion] <- telefonoNuevo
				Escribir "Paciente actualizado; guardar pacientes.json."
			FinSi
		FinSi
	FinSi
FinAlgoritmo
