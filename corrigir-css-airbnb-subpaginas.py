#!/usr/bin/env python3
"""
Corrige o path relativo do CSS nas sub-páginas do artigo de Airbnb.
As páginas foram movidas para subpastas, então:
  css/style.css  →  ../css/style.css
Também corrige outros assets relativos sem barra inicial (images/, js/ etc.)
Idempotente — pula se já usa ../ ou caminho absoluto.
"""
import os, re

ROOT = os.path.dirname(__file__)
AIRBNB = os.path.join(ROOT, "public", "content", "mercado-de-investimento", "airbnb")

SUBPASTAS = [
    "prazo-e-escala",
    "produto-e-conforto",
    "operacao-e-manutencao",
    "viabilidade-economica",
]

# Corrige href/src relativos sem barra inicial e sem ../
# Ex: css/style.css → ../css/style.css
# Não toca em: /caminho/absoluto, https://, ../já-corrigido, #ancora
REL_PAT = re.compile(
    r'((?:href|src)=["\'])(?!(?:https?://|//|/|\.\.?/|#|mailto:))([^"\']+)',
    re.IGNORECASE
)

for sub in SUBPASTAS:
    path = os.path.join(AIRBNB, sub, "index.html")
    if not os.path.isfile(path):
        print(f"  ✗ não encontrado   {sub}/index.html")
        continue

    with open(path, encoding="utf-8") as f:
        content = f.read()

    patched = REL_PAT.sub(r'\1../\2', content)

    if patched == content:
        print(f"  — sem alteração    {sub}/index.html")
        continue

    with open(path, "w", encoding="utf-8") as f:
        f.write(patched)
    print(f"  ✓ corrigido        {sub}/index.html")

print("\nPronto.")
