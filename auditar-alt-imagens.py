#!/usr/bin/env python3
"""
Audita imagens sem atributo alt em todas as páginas HTML do site.
Gera um relatório e depois aplica correções automaticamente.

Distingue:
  - FALTA alt: precisa ser adicionado (problema real de SEO/acessibilidade)
  - alt="": decorativo, correto — não altera
"""
import os, re, json

ROOT   = os.path.dirname(__file__)
PUBLIC = os.path.join(ROOT, "public")

# Encontra <img> com e sem alt
IMG_PAT = re.compile(r'<img\b([^>]*)>', re.IGNORECASE | re.DOTALL)
ALT_PAT = re.compile(r'\balt\s*=', re.IGNORECASE)
SRC_PAT = re.compile(r'\bsrc\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)

def collect_html():
    files = []
    for root, _, fns in os.walk(PUBLIC):
        for fn in fns:
            if fn.endswith(".html"):
                files.append(os.path.join(root, fn))
    return sorted(files)

sem_alt = []  # lista de (arquivo_relativo, src, trecho_img)

for path in collect_html():
    with open(path, encoding="utf-8") as f:
        content = f.read()
    rel = os.path.relpath(path, ROOT)
    for m in IMG_PAT.finditer(content):
        attrs = m.group(1)
        if not ALT_PAT.search(attrs):
            src_m = SRC_PAT.search(attrs)
            src = src_m.group(1) if src_m else "(sem src)"
            sem_alt.append({"arquivo": rel, "src": src, "tag": m.group(0)[:120]})

# --- Relatório ---
print(f"\n{'='*60}")
print(f"  IMAGENS SEM ATRIBUTO alt  ({len(sem_alt)} encontradas)")
print(f"{'='*60}\n")

por_arquivo = {}
for item in sem_alt:
    por_arquivo.setdefault(item["arquivo"], []).append(item["src"])

for arq, srcs in sorted(por_arquivo.items()):
    print(f"  {arq}")
    for s in srcs:
        print(f"    ↳ {s}")
    print()

# Salva JSON para o script de correção
json_path = os.path.join(os.path.dirname(__file__), "_sem_alt.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(sem_alt, f, ensure_ascii=False, indent=2)
print(f"Relatório JSON salvo em: {json_path}")
print("Execute corrigir-alt-imagens.py após revisar.\n")
