# ==========================================
# FUNÇÃO FATORIAL
# ==========================================

def fatorial(n):
    resultado = 1

    for i in range(1, n + 1):
        resultado = resultado * i

    return resultado


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

print("=" * 40)
print("       CALCULADORA DE FATORIAL")
print("=" * 40)

numero = int(input("Digite um número: "))

resultado = fatorial(numero)

print("=" * 40)
print(f"O fatorial de {numero} é: {resultado}")
print("=" * 40)