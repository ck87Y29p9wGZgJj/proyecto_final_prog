Algoritmo CancelarCita
	Definir ids Como Cadena
	Definir idBuscado Como Cadena
	Definir cantidad, i, posicion Como Entero
	Dimension ids[100]
	cantidad <- 0 // Cargar citas existentes.
	Escribir "ID de la cita que desea cancelar:"
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
		Si posicion < cantidad Entonces
			Para i <- posicion Hasta cantidad - 1 Hacer
				ids[i] <- ids[i + 1]
			FinPara
		FinSi
		cantidad <- cantidad - 1
		Escribir "Cita cancelada; guardar citas.json."
	FinSi
FinAlgoritmo
