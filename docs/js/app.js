// Dímelo — app de estudo de espanhol (uso pessoal, offline).
import { icone } from "./icones.js";
import { corrigir, diferenca } from "./corrigir.js";
import { falar, listaVozes, escolherVoz, temFala } from "./fala.js";
import { pedirPersistencia, soMemoria } from "./db.js";
import * as DB from "./db.js";
import * as E from "./estado.js";

const { C, S } = E;
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const app = () => document.getElementById("app");
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const embaralhar = (a) => { a = [...a]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const plural = (n, um, varios) => `${n} ${n === 1 ? um : varios}`;
const ETAPAS = ["Entrada", "Foco na forma", "Prática", "Produção"];
const NIVEIS = ["A1", "A2", "B1", "B2", "C1", "C2"];

// ---------- peças visuais
function azulejo(estado, t = 34) {
  if (estado === "bisque" || estado === "andamento") {
    const contorno = estado === "andamento" ? "#1F3E99" : "#C3CCE0";
    const fundo = estado === "andamento" ? "#F2F5FC" : "#EEF1F7";
    return `<svg width="${t}" height="${t}" viewBox="0 0 40 40" aria-hidden="true"><rect x=".5" y=".5" width="39" height="39" rx="2" fill="${fundo}" stroke="${contorno}"${estado === "andamento" ? ' stroke-dasharray="3 2"' : ""}></rect><path d="M0 12 A12 12 0 0 0 12 0 M28 0 A12 12 0 0 0 40 12 M40 28 A12 12 0 0 0 28 40 M12 40 A12 12 0 0 0 0 28" fill="none" stroke="${contorno}"></path></svg>`;
  }
  const estrela = estado === "vidrada" ? "#D99A1E" : "#FFFFFF";
  const fundo = estado === "vidrada" ? "#FFFFFF" : "#F4C35A";
  return `<svg width="${t}" height="${t}" viewBox="0 0 40 40" aria-hidden="true"><rect x=".5" y=".5" width="39" height="39" rx="2" fill="${fundo}" stroke="#1F3E99"></rect><path d="M0 0 H13 A13 13 0 0 1 0 13 Z M40 0 V13 A13 13 0 0 1 27 0 Z M40 40 H27 A13 13 0 0 1 40 27 Z M0 40 V27 A13 13 0 0 1 13 40 Z" fill="#1F3E99"></path><path d="M20 9 L23 17 L31 20 L23 23 L20 31 L17 23 L9 20 L17 17 Z" fill="${estrela}" stroke="#1F3E99"></path><circle cx="20" cy="20" r="2.4" fill="#1F3E99"></circle></svg>`;
}
const NOME_ESTADO = { bisque: "a estudar", andamento: "em andamento", revisao: "em revisão", vidrada: "dominada" };

function botaoAzulejo(id, t = 34, extra = "") {
  const f = C.fichaPorId.get(id), st = E.estadoFicha(id);
  return `<a class="azulejo-btn ${extra}" href="#ficha:${encodeURIComponent(id)}" aria-label="${esc(f.titulo.pt)}: ${NOME_ESTADO[st]}">${azulejo(st, t)}</a>`;
}

function topo(selo) { return `<header class="top"><p class="marca">Dímelo</p>${selo ? `<span class="selo">${esc(selo)}</span>` : ""}</header>`; }

function nav(ativa) {
  const it = [["hoje", "Hoje", "house"], ["mapa", "Mapa", "map"], ["contrastes", "Contrastes", "languages"], ["eu", "Eu", "user"]];
  return `<nav class="nav" aria-label="Navegação principal">${it.map(([h, n, ic]) => `<a href="#${h}"${h === ativa ? ' aria-current="page"' : ""}>${icone(ic, 24)}<span>${n}</span></a>`).join("")}</nav>`;
}

function barra(rotulo, { etapa, frac } = {}) {
  const ind = etapa ? `<div class="etapas" aria-hidden="true">${[1, 2, 3, 4].map((i) => `<span class="${i < etapa ? "on" : i === etapa ? "agora" : ""}"></span>`).join("")}</div>`
    : frac !== undefined ? `<div class="progresso" aria-hidden="true"><i style="width:${Math.round(frac * 100)}%"></i></div>` : "";
  return `<div class="barra"><button class="icone-btn" data-sair aria-label="Sair da sessão">${icone("arrow-left")}</button><div style="flex:1;display:flex;flex-direction:column;gap:6px"><span class="rotulo">${esc(rotulo)}</span>${ind}</div></div>`;
}

function botaoAudio(texto, rotulo = texto, grande = false) {
  return `<button class="audio${grande ? " grande" : ""}" data-falar="${esc(texto)}" aria-label="Ouvir: ${esc(rotulo)}">${icone("volume-2", grande ? 28 : 20)}</button>`;
}

function marcar(frase, destaque) {
  let out = esc(frase);
  if (!destaque) return out;
  for (const d of destaque.split(" / ").map((x) => x.trim()).filter(Boolean)) {
    const e = esc(d);
    const i = out.indexOf(e);
    if (i >= 0 && !out.slice(0, i).endsWith("<mark>")) out = out.slice(0, i) + `<mark>${e}</mark>` + out.slice(i + e.length);
  }
  return out;
}

function lemaGenero(lema, artigo) {
  const g = { el: "m", los: "m", la: "f", las: "f" }[artigo];
  if (!g) return `<span class="es" lang="es">${esc(lema)}</span>`;
  const resto = lema.slice(artigo.length);
  return `<span class="es" lang="es"><span class="${g}">${esc(artigo)}</span>${esc(resto)}</span>`;
}
const generoTexto = (artigo) => ({ el: "masculino", los: "masculino plural", la: "feminino", las: "feminino plural" }[artigo]);

function ilustracao(hex, alt, cls = "ilustra") { return hex ? `<img class="${cls}" src="img/om/${hex}.svg" alt="${esc(alt)}" width="148" height="148">` : ""; }

function tela(html, foco = true) {
  const a = app();
  a.innerHTML = `<div class="tela">${html}</div>`;
  ligarComuns(a);
  if (foco) { window.scrollTo(0, 0); const h = $("h1", a); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); } }
}

function ligarComuns(el) {
  $$("[data-falar]", el).forEach((b) => b.addEventListener("click", async () => {
    b.classList.add("tocando");
    await falar(b.dataset.falar, { velocidade: b.dataset.lento ? 0.6 : S.config.velocidade, voz: S.config.voz });
    b.classList.remove("tocando");
  }));
  $$("[data-sair]", el).forEach((b) => b.addEventListener("click", () => { sessao = null; location.hash = "#hoje"; rota(); }));
}

function avisar(texto, acao, rotulo) {
  document.querySelector(".aviso")?.remove();
  const d = document.createElement("div");
  d.className = "aviso"; d.setAttribute("role", "status");
  d.innerHTML = `<span>${esc(texto)}</span>${acao ? `<button>${esc(rotulo)}</button>` : ""}`;
  if (acao) d.querySelector("button").onclick = () => { d.remove(); acao(); };
  document.body.appendChild(d);
  if (!acao) setTimeout(() => d.remove(), 3500);
}

// ---------- HOJE
function trapaDoDia(fichaId) {
  const f = fichaId && C.fichaPorId.get(fichaId);
  const ids = f?.contrastes?.length ? f.contrastes : null;
  const dia = Math.floor(Date.now() / 864e5);
  const comPar = C.contrastes.filter((c) => c.errado);
  const daFicha = (ids || []).map((i) => C.contrastePorId.get(i)).filter((c) => c?.errado);
  const lista = daFicha.length ? daFicha : comPar;
  return lista[dia % lista.length];
}

