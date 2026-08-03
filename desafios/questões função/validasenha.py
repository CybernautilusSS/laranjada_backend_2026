# ==========================================
# FUNÇÃO PARA VALIDAR SENHA
# ==========================================

def validar_senha():
    senha = input("Digite a senha: ")

    while senha != "python123":
        print("Senha incorreta! Tente novamente.")
        senha = input("Digite a senha: ")

    print("Senha correta! Acesso permitido.")


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

validar_senha()