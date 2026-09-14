#!/usr/bin/env python3
"""
Adiciona Open Graph tags + JSON-LD (Article + BreadcrumbList) nas 4 sub-páginas do Airbnb.
Idempotente — pula arquivos que já tenham og:title ou ld+json.
"""
import os, re

ROOT   = os.path.dirname(__file__)
AIRBNB = os.path.join(ROOT, "public", "content", "mercado-de-investimento", "airbnb")

PAGES = [
    {
        "slug": "prazo-e-escala",
        "title": "Prazo, escala e implantação | Steel Framing para Airbnb",
        "desc": "Como o Steel Framing pode influenciar prazo, escala, repetição de unidades e implantação em fases em empreendimentos de aluguel por temporada.",
        "h1": "Prazo, escala e implantação",
        "image": "https://www.steelframing.com.br/images/mercado-de-investimento/airbnb/i02.png",
        "date": "2025-09-01",
    },
    {
        "slug": "produto-e-conforto",
        "title": "Produto, conforto e experiência | Steel Framing para Airbnb",
        "desc": "Produto, tipologia, conforto térmico e acústico, experiência do hóspede e posicionamento em empreendimentos de hospedagem com Steel Framing.",
        "h1": "Produto, conforto e experiência",
        "image": "https://www.steelframing.com.br/images/mercado-de-investimento/airbnb/i02.png",
        "date": "2025-09-01",
    },
    {
        "slug": "operacao-e-manutencao",
        "title": "Operação e manutenção | Steel Framing para Airbnb",
        "desc": "Operação, manutenção, automação e disponibilidade do imóvel: como o sistema construtivo pode afetar a gestão de um Airbnb.",
        "h1": "Operação e manutenção",
        "image": "https://www.steelframing.com.br/images/mercado-de-investimento/airbnb/i02.png",
        "date": "2025-09-01",
    },
    {
        "slug": "viabilidade-economica",
        "title": "Viabilidade econômica e decisão | Steel Framing para Airbnb",
        "desc": "CAPEX, OPEX, prazo de retorno e cenários de viabilidade econômica para empreendimentos de aluguel por temporada em Steel Framing.",
        "h1": "Viabilidade econômica e decisão",
        "image": "https://www.steelframing.com.br/images/mercado-de-investimento/airbnb/i02.png",
        "date": "2025-09-01",
    },
]

def build_seo_block(p):
    url = f"https://www.steelframing.com.br/mercado-de-investimento/airbnb-e-aluguel/{p['slug']}/"
    og = f"""<!-- Open Graph -->
<meta property="og:type" content="article"/>
<meta property="og:title" content="{p['title']}"/>
<meta property="og:description" content="{p['desc']}"/>
<meta property="og:url" content="{url}"/>
<meta property="og:image" content="{p['image']}"/>
<meta property="og:site_name" content="Steel Framing"/>
<!-- JSON-LD -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Article",
      "headline": "{p['h1']}",
      "description": "{p['desc']}",
      "url": "{url}",
      "datePublished": "{p['date']}",
      "dateModified": "{p['date']}",
      "author": {{
        "@type": "Person",
        "name": "Pedro Gomes",
        "url": "https://www.steelframing.com.br/sobre/"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Steel Framing",
        "url": "https://www.steelframing.com.br",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://www.steelframing.com.br/images/home/logo-steel-framing.png"
        }}
      }},
      "image": "{p['image']}",
      "mainEntityOfPage": "{url}"
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type":"ListItem","position":1,"name":"Home","item":"https://www.steelframing.com.br/"}},
        {{"@type":"ListItem","position":2,"name":"Mercado de Investimento","item":"https://www.steelframing.com.br/mercado-de-investimento/airbnb-e-aluguel/"}},
        {{"@type":"ListItem","position":3,"name":"Steel Framing para Airbnb","item":"https://www.steelframing.com.br/mercado-de-investimento/airbnb-e-aluguel/"}},
        {{"@type":"ListItem","position":4,"name":"{p['h1']}","item":"{url}"}}
      ]
    }}
  ]
}}
</script>"""
    return og

ANCHOR = '</head>'

for p in PAGES:
    path = os.path.join(AIRBNB, p["slug"], "index.html")
    if not os.path.isfile(path):
        print(f"  ✗ não encontrado: {p['slug']}")
        continue

    with open(path, encoding="utf-8") as f:
        content = f.read()

    if 'og:title' in content or 'ld+json' in content:
        print(f"  — já tem SEO: {p['slug']}")
        continue

    seo_block = build_seo_block(p)
    patched = content.replace(ANCHOR, seo_block + '\n' + ANCHOR, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(patched)
    print(f"  ✓ atualizado: {p['slug']}")

print("\nPronto.")
