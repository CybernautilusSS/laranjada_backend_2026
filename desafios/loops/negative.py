# ==========================================
# SOMA DE NÚMEROS POSITIVOS
# ==========================================

numeros = [-1, 2, -3, 4]

soma = 0

# Percorre todos os números da lista
for n in numeros:

    # Se for negativo, pula para o próximo
    if n < 0:
        continue

    # Soma apenas os números positivos
    soma = soma + n

# ==========================================
# RESULTADO
# ==========================================

print("=" * 40)
print("          RESULTADO")
print("=" * 40)

print(f"Lista: {numeros}")
print(f"Soma dos números positivos: {soma}")

print("=" * 40)