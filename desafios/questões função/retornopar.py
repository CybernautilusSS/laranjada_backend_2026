# ==========================================
# FUNÇÃO PARA CONTAR NÚMEROS PARES
# ==========================================

def contar_pares(inicio, fim):
    quantidade = 0

    for numero in range(inicio, fim + 1):
        if numero % 2 == 0:
            quantidade = quantidade + 1

    return quantidade


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

inicio = int(input("Digite o início do intervalo: "))
fim = int(input("Digite o fim do intervalo: "))

resultado = contar_pares(inicio, fim)

print(f"Existem {resultado} números pares no intervalo.")