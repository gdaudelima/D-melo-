// Estado do aprendizado: cartões FSRS, progresso das fichas e montagem da sessão do dia.
import { db } from "./db.js";

const F = globalThis.FSRS;
export const Nota = { DeNovo: F.Rating.Again, Dificil: F.Rating.Hard, Bom: F.Rating.Good, Facil: F.Rating.Easy };
const agendador = F.fsrs(F.generatorParameters({ enable_fuzz: true, request_retention: 0.9, maximum_interval: 365 }));

export const DOMINADA_DIAS = 21; // estabilidade mínima para o azulejo ficar "vidrado"

export const C = {}; // conteúdo carregado
export const S = { cartoes: new Map(), fichas: new Map(), config: {} };

export const PADRAO = { novasPorDia: 2, maxRevisoes: 60, velocidade: 0.9, voz: "" };

export async function carregar() {
  const r = await fetch("data/conteudo.json");
  Object.assign(C, await r.json());
  C.fichaPorId = new Map(C.fichas.map((f) => [f.id, f]));
  C.itemPorId = new Map(C.itens.map((i) => [i.id, i]));
  C.itensPorFicha = new Map();
  for (const it of C.itens) {
    if (!C.itensPorFicha.has(it.ficha)) C.itensPorFicha.set(it.ficha, []);
    C.itensPorFicha.get(it.ficha).push(it);
  }
  C.contrastePorId = new Map(C.contrastes.map((c) => [c.id, c]));
  const [cs, fs, cfg] = await Promise.all([db.todos("cartoes"), db.todos("fichas"), db.config()]);
  for (const c of cs) S.cartoes.set(c.id, reviver(c));
  for (const f of fs) S.fichas.set(f.id, f);
  S.config = { ...PADRAO, ...cfg };
}

function reviver(c) {
  for (const k of ["due", "last_review"]) if (c.fsrs[k]) c.fsrs[k] = new Date(c.fsrs[k]);
  return c;
}

export const praticaveis = (fichaId) => (C.itensPorFicha.get(fichaId) || []).filter((i) => i.tipo !== "producao");
export const producoes = (fichaId) => (C.itensPorFicha.get(fichaId) || []).filter((i) => i.tipo === "producao");

/** Intervalos que cada botão daria agora (para mostrar no botão). */
export function previsao(itemId, agora = new Date()) {
  const c = S.cartoes.get(itemId)?.fsrs ?? F.createEmptyCard(agora);
  const r = agendador.repeat(c, agora);
  const out = {};
  for (const [nome, g] of Object.entries(Nota)) out[nome] = r[g].card.due - agora;
  return out;
}

export function formatarIntervalo(ms) {
  const min = Math.round(ms / 60000);
  if (min < 60) return `${Math.max(1, min)} min`;
  const h = Math.round(min / 60);
  if (h < 24) return `${h} h`;
  const d = Math.round(h / 24);
  if (d < 31) return d === 1 ? "1 dia" : `${d} dias`;
  const m = Math.round(d / 30);
  return m === 1 ? "1 mês" : `${m} meses`;
}

export async function avaliar(itemId, nota, acertou, agora = new Date()) {
  const it = C.itemPorId.get(itemId);
  const atual = S.cartoes.get(itemId);
  const base = atual?.fsrs ?? F.createEmptyCard(agora);
  // relógio do aparelho voltou no tempo: nunca avaliar "antes" da última revisão
  if (base.last_review && agora < base.last_review) agora = new Date(base.last_review.getTime() + 1000);
  const { card } = agendador.next(base, agora, nota);
  const novo = { id: itemId, ficha: it.ficha, fsrs: card, criado: atual?.criado ?? agora.toISOString() };
  S.cartoes.set(itemId, novo);
  await db.gravar("cartoes", novo);
  await db.gravar("historico", { item: itemId, nota, acertou, em: agora.toISOString() });
  return novo;
}

export async function marcarFicha(id, dados) {
  const f = { id, etapa: 0, ...(S.fichas.get(id) || {}), ...dados };
  S.fichas.set(id, f);
  await db.gravar("fichas", f);
  return f;
}

