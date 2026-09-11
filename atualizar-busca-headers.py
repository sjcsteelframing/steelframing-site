#!/usr/bin/env python3
"""
Substitui o ícone de busca simples (<a class="nav-search-btn">)
pelo form inline com campo de texto em todos os HTMLs do site.
Idempotente: detecta se o form já existe antes de alterar.

Uso: python atualizar-busca-headers.py
"""
import re
import os

BASE = os.path.join(os.path.dirname(__file__), "public", "content")
BUSCA_PAGE = os.path.join(os.path.dirname(__file__), "public", "busca", "index.html")

FORM_HTML = (
    '<form action="/busca/" method="get" class="nav-search-form" role="search">'
    '<input type="search" name="q" class="nav-search-input" placeholder="Buscar…" '
    'aria-label="Buscar no site" autocomplete="off" maxlength="100">'
    '<button type="submit" class="nav-search-btn" aria-label="Buscar">'
    '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>'
    '</svg></button></form>'
)

# Padrão que captura o <a class="nav-search-btn"...>...</a> antigo (uma linha)
OLD_LINK_PATTERN = re.compile(
    r'<a\s[^>]*class="nav-search-btn"[^>]*>.*?</a>',
    re.DOTALL
)

# Fallback: inserir antes de </nav> se ainda não há nada de busca
NAV_CLOSE = '</nav>'

def collect_html_files():
    files = []
    for root, dirs, filenames in os.walk(BASE):
        for fn in filenames:
            if fn.endswith(".html"):
                files.append(os.path.join(root, fn))
    # Inclui a página de busca também (para o form não aparecer nela repetido não é necessário,
    # mas mantemos consistência no header)
    if os.path.isfile(BUSCA_PAGE):
        files.append(BUSCA_PAGE)
    return files

def process(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Já tem o form? Nada a fazer
    if 'class="nav-search-form"' in content:
        return "skip"

    # Tem o link antigo? Substituir
    if 'class="nav-search-btn"' in content and '<a ' in content:
        new_content = OLD_LINK_PATTERN.sub(FORM_HTML, content)
        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return "replaced"

    # Não tem nada: inserir antes de </nav>
    if NAV_CLOSE in content:
        new_content = content.replace(NAV_CLOSE, FORM_HTML + NAV_CLOSE, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return "inserted"

    return "no-nav"

if __name__ == "__main__":
    files = collect_html_files()
    counts = {"replaced": 0, "inserted": 0, "skip": 0, "no-nav": 0}
    for path in files:
        result = process(path)
        counts[result] += 1
        label = {"replaced": "✓ substituído", "inserted": "✓ inserido",
                 "skip": "— já tem form", "no-nav": "⚠ sem </nav>"}.get(result, result)
        rel = os.path.relpath(path, os.path.dirname(__file__))
        print(f"  {label:20s}  {rel}")

    print(f"\nResumo: {counts['replaced']} substituídos · {counts['inserted']} inseridos · "
          f"{counts['skip']} já tinham · {counts['no-nav']} sem nav")
