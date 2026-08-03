# ==========================================
# CLASSE CONTADOR
# ==========================================

class Contador:

    def __init__(self):
        self.valor = 0

    # Método para aumentar o contador
    def aumentar(self):
        self.valor = self.valor + 1

    # Método para diminuir o contador
    def diminuir(self):
        self.valor = self.valor - 1


# ==========================================
# CRIANDO O OBJETO
# ==========================================

contador = Contador()


# ==========================================
# TESTANDO O CONTADOR
# ==========================================

print("=" * 40)
print("          CONTADOR SIMPLES")
print("=" * 40)

print(f"Valor inicial: {contador.valor}")

contador.aumentar()
print(f"Depois de aumentar: {contador.valor}")

contador.aumentar()
print(f"Depois de aumentar: {contador.valor}")

contador.aumentar()
print(f"Depois de aumentar: {contador.valor}")

contador.diminuir()
print(f"Depois de diminuir: {contador.valor}")

contador.diminuir()
print(f"Depois de diminuir: {contador.valor}")

print("=" * 40)