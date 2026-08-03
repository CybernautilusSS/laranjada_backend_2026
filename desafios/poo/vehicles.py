# ==========================================
# CLASSE VEICULO
# ==========================================

class Veiculo:

    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def mostrar_dados(self):
        print(f"Marca: {self.marca}")
        print(f"Modelo: {self.modelo}")


# ==========================================
# SUBCLASSE CARRO
# ==========================================

class Carro(Veiculo):

    def __init__(self, marca, modelo, portas):
        super().__init__(marca, modelo)
        self.portas = portas

    def mostrar_dados(self):
        super().mostrar_dados()
        print(f"Portas: {self.portas}")


# ==========================================
# SUBCLASSE MOTO
# ==========================================

class Moto(Veiculo):

    def __init__(self, marca, modelo, cilindradas):
        super().__init__(marca, modelo)
        self.cilindradas = cilindradas

    def mostrar_dados(self):
        super().mostrar_dados()
        print(f"Cilindradas: {self.cilindradas} cc")


# ==========================================
# CRIANDO OS OBJETOS
# ==========================================

carro1 = Carro("Toyota", "Corolla", 4)
moto1 = Moto("Honda", "CB 500", 500)


# ==========================================
# EXIBINDO OS DADOS
# ==========================================

print("=" * 40)
print("             CARRO")
print("=" * 40)

carro1.mostrar_dados()

print("\n" + "=" * 40)
print("              MOTO")
print("=" * 40)

moto1.mostrar_dados()

print("=" * 40)