# ==========================================================
# SISTEMA DE CONTROLE DE DESCONTO - MERCADO
# ==========================================================

print("=" * 60)
print("          SUPERMERCADO PYTHON")
print("=" * 60)

# ----------------------------------------------------------
# Nome do cliente
# ----------------------------------------------------------

cliente = input("Digite o nome do cliente: ")

# ----------------------------------------------------------
# Cadastro dos Produtos
# Código : [Nome, Preço]
# ----------------------------------------------------------

produtos = {

    1:  ["Arroz 5kg", 29.90],
    2:  ["Feijão Carioca 1kg", 8.49],
    3:  ["Macarrão Espaguete", 5.79],
    4:  ["Óleo de Soja 900ml", 7.99],
    5:  ["Açúcar 5kg", 22.90],
    6:  ["Sal Refinado 1kg", 3.29],
    7:  ["Café 500g", 18.75],
    8:  ["Leite Integral 1L", 5.49],
    9:  ["Manteiga 200g", 13.80],
    10: ["Margarina 500g", 9.35],

    11: ["Pão de Forma", 8.60],
    12: ["Biscoito Recheado", 4.80],
    13: ["Chocolate Barra", 7.25],
    14: ["Refrigerante 2L", 11.99],
    15: ["Suco de Uva 1L", 9.90],
    16: ["Água Mineral 1,5L", 3.99],
    17: ["Sabão em Pó 1kg", 16.40],
    18: ["Detergente", 2.95],
    19: ["Amaciante 2L", 19.70],
    20: ["Água Sanitária", 6.80],

    21: ["Papel Higiênico 12 Rolos", 24.90],
    22: ["Creme Dental", 6.45],
    23: ["Shampoo", 18.30],
    24: ["Condicionador", 19.15],
    25: ["Sabonete", 2.75],
    26: ["Desodorante", 15.90],
    27: ["Escova Dental", 8.10],
    28: ["Esponja de Louça", 2.30],
    29: ["Bombril", 5.50],
    30: ["Saco de Lixo", 12.40],

    31: ["Banana (kg)", 6.90],
    32: ["Maçã (kg)", 10.20],
    33: ["Laranja (kg)", 5.80],
    34: ["Tomate (kg)", 8.95],
    35: ["Batata (kg)", 7.10],
    36: ["Cebola (kg)", 5.65],
    37: ["Alface", 4.25],
    38: ["Cenoura (kg)", 6.55],
    39: ["Frango Inteiro (kg)", 17.90],
    40: ["Carne Bovina (kg)", 42.80],

    41: ["Linguiça Toscana (kg)", 24.70],
    42: ["Ovos Cartela 30un", 27.90],
    43: ["Queijo Mussarela (kg)", 49.50],
    44: ["Presunto (kg)", 31.80],
    45: ["Iogurte Natural", 4.99],
    46: ["Sorvete 2L", 26.90],
    47: ["Pizza Congelada", 21.75],
    48: ["Milho Verde", 4.55],
    49: ["Ervilha", 4.85],
    50: ["Molho de Tomate", 3.70]

}

# ----------------------------------------------------------
# Exibe o catálogo de produtos
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("               CATÁLOGO DE PRODUTOS")
print("=" * 60)

for codigo in produtos:
    nome, preco = produtos[codigo]
    print(f"{codigo:02d} - {nome:<30} R$ {preco:>6.2f}")

print("=" * 60)

# ----------------------------------------------------------
# Carrinho de compras
# ----------------------------------------------------------

carrinho = []

valor_total = 0
total_itens = 0

print("\nAgora escolha os produtos que deseja comprar.")
print("Digite 0 para finalizar a compra.")

print("Digite 0 para finalizar a compra.")

# ==========================================================
# Análise simples do código.
# ==========================================================

