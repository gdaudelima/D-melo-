// Correção de respostas digitadas: tolerante com maiúsculas, espaços e pontuação,
// exigente com artigo e letras; acento faltando vira "quase" (com aviso).

const ARTIGOS = /^(el|la|los|las|un|una|unos|unas)\s+/;

export function limpar(s) {
  return String(s ?? "")
    .normalize("NFC")
    .toLowerCase()
    .replace(/[“”«»"']/g, "")
    .replace(/[¿¡.,;:!?…—–-]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export function semAcento(s) {
  // ñ também é tratada como "quase": é outra letra, mas o erro é de digitação/teclado.
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "").normalize("NFC");
}

/**
 * Compara a resposta com uma lista de respostas aceitas.
 * @returns {{nota:'certo'|'quase'|'errado', motivo?:string, esperado:string}}
 */
export function corrigir(resposta, aceitas) {
  const r = limpar(resposta);
  const lista = aceitas.map((a) => ({ bruto: a, limpo: limpar(a) }));
  if (!r) return { nota: "errado", motivo: "vazia", esperado: aceitas[0] };
  for (const a of lista) if (a.limpo === r) return { nota: "certo", esperado: a.bruto };
  for (const a of lista) {
    if (semAcento(a.limpo) === semAcento(r)) {
      const falta = /ñ/.test(a.limpo) && !/ñ/.test(r) ? "ñ" : "acento";
      return { nota: "quase", motivo: falta, esperado: a.bruto };
    }
  }
  for (const a of lista) {
    const m = a.limpo.match(ARTIGOS);
    if (m && semAcento(a.limpo.slice(m[0].length)) === semAcento(r)) {
      return { nota: "errado", motivo: "artigo", artigo: m[1], esperado: a.bruto };
    }
    const mr = r.match(ARTIGOS);
    if (m && mr && m[1] !== mr[1] && semAcento(a.limpo.slice(m[0].length)) === semAcento(r.slice(mr[0].length))) {
      return { nota: "errado", motivo: "genero", artigo: m[1], esperado: a.bruto };
    }
  }
  return { nota: "errado", esperado: aceitas[0] };
}

/** Diferença palavra a palavra, para mostrar onde a resposta se afastou do modelo. */
export function diferenca(resposta, modelo) {
  const a = limpar(resposta).split(" ").filter(Boolean);
  const b = String(modelo).split(/\s+/).filter(Boolean);
  const bl = b.map((w) => limpar(w));
  // LCS simples (frases curtas)
  const n = a.length, m = b.length;
  const t = Array.from({ length: n + 1 }, () => new Array(m + 1).fill(0));
  for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--)
    t[i][j] = a[i] === bl[j] ? t[i + 1][j + 1] + 1 : Math.max(t[i + 1][j], t[i][j + 1]);
  const marcados = new Array(m).fill(false);
  let i = 0, j = 0;
  while (i < n && j < m) {
    if (a[i] === bl[j]) { marcados[j] = true; i++; j++; }
    else if (t[i + 1][j] >= t[i][j + 1]) i++;
    else j++;
  }
  return b.map((w, k) => ({ palavra: w, igual: marcados[k] }));
}
