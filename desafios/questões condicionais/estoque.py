# ==========================================
# SISTEMA DE VERIFICAÇÃO DE ESTOQUE
# ==========================================

print("=" * 45)
print("       SISTEMA DE VERIFICAÇÃO DE ESTOQUE")
print("=" * 45)

# Entrada de dados
produto = input("Digite o nome do produto: ")

estoque = int(input("Digite a quantidade disponível: "))

pedido = int(input("Digite a quantidade pedida: "))

# ==========================================
# EXIBIÇÃO DAS INFORMAÇÕES
# ==========================================

print("\n" + "=" * 45)
print("             RESUMO DO PEDIDO")
print("=" * 45)

print(f"Produto: {produto}")
print(f"Quantidade em estoque: {estoque}")
print(f"Quantidade pedida: {pedido}")

# ==========================================
# VERIFICAÇÃO DO ESTOQUE
# ==========================================

if pedido > estoque:
    print("\nEstoque insuficiente.")
    
else:
    print("\nPedido confirmado.")

# ==========================================
# QUANTIDADE RESTANTE
# ==========================================

if pedido <= estoque:
    estoque_restante = estoque - pedido

    print(f"Estoque restante: {estoque_restante}")

else:
    print("Não foi possível realizar o pedido.")

# ==========================================
# FINALIZAÇÃO
# ==========================================

print("=" * 45)
print("Obrigado por utilizar o sistema!")
print("=" * 45)