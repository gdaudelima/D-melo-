import json
from pathlib import Path
base = Path(__file__).resolve().parent.parent
d = {"mapa": json.loads((base/"dados/mapa-a1-c2.json").read_text()), "contrastes": json.loads((base/"dados/contrastes-pt-es.json").read_text()), "fichas": json.loads((base/"dados/fichas-a1.json").read_text()), "imagens": json.loads((base/"dados/imagens-a1.json").read_text())}
s = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = (base/"scripts/visualizador.template.html").read_text().replace("__DADOS__", s)
(base/"visualizador").mkdir(exist_ok=True)
(base/"visualizador/index.html").write_text(html)
print(len(html), "bytes")
