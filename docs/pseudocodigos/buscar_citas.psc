Algoritmo BuscarCitas
	Definir ids, pacientes, doctores, fechas, horas Como Cadena
	Definir criterio, valor Como Cadena
	Definir cantidad, i, encontrados Como Entero
	Dimension ids[100]
	Dimension pacientes[100]
	Dimension doctores[100]
	Dimension fechas[100]
	Dimension horas[100]
	cantidad <- 0 // Cargar citas; llenar arreglos con los datos disponibles.
	Escribir "Criterio: paciente, doctor o fecha:"
	Leer criterio
	Escribir "Valor a buscar (ID o fecha AAAA-MM-DD):"
	Leer valor
	encontrados <- 0
	Si cantidad > 0 Entonces
		Para i <- 1 Hasta cantidad Hacer
			Si (criterio = "paciente" Y pacientes[i] = valor) O (criterio = "doctor" Y doctores[i] = valor) O (criterio = "fecha" Y fechas[i] = valor) Entonces
				encontrados <- encontrados + 1
				Escribir "Cita: ", ids[i], " | Fecha: ", fechas[i], " | Hora: ", horas[i]
			FinSi
		FinPara
	FinSi
	Si encontrados = 0 Entonces
		Escribir "No se encontraron citas para ese criterio."
	FinSi
FinAlgoritmo
