# DESIGN.md — Dímelo

Direção visual: **Azulejaria ibérica**. O progresso aparece como um painel de azulejos. Cada ficha dominada é uma peça **vidrada**. Uma ficha a revisar fica em **ocre**. Uma ficha ainda não estudada fica em **biscoito**, isto é, cerâmica crua.

Telas de referência (canvas): https://claude.ai/artifact/BqtrypUwqGCvjcLChRyNkR

## Tokens

| Papel | Valor | Uso |
|---|---|---|
| cal (fundo) | #F6F8FB | fundo da página |
| superfície | #FFFFFF | cartões |
| tinta | #14213D | texto principal (15:1 sobre cal) |
| tinta suave | #4A5670 | texto secundário (6,9:1) |
| cobalto | #1F3E99 | cor primária, botões, palavras masculinas (9,5:1) |
| almagre | #A8392B | palavras femininas, erro (6,4:1) |
| ocre | #D99A1E (fundo do azulejo "revisar": #F4C35A) | **só decorativo** (estrela do azulejo, etapa atual, estado "revisar"); nunca texto sobre branco (2,4:1) |
| linha | #DCE2EE | bordas |
| certo | #E3F0E7 / #1E5233 | fundo / texto (7,7:1) |
| erro | #F8E4E0 / #7A2418 | fundo / texto (8,2:1) |
| caixa PT | #FBF1DC | interferência do português |
| marca | #FBEBC8 | destaque dentro do exemplo |

- Raio dos cantos: 6px, como o rejunte fino de um azulejo.
- Tipografia:
  - Interface na fonte do sistema.
  - Texto em espanhol (`.es`) em **Alegreya**, que será embutida offline na Etapa 4.
  - Corpo do texto com 16px ou mais. Rótulos da navegação com 12px.
- Gênero: o artigo e o substantivo levam cor (cobalto para *el*, almagre para *la*). Sempre há também um texto redundante ("masc."/"fem."), para que a informação nunca dependa só da cor.

## Componentes

- Barra superior em cobalto.
- Barra de etapas da sessão: Regra → Exemplos → Recordar → Produzir.
- Navegação inferior com 4 abas: Hoje, Mapa, Contrastes, Eu.
- Caixa PT (ocre claro) para mostrar a interferência do português.
- Pares ✗/✓ para os erros típicos.
- Botões de áudio por exemplo.
- Botões do FSRS, cada um com o intervalo visível.
- Chips para montar frases.
- Azulejo SVG em 3 estados.

## Movimento (notas de interação, princípios de Emil Kowalski)

- Feedback de toque com `scale(0.97)` em 100ms. Sem atraso na resposta.
- Ao revelar a resposta, a peça sobe 4px e o texto aparece em 160ms com ease-out. Não usar mola nem bounce.
- Quando uma ficha passa a "dominada", o azulejo é "vidrado": um brilho desliza 1× em 400ms. É o único momento de celebração.
- Chips de montagem: transição de posição com FLIP, em 200ms.
- Cumprir `prefers-reduced-motion`: só opacidade, sem deslocamento.
- Nenhuma animação bloqueia a próxima ação.

## Acessibilidade

- Alvos de toque com 44px ou mais.
- Ícones com `aria-hidden` e rótulo em texto.
- Cada exemplo em espanhol terá `lang="es"`.
- Erro e acerto também são indicados por ícone e palavra, além da cor.

## Revisão desta etapa (passe interno degradado)

O revisor independente do Impeccable não estava disponível. A crítica foi feita no próprio fluxo:

- detector com 0 achados;
- contraste calculado para todos os pares de cor;
- tamanhos de fonte verificados.

Ressalvas:

- A sorte de forma do concept-seed foi feita offline (modo degradado, seed:8ee6dc158dfda050).
- Os números de progresso no canvas são de exemplo.
