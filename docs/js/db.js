// Armazenamento no aparelho (IndexedDB). Nada sai do celular.
const NOME = "dimelo";
const VERSAO = 1;
let _db;

function abrir() {
  if (_db) return Promise.resolve(_db);
  return new Promise((ok, falha) => {
    const req = indexedDB.open(NOME, VERSAO);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains("cartoes")) db.createObjectStore("cartoes", { keyPath: "id" }).createIndex("ficha", "ficha");
      if (!db.objectStoreNames.contains("fichas")) db.createObjectStore("fichas", { keyPath: "id" });
      if (!db.objectStoreNames.contains("historico")) db.createObjectStore("historico", { autoIncrement: true });
      if (!db.objectStoreNames.contains("config")) db.createObjectStore("config");
    };
    req.onsuccess = () => { _db = req.result; ok(_db); };
    req.onerror = () => falha(req.error);
  });
}

function tx(loja, modo, fn) {
  return abrir().then((db) => new Promise((ok, falha) => {
    const t = db.transaction(loja, modo);
    const s = t.objectStore(loja);
    let res;
    Promise.resolve(fn(s)).then((r) => { res = r; });
    t.oncomplete = () => ok(res);
    t.onerror = () => falha(t.error);
    t.onabort = () => falha(t.error);
  }));
}

const pedido = (r) => new Promise((ok, falha) => { r.onsuccess = () => ok(r.result); r.onerror = () => falha(r.error); });

// Sem IndexedDB (ex.: prévia em página protegida): guarda só na memória, e o app avisa.
export let soMemoria = false;
const mem = { cartoes: new Map(), fichas: new Map(), historico: new Map(), config: new Map() };
let seq = 0;
async function disponivel() {
  if (soMemoria) return false;
  try { await abrir(); return true; } catch { soMemoria = true; return false; }
}
const memoria = {
  todos: async (l) => [...mem[l].values()],
  pegar: async (l, k) => mem[l].get(k),
  gravar: async (l, v, k) => { mem[l].set(k ?? v.id ?? ++seq, v); },
  gravarVarios: async (l, vs) => { for (const v of vs) mem[l].set(v.id, v); },
  limparTudo: async () => { for (const m of Object.values(mem)) m.clear(); },
  config: async () => Object.fromEntries(mem.config),
};

const idb = {
  todos: (loja) => tx(loja, "readonly", (s) => pedido(s.getAll())),
  pegar: (loja, chave) => tx(loja, "readonly", (s) => pedido(s.get(chave))),
  gravar: (loja, valor, chave) => tx(loja, "readwrite", (s) => pedido(chave === undefined ? s.put(valor) : s.put(valor, chave))),
  gravarVarios: (loja, valores) => tx(loja, "readwrite", (s) => Promise.all(valores.map((v) => pedido(s.put(v))))),
  limparTudo: () => abrir().then((d) => Promise.all(["cartoes", "fichas", "historico", "config"].map((l) => tx(l, "readwrite", (s) => pedido(s.clear()))))),
  async config() {
    const ks = await tx("config", "readonly", (s) => pedido(s.getAllKeys()));
    const vs = await tx("config", "readonly", (s) => pedido(s.getAll()));
    return Object.fromEntries(ks.map((k, i) => [k, vs[i]]));
  },
};

export const db = new Proxy({}, { get: (_, nome) => async (...a) => ((await disponivel()) ? idb : memoria)[nome](...a) });

export async function pedirPersistencia() {
  try {
    if (navigator.storage?.persist && !(await navigator.storage.persisted())) return await navigator.storage.persist();
    return navigator.storage?.persisted ? await navigator.storage.persisted() : false;
  } catch { return false; }
}
