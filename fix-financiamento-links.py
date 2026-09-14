#!/usr/bin/env python3
"""
Adiciona seção 'Leitura relacionada' na página de Financiamento,
que usa estrutura diferente (sem closing-parallax).
Insere antes de </article></main>.
"""
import os

ROOT    = os.path.dirname(__file__)
PATH    = os.path.join(ROOT, "public", "content",
          "mercado-de-investimento", "financiamento-imovel-steel-framing", "index.html")
ANCHOR  = '</article></main>'
MARKER  = 'leitura-relacionada-financiamento'

SECAO = (
'\n<section>\n'
'<div class="section-kicker">Leitura relacionada</div>\n'
'<h2>Continue explorando</h2>\n'
'<div class="related leitura-relacionada-financiamento">\n'
'<div class="card">\n'
'<h3>Steel Framing para Airbnb e Aluguel de Temporada</h3>\n'
'<p>Prazo, escala, produto, operação e viabilidade econômica para empreendimentos de hospedagem.</p>\n'
'<a href="/mercado-de-investimento/airbnb-e-aluguel/">Ver análise →</a>\n'
'</div>\n'
'<div class="card">\n'
'<h3>O que é Light Steel Framing</h3>\n'
'<p>Fundamentos do sistema construtivo, desempenho estrutural e processo industrializado.</p>\n'
'<a href="/steel-framing/o-que-e-light-steel-framing/">Ver conteúdo →</a>\n'
'</div>\n'
'</div>\n'
'</section>\n'
)

with open(PATH, encoding="utf-8") as f:
    content = f.read()

if MARKER in content:
    print("  — já tem leitura relacionada, nada a fazer.")
elif ANCHOR not in content:
    print("  ✗ âncora não encontrada.")
else:
    patched = content.replace(ANCHOR, SECAO + ANCHOR, 1)
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(patched)
    print("  ✓ leitura relacionada adicionada na página de Financiamento.")
