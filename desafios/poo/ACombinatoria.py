"""
Analisador de Placas - Completar Placas Parciais
--------------------------------------------------
Você informa os caracteres que já conhece de uma placa (e usa '?' para
as posições que não sabe) e o sistema gera todas as combinações possíveis
que completam a placa, respeitando o formato escolhido.

Formatos suportados:
  - Antigo (Brasil):   LLLNNNN     ex: ABC1234
  - Mercosul (Brasil): LLLNLNN     ex: ABC1D23
  - Customizado: você pode definir seu próprio padrão com 'L' (letra) e 'N' (número)

Exemplo de uso:
  Formato: mercosul (LLLNLNN)
  Placa parcial informada: AB?1?23   -> ? nas posições desconhecidas
  Resultado: todas as placas possíveis que batem com AB_1_23
"""

import itertools
import string
import csv

LETRAS = string.ascii_uppercase
NUMEROS = string.digits
CORINGA = "?"

PADROES = {
    "antigo": "LLLNNNN",
    "mercosul": "LLLNLNN",
}


def validar_parcial(parcial: str, padrao: str) -> tuple[bool, str]:
    """Verifica se a placa parcial é compatível com o padrão escolhido."""
    if len(parcial) != len(padrao):
        return False, f"Tamanho incorreto: a placa parcial deve ter {len(padrao)} caracteres."

    for i, (char, tipo) in enumerate(zip(parcial, padrao)):
        if char == CORINGA:
            continue
        if tipo == "L" and char not in LETRAS:
            return False, f"Posição {i+1}: '{char}' deveria ser uma LETRA (A-Z) ou '?'."
        if tipo == "N" and char not in NUMEROS:
            return False, f"Posição {i+1}: '{char}' deveria ser um NÚMERO (0-9) ou '?'."

    return True, "OK"


def contar_combinacoes(parcial: str, padrao: str) -> int:
    """Conta quantas combinações possíveis existem para preencher as incógnitas."""
    total = 1
    for char, tipo in zip(parcial, padrao):
        if char != CORINGA:
            continue
        total *= len(LETRAS) if tipo == "L" else len(NUMEROS)
    return total


def gerar_combinacoes_parciais(parcial: str, padrao: str):
    """Gera (via generator) todas as placas completas possíveis a partir da parcial."""
    posicoes_incognitas = [i for i, c in enumerate(parcial) if c == CORINGA]
    conjuntos = [LETRAS if padrao[i] == "L" else NUMEROS for i in posicoes_incognitas]

    for combinacao in itertools.product(*conjuntos):
        placa = list(parcial)
        for pos, char in zip(posicoes_incognitas, combinacao):
            placa[pos] = char
        yield "".join(placa)


def formatar_placa(placa: str, padrao: str) -> str:
    if padrao == PADROES["antigo"]:
        return f"{placa[:3]}-{placa[3:]}"
    return placa


def salvar_em_arquivo(gerador, caminho: str, limite: int | None = None):
    """Salva as combinações geradas em um arquivo CSV."""
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["placa"])
        count = 0
        for placa in gerador:
            writer.writerow([placa])
            count += 1
            if limite and count >= limite:
                break
    return count


def escolher_padrao() -> str:
    print("\nEscolha o formato da placa:")
    print("  1 - Antigo (LLLNNNN)   ex: ABC1234")
    print("  2 - Mercosul (LLLNLNN) ex: ABC1D23")
    print("  3 - Customizado (você define o padrão com L/N)")
    escolha = input("Opção: ").strip()

    if escolha == "1":
        return PADROES["antigo"]
    elif escolha == "2":
        return PADROES["mercosul"]
    elif escolha == "3":
        padrao = input("Digite o padrão (ex: LLNNLL): ").strip().upper()
        if not all(c in "LN" for c in padrao):
            raise ValueError("Padrão inválido: use apenas 'L' e 'N'.")
        return padrao
    else:
        raise ValueError("Opção inválida.")


def main():
    print("=" * 60)
    print("ANALISADOR DE PLACAS - COMPLETAR PLACA PARCIAL")
    print("=" * 60)

    padrao = escolher_padrao()
    print(f"\nFormato escolhido: {padrao} ({len(padrao)} caracteres)")
    print(f"Digite a placa que você conhece, usando '?' para o que não sabe.")
    print(f"Exemplo para o formato {padrao}: {padrao.replace('L', 'A').replace('N', '1', 1)[:2]}?...")

    parcial = input("\nPlaca parcial: ").strip().upper()

    valido, mensagem = validar_parcial(parcial, padrao)
    if not valido:
        print(f"\n❌ Erro: {mensagem}")
        return

    total = contar_combinacoes(parcial, padrao)
    print(f"\n✅ Placa parcial válida: {formatar_placa(parcial, padrao)}")
    print(f"Total de combinações possíveis: {total:,}")

    if total == 0:
        print("A placa já está completa, nenhuma incógnita para preencher.")
        return

    gerador = gerar_combinacoes_parciais(parcial, padrao)

    if total <= 30:
        print("\nCombinações possíveis:")
        for placa in gerador:
            print(f"  {formatar_placa(placa, padrao)}")
    else:
        print(f"\nSão muitas combinações ({total:,}) para mostrar na tela.")
        salvar = input("Deseja salvar todas em um arquivo CSV? (s/n): ").strip().lower()
        if salvar == "s":
            caminho = "placas_geradas.csv"
            limite_input = input("Limite de linhas a salvar (Enter para salvar todas): ").strip()
            limite = int(limite_input) if limite_input else None
            qtd = salvar_em_arquivo(gerador, caminho, limite)
            print(f"\n✅ {qtd:,} combinações salvas em '{caminho}'")
        else:
            print("\nExibindo as 15 primeiras como amostra:")
            for i, placa in enumerate(gerador):
                if i >= 15:
                    print("  ... (demais combinações omitidas)")
                    break
                print(f"  {formatar_placa(placa, padrao)}")


if __name__ == "__main__":
    main()