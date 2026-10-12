Algoritmo RegistrarDoctor
	Definir ids, nombres, especialidades Como Cadena
	Definir nombre, especialidad Como Cadena
	Definir cantidad Como Entero
	Dimension ids[100]
	Dimension nombres[100]
	Dimension especialidades[100]
	cantidad <- 0 // Cargar doctores existentes.
	Escribir "Nombre del doctor:"
	Leer nombre
	Escribir "Especialidad:"
	Leer especialidad
	Si nombre = "" O especialidad = "" Entonces
		Escribir "Error: nombre y especialidad son obligatorios."
	SiNo
		Si cantidad < 100 Entonces
			cantidad <- cantidad + 1
			ids[cantidad] <- ConvertirATexto(cantidad)
			nombres[cantidad] <- nombre
			especialidades[cantidad] <- especialidad
			Escribir "Doctor registrado; guardar doctores.json."
		SiNo
			Escribir "No hay espacio disponible en este ejemplo."
		FinSi
	FinSi
FinAlgoritmo
