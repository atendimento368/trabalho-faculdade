"""
Interface web (Flask) do Sistema de Controle de Gastos Pessoais.
Reaproveita as funções de controle_gastos.py (CSV e relatório).
"""

import os
from datetime import date
from urllib.parse import quote

from flask import Flask, render_template, request, redirect, send_file

from controle_gastos import (
    CATEGORIAS,
    ARQUIVO_RELATORIO,
    carregar_gastos,
    salvar_gastos,
    gerar_relatorio,
    somar_gastos,
    total_por_categoria,
    formatar_valor,
)

app = Flask(__name__)


def voltar(mensagem, tipo):
    """Redireciona para a página inicial com uma mensagem."""
    return redirect(f"/?msg={quote(mensagem)}&tipo={tipo}")


@app.route("/")
def index():
    gastos = carregar_gastos()
    total = somar_gastos(gastos)

    resumo = []
    for categoria, valor in sorted(total_por_categoria(gastos).items(), key=lambda x: -x[1]):
        resumo.append({
            "categoria": categoria,
            "total": formatar_valor(valor),
            "pct": round(valor / total * 100) if total else 0,
            "cor": CATEGORIAS.index(categoria) if categoria in CATEGORIAS else 5,
        })

    lista = []
    for indice, gasto in enumerate(gastos):
        lista.append({
            "indice": indice,
            "data": gasto["data"],
            "descricao": gasto["descricao"],
            "categoria": gasto["categoria"],
            "valor": formatar_valor(gasto["valor"]),
            "cor": CATEGORIAS.index(gasto["categoria"]) if gasto["categoria"] in CATEGORIAS else 5,
        })
    lista.reverse()  # mais recentes primeiro

    return render_template(
        "index.html",
        gastos=lista,
        resumo=resumo,
        total=formatar_valor(total),
        quantidade=len(gastos),
        categorias=CATEGORIAS,
        msg=request.args.get("msg"),
        tipo=request.args.get("tipo", "ok"),
        tem_relatorio=os.path.exists(ARQUIVO_RELATORIO),
    )


@app.route("/adicionar", methods=["POST"])
def adicionar():
    descricao = request.form.get("descricao", "").strip() or "Sem descrição"
    categoria = request.form.get("categoria", "")
    texto_valor = request.form.get("valor", "").replace(",", ".").strip()

    if categoria not in CATEGORIAS:
        return voltar("Escolha uma categoria.", "erro")
    try:
        valor = float(texto_valor)
        if valor <= 0:
            raise ValueError
    except ValueError:
        return voltar("Digite um valor maior que zero. Exemplo: 25,90", "erro")

    gastos = carregar_gastos()
    gastos.append({
        "data": date.today().strftime("%d/%m/%Y"),
        "descricao": descricao,
        "categoria": categoria,
        "valor": valor,
    })
    salvar_gastos(gastos)
    return voltar("Gasto cadastrado!", "ok")


@app.route("/remover/<int:indice>", methods=["POST"])
def remover(indice):
    gastos = carregar_gastos()
    if 0 <= indice < len(gastos):
        removido = gastos.pop(indice)
        salvar_gastos(gastos)
        return voltar(f"Gasto '{removido['descricao']}' removido.", "ok")
    return voltar("Gasto não encontrado.", "erro")


@app.route("/relatorio", methods=["POST"])
def relatorio():
    gastos = carregar_gastos()
    if not gastos:
        return voltar("Nenhum gasto cadastrado para gerar o relatório.", "erro")
    gerar_relatorio(gastos)
    return voltar(f"Relatório salvo em '{ARQUIVO_RELATORIO}'.", "ok")


@app.route("/baixar-relatorio")
def baixar_relatorio():
    return send_file(os.path.abspath(ARQUIVO_RELATORIO), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)