"""
Programa que demuestra constructores y destructores en Python
usando solo funcionalidades básicas del lenguaje.
"""


class CuentaBancaria:
    """
    Clase que representa una cuenta bancaria simple
    con constructor y destructor.
    """

    total_cuentas = 0  # Variable de clase para llevar el conteo

    def __init__(self, titular, saldo_inicial=0):
        """
        Constructor de la clase CuentaBancaria.

        :param titular: Nombre del titular de la cuenta
        :param saldo_inicial: Saldo inicial de la cuenta (opcional)
        """
        self.titular = titular
        self.saldo = saldo_inicial
        self.activa = True
        CuentaBancaria.total_cuentas += 1

        print(f"\nNueva cuenta creada para {self.titular}")
        print(f"Saldo inicial: ${self.saldo:.2f}")
        print(f"Total de cuentas activas: {CuentaBancaria.total_cuentas}")

    def depositar(self, cantidad):
        """Realiza un depósito en la cuenta"""
        if self.activa:
            self.saldo += cantidad
            print(f"Depositados ${cantidad:.2f} en cuenta de {self.titular}")
        else:
            print("Error: La cuenta está cerrada")

    def retirar(self, cantidad):
        """Realiza un retiro de la cuenta"""
        if self.activa:
            if self.saldo >= cantidad:
                self.saldo -= cantidad
                print(f"Retirados ${cantidad:.2f} de cuenta de {self.titular}")
            else:
                print("Fondos insuficientes")
        else:
            print("Error: La cuenta está cerrada")

    def __del__(self):
        """
        Destructor de la clase CuentaBancaria.
        Realiza el cierre formal de la cuenta.
        """
        if hasattr(self, 'activa') and self.activa:
            self.activa = False
            CuentaBancaria.total_cuentas -= 1
            print(f"\nCuenta de {self.titular} está siendo eliminada")
            print(f"Saldo final: ${self.saldo:.2f}")
            print(f"Total de cuentas activas restantes: {CuentaBancaria.total_cuentas}")


class DispositivoIoT:
    """
    Clase que simula un dispositivo IoT simple
    con constructor y destructor.
    """

    def __init__(self, id_dispositivo, tipo):
        """
        Constructor de la clase DispositivoIoT.

        :param id_dispositivo: Identificador único del dispositivo
        :param tipo: Tipo de dispositivo (sensor, actuador, etc.)
        """
        self.id = id_dispositivo
        self.tipo = tipo
        self.conectado = False
        self.encendido = False
        self.registro_eventos = []

        print(f"\nDispositivo {self.id} ({self.tipo}) inicializado")

    def conectar(self):
        """Simula la conexión del dispositivo"""
        if not self.conectado:
            self.conectado = True
            self.registro_eventos.append("Dispositivo conectado")
            print(f"Dispositivo {self.id} conectado")

    def encender(self):
        """Simula encender el dispositivo"""
        if self.conectado and not self.encendido:
            self.encendido = True
            self.registro_eventos.append("Dispositivo encendido")
            print(f"Dispositivo {self.id} encendido")

    def __del__(self):
        """
        Destructor de la clase DispositivoIoT.
        Realiza el apagado seguro del dispositivo.
        """
        if hasattr(self, 'encendido') and self.encendido:
            self.encendido = False
            self.registro_eventos.append("Dispositivo apagado")
            print(f"\nApagando dispositivo {self.id} de manera segura")

        if hasattr(self, 'conectado') and self.conectado:
            self.conectado = False
            self.registro_eventos.append("Dispositivo desconectado")
            print(f"Desconectando dispositivo {self.id}")

        print(f"Registro de eventos de {self.id}:")
        for evento in self.registro_eventos:
            print(f"- {evento}")


def demostracion():
    """Función para demostrar el uso de las clases"""
    print("\n=== DEMOSTRACIÓN CUENTA BANCARIA ===")
    cuenta1 = CuentaBancaria("Karen Infante", 1000)
    cuenta1.depositar(500)
    cuenta1.retirar(200)

    cuenta2 = CuentaBancaria("Brayan Jimenez")
    cuenta2.depositar(1000)

    # Los destructores se llamarán al eliminar los objetos
    del cuenta1
    del cuenta2

    print("\n=== DEMOSTRACIÓN DISPOSITIVO IOT ===")
    sensor = DispositivoIoT("SENS-001", "Sensor de temperatura")
    sensor.conectar()
    sensor.encender()

    # El destructor se llamará al salir de este ámbito
    del sensor


if __name__ == "__main__":
    demostracion()