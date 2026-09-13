#!/usr/bin/env python3
"""
Adiciona tag <link rel="canonical"> self-referencing nas páginas de
paginação do artigo de Airbnb (p1.html, p2.html, p4.html).

Idempotente — pula arquivos que já têm canonical.
"""
import os, re

BASE = os.path.join(os.path.dirname(__file__), "public")
DOMAIN = "https://www.steelframing.com.br"

PAGES = [
    "mercado-de-investimento/airbnb-e-aluguel/p1.html",
    "mercado-de-investimento/airbnb-e-aluguel/p2.html",
    "mercado-de-investimento/airbnb-e-aluguel/p4.html",
]

# Insere o canonical logo após o <meta charset> (sempre presente e sempre primeiro)
CHARSET_PAT = re.compile(r'(<meta\s+charset=[^>]+>)', re.IGNORECASE)

for rel in PAGES:
    path = os.path.join(BASE, rel)
    if not os.path.isfile(path):
        print(f"  ✗ não encontrado   {rel}")
        continue

    with open(path, encoding="utf-8") as f:
        html = f.read()

    if 'rel="canonical"' in html:
        print(f"  — já tem canonical  {rel}")
        continue

    canonical_url = f"{DOMAIN}/{rel.replace(os.sep, '/')}"
    tag = f'<link rel="canonical" href="{canonical_url}">'

    patched = CHARSET_PAT.sub(r'\1\n  ' + tag, html, count=1)

    if patched == html:
        print(f"  ⚠ sem match charset  {rel}")
        continue

    with open(path, "w", encoding="utf-8") as f:
        f.write(patched)
    print(f"  ✓ canonical inserido  {rel}")
    print(f"              → {canonical_url}")

print("\nPronto.")
