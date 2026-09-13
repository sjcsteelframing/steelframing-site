#!/usr/bin/env python3
"""
Atualiza links para as antigas páginas de paginação do artigo de Airbnb
(p1.html, p2.html, p3.html, p4.html) em todos os HTMLs do site.

Substitui tanto URLs absolutas quanto relativas:
  href="/mercado-de-investimento/airbnb-e-aluguel/p1.html"
    → href="/mercado-de-investimento/airbnb-e-aluguel/prazo-e-escala/"
  href="p1.html"  (links relativos dentro do próprio diretório)
    → href="prazo-e-escala/"

Idempotente — pula arquivos sem ocorrência.
Deve rodar APÓS renomear-paginas-airbnb.py.
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

def build_patterns(mapa):
    pats = []
    for old, new in mapa:
        # URL absoluta: /mercado-de-investimento/airbnb-e-aluguel/p1.html
        abs_old = f"{BASE}/{old}"
        abs_new = f"{BASE}/{new}"
        pats.append((re.compile(re.escape(abs_old)), abs_new))
        # URL relativa dentro do diretório airbnb: href="p1.html"
        pats.append((re.compile(r'(?<=["\'])' + re.escape(old) + r'(?=["\'])'), new))
    return pats

PATTERNS = build_patterns(MAPA)

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

    # Verificação rápida
    if not any(old in content for old, _ in MAPA):
        return "skip"

    patched = content
    for pat, new in PATTERNS:
        patched = pat.sub(new, patched)

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
