# ==========================================
# SISTEMA DE MÉDIA ESCOLAR
# ==========================================

print("=" * 45)
print("        SISTEMA DE MÉDIA ESCOLAR")
print("=" * 45)

# Cadastro do aluno
nome = input("Digite o nome do aluno: ")

# Entrada das notas
nota1 = float(input("Digite a nota do 1º bimestre: "))
nota2 = float(input("Digite a nota do 2º bimestre: "))
nota3 = float(input("Digite a nota do 3º bimestre: "))
nota4 = float(input("Digite a nota do 4º bimestre: "))

# ==========================================
# CÁLCULO DA MÉDIA
# ==========================================

media = (nota1 + nota2 + nota3 + nota4) / 4

# ==========================================
# EXIBIÇÃO DAS NOTAS
# ==========================================

print("\n" + "=" * 45)
print("             BOLETIM ESCOLAR")
print("=" * 45)

print(f"Aluno: {nome}")
print(f"1º Bimestre: {nota1:.1f}")
print(f"2º Bimestre: {nota2:.1f}")
print(f"3º Bimestre: {nota3:.1f}")
print(f"4º Bimestre: {nota4:.1f}")

print("-" * 45)
print(f"Média final: {media:.1f}")

# ==========================================
# VERIFICAÇÃO DO RESULTADO
# ==========================================

if media >= 7:
    print("Situação: APROVADO! ✅")
    print("Parabéns! Você passou de ano.")

elif media >= 5:
    print("Situação: RECUPERAÇÃO! ⚠️")
    print("Você ainda pode recuperar sua nota.")

else:
    print("Situação: REPROVADO! ❌")
    print("Infelizmente, você não atingiu a média.")

# ==========================================
# FINALIZAÇÃO
# ==========================================

print("=" * 45)
print("             FIM DO BOLETIM")
print("=" * 45)