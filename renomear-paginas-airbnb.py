#!/usr/bin/env python3
"""
Converte as páginas de paginação p1-p4 do artigo de Airbnb
para URLs descritivas no padrão do site.

Antes: public/content/mercado-de-investimento/airbnb/p1.html
Depois: public/content/mercado-de-investimento/airbnb/prazo-e-escala/index.html

O que faz:
  1. Cria a nova pasta e escreve index.html com canonical self-referencing corrigido
  2. Atualiza links internos entre as sub-páginas (nav próxima/anterior)
  3. Remove o arquivo p*.html antigo (o redirect 301 no vercel.json cobre a URL velha)

Idempotente — pula se a pasta de destino já existe.
"""
import os, re, shutil

ROOT   = os.path.dirname(__file__)
AIRBNB = os.path.join(ROOT, "public", "content", "mercado-de-investimento", "airbnb")
DOMAIN = "https://www.steelframing.com.br"
BASE   = "/mercado-de-investimento/airbnb-e-aluguel"

PAGES = [
    {"old": "p1.html", "new": "prazo-e-escala"},
    {"old": "p2.html", "new": "produto-e-conforto"},
    {"old": "p3.html", "new": "operacao-e-manutencao"},
    {"old": "p4.html", "new": "viabilidade-economica"},
]

# Mapa de substituição de links internos (href antigo → href novo)
LINK_MAP = {f'{BASE}/{p["old"]}': f'{BASE}/{p["new"]}/' for p in PAGES}
# Também cobre hrefs relativos (ex: href="p2.html")
LINK_MAP_REL = {p["old"]: f'{p["new"]}/' for p in PAGES}

CANONICAL_PAT = re.compile(r'<link\s+rel="canonical"\s+href="[^"]*"[^>]*>', re.IGNORECASE)
CHARSET_PAT   = re.compile(r'(<meta\s+charset=[^>]+>)', re.IGNORECASE)

def fix_links(html):
    """Substitui referências a p*.html por novas URLs."""
    for old, new in LINK_MAP.items():
        html = html.replace(f'href="{old}"', f'href="{new}"')
        html = html.replace(f'href="{old}#', f'href="{new}#')
    for old, new in LINK_MAP_REL.items():
        html = html.replace(f'href="{old}"', f'href="{new}"')
        html = html.replace(f'href="{old}#', f'href="{new}#')
    return html

def set_canonical(html, url):
    tag = f'<link rel="canonical" href="{url}">'
    if CANONICAL_PAT.search(html):
        return CANONICAL_PAT.sub(tag, html)
    # Insere após charset se não existir
    return CHARSET_PAT.sub(r'\1\n  ' + tag, html, count=1)

for p in PAGES:
    src  = os.path.join(AIRBNB, p["old"])
    dest_dir  = os.path.join(AIRBNB, p["new"])
    dest_file = os.path.join(dest_dir, "index.html")
    canon_url = f'{DOMAIN}{BASE}/{p["new"]}/'

    if not os.path.isfile(src):
        print(f"  ✗ não encontrado   {p['old']}")
        continue

    if os.path.isdir(dest_dir):
        print(f"  — já existe        {p['new']}/")
        # Ainda remove o .html antigo se sobrou
        if os.path.isfile(src):
            os.remove(src)
            print(f"    ✓ removido       {p['old']}")
        continue

    with open(src, encoding="utf-8") as f:
        html = f.read()

    html = fix_links(html)
    html = set_canonical(html, canon_url)

    os.makedirs(dest_dir)
    with open(dest_file, "w", encoding="utf-8") as f:
        f.write(html)

    os.remove(src)

    print(f"  ✓ {p['old']:12s}  →  {p['new']}/index.html")
    print(f"    canonical: {canon_url}")

print("\nPronto.")
