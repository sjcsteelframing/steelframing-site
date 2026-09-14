#!/usr/bin/env python3
"""
Atualiza o rodapé de TODOS os HTMLs do site que ainda usam o formato antigo da Ágape.

Footer antigo (a remover):
  <p class="agape-support-note">❤ Apoiamos a <a ...>Associação Ágape</a></p>
  — aparece no rodapé inferior, sem logo

Footer novo (a inserir na coluna newsletter):
  <div class="footer-agape">
    <div class="agape-footer-badge"><img src="/images/Agape_logo.png" ... /></div>
    <p>Apoiamos a <a ...>Associação Ágape</a></p>
  </div>

Idempotente — pula arquivos que já tenham footer-agape ou sem o padrão antigo.
"""
import os, re

ROOT = os.path.dirname(__file__)

FOOTER_AGAPE = (
    '\n      <div class="footer-agape">\n'
    '        <div class="agape-footer-badge">'
    '<img src="/images/Agape_logo.png" alt="Associação Ágape" class="agape-footer-logo">'
    '</div>\n'
    '        <p>Apoiamos a <a href="https://agape-sjc.org.br" target="_blank" rel="noopener">'
    'Associação Ágape</a></p>\n'
    '      </div>'
)

ANCHOR = '<p class="newsletter-lgpd">Sem spam. Cancele quando quiser.</p>'

AGAPE_NOTE_PAT = re.compile(
    r'\s*<p\s+class="agape-support-note">.*?</p>',
    re.DOTALL | re.IGNORECASE
)

def collect_html_files():
    files = []
    for root, dirs, filenames in os.walk(os.path.join(ROOT, "public")):
        for fn in filenames:
            if fn.endswith(".html"):
                files.append(os.path.join(root, fn))
    return files

counts = {"atualizado": 0, "ja_ok": 0, "sem_padrao": 0}

for path in collect_html_files():
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Já tem o bloco novo → pula
    if 'footer-agape' in content:
        counts["ja_ok"] += 1
        continue

    # Não tem o padrão antigo de Ágape → página sem rodapé completo, ignora
    if 'agape-support-note' not in content:
        counts["sem_padrao"] += 1
        continue

    # Não tem a âncora da newsletter → footer diferente, ignora
    if ANCHOR not in content:
        counts["sem_padrao"] += 1
        continue

    patched = content.replace(ANCHOR, ANCHOR + FOOTER_AGAPE, 1)
    patched = AGAPE_NOTE_PAT.sub('', patched)

    with open(path, "w", encoding="utf-8") as f:
        f.write(patched)

    rel = os.path.relpath(path, ROOT)
    print(f"  ✓ atualizado   {rel}")
    counts["atualizado"] += 1

print(f"\nResumo: {counts['atualizado']} atualizados · {counts['ja_ok']} já ok · {counts['sem_padrao']} sem padrão")
