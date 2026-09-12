#!/usr/bin/env python3
"""
Adiciona links às normas técnicas (ABNT, PBQP-H, ABCEM) em todas as páginas do site.
Deixa claro ao visitante se o acesso é gratuito ou pago (via tooltip + badge).
Idempotente — não duplica links já existentes.
"""
import os

ROOT = os.path.dirname(__file__)

# ─── URLs confirmadas ─────────────────────────────────────────────────────────
URL_NBR16970  = "https://www.abcem.org.br/site/blog/tudo-que-voce-precisa-saber-sobre-a-norma-brasileira-nbr-16970"
URL_NBR14653  = "https://memoria-spu.gestao.gov.br/normas-e-documentos/abnt-nbr-14653-12019-avaliacao-de-bens/"
URL_PBQPH     = "https://pbqp-h.cidades.gov.br/"
URL_SINAT_DOC = "https://pbqp-h.cidades.gov.br/sistemas/sinat/documentos-homologados/"
URL_ABCEM     = "https://www.abcem.org.br/"

# ─── CSS para badges ──────────────────────────────────────────────────────────
# Injetado uma vez no <head> de cada arquivo que for modificado.
BADGE_CSS = (
    '<style id="ref-badge-css">'
    '.ref-tag{display:inline-block;font-size:.68em;padding:1px 6px;border-radius:3px;'
    'margin-left:5px;vertical-align:middle;font-weight:600;letter-spacing:.03em;white-space:nowrap}'
    '.ref-tag-paid{background:#EDF2FB;color:#2E5A8F;border:1px solid #B5CCEC}'
    '.ref-tag-free{background:#EDF7ED;color:#2A6B2A;border:1px solid #A8D5A8}'
    '</style>'
)

def has_badge_css(html):
    return 'ref-badge-css' in html

def inject_css(html):
    """Injeta o CSS antes de </head>."""
    return html.replace('</head>', BADGE_CSS + '\n</head>', 1)

def badge_paid():
    return '<span class="ref-tag ref-tag-paid">norma ABNT — acesso via ABNT Coleção</span>'

def badge_free():
    return '<span class="ref-tag ref-tag-free">acesso gratuito</span>'

def link(url, text, tooltip):
    return (
        f'<a href="{url}" target="_blank" rel="noopener" '
        f'title="{tooltip}">{text}</a>'
    )

# ─── Substituições por arquivo ────────────────────────────────────────────────

def patch_o_que_e(html):
    """o-que-e-steel-framing/index.html"""
    # Heading da seção — adiciona link logo após o título
    old = '<h2>ABNT NBR 16970</h2>\n<p>A ABNT NBR 16970, publicada em 2022'
    new = (
        '<h2>ABNT NBR 16970</h2>\n'
        '<p>A '
        + link(URL_NBR16970, 'ABNT NBR 16970',
               'Resumo da norma pela ABCEM — o documento completo é adquirido via ABNT Coleção (pago)')
        + ', publicada em 2022'
    )
    html = html.replace(old, new)

    # Lista de referências — NBR 16970
    old = '<li>ABNT NBR 16970:2022 — Light Steel Framing.</li>'
    new = (
        '<li>'
        + link(URL_NBR16970, 'ABNT NBR 16970:2022',
               'Resumo da norma pela ABCEM — documento completo disponível via ABNT Coleção (pago)')
        + ' — Light Steel Framing.' + badge_paid() + '</li>'
    )
    html = html.replace(old, new)

    # Lista de referências — ABCEM
    old = '<li>ABCEM — material técnico sobre a NBR 16970.</li>'
    new = (
        '<li>'
        + link(URL_ABCEM, 'ABCEM',
               'Associação Brasileira de Construção Metálica — portal técnico gratuito')
        + ' — material técnico sobre a NBR 16970.' + badge_free() + '</li>'
    )
    html = html.replace(old, new)

    # Lista de referências — PBQP-H / SiNAT
    old = '<li>PBQP-H / SiNAT — documentos técnicos aplicáveis aos sistemas estruturados em perfis leves de aço.</li>'
    new = (
        '<li>'
        + link(URL_PBQPH, 'PBQP-H',
               'Portal oficial do programa — acesso gratuito')
        + ' / '
        + link(URL_SINAT_DOC, 'SiNAT',
               'Documentos técnicos homologados — acesso gratuito')
        + ' — documentos técnicos aplicáveis aos sistemas estruturados em perfis leves de aço.'
        + badge_free() + '</li>'
    )
    html = html.replace(old, new)

    return html


