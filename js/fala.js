// Áudio por voz sintética do aparelho (funciona offline quando a voz em espanhol está instalada).
let vozes = [];
const sintese = globalThis.speechSynthesis;

function carregarVozes() {
  if (!sintese) return [];
  vozes = sintese.getVoices().filter((v) => /^es([-_]|$)/i.test(v.lang));
  return vozes;
}
if (sintese) {
  carregarVozes();
  sintese.addEventListener?.("voiceschanged", carregarVozes);
}

export function listaVozes() { return carregarVozes(); }

export function escolherVoz(preferida) {
  const vs = carregarVozes();
  return vs.find((v) => v.voiceURI === preferida)
    || vs.find((v) => /es[-_]ES/i.test(v.lang) && v.localService)
    || vs.find((v) => /es[-_]ES/i.test(v.lang))
    || vs.find((v) => v.localService)
    || vs[0] || null;
}

export const temFala = () => !!sintese;

/** Fala o texto em espanhol. Devolve uma promessa que termina quando acaba de falar. */
export function falar(texto, { velocidade = 0.9, voz = "" } = {}) {
  return new Promise((ok) => {
    if (!sintese) return ok(false);
    sintese.cancel();
    const u = new SpeechSynthesisUtterance(texto);
    const v = escolherVoz(voz);
    if (v) u.voice = v;
    u.lang = v?.lang || "es-ES";
    u.rate = velocidade;
    u.onend = () => ok(true);
    u.onerror = () => ok(false);
    sintese.speak(u);
    setTimeout(() => ok(true), 8000); // segurança: alguns aparelhos não disparam onend
  });
}
