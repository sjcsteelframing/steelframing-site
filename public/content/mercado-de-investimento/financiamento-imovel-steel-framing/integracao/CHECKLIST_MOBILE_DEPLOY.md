# Checklist mobile e deploy — FISF

## Mobile

- H1 sem ultrapassar aproximadamente 3–5 linhas nos principais aparelhos.
- Texto do hero legível sobre a imagem sem depender de detalhe visual atrás dele.
- Botões com área de toque confortável e sem sobreposição.
- Sumário mobile abre/fecha corretamente.
- Imagens não provocam rolagem horizontal.
- Tabelas, quando existentes, precisam de wrapper com overflow horizontal.
- Cards derivados empilhados em uma coluna.
- Fontes do corpo em no mínimo 16 px.
- CLS baixo: definir `width`/`height` ou `aspect-ratio` das imagens no framework final.

## Desktop

- Sumário sticky não cobre cabeçalho fixo do site.
- Hero não excede excessivamente a primeira dobra.
- Conteúdo mantém largura de leitura próxima de 750–850 px.
- Imagens editoriais não ficam maiores do que o corpo de conteúdo sem intenção explícita.

## Performance

- Hero com preload/fetchpriority alto no framework final.
- Demais imagens com lazy loading.
- Gerar WebP/AVIF quando possível.
- Evitar servir PNG de ~1800 px para cards pequenos sem `srcset`.
- Usar cache longo para assets versionados.

## Links

- Home → página pilar.
- Mercado de Investimento → página pilar.
- Pilar → 3 derivadas.
- Derivadas → pilar.
- Links internos relevantes para conteúdos de custo, prazo, ROI e conceitos de LSF quando essas páginas estiverem publicadas.

## Pós-publicação

- Conferir 404/redirects.
- Validar canonical.
- Validar dados estruturados.
- Enviar/atualizar sitemap.
- Conferir indexação no Search Console.
- Revisar mobile real em Android e iPhone, não apenas DevTools.

**Consulte sempre um Engenheiro!**
