Algoritmo RegistrarCita
	Definir pacienteId, doctorId, fecha, hora Como Cadena
	Definir pacienteExiste, doctorExiste, horarioOcupado Como Logico
	Definir fechaValida, horaValida Como Logico
	Definir cantidadPacientes, cantidadDoctores, cantidadCitas, i Como Entero
	Definir pacientesExistentes, doctoresExistentes Como Cadena
	Definir citaPaciente, citaDoctor, citaFecha, citaHora Como Cadena
	Dimension pacientesExistentes[100]
	Dimension doctoresExistentes[100]
	Dimension citaPaciente[100]
	Dimension citaDoctor[100]
	Dimension citaFecha[100]
	Dimension citaHora[100]
	cantidadPacientes <- 0 // Cargar pacientes y doctores para validar.
	cantidadDoctores <- 0
	cantidadCitas <- 0
	Escribir "ID del paciente:"
	Leer pacienteId
	Escribir "ID del doctor:"
	Leer doctorId
	Escribir "Fecha (AAAA-MM-DD):"
	Leer fecha
	Escribir "Hora (HH:MM):"
	Leer hora
	pacienteExiste <- Falso
	doctorExiste <- Falso
	Si cantidadPacientes > 0 Entonces
		Para i <- 1 Hasta cantidadPacientes Hacer
			Si pacientesExistentes[i] = pacienteId Entonces
				pacienteExiste <- Verdadero
			FinSi
		FinPara
	FinSi
	Si cantidadDoctores > 0 Entonces
		Para i <- 1 Hasta cantidadDoctores Hacer
			Si doctoresExistentes[i] = doctorId Entonces
				doctorExiste <- Verdadero
			FinSi
		FinPara
	FinSi
	Si No pacienteExiste Entonces
		Escribir "Error: el paciente seleccionado no existe."
	SiNo
		Si No doctorExiste Entonces
			Escribir "Error: el doctor seleccionado no existe."
		SiNo
			fechaValida <- Longitud(fecha) = 10
			horaValida <- Longitud(hora) = 5
			Si No fechaValida O No horaValida Entonces
				Escribir "Error: use fecha AAAA-MM-DD y hora HH:MM."
			SiNo
				horarioOcupado <- Falso
				Si cantidadCitas > 0 Entonces
					Para i <- 1 Hasta cantidadCitas Hacer
						Si citaDoctor[i] = doctorId Y citaFecha[i] = fecha Y citaHora[i] = hora Entonces
							horarioOcupado <- Verdadero
						FinSi
					FinPara
				FinSi
				Si horarioOcupado Entonces
					Escribir "Error: el horario ya esta ocupado."
				SiNo
					Escribir "Cita agendada; guardar citas.json."
				FinSi
			FinSi
		FinSi
	FinSi
FinAlgoritmo