def patch_desempenho(html):
    """o-que-e-steel-framing/desempenho-e-durabilidade/index.html"""
    old = '<li>ABNT NBR 16970:2022 — requisitos de desempenho, projeto estrutural e interfaces.</li>'
    new = (
        '<li>'
        + link(URL_NBR16970, 'ABNT NBR 16970:2022',
               'Resumo da norma pela ABCEM — documento completo disponível via ABNT Coleção (pago)')
        + ' — requisitos de desempenho, projeto estrutural e interfaces.'
        + badge_paid() + '</li>'
    )
    return html.replace(old, new)


def patch_vs_desempenho(html):
    """steelframing-vs-alvenaria/desempenho/index.html (minificado)"""
    # Parágrafo no corpo
    old = 'Documentos do PBQP-H/SiNAT e a série ABNT NBR 16970 tratam o LSF'
    new = (
        'Documentos do '
        + link(URL_PBQPH, 'PBQP-H',
               'Portal oficial do programa — acesso gratuito')
        + '/'
        + link(URL_SINAT_DOC, 'SiNAT',
               'Documentos técnicos homologados — acesso gratuito')
        + ' e a série '
        + link(URL_NBR16970, 'ABNT NBR 16970',
               'Resumo da norma pela ABCEM — documento completo via ABNT Coleção (pago)')
        + ' tratam o LSF'
    )
    html = html.replace(old, new)

    # Referências técnicas (seção refs) — PBQP-H / SiNAT
    old = 'Ministério das Cidades / PBQP-H / SiNAT — avaliação técnica e atendimento à Norma de Desempenho.'
    new = (
        'Ministério das Cidades / '
        + link(URL_PBQPH, 'PBQP-H',
               'Portal oficial do programa — acesso gratuito')
        + ' / '
        + link(URL_SINAT_DOC, 'SiNAT',
               'Documentos técnicos homologados — acesso gratuito')
        + ' — avaliação técnica e atendimento à Norma de Desempenho.'
        + badge_free()
    )
    html = html.replace(old, new)

    # Referências técnicas — NBR 16970:2022
    old = 'Série ABNT NBR 16970:2022 — desempenho, projeto estrutural e interfaces do Light Steel Framing, conforme documentação técnica publicada pelo PBQP-H.'
    new = (
        'Série '
        + link(URL_NBR16970, 'ABNT NBR 16970:2022',
               'Resumo da norma pela ABCEM — documento completo via ABNT Coleção (pago)')
        + ' — desempenho, projeto estrutural e interfaces do Light Steel Framing, conforme documentação técnica publicada pelo PBQP-H.'
        + badge_paid()
    )
    html = html.replace(old, new)

    return html


