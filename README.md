# Controle de Gastos Pessoais

Sistema em Python para registrar gastos do dia a dia, ver o total por categoria e gerar um relatório.

## Requisitos do trabalho

| Requisito | Onde está no código |
|---|---|
| Utilização de funções | Todo o sistema é dividido em funções: `carregar_gastos`, `salvar_gastos`, `somar_gastos`, `total_por_categoria`, `adicionar_gasto`, `listar_gastos`, `gerar_relatorio`, `main`... |
| Leitura de arquivo | `carregar_gastos()` lê o arquivo `gastos.csv` quando o sistema abre |
| Escrita de arquivo | `salvar_gastos()` grava o `gastos.csv` a cada gasto adicionado ou removido; `gerar_relatorio()` grava o `relatorio.txt` |

## Como executar

Precisa apenas do Python 3 instalado (não usa bibliotecas externas).

```
python controle_gastos.py
```

## Menu

```
1 - Adicionar gasto
2 - Listar gastos
3 - Resumo por categoria
4 - Remover gasto
5 - Gerar relatório em arquivo
0 - Sair
```

## Roteiro para a apresentação

1. Rodar o sistema e mostrar que começa com 0 gastos.
2. Adicionar 2 ou 3 gastos (opção 1).
3. Listar (opção 2) e mostrar o resumo por categoria (opção 3).
4. Abrir o arquivo `gastos.csv` e mostrar os dados gravados (**escrita**).
5. Fechar o sistema (opção 0) e abrir de novo: os gastos são carregados do arquivo (**leitura**).
6. Gerar o relatório (opção 5) e abrir o `relatorio.txt`.
