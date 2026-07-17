from getpass import getpass


class Usuario:
    def __init__(self, usuario, senha):
        self.usuario = usuario
        self.__senha = senha  # Senha privada

    def verificar_senha(self, senha):
        return self.__senha == senha


class SistemaLogin:
    def __init__(self):
        self.usuarios = {}

    def cadastrar(self):
        print("\n===== CADASTRO =====")

        usuario = input("Digite um nome de usuário: ")

        if usuario in self.usuarios:
            print("Esse usuário já existe!")
            return

        senha = getpass("Digite uma senha: ")

        self.usuarios[usuario] = Usuario(usuario, senha)

        print("Usuário cadastrado com sucesso!")

    def login(self):
        print("\n===== LOGIN =====")

        usuario = input("Usuário: ")

        if usuario not in self.usuarios:
            print("Usuário não encontrado!")
            return

        tentativas = 6

        while tentativas > 0:
            senha = getpass("Senha: ")

            if self.usuarios[usuario].verificar_senha(senha):
                print(f"\nBem-vindo, {usuario}!")
                return

            tentativas -= 1
            print(f"Senha incorreta! Tentativas restantes: {tentativas}")

        print("\nAcesso bloqueado!")

    def menu(self):
        while True:
            print("\n========= MENU =========")
            print("0 - Cadastro")
            print("1 - Login")
            print("2 - Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "0":
                self.cadastrar()

            elif opcao == "1":
                self.login()

            elif opcao == "2":
                print("Sistema encerrado.")
                break

            else:
                print("Opção inválida!")


# Programa principal
sistema = SistemaLogin()
sistema.menu()