function vHoje() {
  const rev = E.pendentes().length;
  const prox = E.proximaFicha();
  const fp = prox && S.fichas.get(prox);
  const podeNova = !!prox && (fp?.etapa > 0 || E.novasHoje() < S.config.novasPorDia);
  const minutos = Math.max(1, Math.round(Math.min(rev, S.config.maxRevisoes) * 0.3 + (podeNova ? 10 : 0)));
  const f = prox && C.fichaPorId.get(prox);
  const etapa = fp?.etapa || 1;
  const i = prox ? C.trilha.indexOf(prox) : C.trilha.length - 1;
  const ini = Math.max(0, Math.min(i - 3, C.trilha.length - 8));
  const trecho = C.trilha.slice(ini, ini + 8);
  const contagem = trecho.reduce((a, id) => (a[E.estadoFicha(id)] = (a[E.estadoFicha(id)] || 0) + 1, a), {});
  const ct = trapaDoDia(prox);
  const titulo = rev || podeNova ? "Sua sessão de hoje" : "Tudo em dia por hoje";
  const resumo = rev || podeNova
    ? [rev ? plural(rev, "revisão", "revisões") : null, podeNova ? (fp?.etapa ? "continuar a unidade" : "1 unidade nova") : null].filter(Boolean).join(" e ") + ` · cerca de ${minutos} min`
    : prox ? `Você já fez ${plural(S.config.novasPorDia, "unidade nova", "unidades novas")} hoje. Pode adiantar mais uma se quiser.` : "Você concluiu todas as unidades do A1.";
  tela(`${topo(prox ? `A1 · unidade ${i + 1}` : "A1")}
  <main class="miolo">
    <section class="pilha p14">
      <div class="pilha p6"><h1>${titulo}</h1><p class="peq">${esc(resumo)}</p></div>
      ${rev || podeNova ? `<button class="btn" id="comecar">Começar sessão ${icone("arrow-right", 20)}</button>` : prox ? `<button class="btn sec" id="adiantar">Adiantar uma unidade</button>` : ""}
    </section>
    ${f ? `<section class="painel pilha">
      <h2>Unidade atual</h2>
      <p class="grande-es" lang="es">${esc(f.titulo.es)}</p>
      <p class="peq">${esc(f.titulo.pt)} · Etapa ${etapa} de 4 · ${ETAPAS[etapa - 1]}</p>
      <div class="etapas" aria-hidden="true">${[1, 2, 3, 4].map((k) => `<span class="${k < etapa ? "on" : k === etapa ? "agora" : ""}"></span>`).join("")}</div>
      <button class="btn sec" id="unidade">${fp?.etapa ? "Continuar unidade" : "Ver a unidade"}</button>
    </section>` : ""}
    <section class="pilha">
      <div class="linha-ab"><h2>Sua trilha</h2><a href="#mapa" style="font-size:14px;font-weight:600">Ver mapa</a></div>
      <div class="azulejos">${trecho.map((id) => botaoAzulejo(id, 34, id === prox ? "atual" : "")).join("")}</div>
      <p class="peq">${["vidrada", "revisao", "andamento", "bisque"].filter((k) => contagem[k]).map((k) => `${contagem[k]} ${NOME_ESTADO[k]}`).join(" · ")}</p>
    </section>
    <section class="pilha p6">
      <h2>Armadilha do português: ${esc(ct.titulo.toLowerCase())}</h2>
      <p class="nao frase-es" lang="es">${icone("x", 16)}<span>${esc(ct.errado)}</span></p>
      <p class="sim frase-es" lang="es">${icone("check", 16)}<span>${esc(ct.certo)}</span></p>
      <p class="peq">${esc(ct.es)}</p>
    </section>
  </main>${nav("hoje")}`);
  $("#comecar")?.addEventListener("click", () => iniciarSessao({ revisoes: true, unidade: podeNova ? prox : null }));
  $("#adiantar")?.addEventListener("click", () => iniciarSessao({ revisoes: false, unidade: prox }));
  $("#unidade")?.addEventListener("click", () => iniciarSessao({ revisoes: false, unidade: prox }));
}

// ---------- MAPA
let nivelMapa = "A1";
function vMapa() {
  const blocos = [];
  if (nivelMapa === "A1") {
    const est = C.fichas.map((f) => E.estadoFicha(f.id));
    const dom = est.filter((x) => x === "vidrada").length, rev = est.filter((x) => x === "revisao").length;
    for (const [mod, nome] of Object.entries(C.modulos)) {
      const fs = C.trilha.filter((id) => C.fichaPorId.get(id).modulo === mod);
      if (!fs.length) continue;
      const d = fs.filter((id) => E.estadoFicha(id) === "vidrada").length;
      blocos.push(`<section class="pilha p6"><div class="linha-ab"><h2>${esc(nome)}</h2><span class="peq">${d} de ${fs.length}</span></div><div class="azulejos apertado">${fs.map((id) => botaoAzulejo(id, 30)).join("")}</div></section>`);
    }
    blocos.unshift(`<div class="pilha p6"><h1>Painel do A1</h1><p class="peq">${dom} de ${C.fichas.length} fichas dominadas · ${rev} em revisão</p></div>`);
  } else {
    const nos = C.mapa.filter((n) => n.niveis.includes(nivelMapa) && n.prof <= 2);
    blocos.push(`<div class="pilha p6"><h1>Painel do ${nivelMapa}</h1><p class="peq">${nos.length} seções já mapeadas no currículo. O conteúdo deste nível entra na próxima etapa.</p></div>`);
    for (const [mod, nome] of Object.entries(C.modulos)) {
      const ns = nos.filter((n) => n.modulo === mod);
      if (!ns.length) continue;
      blocos.push(`<section class="pilha p6"><div class="linha-ab"><h2>${esc(nome)}</h2><span class="peq">${ns.length} seções</span></div>
        <div class="azulejos apertado" role="img" aria-label="${ns.length} seções ainda sem conteúdo">${ns.map(() => azulejo("bisque", 30)).join("")}</div>
        <details class="secoes"><summary>Ver seções</summary><ul>${ns.map((n) => `<li><span lang="es">${esc(n.es)}</span> — ${esc(n.pt)}</li>`).join("")}</ul></details></section>`);
    }
  }
  tela(`${topo("Mapa")}<main class="miolo">
    <div class="niveis" role="group" aria-label="Nível">${NIVEIS.map((n) => `<button aria-pressed="${n === nivelMapa}" data-nivel="${n}">${n}</button>`).join("")}</div>
    <div class="legenda">${["vidrada", "revisao", "andamento", "bisque"].map((k) => `<span>${azulejo(k, 18)} ${NOME_ESTADO[k]}</span>`).join("")}</div>
    ${blocos.join("")}
  </main>${nav("mapa")}`);
  $$("[data-nivel]").forEach((b) => b.addEventListener("click", () => { nivelMapa = b.dataset.nivel; vMapa(); $(`[data-nivel="${nivelMapa}"]`).focus(); }));
}

