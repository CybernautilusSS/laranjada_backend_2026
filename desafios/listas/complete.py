# ==========================================
# 5 NÚMEROS E SOMA
# ==========================================

numeros = []

# Pedindo 5 números ao usuário
for i in range(5):
    numero = float(input(f"Digite o {i + 1}º número: "))
    numeros.append(numero)

# Calculando a soma
soma = sum(numeros)

# ==========================================
# RESULTADO
# ==========================================

print("=" * 40)
print("             RESULTADO")
print("=" * 40)

print(f"Lista completa: {numeros}")
print(f"Soma dos números: {soma}")

print("=" * 40)