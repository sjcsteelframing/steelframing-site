#!/usr/bin/env python3
"""
Remove "/index.html" do final de hrefs internos em todos os HTMLs do site.
  href="/steel-framing/.../como-funciona/index.html"
  →  href="/steel-framing/.../como-funciona/"

Também limpa src= e action= se usarem /index.html.
Idempotente — não toca em arquivos sem a ocorrência.
NÃO altera URLs externas (http:// / https://).
"""
import os, re

ROOT = os.path.dirname(__file__)
BASE  = os.path.join(ROOT, "public")

# Match: href="/qualquer/coisa/index.html" (só paths internos, sem http)
# Captura: (atributo)(valor antes de index.html)(aspas fechando)
PATTERN = re.compile(
    r'((?:href|src|action)=")(/[^"]*?)index\.html(")',
    re.IGNORECASE
)

def collect_html_files():
    files = []
    for root, dirs, filenames in os.walk(BASE):
        for fn in filenames:
            if fn.endswith(".html"):
                files.append(os.path.join(root, fn))
    return files

def process(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    if 'index.html' not in content:
        return "skip"

    patched = PATTERN.sub(r'\1\2\3', content)  # remove "index.html", mantém barra

    if patched == content:
        return "no-match"

    with open(path, "w", encoding="utf-8") as f:
        f.write(patched)
    return "updated"

if __name__ == "__main__":
    files = collect_html_files()
    counts = {"updated": 0, "skip": 0, "no-match": 0}
    for path in files:
        result = process(path)
        counts[result] += 1
        label = {"updated": "✓ atualizado", "skip": "— sem alteração", "no-match": "⚠ sem match"}.get(result, result)
        rel = os.path.relpath(path, ROOT)
        print(f"  {label:22s}  {rel}")

    print(f"\nResumo: {counts['updated']} atualizados · {counts['skip']} sem alteração · {counts['no-match']} sem match")