def patch_caixa(html):
    """financiamento-imovel-steel-framing/caixa/index.html"""
    # Parágrafo principal — NBR 16970:2022 bold
    old = '<strong>ABNT NBR 16970:2022 — Light Steel Framing</strong>'
    new = (
        '<strong>'
        + link(URL_NBR16970, 'ABNT NBR 16970:2022 — Light Steel Framing',
               'Resumo da norma pela ABCEM — documento completo via ABNT Coleção (pago)')
        + '</strong>'
    )
    html = html.replace(old, new)

    # Menção a SiNAT e DATec no corpo
    old = 'que podem depender da sistemática do SiNAT e de DATec.'
    new = (
        'que podem depender da sistemática do '
        + link(URL_SINAT_DOC, 'SiNAT',
               'Sistema Nacional de Avaliação Técnica — portal PBQP-H, acesso gratuito')
        + ' e de '
        + link(URL_SINAT_DOC, 'DATec',
               'Documentos de Avaliação Técnica — lista de documentos homologados, acesso gratuito')
        + '.'
    )
    html = html.replace(old, new)

    # Menção a NBR 16970-1 no corpo
    old = 'A ABNT NBR 16970-1 se destina a edificações residenciais'
    new = (
        'A '
        + link(URL_NBR16970, 'ABNT NBR 16970-1',
               'Resumo da norma pela ABCEM — documento completo via ABNT Coleção (pago)')
        + ' se destina a edificações residenciais'
    )
    html = html.replace(old, new)

    # Lista de referências — PBQP-H / SiNAT
    old = '<li>Ministério das Cidades / PBQP-H — SiNAT.</li>'
    new = (
        '<li>Ministério das Cidades / '
        + link(URL_PBQPH, 'PBQP-H',
               'Portal oficial do programa — acesso gratuito')
        + ' — '
        + link(URL_SINAT_DOC, 'SiNAT',
               'Documentos técnicos homologados — acesso gratuito')
        + '.' + badge_free() + '</li>'
    )
    html = html.replace(old, new)

    # Lista de referências — NBR 16970-1:2022
    old = '<li>ABNT NBR 16970-1:2022.</li>'
    new = (
        '<li>'
        + link(URL_NBR16970, 'ABNT NBR 16970-1:2022',
               'Resumo da norma pela ABCEM — documento completo via ABNT Coleção (pago)')
        + '.' + badge_paid() + '</li>'
    )
    html = html.replace(old, new)

    return html


def patch_avaliacao(html):
    """financiamento-imovel-steel-framing/avaliacao-bancaria/index.html"""
    # Parágrafo — NBR 14653 bold
    old = '<strong>ABNT NBR 14653</strong>'
    new = (
        '<strong>'
        + link(URL_NBR14653, 'ABNT NBR 14653',
               'Ficha da norma no repositório do governo federal (SPU) — acesso gratuito, inclui PDF')
        + '</strong>'
    )
    html = html.replace(old, new)

    # Lista de referências — NBR 14653
    old = '<li>ABNT NBR 14653 — Avaliação de bens.</li>'
    new = (
        '<li>'
        + link(URL_NBR14653, 'ABNT NBR 14653',
               'Ficha da norma no repositório do governo federal — acesso gratuito, inclui PDF')
        + ' — Avaliação de bens.' + badge_free() + '</li>'
    )
    html = html.replace(old, new)

    return html


# ─── Executor ─────────────────────────────────────────────────────────────────

FILES = {
    "public/content/o-que-e-steel-framing/index.html":
        patch_o_que_e,
    "public/content/o-que-e-steel-framing/desempenho-e-durabilidade/index.html":
        patch_desempenho,
    "public/content/steelframing-vs-alvenaria/desempenho/index.html":
        patch_vs_desempenho,
    "public/content/mercado-de-investimento/financiamento-imovel-steel-framing/caixa/index.html":
        patch_caixa,
    "public/content/mercado-de-investimento/financiamento-imovel-steel-framing/avaliacao-bancaria/index.html":
        patch_avaliacao,
}

for rel_path, patch_fn in FILES.items():
    path = os.path.join(ROOT, rel_path)
    if not os.path.isfile(path):
        print(f"  ✗ não encontrado   {rel_path}")
        continue

    with open(path, encoding="utf-8") as f:
        original = f.read()

    # Pula se já foi processado (qualquer link das URLs alvo já está lá)
    if URL_NBR16970 in original or URL_NBR14653 in original or URL_SINAT_DOC in original:
        print(f"  — já processado    {rel_path}")
        continue

    patched = patch_fn(original)

    if patched == original:
        print(f"  ⚠ sem match        {rel_path}")
        continue

    # Injeta CSS de badges se ainda não estiver no arquivo
    if not has_badge_css(patched):
        patched = inject_css(patched)

    with open(path, "w", encoding="utf-8") as f:
        f.write(patched)

    print(f"  ✓ atualizado       {rel_path}")

print("\nPronto. Verifique visualmente uma página antes do git push.")
