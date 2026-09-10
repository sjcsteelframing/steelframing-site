# FISF — SEO técnico e rotas finais

## Rotas canônicas

- `/mercado-de-investimento/financiamento-steel-framing/`
- `/mercado-de-investimento/financiamento-steel-framing/caixa/`
- `/mercado-de-investimento/financiamento-steel-framing/avaliacao-bancaria/`
- `/mercado-de-investimento/financiamento-steel-framing/capital-proprio-ou-financiamento/`

## Integração

1. Adicionar um card na Home apontando para a página pilar.
2. Adicionar o card principal na página `/mercado-de-investimento/`.
3. Manter os três links derivados dentro da página pilar.
4. Em cada derivada, incluir link contextual de retorno à página pilar.
5. Evitar criar páginas adicionais antes de medir necessidade editorial ou SEO.

## SEO implementado no pacote

- title exclusivo por URL;
- meta description exclusiva;
- canonical absoluto;
- Open Graph;
- Twitter Card;
- `Article` JSON-LD existente;
- `BreadcrumbList` JSON-LD adicionado;
- headings hierárquicos;
- textos alternativos nas imagens;
- lazy loading em imagens internas.

## Antes do deploy

- Revalidar datas e condições de linhas de crédito citadas no conteúdo.
- Confirmar URL definitiva do domínio e protocolo HTTPS.
- Incluir as quatro URLs no sitemap geral do site.
- Verificar se o CMS/Next.js já injeta canonical, OG e schema para evitar duplicidade.
- Testar Lighthouse/PageSpeed depois da integração real.
- Converter imagens pesadas para WebP/AVIF mantendo PNG apenas quando necessário.

## Regra editorial

Steel Framing não deve ser apresentado como gerador automático de financiamento, liquidez, prazo ou retorno. A vantagem econômica só deve aparecer quando derivada de condições técnicas e operacionais concretas.

**Consulte sempre um Engenheiro!**
