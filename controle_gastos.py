"""
Sistema de Controle de Gastos Pessoais

Trabalho de faculdade - Python
Requisitos atendidos:
  - Utilização de funções (todo o sistema é dividido em funções)
  - Utilização de arquivos (os gastos são lidos e gravados em "gastos.csv"
    e o relatório é gravado em "relatorio.txt")
"""

import csv
import os
from datetime import date

ARQUIVO_GASTOS = "gastos.csv"
ARQUIVO_RELATORIO = "relatorio.txt"
CAMPOS = ["data", "descricao", "categoria", "valor"]
CATEGORIAS = ["Alimentação", "Transporte", "Moradia", "Lazer", "Estudos", "Outros"]


# ---------------------------------------------------------------
# Funções de arquivo (leitura e escrita)
# ---------------------------------------------------------------

def carregar_gastos():
    """Lê o arquivo CSV e devolve a lista de gastos."""
    if not os.path.exists(ARQUIVO_GASTOS):
        return []
    gastos = []
    with open(ARQUIVO_GASTOS, "r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            linha["valor"] = float(linha["valor"])
            gastos.append(linha)
    return gastos


def salvar_gastos(gastos):
    """Grava a lista de gastos no arquivo CSV."""
    with open(ARQUIVO_GASTOS, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(gastos)


def gerar_relatorio(gastos):
    """Grava um relatório em texto com o total por categoria."""
    totais = total_por_categoria(gastos)
    with open(ARQUIVO_RELATORIO, "w", encoding="utf-8") as arquivo:
        arquivo.write("RELATÓRIO DE GASTOS\n")
        arquivo.write(f"Gerado em: {date.today().strftime('%d/%m/%Y')}\n")
        arquivo.write("=" * 35 + "\n")
        for categoria, total in totais.items():
            arquivo.write(f"{categoria:<15} {formatar_valor(total):>18}\n")
        arquivo.write("=" * 35 + "\n")
        arquivo.write(f"{'TOTAL':<15} {formatar_valor(somar_gastos(gastos)):>18}\n")
    print(f"\nRelatório salvo no arquivo '{ARQUIVO_RELATORIO}'.")


# ---------------------------------------------------------------
# Funções de cálculo
# ---------------------------------------------------------------

def somar_gastos(gastos):
    """Soma o valor de todos os gastos."""
    total = 0
    for gasto in gastos:
        total += gasto["valor"]
    return total


def total_por_categoria(gastos):
    """Devolve um dicionário {categoria: total gasto}."""
    totais = {}
    for gasto in gastos:
        categoria = gasto["categoria"]
        totais[categoria] = totais.get(categoria, 0) + gasto["valor"]
    return totais


def formatar_valor(valor):
    """Formata um número no padrão brasileiro: R$ 1.234,56"""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


# ---------------------------------------------------------------
# Funções de entrada do usuário
# ---------------------------------------------------------------

def ler_valor(mensagem):
    """Pede um valor numérico positivo até o usuário digitar certo."""
    while True:
        texto = input(mensagem).replace(",", ".")
        try:
            valor = float(texto)
            if valor > 0:
                return valor
            print("O valor precisa ser maior que zero.")
        except ValueError:
            print("Valor inválido. Exemplo: 25,90")


def escolher_categoria():
    """Mostra as categorias e devolve a escolhida."""
    print("\nCategorias:")
    for numero, categoria in enumerate(CATEGORIAS, start=1):
        print(f"  {numero} - {categoria}")
    while True:
        opcao = input("Escolha o número da categoria: ")
        if opcao.isdigit() and 1 <= int(opcao) <= len(CATEGORIAS):
            return CATEGORIAS[int(opcao) - 1]
        print("Opção inválida.")


# ---------------------------------------------------------------
# Funções do menu
# ---------------------------------------------------------------

def adicionar_gasto(gastos):
    """Cadastra um novo gasto e salva no arquivo."""
    print("\n--- NOVO GASTO ---")
    descricao = input("Descrição: ").strip() or "Sem descrição"
    categoria = escolher_categoria()
    valor = ler_valor("Valor (R$): ")
    gasto = {
        "data": date.today().strftime("%d/%m/%Y"),
        "descricao": descricao,
        "categoria": categoria,
        "valor": valor,
    }
    gastos.append(gasto)
    salvar_gastos(gastos)
    print("Gasto cadastrado e salvo!")


def listar_gastos(gastos):
    """Mostra todos os gastos cadastrados."""
    print("\n--- LISTA DE GASTOS ---")
    if not gastos:
        print("Nenhum gasto cadastrado.")
        return
    for numero, gasto in enumerate(gastos, start=1):
        print(f"{numero:>2}. {gasto['data']}  {gasto['descricao']:<20} "
              f"{gasto['categoria']:<12} {formatar_valor(gasto['valor']):>12}")
    print(f"\nTotal gasto: {formatar_valor(somar_gastos(gastos))}")


def mostrar_resumo(gastos):
    """Mostra o total gasto em cada categoria."""
    print("\n--- RESUMO POR CATEGORIA ---")
    if not gastos:
        print("Nenhum gasto cadastrado.")
        return
    for categoria, total in total_por_categoria(gastos).items():
        print(f"{categoria:<15} {formatar_valor(total):>15}")


def remover_gasto(gastos):
    """Remove um gasto pelo número da lista e salva no arquivo."""
    listar_gastos(gastos)
    if not gastos:
        return
    opcao = input("\nNúmero do gasto para remover (Enter para cancelar): ")
    if opcao.isdigit() and 1 <= int(opcao) <= len(gastos):
        removido = gastos.pop(int(opcao) - 1)
        salvar_gastos(gastos)
        print(f"Gasto '{removido['descricao']}' removido.")
    else:
        print("Nada foi removido.")


def mostrar_menu():
    """Exibe o menu principal e devolve a opção escolhida."""
    print("\n===== CONTROLE DE GASTOS =====")
    print("1 - Adicionar gasto")
    print("2 - Listar gastos")
    print("3 - Resumo por categoria")
    print("4 - Remover gasto")
    print("5 - Gerar relatório em arquivo")
    print("0 - Sair")
    return input("Opção: ").strip()


def main():
    """Função principal: carrega os dados e roda o menu."""
    gastos = carregar_gastos()
    print(f"{len(gastos)} gasto(s) carregado(s) do arquivo '{ARQUIVO_GASTOS}'.")

    while True:
        opcao = mostrar_menu()
        if opcao == "1":
            adicionar_gasto(gastos)
        elif opcao == "2":
            listar_gastos(gastos)
        elif opcao == "3":
            mostrar_resumo(gastos)
        elif opcao == "4":
            remover_gasto(gastos)
        elif opcao == "5":
            gerar_relatorio(gastos)
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
