# ==========================================
# VERIFICADOR DE DIA DA SEMANA
# ==========================================

print("=" * 45)
print("       VERIFICADOR DE DIA DA SEMANA")
print("=" * 45)

print("""
1 - Segunda-feira
2 - Terça-feira
3 - Quarta-feira
4 - Quinta-feira
5 - Sexta-feira
6 - Sábado
7 - Domingo
""")

dia = int(input("Digite o número correspondente ao dia: "))

# ==========================================
# SWITCH / MATCH CASE
# ==========================================

match dia:

    case 1:
        nome_dia = "Segunda-feira"
        tipo_dia = "Dia útil"

    case 2:
        nome_dia = "Terça-feira"
        tipo_dia = "Dia útil"

    case 3:
        nome_dia = "Quarta-feira"
        tipo_dia = "Dia útil"

    case 4:
        nome_dia = "Quinta-feira"
        tipo_dia = "Dia útil"

    case 5:
        nome_dia = "Sexta-feira"
        tipo_dia = "Dia útil"

    case 6:
        nome_dia = "Sábado"
        tipo_dia = "Muita resenha e Ice 51 e caipiroska é melhor que caipirinha"

    case 7:
        nome_dia = "Domingo"
        tipo_dia = "Tristeza de final de semana"

    case _:
        nome_dia = "Dia inválido"
        tipo_dia = "Opção inválida"

# ==========================================
# RESULTADO
# ==========================================

print("\n" + "=" * 45)
print("                RESULTADO")
print("=" * 45)

print(f"Dia: {nome_dia}")
print(f"Classificação: {tipo_dia}")

print("=" * 45)