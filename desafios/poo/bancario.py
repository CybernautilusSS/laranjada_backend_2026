
class ContaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.__saldo = saldo

    def consultar_saldo(self):
        print(f"\nTitular: {self.titular}")
        print(f"Saldo: R$ {self.__saldo:.2f}")

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print(f"\nDepósito de R$ {valor:.2f} realizado!")
        else:
            print("\nO valor do depósito deve ser maior que zero.")

    def sacar(self, valor):
        if valor <= 0:
            print("\nO valor do saque deve ser maior que zero.")
        elif valor > self.__saldo:
            print("\nSaldo insuficiente!")
        else:
            self.__saldo -= valor
            print(f"\nSaque de R$ {valor:.2f} realizado!")


# Cadastro do cliente
print("================================")
print("       BANCO PYTHON")
print("================================")

nome = input("Digite o nome do titular: ")

conta = ContaBancaria(nome)

print(f"\nConta criada com sucesso para {nome}!")


# Menu principal
while True:
    print("\n================================")
    print("          MENU DO BANCO")
    print("================================")
    print("1 - Consultar saldo")
    print("2 - Depositar")
    print("3 - Sacar")
    print("4 - Sair")
    print("================================")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        conta.consultar_saldo()

    elif opcao == "2":
        valor = float(input("Digite o valor do depósito: R$ "))
        conta.depositar(valor)

    elif opcao == "3":
        valor = float(input("Digite o valor do saque: R$ "))
        conta.sacar(valor)

    elif opcao == "4":
        print("\nObrigado por utilizar o Banco Python!")
        break

    else:
        print("\nOpção inválida! Escolha uma opção de 1 a 4.")

