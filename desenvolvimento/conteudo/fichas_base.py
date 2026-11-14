"""Construtor e validador das fichas (formato: dados/ficha.schema.json)."""
import json, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MAPA = {n["id"]: n for n in json.loads((BASE / "dados/mapa-a1-c2.json").read_text())["nos"]}
CONTRASTES = {c["id"] for c in json.loads((BASE / "dados/contrastes-pt-es.json").read_text())["contrastes"]}


def F(no, es, pt, *, objetivo, regra, contraste, exemplos, erros, exs, nivel="A1", modulo=None,
      contrastes=None, pre=None, imagem=None, fonte=None, vocabulario=None, variedades=None):
    if no not in MAPA:
        raise KeyError(f"nó inexistente no mapa: {no}")
    n = MAPA[no]
    cts = list(dict.fromkeys((contrastes or []) + [e[3] for e in erros if e[3]]))
    for c in cts:
        if c not in CONTRASTES:
            raise KeyError(f"{no}: contraste inexistente {c}")
    f = {
        "id": f"{no}@{nivel}", "no_mapa": no, "nivel": nivel, "modulo": modulo or n["modulo"],
        "titulo": {"es": es, "pt": pt}, "status": "rascunho", "objetivo": objetivo,
        "explicacao": {"regra": regra, "contraste_pt": contraste},
        "exemplos": [{"es": e[0], "pt": e[1], **({"destaque": e[2]} if len(e) > 2 and e[2] else {}),
                      "audio": "tts:es-ES", **({"imagem": e[3]} if len(e) > 3 and e[3] else {})} for e in exemplos],
        "erros_tipicos": [{"errado": a, "certo": b, "por_que": c, **({"contraste": d} if d else {})} for a, b, c, d in erros],
        "exercicios": [{"tipo": t, "vertente": v, "enunciado": en, "resposta": r if r is not None else "(resposta livre)",
                        **({"feedback_erro": fb} if fb else {})} for t, v, en, r, fb in exs],
        "prerequisitos": pre if pre is not None else n["prerequisitos"],
        "contrastes": cts,
        "fonte": {"pcic_ref": n["pcic_ref"], "url": fonte or n["fonte"] or ""},
    }
    if imagem:
        f["explicacao"]["esquema"] = imagem
    if vocabulario:
        f["vocabulario"] = vocabulario
    if variedades:
        f["variedades"] = variedades
    return f


def salvar(lista, nome):
    out = BASE / "conteudo/fichas" / nome
    out.parent.mkdir(exist_ok=True)
    ids = [f["id"] for f in lista]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        raise ValueError(f"ids duplicados: {dup}")
    try:
        import jsonschema
        sch = json.loads((BASE / "dados/ficha.schema.json").read_text())
        for f in lista:
            jsonschema.validate(f, sch)
    except ImportError:
        print("aviso: jsonschema ausente, validação de esquema pulada", file=sys.stderr)
    out.write_text(json.dumps(lista, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{nome}: {len(lista)} fichas, {sum(len(f['exercicios']) for f in lista)} exercícios, "
          f"{sum(len(f['exemplos']) for f in lista)} exemplos")
