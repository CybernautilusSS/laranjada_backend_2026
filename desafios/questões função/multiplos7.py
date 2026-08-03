# ==========================================
# FUNÇÃO DE NÚMEROS ÍMPARES
# ==========================================

def imprimir_impares(n):
    for numero in range(1, n + 1):

        # Pula os números pares
        if numero % 2 == 0:
            continue

        # Pula os múltiplos de 7
        if numero % 7 == 0:
            continue

        print(numero)


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

numero = int(input("Digite até qual número contar: "))

print("\nNúmeros ímpares, sem múltiplos de 7:")

imprimir_impares(numero)