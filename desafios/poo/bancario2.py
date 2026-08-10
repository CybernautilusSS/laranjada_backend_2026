1

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
import itertools


# ---------------------------------------------------------------------------
# Exceções personalizadas
# ---------------------------------------------------------------------------
class SaldoInsuficienteError(Exception):
    """Lançada quando o saque/transferência excede o saldo (+ limite)."""
    pass


class LimiteExcedidoError(Exception):
    """Lançada quando o valor ou a quantidade de saques excede o limite."""
    pass


class ValorInvalidoError(Exception):
    """Lançada quando um valor de operação é inválido (<= 0)."""
    pass


# ---------------------------------------------------------------------------
# Transação (histórico)
# ---------------------------------------------------------------------------
class Transacao:
    def __init__(self, tipo: str, valor: float):
        self.tipo = tipo
        self.valor = valor
        self.data = datetime.now()

    def __str__(self):
        return f"[{self.data:%d/%m/%Y %H:%M:%S}] {self.tipo:<12} R$ {self.valor:,.2f}"


class Historico:
    def __init__(self):
        self._transacoes: List[Transacao] = []

    def adicionar(self, transacao: Transacao):
        self._transacoes.append(transacao)

    @property
    def transacoes(self):
        return self._transacoes

    def imprimir(self):
        if not self._transacoes:
            print("Nenhuma movimentação registrada.")
            return
        for t in self._transacoes:
            print(t)


# ---------------------------------------------------------------------------
# Cliente
# ---------------------------------------------------------------------------
class Cliente:
    def __init__(self, nome: str, cpf: str, data_nascimento: str, endereco: str = ""):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas: List["Conta"] = []

    def adicionar_conta(self, conta: "Conta"):
        self.contas.append(conta)

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"


# ---------------------------------------------------------------------------
# Conta (classe abstrata) e subclasses
# ---------------------------------------------------------------------------
class Conta(ABC):
    _contador_id = itertools.count(1)

    def __init__(self, cliente: Cliente, agencia: str = "0001"):
        self._id = next(Conta._contador_id)
        self._saldo = 0.0
        self._agencia = agencia
        self._numero = self._id
        self._cliente = cliente
        self._historico = Historico()
        cliente.adicionar_conta(self)

    # ---- Propriedades ----
    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    # ---- Operações básicas ----
    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ValorInvalidoError("O valor do depósito deve ser positivo.")
        self._saldo += valor
        self._historico.adicionar(Transacao("Depósito", valor))
        print(f"Depósito de R$ {valor:,.2f} realizado com sucesso.")

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ValorInvalidoError("O valor do saque deve ser positivo.")
        if valor > self._saldo:
            raise SaldoInsuficienteError("Saldo insuficiente para o saque.")
        self._saldo -= valor
        self._historico.adicionar(Transacao("Saque", valor))
        print(f"Saque de R$ {valor:,.2f} realizado com sucesso.")

    def transferir(self, valor: float, destino: "Conta") -> None:
        self.sacar(valor)
        destino._saldo += valor
        destino._historico.adicionar(Transacao(f"Transf. recebida (Cta {self.numero})", valor))
        self._historico.adicionar(Transacao(f"Transf. enviada (Cta {destino.numero})", valor))
        print(f"Transferência de R$ {valor:,.2f} para a conta {destino.numero} concluída.")

    @abstractmethod
    def tipo(self) -> str:
        ...

    def extrato(self) -> None:
        print(f"\n===== Extrato — Conta {self.numero} ({self.tipo()}) =====")
        print(f"Titular: {self.cliente.nome}")
        self._historico.imprimir()
        print(f"Saldo atual: R$ {self._saldo:,.2f}")
        print("=" * 45)

    def __str__(self):
        return f"Conta {self.numero} | Agência {self.agencia} | {self.tipo()} | Titular: {self.cliente.nome}"


