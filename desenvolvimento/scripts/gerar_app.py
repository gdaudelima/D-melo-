"""Compila o conteúdo (dados/) para o formato do app Dímelo (app/data/conteudo.json),
copia ilustrações, fontes e bibliotecas, e gera o service worker com a lista de arquivos.

Uso: python3 scripts/gerar_app.py
"""
import hashlib, json, re, shutil, unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DADOS = ROOT / "dados"
APP = ROOT / "app"
OM = Path("/home/claude/vendor/om/package/color/svg")
NPM = Path("/tmp/npmw/node_modules")

fichas = json.load(open(DADOS / "fichas-a1.json"))
mapa = json.load(open(DADOS / "mapa-a1-c2.json"))
contrastes = json.load(open(DADOS / "contrastes-pt-es.json"))["contrastes"]

avisos = []
BLANK = re.compile(r"_{1,}")

def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def lista(r):
    return r if isinstance(r, list) else [r]

def alternativas(r):
    """'el médico / la médica' -> ['el médico / la médica', 'el médico', 'la médica']"""
    out = [r]
    if " / " in r:
        out += [p.strip() for p in r.split(" / ")]
    return out

# ---------- vocabulário: índice pt -> imagem
img_por_pt = {}
for f in fichas:
    for v in f.get("vocabulario", []):
        if v.get("imagem"):
            img_por_pt.setdefault(v["pt"].lower(), v["imagem"].split(":")[1])

# ---------- ajustes manuais pontuais (enunciados que não seguem o padrão)
AJUSTES = {
    "Cartaz: 'Horario: de lunes a viernes, de 9:00 a 14:00'. A loja abre no sábado?": {
        "tipo": "escolha", "pergunta": "Cartaz: 'Horario: de lunes a viernes, de 9:00 a 14:00'. A loja abre no sábado?",
        "ops": ["Sí", "No"], "resp": "No", "feedback": "De lunes a viernes = de segunda a sexta."},
    "Você (mulher/homem) responde a uma apresentação: ___": {
        "tipo": "escolha", "pergunta": "Uma mulher responde a uma apresentação:",
        "ops": ["Encantada.", "Encantado.", "Encantadas."], "resp": "Encantada.",
        "feedback": "Encantado concorda com quem fala: mulher diz encantada."},
}

