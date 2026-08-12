import random

# =====================================================
# PERSONAGEM
# =====================================================

player = {
    "nome": "Herói",
    "nivel": 1,
    "vida": 100,
    "vida_max": 100,
    "ataque": 20,
    "defesa": 5,
    "xp": 0,
    "pocoes": 3
}

# =====================================================
# INIMIGO
# =====================================================

inimigo = {
    "nome": "Goblin",
    "vida": 80,
    "vida_max": 80,
    "ataque": 15,
    "defesa": 3,
    "xp": 50
}


# =====================================================
# MOSTRAR STATUS
# =====================================================

def mostrar_status():

    print("\n==============================")
    print("         STATUS")
    print("==============================")

    print(f"Nome: {player['nome']}")
    print(f"Nível: {player['nivel']}")
    print(f"❤️ Vida: {player['vida']}/{player['vida_max']}")
    print(f"⚔️ Ataque: {player['ataque']}")
    print(f"🛡️ Defesa: {player['defesa']}")
    print(f"⭐ XP: {player['xp']}")
    print(f"🧪 Poções: {player['pocoes']}")

    print("==============================")


# =====================================================
# ATAQUE DO JOGADOR
# =====================================================

def atacar():

    dano = random.randint(10, player["ataque"])

    dano -= inimigo["defesa"]

    if dano < 1:
        dano = 1

    # Chance de ataque crítico
    critico = random.randint(1, 100)

    if critico <= 10:

        dano *= 2

        print("\n💥 ATAQUE CRÍTICO!")

    inimigo["vida"] -= dano

    if inimigo["vida"] < 0:
        inimigo["vida"] = 0

    print(f"\n⚔️ Você causou {dano} de dano!")

    print(
        f"👹 Vida do {inimigo['nome']}: "
        f"{inimigo['vida']}/{inimigo['vida_max']}"
    )


# =====================================================
# DEFESA
# =====================================================

def defender():

    print("\n🛡️ Você assumiu uma posição defensiva!")

    dano = random.randint(5, inimigo["ataque"])

    dano -= player["defesa"] * 2

    if dano < 1:
        dano = 1

    player["vida"] -= dano

    print(f"👹 O inimigo atacou e causou {dano} de dano.")

    print(
        f"❤️ Sua vida: "
        f"{player['vida']}/{player['vida_max']}"
    )


# =====================================================
# POÇÃO
# =====================================================

def usar_pocao():

    if player["pocoes"] <= 0:

        print("\n❌ Você não possui mais poções!")

        return False

    cura = 30

    player["vida"] += cura

    if player["vida"] > player["vida_max"]:
        player["vida"] = player["vida_max"]

    player["pocoes"] -= 1

    print(f"\n🧪 Você recuperou {cura} de vida!")

    print(
        f"❤️ Vida: "
        f"{player['vida']}/{player['vida_max']}"
    )

    return True


# =====================================================
# ATAQUE DO INIMIGO
# =====================================================

def ataque_inimigo():

    dano = random.randint(5, inimigo["ataque"])

    dano -= player["defesa"]

    if dano < 1:
        dano = 1

    player["vida"] -= dano

    if player["vida"] < 0:
        player["vida"] = 0

    print(
        f"\n👹 {inimigo['nome']} "
        f"causou {dano} de dano!"
    )

    print(
        f"❤️ Sua vida: "
        f"{player['vida']}/{player['vida_max']}"
    )


# =====================================================
# GANHAR XP
# =====================================================

def ganhar_xp():

    xp_ganho = inimigo["xp"]

    player["xp"] += xp_ganho

    print(f"\n⭐ Você ganhou {xp_ganho} XP!")

    xp_necessario = player["nivel"] * 100

    if player["xp"] >= xp_necessario:

        subir_nivel()


# =====================================================
# SUBIR DE NÍVEL
# =====================================================

def subir_nivel():

    player["nivel"] += 1

    player["vida_max"] += 20
    player["vida"] = player["vida_max"]

    player["ataque"] += 5

    player["defesa"] += 2

    player["xp"] = 0

    print("\n🎉 ============================")
    print("       VOCÊ SUBIU DE NÍVEL!")
    print("==============================")

    print(f"⭐ Novo nível: {player['nivel']}")
    print(f"❤️ Vida máxima: {player['vida_max']}")
    print(f"⚔️ Ataque: {player['ataque']}")
    print(f"🛡️ Defesa: {player['defesa']}")


# =====================================================
# BATALHA
# =====================================================

def batalha():

    print("\n================================")
    print("          ⚔️ BATALHA")
    print("================================")

    print(
        f"\n👹 Um {inimigo['nome']} apareceu!"
    )

    while player["vida"] > 0 and inimigo["vida"] > 0:

        print("\n------------------------------")

        print("Escolha uma ação:")

        print("1 - ⚔️ Atacar")
        print("2 - 🛡️ Defender")
        print("3 - 🧪 Usar poção")
        print("4 - 📊 Ver status")

        escolha = input("\nDigite sua escolha: ")

        if escolha == "1":

            atacar()

            if inimigo["vida"] <= 0:
                break

            ataque_inimigo()

        elif escolha == "2":

            defender()

        elif escolha == "3":

            usou = usar_pocao()

            if usou:

                ataque_inimigo()

        elif escolha == "4":

            mostrar_status()

        else:

            print("\n❌ Opção inválida!")

    # =================================================
    # RESULTADO
    # =================================================

    if player["vida"] <= 0:

        print("\n💀 ============================")
        print("          DERROTA")
        print("==============================")

        print("Você foi derrotado!")

    elif inimigo["vida"] <= 0:

        print("\n🏆 ============================")
        print("          VITÓRIA")
        print("==============================")

        print(
            f"Você derrotou o {inimigo['nome']}!"
        )

        ganhar_xp()


# =====================================================
# INÍCIO DO JOGO
# =====================================================

print("================================")
print("       ⚔️ RPG DE TURNO")
print("================================")

nome = input("\nDigite o nome do seu personagem: ")

if nome != "":
    player["nome"] = nome

print(
    f"\nBem-vindo, {player['nome']}!"
)

batalha()