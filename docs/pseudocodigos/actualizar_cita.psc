Algoritmo ActualizarCita
	Definir ids, pacientes, doctores, fechas, horas Como Cadena
	Definir idBuscado, pacienteId, doctorId, fecha, hora Como Cadena
	Definir cantidad, i, posicion Como Entero
	Definir entidadesValidas, horarioOcupado, doctorExiste Como Logico
	Definir cantidadPacientes, cantidadDoctores Como Entero
	Definir pacientesExistentes, doctoresExistentes Como Cadena
	Dimension ids[100]
	Dimension pacientes[100]
	Dimension doctores[100]
	Dimension fechas[100]
	Dimension horas[100]
	Dimension pacientesExistentes[100]
	Dimension doctoresExistentes[100]
	cantidad <- 0 // Cargar citas; cargar tambien pacientes y doctores.
	cantidadPacientes <- 0
	cantidadDoctores <- 0
	Escribir "ID de la cita que desea actualizar:"
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
		Escribir "Error: cita no encontrada."
	SiNo
		Escribir "ID del paciente:"
		Leer pacienteId
		Escribir "ID del doctor:"
		Leer doctorId
		Escribir "Nueva fecha (AAAA-MM-DD):"
		Leer fecha
		Escribir "Nueva hora (HH:MM):"
		Leer hora
		entidadesValidas <- Falso
		Si cantidadPacientes > 0 Entonces
			Para i <- 1 Hasta cantidadPacientes Hacer
				Si pacientesExistentes[i] = pacienteId Entonces
					entidadesValidas <- Verdadero
				FinSi
			FinPara
		FinSi
		doctorExiste <- Falso
		Si cantidadDoctores > 0 Entonces
			Para i <- 1 Hasta cantidadDoctores Hacer
				Si doctoresExistentes[i] = doctorId Entonces
					doctorExiste <- Verdadero
				FinSi
			FinPara
		FinSi
		entidadesValidas <- entidadesValidas Y doctorExiste
		Si No entidadesValidas Entonces
			Escribir "Error: paciente o doctor invalido."
		SiNo
			Si Longitud(fecha) <> 10 O Longitud(hora) <> 5 Entonces
				Escribir "Error: formato de fecha u hora invalido."
			SiNo
				horarioOcupado <- Falso
				Si cantidad > 0 Entonces
					Para i <- 1 Hasta cantidad Hacer
						Si i <> posicion Y doctores[i] = doctorId Y fechas[i] = fecha Y horas[i] = hora Entonces
							horarioOcupado <- Verdadero
						FinSi
					FinPara
				FinSi
				Si horarioOcupado Entonces
					Escribir "Error: el doctor ya tiene una cita en ese horario."
				SiNo
					pacientes[posicion] <- pacienteId
					doctores[posicion] <- doctorId
					fechas[posicion] <- fecha
					horas[posicion] <- hora
					Escribir "Cita actualizada; guardar citas.json."
				FinSi
			FinSi
		FinSi
	FinSi
FinAlgoritmo