def parse(f, i, e, distratores):
    t, q, r = e["tipo"], e["enunciado"], e["resposta"]
    base = {"id": f"{f['id']}#{i}", "ficha": f["id"], "orig": t, "vertente": e["vertente"],
            "feedback": e.get("feedback_erro")}
    if q in AJUSTES:
        return {**base, **AJUSTES[q]}
    if t in ("producao-livre", "fluencia-cronometrada"):
        m = re.search(r"(\d+)\s*segundos", q)
        return {**base, "tipo": "producao", "pergunta": q,
                "segundos": int(m.group(1)) if m else (60 if t == "fluencia-cronometrada" else None),
                "gravar": bool(re.search(r"\b(Grave|Diga|Leia|Fale|Conte|Faça|diga|leia)\b", q))}

    if t == "escolha-em-contexto":
        grupos = re.findall(r"\(([^()]*/[^()]*)\)", q)
        rs = lista(r)
        if grupos and len(grupos) == len(rs):
            partes, resto = [], q
            for g, rr in zip(grupos, rs):
                antes, resto = resto.split(f"({g})", 1)
                ops = [o.strip() for o in g.split("/")]
                if rr not in ops:
                    avisos.append(f"escolha sem resposta nas opções: {q}")
                    break
                partes += [antes, {"ops": ops, "resp": rr}]
            else:
                partes.append(resto)
                return {**base, "tipo": "escolha-inline", "partes": partes}
        # sem opções: múltipla escolha com distratores tirados da mesma ficha/módulo
        if len(rs) == 1:
            chave = lambda x: sem_acento(re.sub(r"[¡!¿?.,]", "", x).lower().strip())
            ops, vistos = [rs[0]], {chave(rs[0])}
            for d in distratores:
                if chave(d) not in vistos and len(ops) < 4:
                    ops.append(d); vistos.add(chave(d))
            if len(ops) >= 3:
                return {**base, "tipo": "escolha", "pergunta": q, "ops": ops, "resp": rs[0]}
        if BLANK.search(q) and len(BLANK.findall(q)) == len(rs):
            return {**base, "tipo": "digitar", "inline": BLANK.split(q), "campos": [{"resp": [x]} for x in rs]}
        avisos.append(f"escolha virou autoavaliação: {q}")
        return {**base, "tipo": "digitar", "pergunta": q, "campos": [{"resp": [", ".join(rs)]}], "livre": True}

    if t == "lacuna" or (t == "imagem-para-palavra" and "___" in q):
        rs = lista(r)
        pergunta_img = ""
        if q.startswith("Imagem"):
            pergunta_img, q = q.split("Complete:", 1) if "Complete:" in q else ("", q)
            q = q.strip()
        n = len(BLANK.findall(q))
        isolados = all(re.search(rf"(^|[\s¿¡—(]){re.escape(m.group(0))}($|[\s.,;:!?)])", q[max(0, m.start()-1):m.end()+1]) for m in BLANK.finditer(q))
        if n == len(rs) and isolados:
            res = {**base, "tipo": "digitar", "inline": BLANK.split(q.replace("Complete:", "").strip()), "campos": [{"resp": [x]} for x in rs]}
        else:
            # lacuna dentro da palavra: escreve a palavra inteira
            corpo = q.replace("Complete:", "").strip()
            pal = [w.strip(" .,") for w in re.split(r",\s*|\s+", corpo) if "_" in w]
            if len(pal) == len(rs):
                res = {**base, "tipo": "digitar", "pergunta": "Escreva a palavra completa.", "campos": [{"rotulo": p, "resp": [x]} for p, x in zip(pal, rs)]}
            else:
                res = {**base, "tipo": "digitar", "pergunta": corpo, "campos": [{"resp": [x]} for x in rs]}
        if e["tipo"] == "imagem-para-palavra":
            res["dica"] = pergunta_img.replace("Imagem:", "").strip(" .")
        return res

    if t == "imagem-para-palavra":
        m = re.search(r"\[([^\]]+)\]", q)
        pt = m.group(1) if m else q
        alvo = r if isinstance(r, str) else ", ".join(r)
        img = img_por_pt.get(pt.lower())
        com_artigo = bool(re.match(r"^(el|la|los|las)\s", alvo))
        livre = "…" in alvo
        return {**base, "tipo": "digitar", "img": img, "pt": pt,
                "pergunta": "Escreva em espanhol, com o artigo:" if com_artigo else "Escreva em espanhol:",
                "campos": [{"resp": alternativas(alvo)}], "livre": livre}

    if t == "montar-frase":
        toks = re.findall(r"\[([^\]]+)\]", q)
        return {**base, "tipo": "montar", "pergunta": "Ordene as palavras.", "pecas": toks, "resp": r}

    if t == "ditado":
        rs = lista(r)
        m = re.search(r"\[([^\]]+)\]", q)
        if m:  # separar palavras: mostra o bloco, fala a resposta
            return {**base, "tipo": "digitar", "pergunta": "Ouça e separe as palavras:", "mostrar": m.group(1),
                    "fala": rs[0], "campos": [{"resp": rs}]}
        mq = re.search(r"'([^']+)'", q)
        fala = mq.group(1) if mq else q.split(":", 1)[1].strip()
        cab = q.split(":", 1)[0] + "."
        if len(rs) > 1:
            return {**base, "tipo": "digitar", "pergunta": cab, "fala": fala, "campos": [{"rotulo": f"{k+1}ª palavra", "resp": [x]} for k, x in enumerate(rs)]}
        return {**base, "tipo": "digitar", "pergunta": cab, "fala": fala, "campos": [{"resp": [rs[0]]}]}

    if t == "pares-minimos":
        if "afirmação ou pergunta" in q:
            frase = re.search(r"'([^']+)'", q).group(1)
            return {**base, "tipo": "ouvir", "pergunta": "Ouça e marque: afirmação ou pergunta?",
                    "grupos": [[{"fala": frase + ".", "rotulo": "Afirmação"}, {"fala": "¿" + frase + "?", "rotulo": "Pergunta"}]]}
        corpo = q.split(":", 1)[1] if ":" in q else q
        corpo = corpo.replace("¿", "").replace("?", "")
        grupos = []
        for g in corpo.split(";"):
            ws = [w.strip(" '") for w in re.split(r"\s*/\s*|\s+ou\s+", g.strip()) if w.strip(" '")]
            grupos.append([{"fala": w, "rotulo": w} for w in ws])
        return {**base, "tipo": "ouvir", "pergunta": "Ouça e escolha a palavra que você ouviu.", "grupos": grupos}

    if t == "silaba-tonica":
        pal = []
        for s in lista(r):
            sil = s.split("-")
            forte = next(k for k, x in enumerate(sil) if x.upper() == x and any(c.isalpha() for c in x))
            pal.append({"silabas": [x.lower() for x in sil], "forte": forte})
        return {**base, "tipo": "tonica", "pergunta": "Toque na sílaba forte de cada palavra.", "palavras": pal}

    if t == "transformar":
        rs = lista(r)
        if len(rs) > 1:
            cab, corpo = q.split(":", 1)
            itens = [x.strip() for x in corpo.split(",")]
            if len(itens) == len(rs):
                return {**base, "tipo": "digitar", "pergunta": cab + ":", "campos": [{"rotulo": a, "resp": [b]} for a, b in zip(itens, rs)]}
        return {**base, "tipo": "digitar", "pergunta": q, "campos": [{"resp": [", ".join(rs)]}], "longa": len(rs[0].split()) > 3}

    if t == "achar-o-erro":
        corpo = q.split(":", 1)[1].strip() if q.startswith("Toque") else q
        return {**base, "tipo": "digitar", "pergunta": "Esta frase tem um erro. Reescreva certa:", "mostrar": corpo,
                "campos": [{"resp": [r]}], "longa": True, "instrucao": q.split(":", 1)[0] if q.startswith("Toque") else None}

    avisos.append(f"tipo não tratado: {t}: {q}")
    return None

