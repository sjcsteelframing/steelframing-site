#!/usr/bin/env python3
"""
Substitui qualquer <a class="btn-primary" href="mailto:..."> na seção
closing-parallax por href="/contato/" — preserva o texto original do link.
Também cobre o padrão antigo "Fale conosco" caso ainda exista.
Idempotente — pula arquivos sem mailto: em btn-primary.
"""
import os, re

BASE  = os.path.join(os.path.dirname(__file__), "public", "content")
BUSCA = os.path.join(os.path.dirname(__file__), "public", "busca", "index.html")

# Padrão 1: btn-primary com mailto (qualquer texto)
# Ex: <a class="btn-primary" href="mailto:...">Fale com a gente →</a>
BTN_PRIMARY = re.compile(
    r'(<a\s+[^>]*?class="btn-primary"[^>]*?)href="mailto:[^"]*"([^>]*>)',
    re.IGNORECASE | re.DOTALL
)

# Padrão 2 (legado): texto "Fale conosco" com mailto (qualquer classe)
FALE_CONOSCO = re.compile(
    r'<a\s+([^>]*?)href="mailto:[^"]*"([^>]*)>\s*Fale conosco\s*</a>',
    re.IGNORECASE | re.DOTALL
)

def collect_html_files():
    files = []
    for root, dirs, filenames in os.walk(BASE):
        for fn in filenames:
            if fn.endswith(".html"):
                files.append(os.path.join(root, fn))
    if os.path.isfile(BUSCA):
        files.append(BUSCA)
    return files

def process(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    if 'mailto:' not in content:
        return "skip"

    # Padrão 1: btn-primary mailto
    new_content = BTN_PRIMARY.sub(
        lambda m: m.group(1) + 'href="/contato/"' + m.group(2),
        content
    )

    # Padrão 2: "Fale conosco" mailto (legado)
    new_content = FALE_CONOSCO.sub(
        lambda m: f'<a {m.group(1)}href="/contato/"{m.group(2)}>Fale conosco</a>',
        new_content
    )

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
        label = {
            "updated":  "✓ atualizado",
            "skip":     "— sem alteração",
            "no-match": "⚠ sem match"
        }.get(result, result)
        rel = os.path.relpath(path, os.path.dirname(__file__))
        print(f"  {label:22s}  {rel}")

    print(f"\nResumo: {counts['updated']} atualizados · {counts['skip']} sem alteração · {counts['no-match']} sem match")
