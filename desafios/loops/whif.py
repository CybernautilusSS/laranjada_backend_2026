# ==========================================
# VALIDADOR DE NÚMERO POSITIVO
# ==========================================

print("=" * 40)
print("      VALIDADOR DE NÚMERO POSITIVO")
print("=" * 40)

# Primeiro número digitado
numero = int(input("Digite um número positivo: "))

# Repete enquanto o número for inválido
while numero <= 0:
    print("Número inválido!")
    print("Digite um número maior que zero.")

    numero = int(input("Digite um número positivo: "))

# ==========================================
# RESULTADO
# ==========================================

print("=" * 40)
print(f"Número válido: {numero}")
print("Entrada aceita com sucesso!")
print("=" * 40)