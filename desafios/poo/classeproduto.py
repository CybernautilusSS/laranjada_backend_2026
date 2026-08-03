# ==========================================
# CLASSE PRODUTO
# ==========================================

class Produto:

    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    # Método para aplicar desconto
    def aplicar_desconto(self, percentual):
        desconto = self.preco * percentual / 100
        self.preco = self.preco - desconto


# ==========================================
# CRIANDO O PRODUTO
# ==========================================

produto1 = Produto("Notebook", 3000)


# ==========================================
# EXIBINDO O PRODUTO
# ==========================================

print("=" * 40)
print("          PRODUTO")
print("=" * 40)

print(f"Produto: {produto1.nome}")
print(f"Preço original: R$ {produto1.preco:.2f}")

# Aplicando desconto de 10%
produto1.aplicar_desconto(10)

print(f"Preço com desconto: R$ {produto1.preco:.2f}")

print("=" * 40)