while True:

    try:

        codigo = int(input("\nDigite o código do produto (0 para finalizar): "))

        # Finaliza a compra
        if codigo == 0:
            break

        # Verifica se o código existe
        if codigo not in produtos:
            print("❌ Produto não encontrado.")
            continue

        # Solicita a quantidade
        quantidade = int(input("Quantidade: "))

        if quantidade <= 0:
            print("❌ A quantidade deve ser maior que zero.")
            continue

        # Recupera informações do produto
        nome_produto, preco_produto = produtos[codigo]

        # Calcula subtotal
        subtotal = preco_produto * quantidade

        # Adiciona ao carrinho
        carrinho.append({
            "codigo": codigo,
            "nome": nome_produto,
            "preco": preco_produto,
            "quantidade": quantidade,
            "subtotal": subtotal
        })

        # Atualiza totais
        valor_total += subtotal
        total_itens += quantidade

        print("\n===============================")
        print("Produto adicionado ao carrinho!")
        print("===============================")
        print(f"Produto : {nome_produto}")
        print(f"Preço   : R$ {preco_produto:.2f}")
        print(f"Qtd.    : {quantidade}")
        print(f"Subtotal: R$ {subtotal:.2f}")

        print("\nResumo Atual")
        print("-------------------------------")
        print(f"Itens no carrinho : {total_itens}")
        print(f"Valor acumulado   : R$ {valor_total:.2f}")

    except ValueError:
        print("Digite apenas números.")

# ----------------------------------------------------------
# Verifica se o carrinho está vazio
# ----------------------------------------------------------

if len(carrinho) == 0:

    print("\nNenhum produto foi comprado.")
    print("Compra cancelada.")
    exit()

# ----------------------------------------------------------
# Exibe um resumo antes do desconto
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("             RESUMO DO CARRINHO")
print("=" * 60)

for item in carrinho:

    print(
        f'{item["nome"]:<30} '
        f'Qtd: {item["quantidade"]:<3} '
        f'R$ {item["subtotal"]:>8.2f}'
    )

print("-" * 60)
print(f"Quantidade total de itens : {total_itens}")
print(f"Valor total da compra     : R$ {valor_total:.2f}")
print("=" * 60)

# ==========================================================
# PARTE 3 - CÁLCULO DO DESCONTO
# ==========================================================

desconto = 0
valor_desconto = 0
valor_final = valor_total

print("\nVerificando desconto...")

# ----------------------------------------------------------
# Faixas de desconto
# ----------------------------------------------------------

if valor_total > 100:

    if valor_total <= 200:
        desconto = 5

    elif valor_total <= 500:
        desconto = 7

    elif valor_total <= 1000:
        desconto = 12

    else:
        desconto = 20

    print("Desconto aplicado com sucesso!")

else:
    print("A compra não atingiu o valor mínimo para desconto.")

# ----------------------------------------------------------
# Cálculo
# ----------------------------------------------------------

valor_desconto = valor_total * desconto / 100
valor_final = valor_total - valor_desconto

# ----------------------------------------------------------
# Informações do desconto
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("              DESCONTO DA COMPRA")
print("=" * 60)

print(f"Valor bruto.............: R$ {valor_total:.2f}")
print(f"Percentual de desconto..: {desconto}%")
print(f"Valor economizado.......: R$ {valor_desconto:.2f}")
print(f"Valor a pagar...........: R$ {valor_final:.2f}")

print("=" * 60)

# ----------------------------------------------------------
# Mensagem personalizada
# ----------------------------------------------------------

if desconto == 0:

    print("Você não recebeu desconto nesta compra.")

elif desconto == 5:

    print("Parabéns! Você recebeu 5% de desconto.")

elif desconto == 7:

    print("Parabéns! Você recebeu 7% de desconto.")

elif desconto == 12:

    print("Excelente! Você recebeu 12% de desconto.")

elif desconto == 20:

    print("Incrível! Você recebeu o maior desconto disponível (20%).")

# ==========================================================
# Cupom de economia
# ==========================================================

print("\n" + "=" * 60)
print("              CUPOM DE ECONOMIA")
print("=" * 60)

if desconto == 0:
    print("Economia nesta compra : R$ 0.00")
else:
    print(f"Você economizou       : R$ {valor_desconto:.2f}")

