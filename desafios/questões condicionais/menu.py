# ==========================================
# MENU DE ESCOLHA
# ==========================================

print("=" * 40)
print("          MENU DE ESCOLHA")
print("=" * 40)

print("1 - Cadastrar")
print("2 - Consultar")
print("3 - Alterar")
print("4 - Excluir")
print("5 - Sair")

print("=" * 40)

# Solicita a escolha do usuário
escolha = int(input("Digite uma opção de 1 a 5: "))

# ==========================================
# VERIFICAÇÃO DA ESCOLHA
# ==========================================

match escolha:

    case 1:
        print("Você escolheu: Cadastrar")

    case 2:
        print("Você escolheu: Consultar")

    case 3:
        print("Você escolheu: Alterar")

    case 4:
        print("Você escolheu: Excluir")

    case 5:
        print("Você escolheu: Sair")

    case _:
        print("Opção inválida!")

# ==========================================
# RESULTADO FINAL
# ==========================================

print("=" * 40)

if escolha >= 1 and escolha <= 5:
    print(f"Número escolhido: {escolha}")

else:
    print("Nenhum número válido foi escolhido.")

print("=" * 40)