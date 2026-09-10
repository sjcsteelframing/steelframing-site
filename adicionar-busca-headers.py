"""
Adiciona ícone de busca ao nav de todos os HTMLs do site.
Executa uma única vez; idempotente (não adiciona 2x).
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(ROOT, "public")

HTML_FILES = [
    "content/index.html",
    "content/o-que-e-steel-framing/index.html",
    "content/o-que-e-steel-framing/como-funciona/index.html",
    "content/o-que-e-steel-framing/desempenho-e-durabilidade/index.html",
    "content/o-que-e-steel-framing/projeto-e-industrializacao/index.html",
    "content/steelframing-vs-alvenaria/index.html",
    "content/steelframing-vs-alvenaria/custo/index.html",
    "content/steelframing-vs-alvenaria/desempenho/index.html",
    "content/steelframing-vs-alvenaria/fundacoes/index.html",
    "content/steelframing-vs-alvenaria/mao-de-obra/index.html",
    "content/steelframing-vs-alvenaria/prazo/index.html",
    "content/mercado-de-investimento/airbnb/index.html",
    "content/mercado-de-investimento/financiamento-imovel-steel-framing/index.html",
    "content/mercado-de-investimento/financiamento-imovel-steel-framing/avaliacao-bancaria/index.html",
    "content/mercado-de-investimento/financiamento-imovel-steel-framing/caixa/index.html",
    "content/mercado-de-investimento/financiamento-imovel-steel-framing/capital-proprio-ou-financiamento/index.html",
    "content/sobre/index.html",
]

SEARCH_LINK = (
    '<a href="/busca/" class="nav-search-btn" aria-label="Buscar no site" title="Buscar">'
    '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>'
    '</svg></a>'
)

updated = 0
for rel in HTML_FILES:
    path = os.path.join(PUBLIC, rel)
    if not os.path.exists(path):
        print(f"  SKIP: {rel}")
        continue
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if 'nav-search-btn' in html:
        print(f"  JÁ TEM: {rel}")
        continue
    # insere antes de </nav>
    new_html = html.replace("</nav>", SEARCH_LINK + "</nav>", 1)
    if new_html == html:
        print(f"  SEM </nav>: {rel}")
        continue
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"  ✓ {rel}")
    updated += 1

print(f"\n{updated} arquivo(s) atualizado(s)")