class ContaCorrente(Conta):
    def __init__(self, cliente: Cliente, limite: float = 500.0, limite_saques: int = 3, agencia: str = "0001"):
        super().__init__(cliente, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self._saques_realizados = 0

    def tipo(self) -> str:
        return "Conta Corrente"

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ValorInvalidoError("O valor do saque deve ser positivo.")
        if self._saques_realizados >= self.limite_saques:
            raise LimiteExcedidoError("Número máximo de saques diários atingido.")
        if valor > (self._saldo + self.limite):
            raise SaldoInsuficienteError("Saldo e limite insuficientes para o saque.")

        self._saldo -= valor
        self._saques_realizados += 1
        self._historico.adicionar(Transacao("Saque", valor))
        print(f"Saque de R$ {valor:,.2f} realizado com sucesso.")


class ContaPoupanca(Conta):
    def __init__(self, cliente: Cliente, taxa_rendimento: float = 0.005, agencia: str = "0001"):
        super().__init__(cliente, agencia)
        self.taxa_rendimento = taxa_rendimento

    def tipo(self) -> str:
        return "Conta Poupança"

    def render_juros(self) -> None:
        juros = self._saldo * self.taxa_rendimento
        if juros > 0:
            self._saldo += juros
            self._historico.adicionar(Transacao("Rendimento", juros))
            print(f"Rendimento de R$ {juros:,.2f} aplicado.")
        else:
            print("Sem saldo para gerar rendimento.")


# ---------------------------------------------------------------------------
# Banco (agrega clientes e contas)
# ---------------------------------------------------------------------------
class Banco:
    def __init__(self, nome: str):
        self.nome = nome
        self.clientes: List[Cliente] = []
        self.contas: List[Conta] = []

    def cadastrar_cliente(self, nome: str, cpf: str, nascimento: str, endereco: str = "") -> Cliente:
        if self.buscar_cliente_por_cpf(cpf):
            raise ValueError("Já existe um cliente cadastrado com esse CPF.")
        cliente = Cliente(nome, cpf, nascimento, endereco)
        self.clientes.append(cliente)
        return cliente

    def buscar_cliente_por_cpf(self, cpf: str) -> Cliente | None:
        return next((c for c in self.clientes if c.cpf == cpf), None)

    def abrir_conta(self, cliente: Cliente, tipo: str = "corrente") -> Conta:
        if tipo == "corrente":
            conta = ContaCorrente(cliente)
        elif tipo == "poupanca":
            conta = ContaPoupanca(cliente)
        else:
            raise ValueError("Tipo de conta inválido. Use 'corrente' ou 'poupanca'.")
        self.contas.append(conta)
        return conta

    def buscar_conta(self, numero: int) -> Conta | None:
        return next((c for c in self.contas if c.numero == numero), None)

    def listar_contas(self):
        for conta in self.contas:
            print(conta)


# ---------------------------------------------------------------------------
# Interface de linha de comando (menu)
# ---------------------------------------------------------------------------
def menu() -> str:
    opcoes = """
========== BANCO PYTHON ==========
[1] Cadastrar cliente
[2] Abrir conta
[3] Depositar
[4] Sacar
[5] Transferir
[6] Ver extrato
[7] Listar contas
[8] Render juros (poupança)
[0] Sair
=> """
    return input(opcoes)


def main():
    banco = Banco("Banco Python S.A.")

    while True:
        opcao = menu().strip()

        try:
            if opcao == "1":
                nome = input("Nome: ")
                cpf = input("CPF: ")
                nascimento = input("Data de nascimento (dd/mm/aaaa): ")
                endereco = input("Endereço: ")
                cliente = banco.cadastrar_cliente(nome, cpf, nascimento, endereco)
                print(f"Cliente {cliente} cadastrado com sucesso!")

            elif opcao == "2":
                cpf = input("CPF do cliente: ")
                cliente = banco.buscar_cliente_por_cpf(cpf)
                if not cliente:
                    print("Cliente não encontrado.")
                    continue
                tipo = input("Tipo de conta (corrente/poupanca): ").strip().lower()
                conta = banco.abrir_conta(cliente, tipo)
                print(f"Conta criada: {conta}")

            elif opcao == "3":
                numero = int(input("Número da conta: "))
                conta = banco.buscar_conta(numero)
                if not conta:
                    print("Conta não encontrada.")
                    continue
                valor = float(input("Valor do depósito: "))
                conta.depositar(valor)

            elif opcao == "4":
                numero = int(input("Número da conta: "))
                conta = banco.buscar_conta(numero)
                if not conta:
                    print("Conta não encontrada.")
                    continue
                valor = float(input("Valor do saque: "))
                conta.sacar(valor)

            elif opcao == "5":
                origem = int(input("Número da conta de origem: "))
                destino = int(input("Número da conta de destino: "))
                conta_origem = banco.buscar_conta(origem)
                conta_destino = banco.buscar_conta(destino)
                if not conta_origem or not conta_destino:
                    print("Conta de origem ou destino não encontrada.")
                    continue
                valor = float(input("Valor a transferir: "))
                conta_origem.transferir(valor, conta_destino)

            elif opcao == "6":
                numero = int(input("Número da conta: "))
                conta = banco.buscar_conta(numero)
                if not conta:
                    print("Conta não encontrada.")
                    continue
                conta.extrato()

            elif opcao == "7":
                banco.listar_contas()

            elif opcao == "8":
                numero = int(input("Número da conta poupança: "))
                conta = banco.buscar_conta(numero)
                if not isinstance(conta, ContaPoupanca):
                    print("Essa operação é válida apenas para contas poupança.")
                    continue
                conta.render_juros()

            elif opcao == "0":
                print("Obrigado por usar o Banco Python. Até logo!")
                break

            else:
                print("Opção inválida. Tente novamente.")

        except (SaldoInsuficienteError, LimiteExcedidoError, ValorInvalidoError, ValueError) as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    main()