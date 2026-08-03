# ==========================================
# CLASSE AGENDA
# ==========================================

class Agenda:

    def __init__(self):
        self.contatos = []

    # Adiciona um contato na lista
    def adicionar_contato(self, nome):
        self.contatos.append(nome)

    # Mostra todos os contatos
    def mostrar_contatos(self):
        print("\nLista de contatos:")

        for contato in self.contatos:
            print(f"- {contato}")


# ==========================================
# CRIANDO A AGENDA
# ==========================================

agenda = Agenda()


# ==========================================
# ADICIONANDO CONTATOS
# ==========================================

agenda.adicionar_contato("João")
agenda.adicionar_contato("Maria")
agenda.adicionar_contato("Carlos")
agenda.adicionar_contato("Ana")


# ==========================================
# EXIBINDO OS CONTATOS
# ==========================================

print("=" * 40)
print("             MINHA AGENDA")
print("=" * 40)

agenda.mostrar_contatos()

print("=" * 40)