print("=" * 60)

# ==========================================================
# PARTE 4 - NOTA FISCAL
# ==========================================================

from datetime import datetime

agora = datetime.now()

print("\n")
print("=" * 70)
print("                  SUPERMERCADO PYTHON")
print("=" * 70)

print(f"Cliente : {cliente}")
print(f"Data    : {agora.strftime('%d/%m/%Y')}")
print(f"Hora    : {agora.strftime('%H:%M:%S')}")

print("=" * 70)

print(f"{'CÓD':<5}{'PRODUTO':<30}{'QTD':>6}{'UNIT.':>12}{'TOTAL':>15}")

print("-" * 70)

for item in carrinho:

    print(
        f"{item['codigo']:<5}"
        f"{item['nome']:<30}"
        f"{item['quantidade']:>6}"
        f"R$ {item['preco']:>8.2f}"
        f"R$ {item['subtotal']:>10.2f}"
    )

print("-" * 70)

print(f"Quantidade de itens...............: {total_itens}")
print(f"Valor bruto da compra............: R$ {valor_total:.2f}")
print(f"Desconto aplicado................: {desconto}%")
print(f"Valor economizado................: R$ {valor_desconto:.2f}")
print(f"VALOR FINAL......................: R$ {valor_final:.2f}")

print("=" * 70)

# ----------------------------------------------------------
# Classificação da compra
# ----------------------------------------------------------

if valor_final < 100:
    categoria = "Compra Pequena"

elif valor_final < 300:
    categoria = "Compra Média"

elif valor_final < 700:
    categoria = "Compra Grande"

else:
    categoria = "Compra Muito Grande"

print(f"Categoria da compra..............: {categoria}")

print("=" * 70)

# ----------------------------------------------------------
# Mensagem ao cliente
# ----------------------------------------------------------

print("Obrigado por comprar conosco!")
print(f"Esperamos vê-lo novamente, {cliente}!")

print("=" * 70)

# ==========================================================
# ESTATÍSTICAS DA COMPRA
# ==========================================================

media_item = valor_total / total_itens

print("\n")
print("=" * 70)
print("              ESTATÍSTICAS DA COMPRA")
print("=" * 70)

print(f"Produtos diferentes comprados : {len(carrinho)}")
print(f"Quantidade total de itens     : {total_itens}")
print(f"Preço médio por item          : R$ {media_item:.2f}")
print(f"Maior desconto aplicado       : {desconto}%")
print(f"Economia total                : R$ {valor_desconto:.2f}")

print("=" * 70)

# ==========================================================
# PRODUTO MAIS CARO COMPRADO
# ==========================================================

mais_caro = carrinho[0]

for item in carrinho:

    if item["preco"] > mais_caro["preco"]:
        mais_caro = item

print("\nProduto mais caro comprado:")

print(f"Nome      : {mais_caro['nome']}")
print(f"Preço     : R$ {mais_caro['preco']:.2f}")
print(f"Quantidade: {mais_caro['quantidade']}")

print("=" * 70)

# ==========================================================
# PRODUTO MAIS BARATO COMPRADO
# ==========================================================

mais_barato = carrinho[0]

for item in carrinho:

    if item["preco"] < mais_barato["preco"]:
        mais_barato = item

print("\nProduto mais barato comprado:")

print(f"Nome      : {mais_barato['nome']}")
print(f"Preço     : R$ {mais_barato['preco']:.2f}")
print(f"Quantidade: {mais_barato['quantidade']}")

print("=" * 70)

# ==========================================================
# PARTE 5 - RECURSOS EXTRAS
# ==========================================================

print("\n")
print("=" * 70)
print("              FORMA DE PAGAMENTO")
print("=" * 70)

print("1 - Dinheiro")
print("2 - PIX")
print("3 - Cartão de Débito")
print("4 - Cartão de Crédito")

forma_pagamento = 0

while True:

    try:

        forma_pagamento = int(input("\nEscolha a forma de pagamento: "))

        if forma_pagamento >= 1 and forma_pagamento <= 4:
            break

        print("Escolha uma opção válida.")

    except ValueError:

        print("Digite apenas números.")

