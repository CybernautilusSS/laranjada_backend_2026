# ==========================================
# CLASSE LIVRO
# ==========================================

class Livro:

    def __init__(self, titulo):
        self.titulo = titulo
        self.disponivel = True


# ==========================================
# CRIANDO O OBJETO
# ==========================================

livro1 = Livro("O Senhor dos Anéis")


# ==========================================
# EXIBINDO OS DADOS
# ==========================================

print("=" * 40)
print("          INFORMAÇÕES DO LIVRO")
print("=" * 40)

print(f"Título: {livro1.titulo}")
print(f"Disponível: {livro1.disponivel}")

print("=" * 40)