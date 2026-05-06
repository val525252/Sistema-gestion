from abc import ABC, abstractmethod
from datetime import datetime

# login inicio

def registrar_log(mensaje):
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.now()} - {mensaje}\n")

#  clases excepciones personalizadas
class ErrorSistema(Exception):
    pass

class ErrorValidacion(ErrorSistema):
    pass

class ErrorReserva(ErrorSistema):
    pass

# clase abstracta general
class Entidad(ABC):
    def __init__(self, id):
        self._id = id

    @abstractmethod
    def mostrar_info(self):
        pass

# CLIENTE ccliente seccion
class Cliente(Entidad):
    def __init__(self, id, nombre, email):
        super().__init__(id)
        self.nombre = nombre
        self.email = email

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor:
            raise ErrorValidacion("Nombre vacío")
        self._nombre = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise ErrorValidacion("Email inválido")
        self._email = valor

    def mostrar_info(self):
        return f"Cliente: {self._nombre}, Email: {self._email}"

# servicio clase
class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, *args):
        pass

    @abstractmethod
    def descripcion(self):
        pass

# servicio clase herencia
class ReservaSala(Servicio):
    def calcular_costo(self, horas=1):
        return self.precio_base * horas

    def descripcion(self):
        return "Reserva de sala por horas"

class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias=1):
        return self.precio_base * dias

    def descripcion(self):
        return "Alquiler de equipos"

class Asesoria(Servicio):
    def calcular_costo(self, horas=1, descuento=0):
        costo = self.precio_base * horas
        return costo - (costo * descuento)

    def descripcion(self):
        return "Asesoría especializada"

# reservas
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def procesar(self):
        try:
            if self.duracion <= 0:
                raise ErrorReserva("Duración inválida")

            costo = self.servicio.calcular_costo(self.duracion)

        except ErrorReserva as e:
            registrar_log(str(e))
            raise

        except Exception as e:
            registrar_log("Error inesperado: " + str(e))
            raise ErrorSistema("Fallo en procesamiento") from e

        else:
            print(f"Reserva procesada. Costo: {costo}")

        finally:
            print("Intento de procesamiento finalizado")

    def confirmar(self):
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

# simulacion prueba 10 operaciones
def simulacion():
    clientes = []
    servicios = []
    reservas = []

    # cliente valido e invalido prueba
    try:
        clientes.append(Cliente(1, "Ana", "ana@email.com"))
        clientes.append(Cliente(2, "Luis", "correo_invalido")) # error
    except ErrorValidacion as e:
        print("Error cliente:", e)
        registrar_log(str(e))

    # servicios
    try:
        servicios.append(ReservaSala("Sala VIP", 50))
        servicios.append(AlquilerEquipo("Laptop", 30))
        servicios.append(Asesoria("Consultoría", 100))
    except Exception as e:
        registrar_log(str(e))

    # reserva correcta e incorrecta prueba
    for i in range(10):
        try:
            cliente = clientes[0]
            servicio = servicios[i % 3]
            duracion = i - 5 # genera valores negativos

            reserva = Reserva(cliente, servicio, duracion)
            reserva.procesar()

            if i % 2 == 0:
                reserva.confirmar()
            else:
                reserva.cancelar()

            reservas.append(reserva)

        except Exception as e:
            print("Error en reserva:", e)
            registrar_log(str(e))

    print("\nSistema sigue funcionando correctamente.")

# vuelve inicio
if __name__ == "__main__":
    simulacion()