// ---------- FICHA
function vFicha(id) {
  const f = C.fichaPorId.get(id);
  if (!f) { location.hash = "#mapa"; return; }
  const st = E.estadoFicha(id), fp = S.fichas.get(id);
  const temCartoes = E.praticaveis(id).some((i) => S.cartoes.has(i.id));
  tela(`<div class="barra"><a class="icone-btn" href="#mapa" aria-label="Voltar ao mapa">${icone("arrow-left")}</a><span class="rotulo">${esc(C.modulos[f.modulo])} · ${esc(f.nivel)}</span></div>
  <main class="miolo">
    <div style="display:flex;gap:14px;align-items:center">${azulejo(st, 56)}<div class="pilha p6"><h1 lang="es" class="es">${esc(f.titulo.es)}</h1><p class="peq">${esc(f.titulo.pt)} · <span class="etiqueta${st === "vidrada" ? " certo" : st === "revisao" ? " ocre" : ""}">${NOME_ESTADO[st]}</span></p></div></div>
    <p><b>${esc(f.objetivo)}</b></p>
    <p>${esc(f.explicacao.regra)}</p>
    <div class="pilha">${f.exemplos.slice(0, 2).map((x) => `<div style="display:flex;gap:12px;align-items:center">${botaoAudio(x.es)}<div><p class="frase-es" lang="es">${marcar(x.es, x.destaque)}</p><p class="peq">${esc(x.pt)}</p></div></div>`).join("")}</div>
    <div class="pilha">
      <button class="btn" id="estudar">${fp?.concluida ? "Estudar de novo" : fp?.etapa ? "Continuar unidade" : "Estudar esta unidade"}</button>
      ${!fp?.concluida ? `<button class="btn sec" id="pular">Já conheço: ir direto à prática</button>` : ""}
      ${temCartoes ? `<button class="btn sec" id="treinar">Treinar agora</button>` : ""}
    </div>
    ${f.fonte ? `<p class="peq">Referência: <a href="${esc(f.fonte)}" rel="noopener">Plan Curricular del Instituto Cervantes</a>. Conteúdo em rascunho, ainda sem revisão de professor.</p>` : ""}
  </main>${nav("mapa")}`);
  $("#estudar").addEventListener("click", () => iniciarSessao({ revisoes: false, unidade: id, recomecar: !!fp?.concluida }));
  $("#pular")?.addEventListener("click", () => iniciarSessao({ revisoes: false, unidade: id, etapa: 3 }));
  $("#treinar")?.addEventListener("click", () => iniciarSessao({ revisoes: false, treino: E.praticaveis(id).filter((i) => S.cartoes.has(i.id)).map((i) => i.id) }));
}

// ---------- CONTRASTES
let eixoFiltro = "todos";
function vContrastes() {
  const eixos = [...new Set(C.contrastes.map((c) => c.eixo))];
  const nomes = { ...C.modulos, "estrutura-da-frase": "Estrutura", "pronuncia-e-escuta": "Pronúncia" };
  const lista = C.contrastes.filter((c) => eixoFiltro === "todos" || c.eixo === eixoFiltro);
  const treina = (cid) => C.fichas.filter((f) => f.contrastes?.includes(cid)).slice(0, 3);
  tela(`${topo("Contrastes")}<main class="miolo">
    <div class="pilha p6"><h1>Onde o português engana</h1><p class="peq">${C.contrastes.length} diferenças entre português e espanhol que mais causam erro.</p></div>
    <div class="filtros" role="group" aria-label="Filtrar por tipo">${["todos", ...eixos].map((e) => `<button aria-pressed="${e === eixoFiltro}" data-eixo="${e}">${e === "todos" ? "Todos" : esc(nomes[e] || e)}</button>`).join("")}</div>
    ${lista.map((c) => `<article class="bloco pilha">
      <h2 style="font-size:17px">${esc(c.titulo)}</h2>
      <p><b>Português:</b> ${esc(c.pt)}</p>
      <p><b>Espanhol:</b> <span${c.errado ? "" : ' lang="es"'}>${esc(c.es)}</span></p>
      ${c.errado ? `<p class="nao frase-es" lang="es">${icone("x", 16)}<span>${esc(c.errado)}</span></p>
      <div style="display:flex;gap:10px;align-items:center"><p class="sim frase-es" lang="es" style="flex:1">${icone("check", 16)}<span>${esc(c.certo)}</span></p>${botaoAudio(c.certo)}</div>` : ""}
      ${c.nota ? `<p class="peq">${esc(c.nota)}</p>` : ""}
      ${treina(c.id).length ? `<p class="peq">Treine em: ${treina(c.id).map((f) => `<a href="#ficha:${encodeURIComponent(f.id)}">${esc(f.titulo.pt)}</a>`).join(", ")}</p>` : ""}
    </article>`).join("")}
  </main>${nav("contrastes")}`);
  $$("[data-eixo]").forEach((b) => b.addEventListener("click", () => { eixoFiltro = b.dataset.eixo; vContrastes(); $(`[data-eixo="${eixoFiltro}"]`).focus(); }));
}

// ---------- EU
async function vEu() {
  const st = await E.sequenciaDias();
  const concl = C.trilha.filter((id) => S.fichas.get(id)?.concluida);
  const vozes = listaVozes();
  const vozAtual = escolherVoz(S.config.voz);
  const offline = !!navigator.serviceWorker?.controller;
  const pct = st.total ? Math.round((st.acertos / st.total) * 100) : 0;
  tela(`${topo("Eu")}<main class="miolo">
    <div class="pilha p6"><h1>Seu progresso</h1><p class="peq">${offline ? "Pronto para usar sem internet." : "O modo sem internet fica ativo depois da primeira visita completa."}</p></div>
    <div class="numeros"><div><b>${st.dias}</b><span class="peq">${st.dias === 1 ? "dia seguido" : "dias seguidos"}</span></div><div><b>${st.hojeFeitas}</b><span class="peq">respostas hoje</span></div><div><b>${pct}%</b><span class="peq">de acerto</span></div></div>
    <section class="pilha"><h2>Sou capaz de…</h2>
      ${concl.length ? `<ul class="capaz">${concl.map((id) => { const f = C.fichaPorId.get(id); const v = E.estadoFicha(id) === "vidrada"; return `<li>${v ? icone("circle-check", 18) : azulejo("revisao", 18)}<span>${esc(f.objetivo.replace(/^Sou capaz de /, "").replace(/^./, (c) => c.toUpperCase()))}${v ? "" : ' <span class="peq">(em revisão)</span>'}</span></li>`; }).join("")}</ul>`
        : `<p class="peq">Cada unidade concluída aparece aqui como algo que você já sabe fazer em espanhol.</p>`}
    </section>
    <section class="bloco pilha"><h2>Estudo</h2>
      <div class="ajuste"><span>Unidades novas por dia</span><span class="passo"><button class="icone-btn" data-novas="-1" aria-label="Menos">−</button><output id="novas">${S.config.novasPorDia}</output><button class="icone-btn" data-novas="1" aria-label="Mais">+</button></span></div>
      <div class="ajuste"><label for="vel">Velocidade da voz</label><select id="vel" class="entrada" style="width:auto;min-height:44px"><option value="0.7"${S.config.velocidade == 0.7 ? " selected" : ""}>Lenta</option><option value="0.9"${S.config.velocidade == 0.9 ? " selected" : ""}>Normal</option><option value="1"${S.config.velocidade == 1 ? " selected" : ""}>Rápida</option></select></div>
      ${temFala() ? `<div class="campo"><label for="voz">Voz em espanhol</label>${vozes.length ? `<select id="voz" class="entrada">${vozes.map((v) => `<option value="${esc(v.voiceURI)}"${vozAtual?.voiceURI === v.voiceURI ? " selected" : ""}>${esc(v.name)} (${esc(v.lang)})${v.localService ? "" : " · precisa de internet"}</option>`).join("")}</select>` : `<p class="caixa-pt">Nenhuma voz em espanhol encontrada. No Android: Configurações → Acessibilidade → Conversão de texto em voz → baixe a voz "Espanhol (Espanha)".</p>`}
        <button class="btn sec" data-falar="Hola, ¿qué tal? Me llamo Dímelo.">${icone("volume-2", 20)} Testar a voz</button></div>` : `<p class="caixa-pt">Este navegador não tem voz sintética; os botões de áudio não vão tocar.</p>`}
    </section>
    <section class="bloco pilha"><h2>Cópia de segurança</h2>
      <p class="peq">Seu progresso fica só neste aparelho. Salve uma cópia de vez em quando (ou antes de trocar de celular).</p>
      <div class="duas"><button class="btn sec" id="exportar">${icone("download", 18)} Salvar cópia</button><label class="btn sec" for="importar" style="cursor:pointer">${icone("upload", 18)} Restaurar</label></div>
      <input type="file" id="importar" accept="application/json,.json" class="so-leitor">
      <div id="apagar-area"><button class="btn leve" id="apagar">${icone("trash-2", 16)} Apagar todo o progresso</button></div>
    </section>
    <section class="pilha p6"><h2>Sobre</h2>
      <p class="peq">Conteúdo A1 em rascunho (versão ${esc(C.versao)}), baseado no Plan Curricular del Instituto Cervantes. Revisão espaçada: FSRS (ts-fsrs, MIT). Ilustrações: OpenMoji, CC BY-SA 4.0. Fonte: Alegreya (SIL OFL). Ícones: Lucide (ISC).</p>
    </section>
  </main>${nav("eu")}`);
  $$("[data-novas]").forEach((b) => b.addEventListener("click", async () => {
    const v = Math.min(5, Math.max(1, S.config.novasPorDia + Number(b.dataset.novas)));
    await E.salvarConfig("novasPorDia", v); $("#novas").textContent = v;
  }));
  $("#vel").addEventListener("change", (e) => E.salvarConfig("velocidade", Number(e.target.value)));
  $("#voz")?.addEventListener("change", (e) => E.salvarConfig("voz", e.target.value));
  $("#exportar").addEventListener("click", async () => {
    const dados = await E.exportar();
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify(dados)], { type: "application/json" }));
    a.download = `dimelo-copia-${new Date().toLocaleDateString("sv-SE")}.json`;
    document.body.appendChild(a); a.click(); a.remove();
    avisar("Cópia salva na pasta de downloads.");
  });
  $("#importar").addEventListener("change", async (e) => {
    const arq = e.target.files[0]; if (!arq) return;
    try { await E.importar(JSON.parse(await arq.text())); avisar("Progresso restaurado."); vEu(); }
    catch (err) { avisar(err.message || "Não consegui ler este arquivo."); }
  });
  $("#apagar").addEventListener("click", () => {
    $("#apagar-area").innerHTML = `<div class="caixa-pt pilha revela"><p><b>Apagar tudo?</b> Revisões, unidades e histórico somem deste aparelho. Isso não tem volta.</p><div class="duas"><button class="btn sec" id="cancelar">Cancelar</button><button class="btn alerta" id="confirmar">Apagar</button></div></div>`;
    $("#cancelar").onclick = () => vEu();
    $("#confirmar").onclick = async () => { await E.apagarTudo(); avisar("Progresso apagado."); vEu(); };
  });
}

