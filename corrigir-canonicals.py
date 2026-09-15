"""
Corrige canonical tags errados em todos os HTML do site steelframing.com.br.

Problema: os arquivos HTML internos têm canonical hardcoded com URL errada
porque o vercel.json mapeia caminhos diferentes dos nomes de pasta.

Uso: python corrigir-canonicals.py
Rode na pasta raiz do projeto (onde está o vercel.json).
"""

import re
import json
from pathlib import Path

BASE = "https://steelframing.com.br"

# Mapeamento: arquivo HTML relativo → URL pública canônica
# Baseado no vercel.json
MAPA = {
    "public/content/index.html": "/",
    "public/content/contato/index.html": "/contato/",
    "public/content/sobre/index.html": "/sobre/",
    # steel-framing / o-que-e
    "public/content/o-que-e-steel-framing/index.html": "/steel-framing/o-que-e-light-steel-framing/",
    "public/content/o-que-e-steel-framing/como-funciona/index.html": "/steel-framing/o-que-e-light-steel-framing/como-funciona/",
    "public/content/o-que-e-steel-framing/desempenho-e-durabilidade/index.html": "/steel-framing/o-que-e-light-steel-framing/desempenho-e-durabilidade/",
    "public/content/o-que-e-steel-framing/projeto-e-industrializacao/index.html": "/steel-framing/o-que-e-light-steel-framing/projeto-e-industrializacao/",
    # steel-framing FAQ
    "public/content/steel-framing/enferruja/index.html": "/steel-framing/enferruja/",
    "public/content/steel-framing/pega-fogo/index.html": "/steel-framing/pega-fogo/",
    # steel-framing x alvenaria
    "public/content/steelframing-vs-alvenaria/index.html": "/steel-framing-x-alvenaria/",
    "public/content/steelframing-vs-alvenaria/custo/index.html": "/steel-framing-x-alvenaria/custo/",
    "public/content/steelframing-vs-alvenaria/desempenho/index.html": "/steel-framing-x-alvenaria/desempenho/",
    "public/content/steelframing-vs-alvenaria/fundacoes/index.html": "/steel-framing-x-alvenaria/fundacoes/",
    "public/content/steelframing-vs-alvenaria/mao-de-obra/index.html": "/steel-framing-x-alvenaria/mao-de-obra/",
    "public/content/steelframing-vs-alvenaria/prazo/index.html": "/steel-framing-x-alvenaria/prazo/",
    # mercado / airbnb
    "public/content/mercado-de-investimento/airbnb/index.html": "/mercado-de-investimento/airbnb-e-aluguel/",
    "public/content/mercado-de-investimento/airbnb/operacao-e-manutencao/index.html": "/mercado-de-investimento/airbnb-e-aluguel/operacao-e-manutencao/",
    "public/content/mercado-de-investimento/airbnb/prazo-e-escala/index.html": "/mercado-de-investimento/airbnb-e-aluguel/prazo-e-escala/",
    "public/content/mercado-de-investimento/airbnb/produto-e-conforto/index.html": "/mercado-de-investimento/airbnb-e-aluguel/produto-e-conforto/",
    "public/content/mercado-de-investimento/airbnb/viabilidade-economica/index.html": "/mercado-de-investimento/airbnb-e-aluguel/viabilidade-economica/",
    # mercado / financiamento
    "public/content/mercado-de-investimento/financiamento-imovel-steel-framing/index.html": "/mercado-de-investimento/financiamento-steel-framing/",
    "public/content/mercado-de-investimento/financiamento-imovel-steel-framing/avaliacao-bancaria/index.html": "/mercado-de-investimento/financiamento-steel-framing/avaliacao-bancaria/",
    "public/content/mercado-de-investimento/financiamento-imovel-steel-framing/caixa/index.html": "/mercado-de-investimento/financiamento-steel-framing/caixa/",
    "public/content/mercado-de-investimento/financiamento-imovel-steel-framing/capital-proprio-ou-financiamento/index.html": "/mercado-de-investimento/financiamento-steel-framing/capital-proprio-ou-financiamento/",
}

# Regex para encontrar qualquer canonical (com ou sem www, qualquer URL)
CANONICAL_RE = re.compile(
    r'<link\s[^>]*rel=["\']canonical["\'][^>]*/?>|'
    r'<link\s[^>]*href=[^>]+rel=["\']canonical["\'][^>]*/?>',
    re.IGNORECASE
)

def corrigir_arquivo(arquivo, url_publica):
    caminho = Path(arquivo)
    if not caminho.exists():
        print(f"  [SKIP] não encontrado: {arquivo}")
        return

    html = caminho.read_text(encoding="utf-8")
    canonical_correto = f'<link rel="canonical" href="{BASE}{url_publica}"/>'

    # Encontrar todos os canonicals existentes
    encontrados = CANONICAL_RE.findall(html)

    if not encontrados:
        # Inserir após o charset
        html_novo = html.replace(
            '<meta charset="utf-8"/>',
            f'<meta charset="utf-8"/>\n{canonical_correto}'
        )
        if html_novo == html:
            print(f"  [WARN] sem canonical e sem charset em: {arquivo}")
            return
        caminho.write_text(html_novo, encoding="utf-8")
        print(f"  [ADD] canonical inserido: {url_publica}")
        return

    # Verificar se já está correto
    correto_presente = any(
        f'href="{BASE}{url_publica}"' in c or f"href='{BASE}{url_publica}'" in c
        for c in encontrados
    )

    if correto_presente and len(encontrados) == 1:
        print(f"  [OK]  já correto: {url_publica}")
        return

    # Substituir o primeiro canonical pelo correto e remover os extras
    primeiro = True
    def substituir(m):
        nonlocal primeiro
        if primeiro:
            primeiro = False
            return canonical_correto
        return ""  # remover duplicatas

    html_novo = CANONICAL_RE.sub(substituir, html)
    caminho.write_text(html_novo, encoding="utf-8")

    if len(encontrados) > 1:
        print(f"  [FIX] {len(encontrados)} canonicals → 1 correto: {url_publica}")
    else:
        print(f"  [FIX] corrigido: {url_publica}")

print("=" * 60)
print("Correção de canonical tags — steelframing.com.br")
print("=" * 60)

for arquivo, url in MAPA.items():
    corrigir_arquivo(arquivo, url)

print()
print("Concluído. Agora faça:")
print("  git add -A")
print('  git commit -m "fix: corrige canonical tags em todas as páginas"')
print("  git push")
