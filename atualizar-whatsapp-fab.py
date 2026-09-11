#!/usr/bin/env python3
"""
Atualiza todos os botões FAB do WhatsApp no site:
- Corrige o número para 5512991856900
- Adiciona mensagem pré-preenchida para identificar contatos vindos do site
Idempotente.
"""
import os, re
from urllib.parse import quote

BASE     = os.path.join(os.path.dirname(__file__), "public", "content")
BUSCA    = os.path.join(os.path.dirname(__file__), "public", "busca", "index.html")

WA_NUMBER = "5512991856900"
WA_MSG    = "Olá! Vim pelo site steelframing.com.br e gostaria de falar sobre Steel Framing."
NEW_URL   = f"https://wa.me/{WA_NUMBER}?text={quote(WA_MSG)}"

# Captura o href atual dentro de qualquer <a ... class="fab fab-whatsapp" ...>
FAB_ANCHOR = re.compile(
    r'(<a\b[^>]*\bfab-whatsapp\b[^>]*>)',
    re.DOTALL
)
HREF_ATTR = re.compile(r'\bhref="([^"]*)"')


def fix_fab_href(tag_html):
    """Substitui o href dentro da tag de abertura do FAB."""
    if f'href="{NEW_URL}"' in tag_html:
        return tag_html, False   # já está correto
    new_tag = HREF_ATTR.sub(f'href="{NEW_URL}"', tag_html)
    return new_tag, new_tag != tag_html


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

    if "fab-whatsapp" not in content:
        return "skip"

    changed = False
    def replacer(m):
        nonlocal changed
        new_tag, did_change = fix_fab_href(m.group(1))
        if did_change:
            changed = True
        return new_tag

    new_content = FAB_ANCHOR.sub(replacer, content)

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return "updated"
    return "skip"


if __name__ == "__main__":
    print(f"URL destino: {NEW_URL}\n")
    files = collect_html_files()
    counts = {"updated": 0, "skip": 0}
    for path in files:
        result = process(path)
        counts[result] += 1
        label = {"updated": "✓ atualizado", "skip": "— sem alteração"}.get(result, result)
        rel = os.path.relpath(path, os.path.dirname(__file__))
        print(f"  {label:20s}  {rel}")

    print(f"\nResumo: {counts['updated']} atualizados · {counts['skip']} sem alteração")
