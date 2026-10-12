Algoritmo RegistrarPaciente
	Definir nombre, identificacion, telefono Como Cadena
	Definir ids, nombres, identificaciones, telefonos Como Cadena
	Definir cantidad, i Como Entero
	Definir identificacionRepetida Como Logico

	Dimension ids[100]
	Dimension nombres[100]
	Dimension identificaciones[100]
	Dimension telefonos[100]

	// Datos de ejemplo que representan los pacientes ya cargados.
	cantidad <- 0

	Escribir "Nombre del paciente:"
	Leer nombre
	Escribir "Identificacion del paciente:"
	Leer identificacion
	Escribir "Telefono del paciente (opcional):"
	Leer telefono

	Si nombre = "" O identificacion = "" Entonces
		Escribir "Error: el nombre y la identificacion son obligatorios."
	SiNo
		identificacionRepetida <- Falso

		Si cantidad > 0 Entonces
			Para i <- 1 Hasta cantidad Hacer
				Si identificaciones[i] = identificacion Entonces
					identificacionRepetida <- Verdadero
				FinSi
			FinPara
		FinSi

		Si identificacionRepetida Entonces
			Escribir "Error: la identificacion ya esta registrada."
		SiNo
			Si cantidad < 100 Entonces
				cantidad <- cantidad + 1
				ids[cantidad] <- ConvertirATexto(cantidad)
				nombres[cantidad] <- nombre
				identificaciones[cantidad] <- identificacion
				telefonos[cantidad] <- telefono

				// En el sistema real se guardan tambien nombre y telefono en pacientes.json.
				Escribir "Paciente registrado correctamente."
				Escribir "ID interno de ejemplo: ", ids[cantidad]
			SiNo
				Escribir "Error: se alcanzo el maximo de pacientes del ejemplo."
			FinSi
		FinSi
	FinSi
FinAlgoritmo
