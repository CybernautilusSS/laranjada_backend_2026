# ==========================================
# SOMA ACUMULADA COM WHILE
# ==========================================

print("=" * 40)
print("         SOMA ACUMULADA")
print("=" * 40)

# Variável que vai armazenar a soma
total = 0

# Primeiro valor
valor = float(input("Digite um valor (0 para terminar): "))

# Enquanto o usuário não digitar 0
while valor != 0:

    # Adiciona o valor ao total
    total = total + valor

    # Pede outro valor
    valor = float(input("Digite outro valor (0 para terminar): "))

# ==========================================
# RESULTADO
# ==========================================

print("=" * 40)
print(f"Total acumulado: R$ {total:.2f}")
print("=" * 40)