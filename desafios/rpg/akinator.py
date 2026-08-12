import time

print("=" * 50)
print("           🧞 AKINATOR PYTHON")
print("=" * 50)

print("\nPense em um personagem famoso.")
print("Eu vou tentar descobrir quem é!")
print()

input("Quando estiver pronto, pressione ENTER...")

# ==========================================================
# FUNÇÃO PARA PERGUNTAS
# ==========================================================

def perguntar(pergunta):

    while True:

        resposta = input(pergunta + " (s/n): ").lower()

        if resposta == "s":
            return True

        elif resposta == "n":
            return False

        else:
            print("Digite apenas S para sim ou N para não.")


# ==========================================================
# PERGUNTAS
# ==========================================================

famoso = perguntar(
    "\nSeu personagem é uma pessoa real?"
)

if famoso:

    homem = perguntar(
        "Seu personagem é homem?"
    )

    if homem:

        jogador = perguntar(
            "Ele é jogador de futebol?"
        )

        if jogador:

            brasileiro = perguntar(
                "Ele é brasileiro?"
            )

            if brasileiro:

                print("\n🤔 Estou pensando...")

                time = perguntar(
                    "Ele é conhecido por jogar no Brasil?"
                )

                if time:

                    print("\n⚽ Meu palpite é: Neymar!")
                else:

                    print("\n⚽ Meu palpite é: Ronaldinho Gaúcho!")

            else:

                print(
                    "\n⚽ Meu palpite é: Cristiano Ronaldo!"
                )

        else:

            cantor = perguntar(
                "Ele é cantor?"
            )

            if cantor:

                print(
                    "\n🎤 Meu palpite é: Michael Jackson!"
                )

            else:

                ator = perguntar(
                    "Ele é ator?"
                )

                if ator:

                    print(
                        "\n🎬 Meu palpite é: Tom Cruise!"
                    )

                else:

                    print(
                        "\n🤔 Não consegui descobrir!"
                    )

    else:

        cantora = perguntar(
            "Ela é cantora?"
        )

        if cantora:

            brasileira = perguntar(
                "Ela é brasileira?"
            )

            if brasileira:

                print(
                    "\n🎤 Meu palpite é: Anitta!"
                )

            else:

                print(
                    "\n🎤 Meu palpite é: Taylor Swift!"
                )

        else:

            atriz = perguntar(
                "Ela é atriz?"
            )

            if atriz:

                print(
                    "\n🎬 Meu palpite é: Angelina Jolie!"
                )

            else:

                print(
                    "\n🤔 Não consegui descobrir!"
                )

# ==========================================================
# PERSONAGEM FICTÍCIO
# ==========================================================

else:

    humano = perguntar(
        "Seu personagem é humano?"
    )

    if humano:

        usa_mascara = perguntar(
            "Ele usa máscara?"
        )

        if usa_mascara:

            super_heroi = perguntar(
                "Ele é um super-herói?"
            )

            if super_heroi:

                print(
                    "\n🦸 Meu palpite é: Homem-Aranha!"
                )

            else:

                print(
                    "\n🦹 Meu palpite é: algum personagem mascarado!"
                )

        else:

            escola = perguntar(
                "Ele frequenta uma escola de magia?"
            )

            if escola:

                print(
                    "\n🧙 Meu palpite é: Harry Potter!"
                )

            else:

                print(
                    "\n🤔 Meu palpite é: Naruto!"
                )

    else:

        animal = perguntar(
            "Seu personagem é um animal?"
        )

        if animal:

            gato = perguntar(
                "Ele é um gato?"
            )

            if gato:

                print(
                    "\n🐱 Meu palpite é: Garfield!"
                )

            else:

                rato = perguntar(
                    "Ele é um rato?"
                )

                if rato:

                    print(
                        "\n🐭 Meu palpite é: Mickey Mouse!"
                    )

                else:

                    print(
                        "\n🐾 Meu palpite é: um animal famoso!"
                    )

        else:

            anime = perguntar(
                "Seu personagem vem de um anime?"
            )

            if anime:

                print(
                    "\n⚡ Meu palpite é: Goku!"
                )

            else:

                jogo = perguntar(
                    "Seu personagem vem de um jogo?"
                )

                if jogo:

                    print(
                        "\n🎮 Meu palpite é: Mario!"
                    )

                else:

                    print(
                        "\n🤔 Não consegui descobrir!"
                    )

print("\nObrigado por jogar! 🧞")