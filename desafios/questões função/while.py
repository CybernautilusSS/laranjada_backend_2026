# ==========================================
# FUNÇÃO CONTAR
# ==========================================

def contar(n):
    numero = 1

    while numero <= n:
        print(numero)
        numero = numero + 1


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

numero = int(input("Digite um número: "))

contar(numero)