# ----------------------------------------------------------
# Nome da forma de pagamento
# ----------------------------------------------------------

if forma_pagamento == 1:
    pagamento = "Dinheiro"

elif forma_pagamento == 2:
    pagamento = "PIX"

elif forma_pagamento == 3:
    pagamento = "Cartão de Débito"

else:
    pagamento = "Cartão de Crédito"

# ----------------------------------------------------------
# Desconto adicional para PIX
# ----------------------------------------------------------

desconto_pix = 0
valor_desconto_pix = 0

if forma_pagamento == 2:

    desconto_pix = 3

    valor_desconto_pix = valor_final * desconto_pix / 100

    valor_final -= valor_desconto_pix

    print("\nPagamento via PIX detectado.")
    print("Você recebeu mais 3% de desconto!")

print("=" * 70)
print(f"Forma de pagamento : {pagamento}")
print(f"Desconto PIX       : R$ {valor_desconto_pix:.2f}")
print(f"Valor Final        : R$ {valor_final:.2f}")
print("=" * 70)

# ==========================================================
# GERAÇÃO DO CUPOM FISCAL
# ==========================================================

arquivo = open("Cupom_Fiscal.txt", "w", encoding="utf-8")

arquivo.write("=" * 60 + "\n")
arquivo.write("             SUPERMERCADO PYTHON\n")
arquivo.write("=" * 60 + "\n\n")

arquivo.write(f"Cliente: {cliente}\n")
arquivo.write(f"Data: {agora.strftime('%d/%m/%Y')}\n")
arquivo.write(f"Hora: {agora.strftime('%H:%M:%S')}\n\n")

arquivo.write("ITENS COMPRADOS\n")
arquivo.write("-" * 60 + "\n")

for item in carrinho:

    arquivo.write(
        f"{item['nome']} | "
        f"Qtd:{item['quantidade']} | "
        f"Unit:R$ {item['preco']:.2f} | "
        f"Total:R$ {item['subtotal']:.2f}\n"
    )

arquivo.write("-" * 60 + "\n")

arquivo.write(f"Quantidade de itens : {total_itens}\n")
arquivo.write(f"Valor Bruto         : R$ {valor_total:.2f}\n")
arquivo.write(f"Desconto            : {desconto}%\n")
arquivo.write(f"Economia            : R$ {valor_desconto:.2f}\n")
arquivo.write(f"Desconto PIX        : R$ {valor_desconto_pix:.2f}\n")
arquivo.write(f"Valor Final         : R$ {valor_final:.2f}\n")
arquivo.write(f"Pagamento           : {pagamento}\n")

arquivo.write("\nObrigado pela preferência!\n")

arquivo.close()

print("\nCupom Fiscal salvo com sucesso!")
print("Arquivo criado: Cupom_Fiscal.txt")

# ==========================================================
# RELATÓRIO DA COMPRA
# ==========================================================

print("\n")
print("=" * 70)
print("              RELATÓRIO FINAL")
print("=" * 70)

print(f"Cliente.................... {cliente}")
print(f"Produtos diferentes........ {len(carrinho)}")
print(f"Itens comprados............ {total_itens}")
print(f"Valor bruto............... R$ {valor_total:.2f}")
print(f"Desconto principal........ R$ {valor_desconto:.2f}")
print(f"Desconto PIX.............. R$ {valor_desconto_pix:.2f}")

economia_total = valor_desconto + valor_desconto_pix

print(f"Economia total............ R$ {economia_total:.2f}")

print(f"Valor pago................ R$ {valor_final:.2f}")

print(f"Forma de pagamento........ {pagamento}")

print("=" * 70)

# ==========================================================
# MENSAGEM FINAL
# ==========================================================

print("\nMuito obrigado por comprar conosco!")

if economia_total > 0:

    print(f"Você economizou R$ {economia_total:.2f} nesta compra!")

print("Esperamos vê-lo novamente em breve!")

print("=" * 70)

