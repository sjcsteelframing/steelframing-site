#!/usr/bin/env python3
"""
Corrige links da ABNT NBR 16970 que apontam para a ABCEM mas usam
"ABNT NBR 16970" como texto-âncora — induzia o visitante a esperar o site da ABNT.

Novo formato:
  ABNT NBR 16970:2022 — <a href="...ABCEM...">resumo gratuito · ABCEM ↗</a>

Idempotente — detecta marker "resumo gratuito · ABCEM" antes de alterar.
"""
import os, re

ROOT = os.path.dirname(__file__)

URL_NBR16970 = (
    "https://www.abcem.org.br/site/blog/"
    "tudo-que-voce-precisa-saber-sobre-a-norma-brasileira-nbr-16970"
)

# Match: <a href="URL_ABCEM" ...atributos...>ABNT NBR 16970{qualquer coisa}</a>
LINK_PAT = re.compile(
    r'<a\s+href="' + re.escape(URL_NBR16970) + r'"([^>]*)>'
    r'(ABNT NBR 16970[^<]*?)'
    r'</a>',
    re.DOTALL
)

MARKER = "resumo gratuito · ABCEM"  # prova de que o arquivo já foi corrigido

def replacer(m):
    attrs    = m.group(1).strip()  # atributos originais do <a>
    normname = m.group(2).strip()  # ex: "ABNT NBR 16970:2022"
    return (
        f'{normname} — '
        f'<a href="{URL_NBR16970}" {attrs}>'
        f'resumo gratuito · ABCEM ↗</a>'
    )

FILES = [
    "public/content/o-que-e-steel-framing/index.html",
    "public/content/o-que-e-steel-framing/desempenho-e-durabilidade/index.html",
    "public/content/steelframing-vs-alvenaria/desempenho/index.html",
    "public/content/mercado-de-investimento/financiamento-imovel-steel-framing/caixa/index.html",
]

for rel_path in FILES:
    path = os.path.join(ROOT, rel_path)
    if not os.path.isfile(path):
        print(f"  ✗ não encontrado   {rel_path}")
        continue

    with open(path, encoding="utf-8") as f:
        html = f.read()

    if MARKER in html:
        print(f"  — já corrigido     {rel_path}")
        continue

    patched = LINK_PAT.sub(replacer, html)

    if patched == html:
        print(f"  ⚠ sem match        {rel_path}")
        continue

    with open(path, "w", encoding="utf-8") as f:
        f.write(patched)
    print(f"  ✓ corrigido        {rel_path}")

print("\nPronto.")
