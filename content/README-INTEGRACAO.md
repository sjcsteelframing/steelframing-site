# Home do steelframing.com.br — V1 de integração

Esta pasta contém a primeira versão consolidada da Home principal:

- `index.html`
- `assets/css/home.css`
- `assets/js/home.js`

## Estrutura adotada

A Home funciona como hub institucional e editorial, não como página comercial de construtora.

Fluxo:
1. Hero institucional
2. Posicionamento da plataforma
3. Quatro caminhos de navegação
4. Conteúdos em destaque
5. Lógica editorial: característica técnica → consequência prática → consequência econômica
6. Desempenho = sistema completo
7. Mercado de investimento
8. Missão
9. Rodapé

## Pendência controlada: nomes exatos das imagens

Os arquivos reais enviados em `public/images/home` ainda precisam ser cruzados com o código.

Para evitar espalhar referências provisórias pelo HTML, os nomes estão centralizados em:

`assets/js/home.js`

Objeto:

`HOME_IMAGES`

Na consolidação final, basta substituir os nomes provisórios pelos nomes exatos existentes em `public/images/home`.

## URLs adotadas provisoriamente

- `/steel-framing/`
- `/steel-framing/o-que-e-light-steel-framing/`
- `/steel-framing-x-alvenaria/`
- `/mercado-de-investimento/`
- `/mercado-de-investimento/airbnb-e-aluguel/`
- `/formacao/`
- `/sobre/`
- `/contato/`

Essas rotas devem ser conferidas contra a árvore final antes do deploy.

## Regra editorial aplicada

O texto evita afirmar que o Light Steel Framing seja automaticamente mais barato, rápido,
sustentável, eficiente, durável ou rentável.

Também diferencia o sistema estrutural do desempenho do edifício e trata ROI como resultado
de variáveis do empreendimento, não como consequência automática do sistema construtivo.

Consulte sempre um Engenheiro!


## Correção V2
A V1 usava caminhos absolutos para CSS e JavaScript (`/assets/...`), adequados ao deploy,
mas inadequados para abrir o arquivo diretamente no computador via `file://`.

Nesta V2:
- CSS usa `./assets/css/home.css`
- JavaScript usa `./assets/js/home.js`
- imagens permanecem como placeholders visuais até o cruzamento com `public/images/home`

Assim, ao extrair o ZIP e abrir `index.html`, o layout deve aparecer normalmente.


## Correções V3

- Logo do cabeçalho substituído pelo logo oficial do Steel Framing.
- Menu principal atualizado para:
  Home | Steel Framing | Mercado de Investimento | Steel Framing vs Alvenaria | Sobre | Contato
- Rodapé central repete todas as opções do menu.
- Bloco de URL/rede social inclui ícone do Instagram.
- Rodapé finaliza com “Deus é fiel” alinhado à direita.
- Mantida a frase obrigatória “Consulte sempre um Engenheiro!”.

### Imagens da Home
Os arquivos de imagem enviados no ZIP `public/images/home` ainda não puderam ser lidos
pelo ambiente de geração de arquivos. Por isso, esta V3 não inventa nomes nem troca imagens.
Assim que os arquivos de `public/images/home` forem fornecidos individualmente ou estiverem
acessíveis pelo repositório, o mapeamento será concluído.


## V4 — correções de proporção
- Logo do cabeçalho reduzido para 46 px.
- Logo do rodapé reduzido e substituído pela versão oficial para fundo escuro.
- Ícone do Instagram reduzido para 18 px e convertido para versão branca para fundo escuro.
- “Deus é fiel” permanece à direita no fechamento do rodapé.

## Imagens da Home — pendência real
As imagens não aparecem nesta prévia porque os arquivos do `home.zip` não estão acessíveis
ao ambiente que monta o pacote final. Na V3 os caminhos também estavam intencionalmente
nulos, portanto não havia como as imagens carregarem.

Não foram inventados nomes de arquivo.
A correção definitiva exige os nomes/arquivos de `public/images/home`.


## V5 — Home com imagens reais

Mapeamento aplicado:

- Hero: `public/images/home/SF_hero_principal.jpg`
- O que é Light Steel Framing: `public/images/home/lsf-significado-do-nome.png`
- Steel Framing vs Alvenaria: `public/images/home/steel-framing-vs-alvenaria-criterios-de-decisao.png`
- Airbnb e Aluguel: `public/images/home/i23.png`
- Mercado de Investimento: `public/images/home/SF_home_mercado-investimento.jpg`

Abertura local (`file://`): usa `./public/images/home/`.
Publicação: usa `/images/home/`, considerando `public` como raiz pública.

Consulte sempre um Engenheiro!


## V7 — Home fechada

Alterações finais:
- Hero principal permanece na versão técnica da V5.
- A imagem acolhedora foi reaproveitada no fechamento da Home, antes do rodapé.
- Criada seção parallax de fechamento.
- Desktop: efeito de fundo fixo/parallax.
- Mobile: versão estável sem `background-attachment: fixed`.
- Incluído CTA “Fale conosco”.
- Newsletter não foi incluída nesta fase; fica para a Fase 2.
- Rodapé, menu, logos e imagens dos cards permanecem conforme a versão aprovada.

Asset da seção final:
`public/images/home/SF_home_encerramento.jpg`

Consulte sempre um Engenheiro!


## V8 — quadro final mais transparente

Ajuste aplicado na seção “Conhecimento que se transforma em decisão”:
- fundo do quadro reduzido de 64% para 38% de opacidade;
- borda levemente suavizada;
- blur reduzido para deixar a imagem de fundo mais presente sem perder legibilidade.

Consulte sempre um Engenheiro!


## V9 — ajuste do card 04

No bloco “Por onde começar”:
- “Formação profissional” foi substituído por “Conhecimento e atualização”.
- A descrição e o link visual do card também foram ajustados.
- O destino técnico `/formacao/` foi preservado nesta etapa para não quebrar a navegação existente.

Consulte sempre um Engenheiro!
