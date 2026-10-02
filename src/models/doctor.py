class Doctor:
    def __init__(self, id, nombre, especialidad):
        self.id = id
        self.nombre = nombre
        self.especialidad = especialidad

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "especialidad": self.especialidad
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre"),
            especialidad=data.get("especialidad")
        )
