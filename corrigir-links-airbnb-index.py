#!/usr/bin/env python3
"""
Corrige os links p1-p4 na página principal do artigo de Airbnb
e em qualquer outro HTML do site que ainda referencie essas URLs.

Cobre tanto hrefs relativos (p1.html) quanto absolutos
(/mercado-de-investimento/airbnb-e-aluguel/p1.html).
"""
import os, re

ROOT = os.path.dirname(__file__)
BASE = "/mercado-de-investimento/airbnb-e-aluguel"

MAPA = [
    ("p1.html", "prazo-e-escala/"),
    ("p2.html", "produto-e-conforto/"),
    ("p3.html", "operacao-e-manutencao/"),
    ("p4.html", "viabilidade-economica/"),
]

# Substitui href="p1.html" e href="/mercado-.../p1.html"
def build_pattern(old, new, base):
    abs_old = re.escape(f"{base}/{old}")
    rel_old = re.escape(old)
    # Captura href=" ou href=' antes, e " ou ' depois
    return re.compile(
        r'(href=["\'])(?:' + abs_old + r'|' + rel_old + r')(["\'])',
        re.IGNORECASE
    ), r'\g<1>' + new + r'\g<2>'

PATTERNS = [build_pattern(old, new, BASE) for old, new in MAPA]

def collect_html_files():
    files = []
    for root, dirs, filenames in os.walk(os.path.join(ROOT, "public")):
        for fn in filenames:
            if fn.endswith(".html"):
                files.append(os.path.join(root, fn))
    return files

def process(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    if not any(old in content for old, _ in MAPA):
        return "skip"

    patched = content
    for pat, repl in PATTERNS:
        patched = pat.sub(repl, patched)

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
        if result == "updated":
            rel = os.path.relpath(path, ROOT)
            print(f"  ✓ atualizado   {rel}")

    print(f"\nResumo: {counts['updated']} atualizados · {counts['skip']} sem ocorrência · {counts['no-match']} sem match")