// ---------- SESSÃO
let sessao = null;

function iniciarSessao({ revisoes, unidade, etapa, recomecar, treino }) {
  sessao = {
    fila: treino ? embaralhar(treino) : revisoes ? E.filaRevisoes() : [],
    modo: treino ? "treino" : "revisao",
    feitas: 0, acertos: 0, total: 0,
    unidade, etapaInicial: etapa, recomecar,
    repeticoes: {},
  };
  sessao.total = sessao.fila.length;
  location.hash = "#sessao";
  avancar();
}

async function avancar() {
  if (!sessao) return rota();
  if (sessao.fila.length) return mostrarItem(sessao.fila.shift());
  if (sessao.modo !== "unidade" && sessao.unidade) return comecarUnidade();
  if (sessao.modo === "unidade") return proximaEtapa();
  return fimSessao();
}

async function comecarUnidade() {
  const id = sessao.unidade;
  const fp = S.fichas.get(id);
  let etapa = sessao.etapaInicial || (sessao.recomecar ? 1 : fp?.concluida ? 1 : fp?.etapa || 1);
  await E.marcarFicha(id, { etapa, iniciada: fp?.iniciada || new Date().toISOString() });
  sessao.modo = "unidade";
  sessao.etapa = etapa;
  mostrarEtapa();
}

async function proximaEtapa() {
  sessao.etapa++;
  if (sessao.etapa > 4) return concluirUnidade();
  await E.marcarFicha(sessao.unidade, { etapa: sessao.etapa });
  mostrarEtapa();
}

function mostrarEtapa() {
  const id = sessao.unidade, f = C.fichaPorId.get(id), k = sessao.etapa;
  const rot = `Etapa ${k} de 4 · ${ETAPAS[k - 1]}`;
  if (k === 1) {
    const voc = f.vocabulario;
    tela(`${barra(rot, { etapa: 1 })}<main class="miolo sem-nav">
      <div class="pilha p6"><p class="peq">${esc(f.titulo.pt)}</p><h1 class="es" lang="es">${esc(f.titulo.es)}</h1></div>
      <p class="caixa-pt"><b>Objetivo:</b> ${esc(f.objetivo)}</p>
      ${voc.length ? `<section class="pilha"><h2>Palavras desta unidade</h2><p class="peq">Ouça e observe o artigo: azul é masculino, vermelho é feminino.</p>
        <div class="grade-vocab">${voc.map((v) => `<div class="vocab"><div class="topo">${v.img ? ilustracao(v.img, v.pt, "ilustra peq") : `<span></span>`}${botaoAudio(v.lema)}</div><span class="lema">${lemaGenero(v.lema, v.artigo)}</span><span class="peq">${esc(v.pt)}${v.artigo ? ` · ${v.artigo === "el" || v.artigo === "los" ? "masc." : "fem."}` : ""}</span></div>`).join("")}</div></section>` : ""}
      <section class="pilha"><h2>Ouça os exemplos</h2>
        ${f.exemplos.map((x) => `<div style="display:flex;gap:12px;align-items:center">${botaoAudio(x.es)}<div><p class="frase-es" lang="es">${esc(x.es)}</p><p class="peq">${esc(x.pt)}</p></div></div>`).join("")}
      </section>
      <div class="espaco"></div>
      <div class="rodape"><button class="btn" id="seguir">Continuar</button><button class="btn leve" id="pular">Já conheço: ir direto à prática</button></div>
    </main>`);
    $("#seguir").onclick = proximaEtapa;
    $("#pular").onclick = async () => { sessao.etapa = 2; await proximaEtapa(); };
  } else if (k === 2) {
    tela(`${barra(rot, { etapa: 2 })}<main class="miolo sem-nav">
      <h1>${esc(f.titulo.pt)}</h1>
      <p>${esc(f.explicacao.regra)}</p>
      <div class="pilha">${f.exemplos.map((x) => `<div class="painel" style="display:flex;gap:12px;align-items:center">${botaoAudio(x.es)}<div><p class="frase-es" lang="es">${marcar(x.es, x.destaque)}</p><p class="peq">${esc(x.pt)}</p></div></div>`).join("")}</div>
      ${f.explicacao.contraste_pt ? `<div class="caixa-pt"><b>No português:</b> ${esc(f.explicacao.contraste_pt)}</div>` : ""}
      ${f.erros_tipicos.length ? `<section class="pilha"><h2>Erros típicos</h2>${f.erros_tipicos.map((e) => `<div class="pilha p6"><p class="nao frase-es" lang="es">${icone("x", 16)}<span>${esc(e.errado)}</span></p><p class="sim frase-es" lang="es">${icone("check", 16)}<span>${esc(e.certo)}</span></p><p class="peq">${esc(e.por_que)}</p></div>`).join("")}</section>` : ""}
      <div class="espaco"></div>
      <div class="rodape"><button class="btn" id="seguir">Entendi, praticar</button></div>
    </main>`);
    $("#seguir").onclick = proximaEtapa;
  } else if (k === 3) {
    const itens = E.praticaveis(id);
    const voc = itens.filter((i) => i.tipo === "vocab"), ex = itens.filter((i) => i.tipo !== "vocab");
    sessao.fila = [...voc, ...ex].map((i) => i.id);
    sessao.total = sessao.fila.length; sessao.feitas = 0;
    if (!sessao.fila.length) return proximaEtapa();
    avancar();
  } else if (k === 4) {
    sessao.producoes = E.producoes(id);
    sessao.iProd = 0;
    if (!sessao.producoes.length) return proximaEtapa();
    mostrarProducao();
  }
}

