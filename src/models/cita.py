# MODELO: Cita
# Representa una cita medica agendada

class Cita:
    def __init__(self, id, paciente_id, doctor_id, fecha, hora):
        # Asignamos los atributos del objeto
        self.id = str(id)
        self.paciente_id = str(paciente_id)
        self.doctor_id = str(doctor_id)
        self.fecha = str(fecha)
        self.hora = str(hora)

    def to_dict(self):
        # Convertimos la cita a diccionario para guardarla en citas.json
        datos = {
            "id": self.id,
            "paciente_id": self.paciente_id,
            "doctor_id": self.doctor_id,
            "fecha": self.fecha,
            "hora": self.hora
        }
        return datos

    @classmethod
    def from_dict(cls, data):
        # Verificamos que sea un diccionario
        if not isinstance(data, dict):
            raise ValueError("Los datos de la cita deben ser un diccionario.")

        # Validamos que esten todos los datos requeridos
        campos = ["id", "paciente_id", "doctor_id", "fecha", "hora"]
        for campo in campos:
            if campo not in data or data[campo] == "":
                raise ValueError(f"El campo '{campo}' de la cita es obligatorio.")

        # Retornamos la nueva cita
        return cls(
            id=data["id"],
            paciente_id=data["paciente_id"],
            doctor_id=data["doctor_id"],
            fecha=data["fecha"],
            hora=data["hora"]
        )
