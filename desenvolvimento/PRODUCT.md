# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

delegated: HTML, CSS e JavaScript puros, sem framework e sem etapa de build, empacotados como PWA instalável (manifest + service worker) com dados no aparelho (IndexedDB). Motivo: app de uso pessoal que precisa funcionar offline com internet instável, ser fácil de abrir e manter, e carregar rápido no celular. Revisão espaçada com o algoritmo FSRS (biblioteca de código aberto incluída no projeto).

## Users

Uma única usuária: brasileira, falante nativa de português, estudante de espanhol em nível intermediário inicial, com lacunas básicas que quer fechar. Usa principalmente o celular, em sessões curtas do dia a dia, às vezes com internet instável. Já usou o Duolingo e não gostou para aprender de verdade (gamificação no lugar de explicação).

## Product Purpose

Aplicativo pessoal para aprender e treinar espanhol do A1 ao C2 — expressões, vocabulário, regras, ortografia e escuta — com base em evidências de ensino de línguas. Sucesso = a usuária fecha as lacunas do A1–A2, retém o que estuda (revisão espaçada) e passa a produzir frases corretas, sobretudo nas estruturas em que o português interfere.

## Positioning

Feito para quem fala português do Brasil: cada conteúdo traz o contraste com o português e treina os erros típicos de brasileiros (assimetria pronominal — sujeito omitido, objeto retomado, duplicação —, gustar, hay/está, falsos amigos, palavras que mudam de gênero ou de sílaba tônica). Currículo completo ancorado no Plan Curricular del Instituto Cervantes, não numa sequência de jogo.

## Operating Context

- Sessões curtas (10–20 min) no celular; a sessão abre com as revisões do dia e depois avança na unidade.
- Ciclo de unidade: entrada (cena + áudio) → foco na forma (regra curta + contraste PT) → prática (recuperação ativa) → produção/fluência → itens entram na revisão espaçada.
- Complementa as aulas presenciais da escola; a usuária pode querer estudar o tema da aula da semana.

## Capabilities and Constraints

- Conteúdo em `dados/`: mapa A1–C2 com 339 seções (`mapa-a1-c2.json`), 107 fichas A1 (`fichas-a1.json`), 26 contrastes PT–ES (`contrastes-pt-es.json`), modelo de ficha (`ficha.schema.json`).
- Módulos: regras, estrutura da frase, pronúncia e escuta, ortografia, expressões, vocabulário, leitura e escrita, cultura, estratégias.
- Tipos de exercício: imagem→palavra, lacuna, montar frase, transformar, achar o erro, ditado, pares mínimos, sílaba tônica, escolha em contexto, produção livre, fluência cronometrada.
- Precisa funcionar offline. Áudio inicial por voz sintética do navegador (es-ES); áudio gravado depois.
- Língua da interface: português do Brasil; conteúdo de estudo em espanhol (variedade de referência: Espanha, com notas das variedades americanas).
- Uso pessoal, sem contas, sem servidor, sem publicação.
- Indecidido: diagnóstico inicial (formato e duração); prática de fala com gravação (etapa posterior).

## Brand Commitments

- Nome provisório: **Dímelo** (a usuária perguntou "Dímelo ou Me lo dice?"; escolhido Dímelo: imperativo com pronomes enclíticos — "diga-me isso", tratamento tú —, com acento obrigatório; o nome é ele mesmo uma lição de estrutura pronominal).
- Voz: direta, didática, em português, explicando o porquê do erro; nunca infantilizada, sem gamificação punitiva (vidas, rankings).
- Ilustrações: OpenMoji (CC BY-SA 4.0), simples; a cor do lema indica o gênero gramatical.

## Evidence on Hand

- Fundamentação: documento "App de Espanhol — Fundamentos, Referências e Estrutura" (prática espaçada — Kim & Webb 2022; quatro vertentes de Nation; codificação dupla e carga cognitiva; aprendizagem multimídia de Mayer; assimetria pronominal — González 1994).
- Não há depoimentos, métricas de uso nem marca registrada; não inventar.

## Product Principles

1. Explicar antes de pontuar: todo erro recebe a regra em uma linha e, quando for o caso, a interferência do português.
2. Lembrar antes de ver: a resposta só aparece depois da tentativa (prática de recuperação).
3. Uma ideia por tela; imagem só quando ensina (palavras concretas), nunca decorativa.
4. Equilíbrio das quatro vertentes (entrada, forma, produção, fluência), não só cartões.
5. Progresso medido em "sou capaz de…" (descritores MCER), não em pontos.

## Accessibility & Inclusion

Leitura confortável no celular (texto ≥ 16px no conteúdo, alvos de toque ≥ 44px), contraste WCAG AA, uso com uma mão, nenhum significado transmitido só por cor (gênero também indicado pelo artigo), respeito a "reduzir movimento".