export async function salvarConfig(k, v) {
  S.config[k] = v;
  await db.gravar("config", v, k);
}

/** bisque = a estudar; revisao = estudada, em consolidação; vidrada = dominada. */
export function estadoFicha(id, agora = new Date()) {
  const f = S.fichas.get(id);
  const itens = praticaveis(id);
  const cartoes = itens.map((i) => S.cartoes.get(i.id)).filter(Boolean);
  if (!f?.concluida && cartoes.length === 0) return f?.etapa ? "andamento" : "bisque";
  if (itens.length && cartoes.length === itens.length && cartoes.every((c) => c.fsrs.state === F.State.Review && c.fsrs.stability >= DOMINADA_DIAS)) return "vidrada";
  if (!f?.concluida) return "andamento";
  return "revisao";
}

export function pendentes(agora = new Date()) {
  const lim = agora.getTime();
  return [...S.cartoes.values()].filter((c) => c.fsrs.due.getTime() <= lim && C.itemPorId.has(c.id));
}

export function proximaFicha() {
  const emAndamento = C.trilha.find((id) => { const f = S.fichas.get(id); return f && !f.concluida && f.etapa > 0; });
  if (emAndamento) return emAndamento;
  return C.trilha.find((id) => !S.fichas.get(id)?.concluida) ?? null;
}

const hoje = (d = new Date()) => d.toLocaleDateString("sv-SE"); // AAAA-MM-DD local
export function novasHoje() {
  return [...S.fichas.values()].filter((f) => f.iniciada && hoje(new Date(f.iniciada)) === hoje()).length;
}

/** Ordena as revisões: mais atrasadas primeiro, mas sem duas seguidas da mesma ficha. */
export function filaRevisoes(agora = new Date()) {
  const p = pendentes(agora).sort((a, b) => a.fsrs.due - b.fsrs.due).slice(0, S.config.maxRevisoes);
  const out = [];
  while (p.length) {
    const k = p.findIndex((c) => c.ficha !== out.at(-1)?.ficha);
    out.push(p.splice(k === -1 ? 0 : k, 1)[0]);
  }
  return out.map((c) => c.id);
}

export function sequenciaDias() {
  return import("./db.js").then(({ db }) => db.todos("historico")).then((h) => {
    const dias = new Set(h.map((x) => hoje(new Date(x.em))));
    let n = 0; const d = new Date();
    if (!dias.has(hoje(d))) d.setDate(d.getDate() - 1);
    while (dias.has(hoje(d))) { n++; d.setDate(d.getDate() - 1); }
    return { dias: n, total: h.length, acertos: h.filter((x) => x.acertou).length, hojeFeitas: h.filter((x) => hoje(new Date(x.em)) === hoje()).length };
  });
}

export async function exportar() {
  const [cartoes, fichas, historico, config] = await Promise.all([db.todos("cartoes"), db.todos("fichas"), db.todos("historico"), db.config()]);
  return { app: "dimelo", formato: 1, exportado: new Date().toISOString(), cartoes, fichas, historico, config };
}

export async function importar(dados) {
  if (dados?.app !== "dimelo" || !Array.isArray(dados.cartoes)) throw new Error("Arquivo não é um backup do Dímelo.");
  await db.limparTudo();
  await db.gravarVarios("cartoes", dados.cartoes);
  await db.gravarVarios("fichas", dados.fichas || []);
  for (const h of dados.historico || []) await db.gravar("historico", h);
  for (const [k, v] of Object.entries(dados.config || {})) await db.gravar("config", v, k);
  S.cartoes.clear(); S.fichas.clear();
  for (const c of dados.cartoes) S.cartoes.set(c.id, reviver(structuredClone(c)));
  for (const f of dados.fichas || []) S.fichas.set(f.id, f);
  S.config = { ...PADRAO, ...(dados.config || {}) };
}

export async function apagarTudo() {
  await db.limparTudo();
  S.cartoes.clear(); S.fichas.clear(); S.config = { ...PADRAO };
}