# ---------- itens por ficha
itens = []
vocab_vistos = set()
for f in fichas:
    esc = [e for e in f["exercicios"] if e["tipo"] == "escolha-em-contexto" and "(" not in e["enunciado"]]
    lemas = {v["lema"] for v in f.get("vocabulario", [])}
    pts = [v["pt"] for v in f.get("vocabulario", [])]
    for i, e in enumerate(f["exercicios"]):
        if e["tipo"] == "imagem-para-palavra" and e["resposta"] in lemas:
            continue  # já coberto pelo cartão de vocabulário
        if e["tipo"] == "escolha-em-contexto" and e["enunciado"].startswith("O que significa"):
            distr = [p for p in pts if p != e["resposta"]]
        else:
            distr = [x["resposta"] for x in esc if x is not e and isinstance(x["resposta"], str)]
            if len(distr) < 2:  # completa com respostas do mesmo módulo
                distr += [x["resposta"] for g in fichas if g["modulo"] == f["modulo"] and g is not f
                          for x in g["exercicios"] if x["tipo"] == "escolha-em-contexto" and "(" not in x["enunciado"] and isinstance(x["resposta"], str)][:6]
        it = parse(f, i, e, distr)
        if it:
            itens.append(it)
    for v in f.get("vocabulario", []):
        if v["lema"] in vocab_vistos:
            continue
        vocab_vistos.add(v["lema"])
        img = v["imagem"].split(":")[1] if v.get("imagem") else None
        itens.append({"id": "V:" + v["lema"], "ficha": f["id"], "orig": "vocabulario", "vertente": "foco-na-forma",
                      "tipo": "vocab", "lema": v["lema"], "artigo": v.get("artigo"), "pt": v["pt"],
                      "img": img, "alerta": v.get("alerta_pt")})

# ---------- trilha: rodízio entre módulos, respeitando pré-requisitos
ORDEM_MOD = ["expressoes", "pronuncia-e-escuta", "regras", "vocabulario", "estrutura-da-frase", "ortografia", "cultura", "leitura-e-escrita"]
INICIO = ["FUN-5.1@A1", "ORT-1.1@A1", "PRO-5.1@A1", "FUN-5.4@A1", "GRA-7.1.4@A1", "NE-3@A1"]
por_mod = defaultdict(list)
for f in fichas:
    if f["id"] not in INICIO:
        por_mod[f["modulo"]].append(f)
no_para_ficha = {f["no_mapa"]: f["id"] for f in fichas}
trilha = list(INICIO)
while any(por_mod.values()):
    avancou = False
    for mod in ORDEM_MOD:
        fila = por_mod[mod]
        for k, f in enumerate(fila):
            pre = [no_para_ficha[p] for p in f["prerequisitos"] if p in no_para_ficha]
            if all(p in trilha for p in pre):
                trilha.append(f["id"]); fila.pop(k); avancou = True
                break
    if not avancou:  # ciclo ou pré-requisito ausente: libera o primeiro
        for mod in ORDEM_MOD:
            if por_mod[mod]:
                trilha.append(por_mod[mod].pop(0)["id"]); break
assert len(trilha) == len(fichas) == len(set(trilha))

