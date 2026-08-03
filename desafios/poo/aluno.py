# ==========================================
# CLASSE ALUNO
# ==========================================

class Aluno:

    def __init__(self, nome):
        self.nome = nome

    def estudar(self):
        print(f"{self.nome} está estudando!")


# ==========================================
# CRIANDO Aluno Objeto
# ==========================================

aluno1 = Aluno("João")


# ==========================================
# CHAMANDO O MÉTODO
# ==========================================

print("=" * 40)
print("          SISTEMA DO ALUNO")
print("=" * 40)

print(f"Aluno: {aluno1.nome}")

aluno1.estudar()

print("=" * 40)