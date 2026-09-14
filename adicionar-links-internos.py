#!/usr/bin/env python3
"""
Melhora linkagem interna entre módulos do site.

Ações:
  1. Corrige link quebrado em o-que-e-steel-framing
  2. Adiciona seção "Leitura relacionada" antes do closing-parallax em:
     - 4 sub-páginas do Airbnb  → Financiamento + o-que-e LSF
     - Página principal Financiamento → Airbnb
     - Página principal o-que-e-steel-framing → Financiamento

Idempotente — pula arquivos que já contenham 'leitura-relacionada'.
"""
import os, re

ROOT   = os.path.dirname(__file__)
CONTENT = os.path.join(ROOT, "public", "content")

ANCHOR = '<section class="closing-parallax"'

def secao_relacionada(links):
    """
    links: lista de (href, titulo, descricao)
    Usa as classes .card-grid e .card já existentes no CSS do site.
    """
    itens = "\n".join(
        f'<article class="card">\n'
        f'<h3>{titulo}</h3>\n'
        f'<p>{desc}</p>\n'
        f'<a class="go" href="{href}">Ler mais →</a>\n'
        f'</article>'
        for href, titulo, desc in links
    )
    return (
        '<section class="section section-soft">\n'
        '<div class="content-narrow">\n'
        '<div class="eyebrow">Leitura relacionada</div>\n'
        '<h2>Continue explorando</h2>\n'
        f'<div class="card-grid leitura-relacionada">\n{itens}\n</div>\n'
        '</div>\n'
        '</section>\n'
    )

TAREFAS = [
    # (caminho_relativo, links_relacionados)
    (
        "mercado-de-investimento/airbnb/prazo-e-escala/index.html",
        [
            ("/mercado-de-investimento/financiamento-steel-framing/",
             "Steel Framing para Financiamento CAIXA",
             "NBR 16970, DATec, documentação técnica e financiamento bancário."),
            ("/steel-framing/o-que-e-light-steel-framing/",
             "O que é Light Steel Framing",
             "Fundamentos do sistema construtivo, desempenho e industrialização."),
        ]
    ),
    (
        "mercado-de-investimento/airbnb/produto-e-conforto/index.html",
        [
            ("/mercado-de-investimento/financiamento-steel-framing/",
             "Steel Framing para Financiamento CAIXA",
             "NBR 16970, DATec, documentação técnica e financiamento bancário."),
            ("/steel-framing/o-que-e-light-steel-framing/",
             "O que é Light Steel Framing",
             "Fundamentos do sistema construtivo, desempenho e industrialização."),
        ]
    ),
    (
        "mercado-de-investimento/airbnb/operacao-e-manutencao/index.html",
        [
            ("/mercado-de-investimento/financiamento-steel-framing/",
             "Steel Framing para Financiamento CAIXA",
             "NBR 16970, DATec, documentação técnica e financiamento bancário."),
            ("/steel-framing/o-que-e-light-steel-framing/",
             "O que é Light Steel Framing",
             "Fundamentos do sistema construtivo, desempenho e industrialização."),
        ]
    ),
    (
        "mercado-de-investimento/airbnb/viabilidade-economica/index.html",
        [
            ("/mercado-de-investimento/financiamento-steel-framing/",
             "Steel Framing para Financiamento CAIXA",
             "NBR 16970, DATec, documentação técnica e financiamento bancário."),
            ("/steel-framing/o-que-e-light-steel-framing/",
             "O que é Light Steel Framing",
             "Fundamentos do sistema construtivo, desempenho e industrialização."),
        ]
    ),
    (
        "mercado-de-investimento/financiamento-imovel-steel-framing/index.html",
        [
            ("/mercado-de-investimento/airbnb-e-aluguel/",
             "Steel Framing para Airbnb e Aluguel de Temporada",
             "Prazo, escala, produto, operação e viabilidade econômica para empreendimentos de hospedagem."),
            ("/steel-framing/o-que-e-light-steel-framing/",
             "O que é Light Steel Framing",
             "Fundamentos do sistema construtivo, desempenho e industrialização."),
        ]
    ),
    (
        "o-que-e-steel-framing/index.html",
        [
            ("/mercado-de-investimento/financiamento-steel-framing/",
             "Steel Framing para Financiamento CAIXA",
             "Como financiar um imóvel em Steel Framing: NBR 16970, DATec e documentação bancária."),
            ("/mercado-de-investimento/airbnb-e-aluguel/",
             "Steel Framing para Airbnb e Aluguel de Temporada",
             "Prazo, escala, produto e viabilidade econômica para empreendimentos de hospedagem."),
        ]
    ),
]

# Link quebrado a corrigir em o-que-e-steel-framing
LINK_QUEBRADO = {
    "arquivo": "o-que-e-steel-framing/index.html",
    "antigo":  "/mercado-e-investimentos/steel-framing-para-airbnb/",
    "novo":    "/mercado-de-investimento/airbnb-e-aluguel/",
}

counts = {"atualizado": 0, "ja_ok": 0, "nao_encontrado": 0}

# 1. Corrige link quebrado
path_lq = os.path.join(CONTENT, LINK_QUEBRADO["arquivo"])
if os.path.isfile(path_lq):
    with open(path_lq, encoding="utf-8") as f:
        txt = f.read()
    if LINK_QUEBRADO["antigo"] in txt:
        txt = txt.replace(LINK_QUEBRADO["antigo"], LINK_QUEBRADO["novo"])
        with open(path_lq, "w", encoding="utf-8") as f:
            f.write(txt)
        print(f"  🔗 link corrigido: {LINK_QUEBRADO['arquivo']}")
    else:
        print(f"  — link já corrigido ou ausente: {LINK_QUEBRADO['arquivo']}")

# 2. Insere seções de leitura relacionada
for rel_path, links in TAREFAS:
    path = os.path.join(CONTENT, rel_path)
    if not os.path.isfile(path):
        print(f"  ✗ não encontrado: {rel_path}")
        counts["nao_encontrado"] += 1
        continue

    with open(path, encoding="utf-8") as f:
        content = f.read()

    if "leitura-relacionada" in content:
        print(f"  — já tem leitura relacionada: {rel_path}")
        counts["ja_ok"] += 1
        continue

    if ANCHOR not in content:
        print(f"  ? âncora não encontrada: {rel_path}")
        counts["nao_encontrado"] += 1
        continue

    secao = secao_relacionada(links)
    patched = content.replace(ANCHOR, secao + ANCHOR, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(patched)

    print(f"  ✓ atualizado: {rel_path}")
    counts["atualizado"] += 1

print(f"\nResumo: {counts['atualizado']} atualizados · {counts['ja_ok']} já ok · {counts['nao_encontrado']} não encontrados")
