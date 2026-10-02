class Cita:
    def __init__(self, id, paciente_id, doctor_id, fecha, hora):
        self.id = id
        self.paciente_id = paciente_id
        self.doctor_id = doctor_id
        self.fecha = fecha
        self.hora = hora

    def to_dict(self):
        return {
            "id": self.id,
            "paciente_id": self.paciente_id,
            "doctor_id": self.doctor_id,
            "fecha": self.fecha,
            "hora": self.hora
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            paciente_id=data.get("paciente_id"),
            doctor_id=data.get("doctor_id"),
            fecha=data.get("fecha"),
            hora=data.get("hora")
        )
