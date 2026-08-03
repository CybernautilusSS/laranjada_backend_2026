# ==========================================
# SOMA ATÉ ZERO
# ==========================================

print("=" * 40)
print("             SOMA ATÉ ZERO")
print("=" * 40)

# Variável para armazenar a soma
soma = 0

# Loop principal
while True:

    numero = int(input("Digite um número (0 para encerrar): "))

    # Verifica antes de somar
    if numero == 0:
        break

    # Adiciona o número à soma
    soma = soma + numero

# ==========================================
# RESULTADO
# ==========================================

print("=" * 40)
print(f"A soma dos números é: {soma}")
print("=" * 40)