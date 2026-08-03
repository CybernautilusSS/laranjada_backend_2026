# ==========================================
# FUNÇÃO DE LOGIN
# ==========================================

def login():
    senha_correta = "python123"
    tentativas = 0

    while tentativas < 3:
        senha = input("Digite a senha: ")

        if senha == senha_correta:
            print("Login realizado com sucesso!")
            return

        else:
            tentativas = tentativas + 1
            print("Senha incorreta!")
            print(f"Tentativa {tentativas} de 3.")

    print("Número máximo de tentativas atingido.")
    print("Acesso bloqueado.")


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

print("=" * 40)
print("          SISTEMA DE LOGIN")
print("=" * 40)

login()