# ---------- fichas enxutas para o app
fichas_app = []
for f in fichas:
    fichas_app.append({k: f[k] for k in ("id", "no_mapa", "nivel", "modulo", "titulo", "objetivo", "explicacao", "exemplos", "erros_tipicos", "contrastes", "status")}
                      | {"vocabulario": [{"lema": v["lema"], "artigo": v.get("artigo"), "pt": v["pt"], "img": v["imagem"].split(":")[1] if v.get("imagem") else None, "alerta": v.get("alerta_pt")} for v in f.get("vocabulario", [])],
                         "fonte": (f.get("fonte") or {}).get("url")})

# ---------- mapa resumido (estrutura completa A1–C2)
mapa_app = [{"id": n["id"], "es": n["titulo"]["es"], "pt": n["titulo"]["pt"], "modulo": n["modulo"],
             "niveis": n["niveis"], "prof": n["profundidade"]} for n in mapa["nos"]]

conteudo = {"versao": None, "fichas": fichas_app, "itens": itens, "trilha": trilha,
            "contrastes": contrastes, "mapa": mapa_app,
            "modulos": {"expressoes": "Expressões", "regras": "Regras", "estrutura-da-frase": "Estrutura da frase",
                        "vocabulario": "Vocabulário", "ortografia": "Ortografia", "pronuncia-e-escuta": "Pronúncia e escuta",
                        "cultura": "Cultura", "leitura-e-escrita": "Leitura e escrita", "estrategias": "Estratégias"}}

# ---------- cópia de arquivos
(APP / "data").mkdir(parents=True, exist_ok=True)
(APP / "img" / "om").mkdir(parents=True, exist_ok=True)
(APP / "fonts").mkdir(exist_ok=True)
(APP / "js" / "vendor").mkdir(parents=True, exist_ok=True)
usadas = {it.get("img") for it in itens if it.get("img")} | {v["img"] for f in fichas_app for v in f["vocabulario"] if v["img"]}
for old in (APP / "img" / "om").glob("*.svg"):
    if old.stem not in usadas:
        old.unlink()
for h in usadas:
    shutil.copy(OM / f"{h}.svg", APP / "img" / "om" / f"{h}.svg")
for w in ("500-normal", "700-normal", "700-italic"):
    shutil.copy(NPM / "@fontsource/alegreya/files" / f"alegreya-latin-{w}.woff2", APP / "fonts" / f"alegreya-{w}.woff2")
shutil.copy(NPM / "ts-fsrs/dist/index.umd.js", APP / "js/vendor/ts-fsrs.umd.js")

# ---------- ícones (Lucide, ISC) num módulo JS
LUC = Path("/home/claude/vendor/lucide/package/icons")
ICONES = ["house", "map", "languages", "user", "arrow-left", "arrow-right", "volume-2", "x", "check", "lightbulb",
          "rotate-ccw", "snail", "mic", "square", "play", "download", "upload", "trash-2", "timer", "info",
          "chevron-right", "book-open", "wifi-off", "circle-check", "undo-2", "pause", "refresh-cw"]
ics = {}
for n in ICONES:
    t = (LUC / f"{n}.svg").read_text()
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r'\s*class="[^"]*"', "", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r'width="24" height="24"', 'width="__T__" height="__T__"', t)
    t = t.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)
    ics[n] = t
(APP / "js" / "icones.js").write_text("// Ícones Lucide (ISC License)\nconst I = " + json.dumps(ics, ensure_ascii=False) +
    ";\nexport const icone = (n, t = 22) => (I[n] || '').replaceAll('__T__', t);\n", encoding="utf-8")

txt = json.dumps(conteudo, ensure_ascii=False, separators=(",", ":"))
conteudo["versao"] = hashlib.sha1(txt.encode()).hexdigest()[:10]
(APP / "data" / "conteudo.json").write_text(json.dumps(conteudo, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

# ---------- service worker: lista de arquivos + versão pelo hash de tudo
arquivos = sorted(str(p.relative_to(APP)).replace("\\", "/") for p in APP.rglob("*")
                  if p.is_file() and p.name not in ("sw.js", "README.md") and not p.name.startswith("."))
h = hashlib.sha1()
for a in arquivos:
    h.update(a.encode()); h.update((APP / a).read_bytes())
versao = h.hexdigest()[:10]
sw = (ROOT / "scripts" / "sw.template.js").read_text()
sw = sw.replace("__VERSAO__", versao).replace("__ARQUIVOS__", json.dumps(["./"] + arquivos, ensure_ascii=False, indent=1))
(APP / "sw.js").write_text(sw, encoding="utf-8")

from collections import Counter
print("itens:", len(itens), Counter(i["tipo"] for i in itens))
print("trilha começa:", trilha[:10])
print("imagens:", len(usadas), "versão:", versao)
for a in avisos:
    print("AVISO:", a)