function rotuloItem() {
  if (sessao.modo === "unidade") return { rot: `Etapa 3 de 4 · Prática · ${Math.min(sessao.feitas + 1, sessao.total)} de ${sessao.total}`, op: { etapa: 3 } };
  const t = sessao.modo === "treino" ? "Treino" : "Revisão";
  return { rot: `${t} ${Math.min(sessao.feitas + 1, sessao.total)} de ${sessao.total}`, op: { frac: sessao.feitas / Math.max(1, sessao.total) } };
}

// ----- um item (exercício ou cartão)
function mostrarItem(itemId) {
  const it = C.itemPorId.get(itemId);
  if (!it) return avancar();
  const { rot, op } = rotuloItem();
  const r = RENDER[it.tipo](it);
  tela(`${barra(rot, op)}<main class="miolo sem-nav" data-item="${esc(it.id)}">${r.html}<div id="resultado" class="pilha" aria-live="polite"></div><div class="espaco"></div><div class="rodape" id="acoes">${r.acoes || ""}</div></main>`);
  r.ligar?.($("main"), (res) => mostrarResultado(it, res));
  if (r.falaInicial) setTimeout(() => falar(r.falaInicial, { velocidade: S.config.velocidade, voz: S.config.voz }), 250);
}

function teclado(campos) {
  // linha de acentos: insere na posição do cursor sem tirar o foco
  return `<div class="acentos" aria-label="Letras especiais">${["á", "é", "í", "ó", "ú", "ñ", "ü", "¿", "¡"].map((c) => `<button type="button" data-letra="${c}" tabindex="-1">${c}</button>`).join("")}</div>`;
}
function ligarTeclado(el) {
  let ultimo = $("input.entrada, textarea.entrada", el);
  $$("input.entrada, textarea.entrada", el).forEach((i) => i.addEventListener("focus", () => (ultimo = i)));
  $$("[data-letra]", el).forEach((b) => {
    b.addEventListener("pointerdown", (e) => e.preventDefault());
    b.addEventListener("click", () => {
      if (!ultimo) return;
      const s = ultimo.selectionStart ?? ultimo.value.length, e2 = ultimo.selectionEnd ?? s;
      ultimo.value = ultimo.value.slice(0, s) + b.dataset.letra + ultimo.value.slice(e2);
      ultimo.focus(); ultimo.setSelectionRange(s + 1, s + 1);
    });
  });
}
const atributosEntrada = `autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" lang="es" enterkeyhint="done"`;

