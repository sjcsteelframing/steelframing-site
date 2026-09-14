#!/usr/bin/env python3
"""
Atualiza o rodapé das 4 sub-páginas do artigo de Airbnb para o formato atual do site.

Diferença entre as sub-páginas (footer antigo) e as demais páginas do site (footer novo):
  ANTIGO — Ágape aparece só como texto no rodapé inferior:
    <p class="agape-support-note">❤ Apoiamos a <a ...>Associação Ágape</a></p>

  NOVO — Ágape aparece como logo + link na coluna newsletter E o texto do rodapé inferior some:
    <div class="footer-agape">
      <div class="agape-footer-badge"><img src="/images/Agape_logo.png" ... /></div>
      <p>Apoiamos a <a ...>Associação Ágape</a></p>
    </div>

O script faz duas substituições em cada arquivo:
  1. Insere o bloco footer-agape após "Sem spam. Cancele quando quiser."
  2. Remove o <p class="agape-support-note"> do rodapé inferior

Idempotente — pula arquivos que já tenham footer-agape ou sem o padrão antigo.
"""
import os, re

ROOT   = os.path.dirname(__file__)
AIRBNB = os.path.join(ROOT, "public", "content", "mercado-de-investimento", "airbnb")

SUBPAGINAS = [
    "prazo-e-escala",
    "produto-e-conforto",
    "operacao-e-manutencao",
    "viabilidade-economica",
]

# Bloco a inserir (mesmo espaçamento do arquivo-fonte da página LSF)
FOOTER_AGAPE = (
    '\n      <div class="footer-agape">\n'
    '        <div class="agape-footer-badge">'
    '<img src="/images/Agape_logo.png" alt="Associação Ágape" class="agape-footer-logo">'
    '</div>\n'
    '        <p>Apoiamos a <a href="https://agape-sjc.org.br" target="_blank" rel="noopener">'
    'Associação Ágape</a></p>\n'
    '      </div>'
)

# Âncora: insere depois desta string (presente em todos os footers do site)
ANCHOR = '<p class="newsletter-lgpd">Sem spam. Cancele quando quiser.</p>'

# Padrão antigo a remover do rodapé inferior (inclui variações de espaço/nova linha)
AGAPE_NOTE_PAT = re.compile(
    r'\s*<p\s+class="agape-support-note">.*?</p>',
    re.DOTALL | re.IGNORECASE
)

for sub in SUBPAGINAS:
    path = os.path.join(AIRBNB, sub, "index.html")
    if not os.path.isfile(path):
        print(f"  ✗ não encontrado   {sub}/index.html")
        continue

    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Já tem o bloco novo → pula
    if 'footer-agape' in content:
        print(f"  — já atualizado    {sub}/index.html")
        continue

    # Não tem o padrão antigo → informa
    if ANCHOR not in content:
        print(f"  ? âncora não encontrada em   {sub}/index.html")
        continue

    # 1. Insere o bloco footer-agape após a âncora
    patched = content.replace(ANCHOR, ANCHOR + FOOTER_AGAPE, 1)

    # 2. Remove o <p class="agape-support-note"> do rodapé inferior
    patched = AGAPE_NOTE_PAT.sub('', patched)

    with open(path, "w", encoding="utf-8") as f:
        f.write(patched)
    print(f"  ✓ atualizado       {sub}/index.html")

print("\nPronto.")
