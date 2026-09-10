"""
Gera public/busca/search-index.json lendo todos os HTMLs do site.
Executar antes de cada git push quando houver novas páginas.
"""
import os, json, re
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(ROOT, "public")

# Mapeamento file-path → URL pública
URL_MAP = {
    "content/index.html":                                                                          "/",
    "content/o-que-e-steel-framing/index.html":                                                   "/steel-framing/o-que-e-light-steel-framing/",
    "content/o-que-e-steel-framing/como-funciona/index.html":                                     "/steel-framing/o-que-e-light-steel-framing/como-funciona/",
    "content/o-que-e-steel-framing/desempenho-e-durabilidade/index.html":                         "/steel-framing/o-que-e-light-steel-framing/desempenho-e-durabilidade/",
    "content/o-que-e-steel-framing/projeto-e-industrializacao/index.html":                        "/steel-framing/o-que-e-light-steel-framing/projeto-e-industrializacao/",
    "content/steelframing-vs-alvenaria/index.html":                                               "/steel-framing-x-alvenaria/",
    "content/steelframing-vs-alvenaria/custo/index.html":                                         "/steel-framing-x-alvenaria/custo/",
    "content/steelframing-vs-alvenaria/desempenho/index.html":                                    "/steel-framing-x-alvenaria/desempenho/",
    "content/steelframing-vs-alvenaria/fundacoes/index.html":                                     "/steel-framing-x-alvenaria/fundacoes/",
    "content/steelframing-vs-alvenaria/mao-de-obra/index.html":                                   "/steel-framing-x-alvenaria/mao-de-obra/",
    "content/steelframing-vs-alvenaria/prazo/index.html":                                         "/steel-framing-x-alvenaria/prazo/",
    "content/mercado-de-investimento/airbnb/index.html":                                          "/mercado-de-investimento/airbnb-e-aluguel/",
    "content/mercado-de-investimento/financiamento-imovel-steel-framing/index.html":              "/mercado-de-investimento/financiamento-steel-framing/",
    "content/mercado-de-investimento/financiamento-imovel-steel-framing/avaliacao-bancaria/index.html":          "/mercado-de-investimento/financiamento-steel-framing/avaliacao-bancaria/",
    "content/mercado-de-investimento/financiamento-imovel-steel-framing/caixa/index.html":                       "/mercado-de-investimento/financiamento-steel-framing/caixa/",
    "content/mercado-de-investimento/financiamento-imovel-steel-framing/capital-proprio-ou-financiamento/index.html": "/mercado-de-investimento/financiamento-steel-framing/capital-proprio-ou-financiamento/",
    "content/sobre/index.html":                                                                    "/sobre/",
}

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.headings = []
        self.body_text = []
        self._in_title = False
        self._in_body = False
        self._skip_tags = {"script","style","noscript","head","nav","footer","figure","figcaption"}
        self._capture = False
        self._current_h = None
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag == "meta" and attrs.get("name","").lower() == "description":
            self.description = attrs.get("content","")
        if tag == "body":
            self._in_body = True
        if self._in_body:
            if tag in self._skip_tags:
                self._skip_depth += 1
            elif tag in ("h2","h3"):
                self._current_h = []
            elif tag == "main" or tag == "article":
                self._capture = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if self._in_body and tag in self._skip_tags:
            self._skip_depth = max(0, self._skip_depth - 1)
        if tag in ("h2","h3") and self._current_h is not None:
            txt = " ".join(self._current_h).strip()
            if txt:
                self.headings.append(txt)
            self._current_h = None

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        if self._in_title:
            self.title += data
        if self._in_body and self._skip_depth == 0:
            if self._current_h is not None:
                self._current_h.append(data)
            elif self._capture:
                self.body_text.append(data)

def extract(filepath):
    with open(filepath, encoding="utf-8") as f:
        html = f.read()
    p = PageParser()
    p.feed(html)
    # limpa título (remove sufixo " | Steel Framing")
    title = re.sub(r"\s*\|\s*Steel Framing.*$", "", p.title).strip()
    # excerpt: primeiros 280 chars do body
    body = " ".join(p.body_text)
    body = re.sub(r"\s+", " ", body).strip()
    excerpt = body[:280] + ("…" if len(body) > 280 else "")
    return {
        "title": title,
        "description": p.description,
        "headings": p.headings[:8],
        "excerpt": excerpt,
    }

index = []
for rel_path, url in URL_MAP.items():
    abs_path = os.path.join(PUBLIC, rel_path)
    if not os.path.exists(abs_path):
        print(f"  SKIP (não encontrado): {rel_path}")
        continue
    data = extract(abs_path)
    index.append({"url": url, **data})
    print(f"  ✓ {url}")

out_dir = os.path.join(PUBLIC, "busca")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "search-index.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)
print(f"\nÍndice gerado: {out_path} ({len(index)} páginas)")
