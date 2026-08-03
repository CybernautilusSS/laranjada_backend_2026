# ==========================================
# CLASSE CONTADOR DE OBJETOS
# ==========================================

class Pessoa:

    # Atributo da classe
    quantidade = 0

    def __init__(self, nome):
        self.nome = nome

        # Aumenta o contador a cada objeto criado
        Pessoa.quantidade += 1


# ==========================================
# CRIANDO OS OBJETOS
# ==========================================

pessoa1 = Pessoa("João")
pessoa2 = Pessoa("Maria")
pessoa3 = Pessoa("Carlos")
pessoa4 = Pessoa("Ana")


# ==========================================
# EXIBINDO O RESULTADO
# ==========================================

print("=" * 40)
print("       CONTADOR DE OBJETOS")
print("=" * 40)

print(f"Pessoa 1: {pessoa1.nome}")
print(f"Pessoa 2: {pessoa2.nome}")
print(f"Pessoa 3: {pessoa3.nome}")
print(f"Pessoa 4: {pessoa4.nome}")

print("-" * 40)

print(f"Quantidade de objetos criados: {Pessoa.quantidade}")

print("=" * 40)