const RENDER = {
  vocab(it) {
    const comArtigo = !!it.artigo;
    return {
      html: `<div class="cartao-centro">
        <p class="peq">${comArtigo ? "Como se diz em espanhol? Escreva com o artigo." : "Como se diz em espanhol?"}</p>
        ${ilustracao(it.img, `Ilustração: ${it.pt}`)}
        <p style="font-size:20px;font-weight:600">${esc(it.pt)}</p>
        <div class="campo" style="width:100%"><label for="r0" class="so-leitor">Sua resposta</label><input id="r0" class="entrada" style="text-align:center" ${atributosEntrada}></div>
        ${teclado()}
      </div>`,
      acoes: `<button class="btn" id="verificar">Verificar</button><button class="btn leve" id="naosei">Não lembro</button>`,
      ligar(el, fim) {
        ligarTeclado(el);
        const inp = $("#r0", el); setTimeout(() => inp.focus(), 50);
        const ok = () => fim({ ...corrigir(inp.value, [it.lema]), resposta: inp.value, entradas: [inp] });
        $("#verificar", el).onclick = ok;
        inp.addEventListener("keydown", (e) => { if (e.key === "Enter") ok(); });
        $("#naosei", el).onclick = () => fim({ nota: "errado", esperado: it.lema, resposta: "", entradas: [inp], naoSei: true });
      },
    };
  },

  digitar(it) {
    let corpo = "";
    if (it.img) corpo += ilustracao(it.img, `Ilustração: ${it.pt || ""}`);
    if (it.dica) corpo += `<p class="caixa-pt">${icone("lightbulb", 16)} Imagine: ${esc(it.dica)}.</p>`;
    if (it.fala) corpo += `<div style="display:flex;gap:12px;align-items:center;justify-content:center">${botaoAudio(it.fala, "o áudio", true)}<button class="audio" data-falar="${esc(it.fala)}" data-lento="1" aria-label="Ouvir devagar">${icone("snail", 20)}</button></div>`;
    if (it.mostrar) corpo += `<p class="painel frase-es" lang="es">${esc(it.mostrar)}</p>`;
    if (it.pt && !it.img) corpo += `<p style="font-size:20px;font-weight:600;text-align:center">${esc(it.pt)}</p>`;
    let campos;
    if (it.inline) {
      campos = `<p class="frase-inline" lang="es">${it.inline.map((t, k) => esc(t) + (k < it.campos.length ? `<label class="so-leitor" for="r${k}">Lacuna ${k + 1}</label><input id="r${k}" class="entrada inline" ${atributosEntrada}>` : "")).join("")}</p>`;
    } else {
      const multi = it.campos.length > 1;
      campos = it.campos.map((c, k) => `<div class="campo"><label for="r${k}"${!multi && !c.rotulo ? ' class="so-leitor"' : ""}>${c.rotulo ? `<span lang="es">${esc(c.rotulo)}</span>` : multi ? `${k + 1}` : "Sua resposta"}</label>${it.longa ? `<textarea id="r${k}" class="entrada" rows="2" ${atributosEntrada}></textarea>` : `<input id="r${k}" class="entrada" ${atributosEntrada}>`}</div>`).join("");
    }
    return {
      html: `<p class="peq">${esc(it.instrucao || it.pergunta || "Complete.")}</p>${corpo}<div class="pilha">${campos}</div>${teclado()}`,
      acoes: `<button class="btn" id="verificar">Verificar</button><button class="btn leve" id="naosei">Não sei</button>`,
      falaInicial: it.fala,
      ligar(el, fim) {
        ligarTeclado(el);
        const ins = $$(".entrada", el); setTimeout(() => ins[0]?.focus(), 50);
        const ok = () => {
          const res = it.campos.map((c, k) => corrigir(ins[k].value, c.resp));
          const nota = res.every((r) => r.nota === "certo") ? "certo" : res.every((r) => r.nota !== "errado") ? "quase" : "errado";
          fim({ nota, partes: res, resposta: ins.map((i) => i.value).join(" · "), esperado: res.map((r) => r.esperado).join(" · "), entradas: ins, motivo: res.find((r) => r.motivo)?.motivo, artigo: res.find((r) => r.artigo)?.artigo, livre: it.livre || it.longa });
        };
        $("#verificar", el).onclick = ok;
        ins.forEach((i, k) => i.addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); k < ins.length - 1 ? ins[k + 1].focus() : ok(); } }));
        $("#naosei", el).onclick = () => fim({ nota: "errado", naoSei: true, resposta: "", esperado: it.campos.map((c) => c.resp[0]).join(" · "), entradas: ins });
      },
    };
  },

  escolha(it) {
    const ops = embaralhar(it.ops);
    const ehPt = /^O que significa/.test(it.pergunta);
    return {
      html: `<p class="peq">Escolha a resposta.</p><p class="${/[¿¡—]|^[A-ZÁÉÍÓÚ][a-z]+ (de|en|la|el)/.test(it.pergunta) && !ehPt ? "frase-es" : ""}" style="font-size:19px">${esc(it.pergunta)}</p>
        <div class="opcoes">${ops.map((o) => `<button class="opcao${ehPt ? " pt" : ""}" data-op="${esc(o)}"${ehPt ? "" : ' lang="es"'}>${esc(o)}</button>`).join("")}</div>`,
      ligar(el, fim) {
        $$("[data-op]", el).forEach((b) => b.addEventListener("click", () => {
          const certo = b.dataset.op === it.resp;
          $$("[data-op]", el).forEach((x) => { x.disabled = true; if (x.dataset.op === it.resp) x.classList.add("certa"); });
          if (!certo) b.classList.add("errada");
          fim({ nota: certo ? "certo" : "errado", resposta: b.dataset.op, esperado: it.resp });
        }));
      },
    };
  },

  "escolha-inline"(it) {
    let g = 0;
    const html = it.partes.map((p) => typeof p === "string" ? esc(p)
      : `<span class="segmento" role="group" aria-label="Opções ${++g}" data-grupo="${g - 1}">${p.ops.map((o) => `<button class="opcao" aria-pressed="false" data-op="${esc(o)}">${esc(o)}</button>`).join("")}</span>`).join("");
    const grupos = it.partes.filter((p) => typeof p !== "string");
    return {
      html: `<p class="peq">Toque na opção certa${grupos.length > 1 ? " em cada espaço" : ""}.</p><p class="frase-inline" lang="es">${html}</p>`,
      acoes: `<button class="btn" id="verificar" disabled>Verificar</button>`,
      ligar(el, fim) {
        const esc2 = new Array(grupos.length).fill(null);
        $$("[data-grupo]", el).forEach((s) => $$("[data-op]", s).forEach((b) => b.addEventListener("click", () => {
          $$("[data-op]", s).forEach((x) => x.setAttribute("aria-pressed", x === b));
          esc2[s.dataset.grupo] = b.dataset.op;
          $("#verificar", el).disabled = esc2.includes(null);
        })));
        $("#verificar", el).onclick = () => {
          let ok = true;
          $$("[data-grupo]", el).forEach((s, k) => $$("[data-op]", s).forEach((x) => {
            x.disabled = true;
            if (x.dataset.op === grupos[k].resp) x.classList.add("certa");
            else if (x.getAttribute("aria-pressed") === "true") { x.classList.add("errada"); ok = false; }
          }));
          const frase = it.partes.map((p, i) => typeof p === "string" ? p : p.resp).join("");
          fim({ nota: ok ? "certo" : "errado", resposta: esc2.join(" · "), esperado: frase });
        };
      },
    };
  },

  montar(it) {
    return {
      html: `<p class="peq">${esc(it.pergunta)} Toque numa palavra para colocar ou tirar.</p>
        <div class="frase-montada" id="frase" aria-label="Sua frase" lang="es"></div>
        <div class="banco" id="banco" aria-label="Palavras disponíveis" lang="es">${it.pecas.map((p, k) => `<button class="chip" data-k="${k}">${esc(p)}</button>`).join("")}</div>`,
      acoes: `<button class="btn" id="verificar" disabled>Verificar</button>`,
      ligar(el, fim) {
        const frase = $("#frase", el), banco = $("#banco", el);
        $$(".chip", el).forEach((c) => c.addEventListener("click", () => {
          flip($$(".chip", el), () => (c.parentElement === banco ? frase : banco).appendChild(c));
          $("#verificar", el).disabled = frase.children.length === 0;
        }));
        $("#verificar", el).onclick = () => {
          const txt = $$(".chip", frase).map((c) => c.textContent).join(" ");
          const r = corrigir(txt, [it.resp]);
          fim({ ...r, nota: r.nota === "quase" ? "certo" : r.nota, resposta: txt, esperado: it.resp });
        };
      },
    };
  },

  ouvir(it) {
    const escolhidos = it.grupos.map((g) => g[Math.floor(Math.random() * g.length)]);
    return {
      html: `<p class="peq">${esc(it.pergunta)}</p>${it.grupos.map((g, k) => `<div class="painel pilha" data-grupo="${k}">
        <div style="display:flex;gap:10px;align-items:center">${botaoAudio(escolhidos[k].fala, `áudio ${k + 1}`, true)}<button class="audio" data-falar="${esc(escolhidos[k].fala)}" data-lento="1" aria-label="Ouvir devagar">${icone("snail", 20)}</button><span class="peq">${it.grupos.length > 1 ? `Áudio ${k + 1}` : ""}</span></div>
        <div class="duas">${g.map((o) => `<button class="opcao" aria-pressed="false" data-op="${esc(o.rotulo)}" lang="es">${esc(o.rotulo)}</button>`).join("")}</div></div>`).join("")}`,
      acoes: `<button class="btn" id="verificar" disabled>Verificar</button>`,
      falaInicial: escolhidos[0].fala,
      ligar(el, fim) {
        const resp = new Array(it.grupos.length).fill(null);
        $$("[data-grupo]", el).forEach((s) => $$("[data-op]", s).forEach((b) => b.addEventListener("click", () => {
          $$("[data-op]", s).forEach((x) => x.setAttribute("aria-pressed", x === b));
          resp[s.dataset.grupo] = b.dataset.op;
          $("#verificar", el).disabled = resp.includes(null);
        })));
        $("#verificar", el).onclick = () => {
          let ok = true;
          $$("[data-grupo]", el).forEach((s, k) => $$("[data-op]", s).forEach((x) => {
            x.disabled = true;
            if (x.dataset.op === escolhidos[k].rotulo) x.classList.add("certa");
            else if (x.getAttribute("aria-pressed") === "true") { x.classList.add("errada"); ok = false; }
          }));
          fim({ nota: ok ? "certo" : "errado", resposta: resp.join(" · "), esperado: escolhidos.map((e) => e.rotulo).join(" · ") });
        };
      },
    };
  },

  tonica(it) {
    return {
      html: `<p class="peq">${esc(it.pergunta)}</p>${it.palavras.map((p, k) => `<div class="pilha p6" data-palavra="${k}"><div style="display:flex;gap:10px;align-items:center">${botaoAudio(p.silabas.join(""))}<span class="peq">Palavra ${k + 1}</span></div>
        <div class="silabas" role="group" aria-label="Sílabas de ${esc(p.silabas.join(""))}" lang="es">${p.silabas.map((s, j) => `<button class="opcao" aria-pressed="false" data-j="${j}">${esc(s)}</button>`).join("")}</div></div>`).join("")}`,
      acoes: `<button class="btn" id="verificar" disabled>Verificar</button>`,
      ligar(el, fim) {
        const resp = new Array(it.palavras.length).fill(null);
        $$("[data-palavra]", el).forEach((w) => $$("[data-j]", w).forEach((b) => b.addEventListener("click", () => {
          $$("[data-j]", w).forEach((x) => x.setAttribute("aria-pressed", x === b));
          resp[w.dataset.palavra] = Number(b.dataset.j);
          $("#verificar", el).disabled = resp.includes(null);
        })));
        $("#verificar", el).onclick = () => {
          let ok = true;
          $$("[data-palavra]", el).forEach((w, k) => $$("[data-j]", w).forEach((x) => {
            x.disabled = true;
            if (Number(x.dataset.j) === it.palavras[k].forte) x.classList.add("certa");
            else if (x.getAttribute("aria-pressed") === "true") { x.classList.add("errada"); ok = false; }
          }));
          fim({ nota: ok ? "certo" : "errado", resposta: "", esperado: it.palavras.map((p) => p.silabas.map((s, j) => (j === p.forte ? s.toUpperCase() : s)).join("-")).join(" · ") });
        };
      },
    };
  },
};

// animação FLIP para as peças de montar (200ms)
function flip(els, mudar) {
  const reduz = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const antes = new Map(els.map((e) => [e, e.getBoundingClientRect()]));
  mudar();
  if (reduz) return;
  for (const e of els) {
    const a = antes.get(e), d = e.getBoundingClientRect();
    const dx = a.left - d.left, dy = a.top - d.top;
    if (!dx && !dy) continue;
    e.animate([{ transform: `translate(${dx}px,${dy}px)` }, { transform: "none" }], { duration: 200, easing: "cubic-bezier(.23,1,.32,1)" });
  }
}

