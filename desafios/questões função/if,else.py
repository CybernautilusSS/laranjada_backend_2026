# ==========================================
# FUNÇÃO PARA DESCOBRIR O MAIOR NÚMERO
# ==========================================

def maior(a, b):

    if a > b:
        return a

    else:
        return b


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

print("=" * 40)
print("       VERIFICADOR DE MAIOR NÚMERO")
print("=" * 40)

numero1 = float(input("Digite o primeiro número: "))
numero2 = float(input("Digite o segundo número: "))

resultado = maior(numero1, numero2)

print("=" * 40)
print(f"O maior número é: {resultado}")
print("=" * 40) 