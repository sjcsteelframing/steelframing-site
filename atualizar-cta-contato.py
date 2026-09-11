#!/usr/bin/env python3
"""
Substitui o botão CTA "Fale conosco" com mailto: na seção closing-parallax
por href="/contato/" em todos os HTMLs do site.
Idempotente.
"""
import os, re

BASE  = os.path.join(os.path.dirname(__file__), "public", "content")
BUSCA = os.path.join(os.path.dirname(__file__), "public", "busca", "index.html")

# Padrão: qualquer <a ... href="mailto:..."> que contenha "Fale conosco"
MAILTO_CTA = re.compile(
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

    if 'Fale conosco' not in content or 'mailto:' not in content:
        return "skip"

    def replacer(m):
        before = m.group(1)
        after  = m.group(2)
        return f'<a {before}href="/contato/"{after}>Fale conosco</a>'

    new_content = MAILTO_CTA.sub(replacer, content)

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