// ----- resultado e avaliação FSRS
function mostrarResultado(it, res) {
  const area = $("#resultado"), acoes = $("#acoes");
  (res.entradas || []).forEach((i, k) => { i.readOnly = true; const p = res.partes?.[k]; i.classList.add((p?.nota ?? res.nota) === "errado" ? "mal" : "ok"); });
  $$(".acentos").forEach((a) => a.remove());
  const ficha = C.fichaPorId.get(it.ficha);

  if (res.nota !== "errado") {
    let extra = "";
    if (it.tipo === "vocab") {
      extra = `<div class="painel pilha p6 cartao-centro"><p style="display:flex;align-items:center;gap:10px">${botaoAudio(it.lema)}<span style="font-size:28px">${lemaGenero(it.lema, it.artigo)}</span></p>${it.artigo ? `<p class="peq">${esc(it.pt)} · ${generoTexto(it.artigo)} em espanhol</p>` : ""}</div>${it.alerta ? `<p class="caixa-pt">${icone("lightbulb", 16)} ${esc(it.alerta)}</p>` : ""}`;
      setTimeout(() => falar(it.lema, { velocidade: S.config.velocidade, voz: S.config.voz }), 150);
    }
    const quase = res.nota === "quase" ? `<p class="caixa-pt">${icone("info", 16)} Quase: ${res.motivo === "ñ" ? "repare no <b>ñ</b>" : "falta acento"}. Forma certa: <span class="es" lang="es">${esc(res.esperado)}</span></p>` : "";
    const certo = res.nota === "certo" && it.tipo !== "vocab" ? `<p class="sim">${icone("check", 16)}<span>Certo!${res.esperado && it.tipo !== "escolha" ? ` <span class="es" lang="es">${esc(res.esperado)}</span>` : ""}</span></p>` : "";
    area.innerHTML = `<div class="pilha revela">${certo}${quase}${extra}</div>`;
    ligarComuns(area);
    mostrarNotas(it, res.nota === "quase" ? "Dificil" : "Bom", true);
    return;
  }

  // errado: autoavaliação para respostas abertas; explicação sempre
  const dif = (it.tipo === "digitar" && res.resposta && !res.naoSei) ? diferenca(res.resposta, res.esperado).map((w) => w.igual ? esc(w.palavra) : `<mark>${esc(w.palavra)}</mark>`).join(" ") : esc(res.esperado);
  const motivo = res.motivo === "artigo" ? `Falta o artigo: <b class="${/^(el|los)$/.test(res.artigo) ? "m" : "f"}">${esc(res.artigo)}</b>. Em espanhol o gênero faz parte da palavra.`
    : res.motivo === "genero" ? `O gênero é outro: <b class="${/^(el|los)$/.test(res.artigo) ? "m" : "f"}">${esc(res.artigo)}</b>.` : null;
  const porque = it.feedback || motivo || (it.tipo === "vocab" ? it.alerta : null) || primeiraFrase(ficha.explicacao.regra);
  const vemPt = it.tipo !== "vocab" && ficha.explicacao.contraste_pt && !it.feedback ? ficha.explicacao.contraste_pt : null;
  area.innerHTML = `<div class="pilha revela">
    <h2 style="font-size:20px;color:var(--almagre)">${res.naoSei ? "Veja a resposta" : res.livre ? "Compare com o modelo" : "Ainda não"}</h2>
    ${res.resposta && !res.naoSei ? `<p class="nao">${icone("x", 16)}<span class="es" lang="es">${esc(res.resposta)}</span></p>` : ""}
    <p class="sim">${icone("check", 16)}<span class="es" lang="es">${dif}</span></p>
    ${it.tipo === "vocab" ? `<p style="display:flex;align-items:center;gap:10px">${botaoAudio(it.lema)}<span class="peq">${it.artigo ? `${esc(it.pt)} · ${generoTexto(it.artigo)}` : esc(it.pt)}</span></p>` : ""}
    <div class="painel pilha p6"><h2>Por quê</h2><p>${motivo && porque === motivo ? porque : esc(porque)}</p></div>
    ${vemPt ? `<div class="caixa-pt"><b>Vem do português:</b> ${esc(vemPt)}</div>` : ""}
  </div>`;
  ligarComuns(area);
  if (it.tipo === "vocab") setTimeout(() => falar(it.lema, { velocidade: S.config.velocidade, voz: S.config.voz }), 150);
  const podeContestar = (it.tipo === "digitar" || it.tipo === "vocab") && res.resposta && !res.naoSei;
  acoes.innerHTML = `${podeContestar ? `<button class="btn leve" id="valeu">${res.livre ? "Acertei: minha resposta é equivalente" : "Minha resposta também está certa"}</button>` : ""}
    <div class="duas"><button class="btn sec" id="refazer">${icone("rotate-ccw", 18)} Refazer</button><button class="btn" id="continuar">Continuar</button></div>`;
  $("#continuar").onclick = () => registrar(it, E.Nota.DeNovo, false);
  $("#refazer").onclick = () => registrar(it, E.Nota.DeNovo, false, true);
  $("#valeu")?.addEventListener("click", () => { area.querySelector("h2").textContent = "Certo, valeu a sua"; mostrarNotas(it, "Bom", true); });
  $("#continuar").focus({ preventScroll: true });
}

const primeiraFrase = (t) => (String(t).match(/^.*?[.!?](\s|$)/) || [t])[0].trim();

function mostrarNotas(it, sugerida, acertou) {
  const prev = E.previsao(it.id);
  const nomes = [["DeNovo", "De novo"], ["Dificil", "Difícil"], ["Bom", "Bom"], ["Facil", "Fácil"]];
  $("#acoes").innerHTML = `<p class="peq">Quão fácil foi lembrar?</p><div class="notas">${nomes.map(([k, n]) =>
    `<button class="btn ${k === sugerida ? "" : "sec"}${k === "DeNovo" ? " denovo" : ""}" data-nota="${k}">${n}<small>${E.formatarIntervalo(prev[k])}</small></button>`).join("")}</div>`;
  $$("[data-nota]").forEach((b) => b.addEventListener("click", () => registrar(it, E.Nota[b.dataset.nota], acertou && b.dataset.nota !== "DeNovo")));
  $(`[data-nota="${sugerida}"]`).focus({ preventScroll: true });
}

async function registrar(it, nota, acertou, refazerJa = false) {
  $$("#acoes button").forEach((b) => (b.disabled = true));
  const c = await E.avaliar(it.id, nota, acertou);
  sessao.feitas++;
  if (acertou) sessao.acertos++;
  // passos curtos do FSRS: se o cartão volta em menos de 15 min, ele reaparece nesta sessão
  const n = (sessao.repeticoes[it.id] = (sessao.repeticoes[it.id] || 0) + 1);
  if (n <= 3 && c.fsrs.due - Date.now() < 15 * 60000) {
    if (refazerJa) sessao.fila.unshift(it.id);
    else sessao.fila.splice(Math.min(sessao.fila.length, 3), 0, it.id);
    sessao.total++;
  }
  avancar();
}

