# MODELO: Paciente
# Representa la informacion de un paciente

class Paciente:
    def __init__(self, id, nombre, identificacion, telefono=""):
        # Asignamos los atributos recibidos
        self.id = str(id)
        self.nombre = str(nombre)
        self.identificacion = str(identificacion)
        self.telefono = str(telefono) if telefono is not None else ""

    def to_dict(self):
        # Convertimos el objeto en un diccionario para guardarlo en JSON
        datos = {
            "id": self.id,
            "nombre": self.nombre,
            "identificacion": self.identificacion,
            "telefono": self.telefono
        }
        return datos

    @classmethod
    def from_dict(cls, data):
        # Verificamos que los datos vengan en un diccionario valido
        if not isinstance(data, dict):
            raise ValueError("Los datos del paciente deben ser un diccionario.")

        # Validamos los campos obligatorios
        if "id" not in data or data["id"] == "":
            raise ValueError("El id del paciente es obligatorio.")
        if "nombre" not in data or data["nombre"] == "":
            raise ValueError("El nombre del paciente es obligatorio.")
        if "identificacion" not in data or data["identificacion"] == "":
            raise ValueError("La identificacion del paciente es obligatoria.")

        # El telefono es opcional
        telefono = data.get("telefono", "")
        if telefono is None:
            telefono = ""

        # Creamos y retornamos la instancia del paciente
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            identificacion=data["identificacion"],
            telefono=telefono
        )
