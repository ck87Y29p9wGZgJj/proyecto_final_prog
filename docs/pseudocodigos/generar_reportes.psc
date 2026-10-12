Algoritmo GenerarReportes
	Definir ids, doctores, fechas, horas, pacientes Como Cadena
	Definir tipoReporte, doctorElegido, fechaHoy Como Cadena
	Definir cantidad, i, j, encontrados Como Entero
	Definir aux Como Cadena
	Dimension ids[100]
	Dimension doctores[100]
	Dimension fechas[100]
	Dimension horas[100]
	Dimension pacientes[100]
	cantidad <- 0 // Cargar citas y datos para mostrar paciente y doctor.
	Escribir "Tipo de reporte: dia o doctor:"
	Leer tipoReporte
	Si tipoReporte = "dia" Entonces
		Escribir "Fecha de hoy (AAAA-MM-DD):"
		Leer fechaHoy
		Escribir "Reporte de citas del dia: ", fechaHoy
		Si cantidad > 0 Entonces
			Para i <- 1 Hasta cantidad Hacer
				Si fechas[i] = fechaHoy Entonces
					Escribir horas[i], " | Paciente: ", pacientes[i], " | Doctor: ", doctores[i]
				FinSi
			FinPara
		FinSi
	SiNo
		Si tipoReporte = "doctor" Entonces
			Escribir "ID del doctor:"
			Leer doctorElegido
			encontrados <- 0
			Si cantidad > 0 Entonces
				Para i <- 1 Hasta cantidad Hacer
					Si doctores[i] = doctorElegido Entonces
						encontrados <- encontrados + 1
					FinSi
				FinPara
			FinSi
			// Ordenamiento sencillo por fecha y hora para el reporte del doctor.
			Si cantidad > 1 Entonces
			Para i <- 1 Hasta cantidad - 1 Hacer
				Para j <- 1 Hasta cantidad - i Hacer
					Si fechas[j] > fechas[j + 1] O (fechas[j] = fechas[j + 1] Y horas[j] > horas[j + 1]) Entonces
						aux <- fechas[j]
						fechas[j] <- fechas[j + 1]
						fechas[j + 1] <- aux
						aux <- horas[j]
						horas[j] <- horas[j + 1]
						horas[j + 1] <- aux
						aux <- doctores[j]
						doctores[j] <- doctores[j + 1]
						doctores[j + 1] <- aux
						aux <- pacientes[j]
						pacientes[j] <- pacientes[j + 1]
						pacientes[j + 1] <- aux
						aux <- ids[j]
						ids[j] <- ids[j + 1]
						ids[j + 1] <- aux
					FinSi
				FinPara
			FinPara
			FinSi
			Si cantidad > 0 Entonces
				Para i <- 1 Hasta cantidad Hacer
					Si doctores[i] = doctorElegido Entonces
						Escribir fechas[i], " ", horas[i], " | Paciente: ", pacientes[i], " | Doctor: ", doctores[i]
					FinSi
				FinPara
			FinSi
		SiNo
			Escribir "Tipo de reporte no reconocido."
		FinSi
	FinSi
FinAlgoritmo
