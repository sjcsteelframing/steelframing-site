#!/usr/bin/env python3
"""
Substitui href="mailto:pedro@steelframing.com.br">Contato
por href="/contato/">Contato em todos os HTMLs do site.
Também atualiza links de footer que ainda apontem para mailto.
Idempotente.
"""
import os, re

BASE = os.path.join(os.path.dirname(__file__), "public", "content")
BUSCA_PAGE = os.path.join(os.path.dirname(__file__), "public", "busca", "index.html")

# Nav: <a href="mailto:...">Contato</a>  →  <a href="/contato/">Contato</a>
MAILTO_NAV = re.compile(
    r'<a\s+href="mailto:[^"]*"\s*>Contato</a>',
    re.IGNORECASE
)
NAV_REPLACEMENT = '<a href="/contato/">Contato</a>'

# Footer: mesma coisa
MAILTO_FOOTER = re.compile(
    r'<a\s+href="mailto:[^"]*"\s*>Contato</a>',
    re.IGNORECASE
)

def collect_html_files():
    files = []
    for root, dirs, filenames in os.walk(BASE):
        for fn in filenames:
            if fn.endswith(".html"):
                files.append(os.path.join(root, fn))
    if os.path.isfile(BUSCA_PAGE):
        files.append(BUSCA_PAGE)
    return files

def process(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Já tem /contato/ no lugar certo? (não é a própria página de contato)
    if 'href="/contato/">Contato</a>' in content and 'href="mailto:' not in content:
        return "skip"

    if 'href="mailto:' not in content:
        return "skip"

    new_content = MAILTO_NAV.sub(NAV_REPLACEMENT, content)
    if new_content == content:
        return "no-match"

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return "updated"

if __name__ == "__main__":
    files = collect_html_files()
    counts = {"updated": 0, "skip": 0, "no-match": 0}
    for path in files:
        result = process(path)
        counts[result] += 1
        label = {"updated": "✓ atualizado", "skip": "— sem alteração", "no-match": "⚠ sem match"}.get(result, result)
        rel = os.path.relpath(path, os.path.dirname(__file__))
        print(f"  {label:22s}  {rel}")

    print(f"\nResumo: {counts['updated']} atualizados · {counts['skip']} sem alteração · {counts['no-match']} sem match")
