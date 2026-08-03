# ==========================================
# FUNÇÃO TABUADA
# ==========================================

def tabuada(n):
    for i in range(1, 11):
        resultado = n * i
        print(f"{n} x {i} = {resultado}")


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

numero = int(input("Digite um número: "))

tabuada(numero)