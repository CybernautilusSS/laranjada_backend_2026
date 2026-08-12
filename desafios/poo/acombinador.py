"""
Validador de Placas de Trânsito (Brasil)
------------------------------------------
Verifica se uma placa está no formato correto:

  - Antigo:    LLLNNNN     ex: ABC1234 ou ABC-1234
  - Mercosul:  LLLNLNN     ex: ABC1D23

Detecta automaticamente qual padrão a placa segue (se houver) e aponta
exatamente qual posição está incorreta, caso não seja válida.

IMPORTANTE: este validador checa apenas a ESTRUTURA da placa (se os
caracteres batem com o padrão letra/número esperado). Ele NÃO consulta
nenhuma base de dados e não informa se a placa existe de fato ou a quem
pertence — isso só pode ser feito por canais oficiais (Detran, Sinesp
Cidadão), mediante autenticação.
"""

import string

LETRAS = string.ascii_uppercase
NUMEROS = string.digits

PADROES = {
    "antigo": "LLLNNNN",     # ex: ABC1234
    "mercosul": "LLLNLNN",   # ex: ABC1D23
}


def limpar_placa(placa: str) -> str:
    """Remove espaços, traços e deixa em maiúsculo."""
    return placa.strip().upper().replace("-", "").replace(" ", "")


def validar_contra_padrao(placa: str, padrao: str):
    """Valida uma placa (já limpa) contra um padrão específico.
    Retorna (valido: bool, erros: list[str])
    """
    erros = []

    if len(placa) != len(padrao):
        erros.append(f"Tamanho incorreto: esperado {len(padrao)} caracteres, recebido {len(placa)}.")
        return False, erros

    for i, (char, tipo) in enumerate(zip(placa, padrao)):
        posicao = i + 1
        if tipo == "L" and char not in LETRAS:
            erros.append(f"Posição {posicao}: '{char}' deveria ser uma LETRA (A-Z).")
        elif tipo == "N" and char not in NUMEROS:
            erros.append(f"Posição {posicao}: '{char}' deveria ser um NÚMERO (0-9).")

    return len(erros) == 0, erros


def identificar_formato(placa: str):
    """
    Tenta identificar automaticamente qual padrão a placa segue.
    Retorna o nome do formato válido, ou None se não bater com nenhum.
    """
    for nome, padrao in PADROES.items():
        valido, _ = validar_contra_padrao(placa, padrao)
        if valido:
            return nome
    return None


def formatar_exibicao(placa: str, formato: str) -> str:
    if formato == "antigo":
        return f"{placa[:3]}-{placa[3:]}"
    return placa


def analisar_placa(placa_bruta: str) -> dict:
    """Executa a análise completa de uma placa e retorna um relatório."""
    placa = limpar_placa(placa_bruta)
    formato_detectado = identificar_formato(placa)

    resultado = {
        "entrada_original": placa_bruta,
        "placa_normalizada": placa,
        "valida": formato_detectado is not None,
        "formato": formato_detectado,
        "erros_por_formato": {},
    }

    if formato_detectado is None:
        # Guarda os erros de cada padrão testado, pra ajudar a diagnosticar
        for nome, padrao in PADROES.items():
            _, erros = validar_contra_padrao(placa, padrao)
            resultado["erros_por_formato"][nome] = erros

    return resultado


def imprimir_relatorio(resultado: dict):
    print("-" * 60)
    print(f"Placa informada : {resultado['entrada_original']}")
    print(f"Normalizada     : {resultado['placa_normalizada']}")

    if resultado["valida"]:
        formato = resultado["formato"]
        exibicao = formatar_exibicao(resultado["placa_normalizada"], formato)
        print(f"Status          : ✅ VÁLIDA (formato {formato})")
        print(f"Exibição padrão : {exibicao}")
    else:
        print("Status          : ❌ INVÁLIDA (não bate com nenhum formato conhecido)")
        for nome, erros in resultado["erros_por_formato"].items():
            print(f"\n  Testando formato '{nome}' ({PADROES[nome]}):")
            for erro in erros:
                print(f"    - {erro}")
    print("-" * 60)


def main():
    print("=" * 60)
    print("VALIDADOR DE FORMATO DE PLACAS (Antigo e Mercosul)")
    print("=" * 60)
    print("Digite 'sair' para encerrar.\n")

    while True:
        entrada = input("Digite a placa para validar: ").strip()
        if entrada.lower() == "sair":
            print("Encerrado.")
            break
        if not entrada:
            continue

        resultado = analisar_placa(entrada)
        imprimir_relatorio(resultado)
        print()


if __name__ == "__main__":
    main()