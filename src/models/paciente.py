class Paciente:
    def __init__(self, id, nombre, identificacion, telefono):
        self.id = id
        self.nombre = nombre
        self.identificacion = identificacion
        self.telefono = telefono

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "identificacion": self.identificacion,
            "telefono": self.telefono
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre"),
            identificacion=data.get("identificacion"),
            telefono=data.get("telefono")
        )
