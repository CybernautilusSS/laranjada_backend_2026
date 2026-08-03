# ==========================================
# CLASSE PESSOA
# ==========================================

class Pessoa:

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade


# ==========================================
# CRIANDO UM OBJETO
# ==========================================

pessoa1 = Pessoa("João", 20)


# ==========================================
# EXIBINDO OS DADOS
# ==========================================

print("=" * 40)
print("          DADOS DA PESSOA")
print("=" * 40)

print(f"Nome: {pessoa1.nome}")
print(f"Idade: {pessoa1.idade} anos")

print("=" * 40)