// ----- produção e fluência (não entram na revisão: são para usar a língua)
function mostrarProducao() {
  const it = sessao.producoes[sessao.iProd];
  const gravar = it.gravar && typeof MediaRecorder !== "undefined" && navigator.mediaDevices?.getUserMedia;
  tela(`${barra(`Etapa 4 de 4 · Produção · ${sessao.iProd + 1} de ${sessao.producoes.length}`, { etapa: 4 })}<main class="miolo sem-nav">
    <h1>${it.segundos ? "Desafio de fluência" : "Agora é com você"}</h1>
    <p style="font-size:18px">${esc(it.pergunta)}</p>
    ${it.segundos ? `<div class="painel" style="display:flex;align-items:center;gap:12px">${icone("timer", 24)}<span style="font-size:28px;font-weight:700;font-variant-numeric:tabular-nums" id="relogio">${it.segundos}s</span><span class="espaco"></span><button class="btn sec" style="width:auto" id="cronometro">Iniciar</button></div>` : ""}
    ${gravar ? `<div class="painel pilha"><div style="display:flex;gap:10px;align-items:center"><button class="audio grande" id="gravar" aria-label="Gravar">${icone("mic", 28)}</button><span class="peq" id="gstatus">Grave sua resposta e ouça de volta. A gravação não é guardada.</span></div><audio id="ouvirg" controls hidden></audio></div>` : ""}
    <div class="campo"><label for="texto">Escreva aqui (opcional)</label><textarea id="texto" class="entrada" ${atributosEntrada}></textarea></div>
    ${teclado()}
    <p class="peq">Não há correção automática aqui: o objetivo é usar o que você aprendeu. Compare com os exemplos da unidade se quiser.</p>
    <div class="espaco"></div>
    <div class="rodape"><button class="btn" id="feito">Feito</button><button class="btn leve" id="pular">Pular</button></div>
  </main>`);
  ligarTeclado(app());
  if (it.segundos) {
    let t = null, resta = it.segundos;
    $("#cronometro").onclick = (e) => {
      if (t) { clearInterval(t); t = null; e.target.textContent = "Continuar"; return; }
      e.target.textContent = "Pausar";
      t = setInterval(() => { resta--; $("#relogio").textContent = `${resta}s`; if (resta <= 0) { clearInterval(t); t = null; e.target.textContent = "Tempo!"; e.target.disabled = true; navigator.vibrate?.(200); } }, 1000);
    };
  }
  if (gravar) {
    let rec = null, partes = [];
    $("#gravar").onclick = async () => {
      if (rec) { rec.stop(); return; }
      try {
        const st = await navigator.mediaDevices.getUserMedia({ audio: true });
        rec = new MediaRecorder(st); partes = [];
        rec.ondataavailable = (e) => partes.push(e.data);
        rec.onstop = () => { st.getTracks().forEach((t) => t.stop()); const a = $("#ouvirg"); a.src = URL.createObjectURL(new Blob(partes, { type: rec.mimeType })); a.hidden = false; rec = null; $("#gravar").innerHTML = icone("mic", 28); $("#gravar").setAttribute("aria-label", "Gravar de novo"); $("#gstatus").textContent = "Ouça e compare com os exemplos."; };
        rec.start(); $("#gravar").innerHTML = icone("square", 24); $("#gravar").setAttribute("aria-label", "Parar"); $("#gstatus").textContent = "Gravando… toque para parar.";
      } catch { $("#gstatus").textContent = "Sem acesso ao microfone. Fale em voz alta mesmo assim."; }
    };
  }
  const seguir = () => { sessao.iProd++; sessao.iProd < sessao.producoes.length ? mostrarProducao() : proximaEtapa(); };
  $("#feito").onclick = seguir; $("#pular").onclick = seguir;
}

async function concluirUnidade() {
  const id = sessao.unidade, f = C.fichaPorId.get(id);
  const jaEra = S.fichas.get(id)?.concluida;
  await E.marcarFicha(id, { etapa: 4, concluida: jaEra || new Date().toISOString() });
  const st = E.estadoFicha(id);
  const prox = E.proximaFicha();
  const podeMais = prox && E.novasHoje() < S.config.novasPorDia;
  sessao.modo = "fim"; sessao.unidade = null;
  tela(`<main class="miolo sem-nav" style="justify-content:center">
    <div class="cartao-centro pilha p14" style="padding-top:40px">
      <div class="vidrar" style="border-radius:2px">${azulejo(st, 96)}</div>
      <h1>Unidade concluída</h1>
      <p class="grande-es" lang="es">${esc(f.titulo.es)}</p>
      <p class="caixa-pt" style="text-align:left"><b>Agora você:</b> ${esc(f.objetivo.replace(/^Sou capaz de /, "é capaz de "))}</p>
      <p class="peq">As atividades desta unidade entram na sua revisão. O azulejo fica vidrado quando você lembrar de tudo com folga de três semanas.</p>
    </div>
    <div class="espaco"></div>
    <div class="rodape">${podeMais ? `<button class="btn" id="mais">Próxima unidade</button>` : ""}<button class="btn ${podeMais ? "sec" : ""}" id="inicio">Voltar ao início</button></div>
  </main>`);
  $("#mais")?.addEventListener("click", () => iniciarSessao({ revisoes: false, unidade: prox }));
  $("#inicio").onclick = () => { sessao = null; location.hash = "#hoje"; rota(); };
}

function fimSessao() {
  const s = sessao; sessao = null;
  const pct = s.feitas ? Math.round((s.acertos / s.feitas) * 100) : 0;
  tela(`<main class="miolo sem-nav" style="justify-content:center"><div class="cartao-centro pilha p14" style="padding-top:40px">
    <div class="vidrar">${azulejo("vidrada", 96)}</div>
    <h1>${s.feitas ? "Revisão feita" : "Nada para revisar agora"}</h1>
    ${s.feitas ? `<p>${plural(s.feitas, "resposta", "respostas")} · ${pct}% de acerto na primeira tentativa ou depois de corrigir.</p>` : `<p>Os cartões voltam quando estiverem perto de ser esquecidos.</p>`}
  </div><div class="espaco"></div><div class="rodape"><a class="btn" href="#hoje">Voltar ao início</a></div></main>`);
}

// ---------- rotas
function rota() {
  document.querySelector(".aviso:not([data-fixo])")?.remove();
  const h = decodeURIComponent(location.hash.slice(1)) || "hoje";
  if (h === "sessao") { if (!sessao) { location.replace("#hoje"); return vHoje(); } return; }
  sessao = null;
  if (h.startsWith("ficha:")) return vFicha(h.slice(6));
  ({ hoje: vHoje, mapa: vMapa, contrastes: vContrastes, eu: vEu }[h] || vHoje)();
}

// ---------- início
async function iniciar() {
  try {
    await E.carregar();
  } catch (e) {
    app().innerHTML = `<main class="miolo"><h1>Não consegui abrir o conteúdo</h1><p>${esc(e.message)}</p><p class="peq">Feche e abra o app de novo. Se for a primeira vez, é preciso estar com internet.</p></main>`;
    return;
  }
  window.addEventListener("hashchange", rota);
  rota();
  if (DB.soMemoria) { avisar("Modo prévia: o progresso não fica salvo nesta página.", () => {}, "Ok"); document.querySelector(".aviso")?.setAttribute("data-fixo", ""); }
  pedirPersistencia();
  if ("serviceWorker" in navigator && location.protocol !== "file:") {
    try {
      const reg = await navigator.serviceWorker.register("sw.js");
      const oferecer = (w) => {
        const d = avisar; d("Nova versão do Dímelo pronta.", () => { w.postMessage("atualizar"); }, "Atualizar");
        document.querySelector(".aviso")?.setAttribute("data-fixo", "");
      };
      if (reg.waiting && navigator.serviceWorker.controller) oferecer(reg.waiting);
      reg.addEventListener("updatefound", () => {
        const w = reg.installing;
        w?.addEventListener("statechange", () => { if (w.state === "installed" && navigator.serviceWorker.controller) oferecer(w); });
      });
      // recarrega só quando uma versão nova substitui outra (não na primeira instalação)
      let recarregou = false;
      const tinhaControle = !!navigator.serviceWorker.controller;
      navigator.serviceWorker.addEventListener("controllerchange", () => { if (tinhaControle && !recarregou) { recarregou = true; location.reload(); } });
    } catch { /* sem service worker: funciona online */ }
  }
  window.addEventListener("offline", () => avisar("Sem internet. Tudo continua funcionando."));
}

window.__dimelo = { C, S, E }; // usado pelos testes automáticos
iniciar();
