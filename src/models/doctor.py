# MODELO: Doctor
# Representa a un medico del consultorio

class Doctor:
    def __init__(self, id, nombre, especialidad):
        # Asignamos los atributos recibidos
        self.id = str(id)
        self.nombre = str(nombre)
        self.especialidad = str(especialidad)

    def to_dict(self):
        # Convertimos el objeto en un diccionario para poder guardarlo en JSON
        datos = {
            "id": self.id,
            "nombre": self.nombre,
            "especialidad": self.especialidad
        }
        return datos

    @classmethod
    def from_dict(cls, data):
        # Verificamos que sea un diccionario
        if not isinstance(data, dict):
            raise ValueError("Los datos del doctor deben ser un diccionario.")

        # Validamos los campos obligatorios
        if "id" not in data or data["id"] == "":
            raise ValueError("El id del doctor es obligatorio.")
        if "nombre" not in data or data["nombre"] == "":
            raise ValueError("El nombre del doctor es obligatorio.")
        if "especialidad" not in data or data["especialidad"] == "":
            raise ValueError("La especialidad del doctor es obligatoria.")

        # Retornamos la nueva instancia
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            especialidad=data["especialidad"]
        )
