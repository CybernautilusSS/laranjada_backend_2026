# ==========================================
# SISTEMA DE CONTROLE DE DESCONTO
# ==========================================

print("=" * 45)
print("      SISTEMA DE CONTROLE DE DESCONTO")
print("=" * 45)

# Solicita o nome do cliente
nome = input("Digite o nome do cliente: ")

# Solicita o valor da compra
valor_compra = float(input("Digite o valor da compra: R$ "))

# Inicializa as variáveis
desconto = 0
valor_desconto = 0
valor_final = valor_compra

# ==========================================
# VERIFICAÇÃO DO DESCONTO
# ==========================================

if valor_compra > 100:
    print("\nDesconto aplicado!")

    if valor_compra <= 200:
        desconto = 5

    elif valor_compra <= 500:
        desconto = 7

    elif valor_compra <= 1000:
        desconto = 12

    else:
        desconto = 20

else:
    print("\nNenhum desconto foi aplicado.")

# ==========================================
# CÁLCULO DO DESCONTO
# ==========================================

valor_desconto = valor_compra * desconto / 100

valor_final = valor_compra - valor_desconto

# ==========================================
# EXIBIÇÃO DO RESULTADO
# ==========================================

print("\n" + "=" * 45)
print("             RESUMO DA COMPRA")
print("=" * 45)

print(f"Cliente: {nome}")
print(f"Valor original: R$ {valor_compra:.2f}")
print(f"Desconto: {desconto}%")
print(f"Valor do desconto: R$ {valor_desconto:.2f}")
print(f"Valor final: R$ {valor_final:.2f}")

# ==========================================
# MENSAGEM DE ACORDO COM O DESCONTO
# ==========================================

if desconto == 0:
    print("Você não recebeu desconto.")

elif desconto == 5:
    print("Você recebeu um desconto de 5%.")

elif desconto == 10:
    print("Você recebeu um desconto de 7%.")

elif desconto == 15:
    print("Você recebeu um desconto de 12%.")

else:
    print("Você recebeu o maior desconto: 20%!")

# ==========================================
# FINALIZAÇÃO
# ==========================================

print("=" * 45)
print("Obrigado pela sua compra!")
print("Volte sempre!")
print("=" * 45)