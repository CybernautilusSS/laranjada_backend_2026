# ==========================================
# SISTEMA DE SENHA
# ==========================================

print("=" * 40)
print("          SISTEMA DE LOGIN")
print("=" * 40)

senha_correta = "senha123"

while True:

    senha = input("Digite a senha: ")

    if senha == senha_correta:
        print("Senha correta!")
        print("Acesso liberado!")
        break

    else:
        print("Senha incorreta!")
        print("Tente novamente.")

print("=" * 40)
print("Fim do programa!")
print("=" * 40)