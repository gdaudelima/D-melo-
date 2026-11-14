"""Gera o mapa de conhecimento A1–C2 do app (Etapa 1).

Base: Plan Curricular del Instituto Cervantes, Niveles de referencia para el español (PCIC).
Cada nó = uma seção de inventário do PCIC (ou uma camada própria do app: contrastes PT–ES
e estrutura da frase). Campos:
  grupos      fases do PCIC em que a seção aparece: A (A1-A2), B (B1-B2), C (C1-C2)
  verificado  True  = número, título e grupos conferidos no índice/inventários do PCIC (CVC)
              False = estrutura montada a partir do conhecimento geral do PCIC; conferir na Etapa 2
  resumo      o que o PCIC prevê em cada nível (paráfrase curta), quando já conferido
"""
import json, re, sys
from pathlib import Path

PCIC = "https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/"
INV_URL = {
    "GRA": "niveles/02_gramatica_inventario_{g}.htm",
    "PRO": "niveles/03_pronunciacion_inventario_{g}.htm",
    "ORT": "niveles/04_ortografia_inventario_{g}.htm",
    "FUN": "niveles/05_funciones_inventario_{g}.htm",
    "TAC": "niveles/06_tacticas_pragmaticas_inventario_{g}.htm",
    "GEN": "niveles/07_generos_discursivos_inventario_{g}.htm",
    "NG": "niveles/08_nociones_generales_inventario_{g}.htm",
    "NE": "niveles/09_nociones_especificas_inventario_{g}.htm",
    "SAB": "niveles/11_saberes_y_comportamientos_inventario.htm",
}
GRUPO_URL = {"A": "a1-a2", "B": "b1-b2", "C": "c1-c2"}
NIVEIS = {"A": ["A1", "A2"], "B": ["B1", "B2"], "C": ["C1", "C2"]}

INVENTARIOS = {
    "GRA": dict(nome_es="Gramática", nome_pt="Gramática", componente="gramatical", modulo="regras"),
    "PRO": dict(nome_es="Pronunciación y prosodia", nome_pt="Pronúncia e prosódia", componente="gramatical", modulo="pronuncia-e-escuta",
                nota="O PCIC apresenta pronúncia por fases (A, B, C), não por nível."),
    "ORT": dict(nome_es="Ortografía", nome_pt="Ortografia", componente="gramatical", modulo="ortografia"),
    "FUN": dict(nome_es="Funciones", nome_pt="Funções comunicativas (expressões)", componente="pragmatico-discursivo", modulo="expressoes"),
    "TAC": dict(nome_es="Tácticas y estrategias pragmáticas", nome_pt="Táticas e estratégias pragmáticas", componente="pragmatico-discursivo", modulo="estrutura-da-frase"),
    "GEN": dict(nome_es="Géneros discursivos y productos textuales", nome_pt="Gêneros textuais", componente="pragmatico-discursivo", modulo="leitura-e-escrita"),
    "NG": dict(nome_es="Nociones generales", nome_pt="Noções gerais", componente="nocional", modulo="vocabulario"),
    "NE": dict(nome_es="Nociones específicas", nome_pt="Noções específicas (vocabulário por tema)", componente="nocional", modulo="vocabulario"),
    "REF": dict(nome_es="Referentes culturales", nome_pt="Referentes culturais", componente="cultural", modulo="cultura",
                nota="Organizado por fases (aproximação, aprofundamento, consolidação)."),
    "SAB": dict(nome_es="Saberes y comportamientos socioculturales", nome_pt="Saberes e comportamentos socioculturais", componente="cultural", modulo="cultura",
                nota="Organizado por fases (aproximação, aprofundamento, consolidação)."),
    "INT": dict(nome_es="Habilidades y actitudes interculturales", nome_pt="Habilidades e atitudes interculturais", componente="cultural", modulo="estrategias"),
    "APR": dict(nome_es="Procedimientos de aprendizaje", nome_pt="Procedimentos de aprendizagem", componente="aprendizagem", modulo="estrategias"),
    "EF": dict(nome_es="Estructura de la frase (capa contrastiva)", nome_pt="Estrutura da frase (camada contrastiva do app)", componente="contrastivo", modulo="estrutura-da-frase",
               nota="Camada própria do app, baseada na assimetria pronominal PT–ES (González, 1994); cada nó remete às seções do PCIC."),
}

NODES = []

def N(inv, ref, es, pt, grupos="ABC", v=True, resumo=None, inicio=None, pre=(), contr=(), modulo=None, nota=None):
    NODES.append(dict(inv=inv, ref=ref, es=es, pt=pt, grupos=grupos, v=v, resumo=resumo or {},
                      inicio=inicio, pre=list(pre), contr=list(contr), modulo=modulo, nota=nota))

# ---------------------------------------------------------------- GRAMÁTICA
G = "GRA"
N(G, "1", "El sustantivo", "O substantivo")
N(G, "1.1", "Clases de sustantivos", "Tipos de substantivos", resumo={
    "A1": "Nomes próprios sem artigo (María, España), hipocorísticos (Pepe), formas de tratamento (el Sr. Fernández); nomes de períodos (mediodía, tarde, noche).",
    "A2": "Topônimos com artigo (La Habana), instituições, cargos, disciplinas; nomes de eventos (accidente, concierto)."})
N(G, "1.2", "El género de los sustantivos", "Gênero dos substantivos", contr=["CT-HETEROGENERICOS"], resumo={
    "A1": "Masculino em -o / feminino em -a; outras vogais e consoantes (el peine, la solución); femininos em -o por abreviação (la moto, la foto); heteronímia (padre/madre).",
    "A2": "Masculinos em -a (el problema, el día) e cores (el naranja); la mano; femininos em -esa, -triz, -ina, -isa; invariáveis em -ista (el/la artista)."})
N(G, "1.3", "El número de los sustantivos", "Número dos substantivos", resumo={
    "A1": "Plural em -s após vogal e -es após consoante (árbol/árboles); país/países.",
    "A2": "Invariáveis em -s não agudos (el lunes/los lunes); plurais lexicais (las gafas, los pantalones)."})
N(G, "2", "El adjetivo", "O adjetivo")
N(G, "2.1", "Clases de adjetivos", "Tipos de adjetivos", resumo={
    "A1": "Qualificativos como complemento (el chico guapo) e atributo (es guapo); gentílicos frequentes.",
    "A2": "Pares de opostos (bonito/feo, bueno/malo).",
    "B1": "Prefixação em adjetivos valorativos (agradable/desagradable).",
    "B2": "Cores aproximativas (rojizo); complemento predicativo; restrições dos relacionais.",
    "C1": "Cores compostas (azul marino, invariável); usos relacionais e qualificativos; cuyo.",
    "C2": "Cores compostas soldadas (rojiblanco); gentílicos pouco frequentes."})
N(G, "2.2", "El género del adjetivo", "Gênero do adjetivo", resumo={
    "A1": "alto/alta; gentílicos em consoante (español/española); invariáveis (fácil, marroquí).",
    "A2": "Derivados em -dor/-tor (creador/creadora); invariáveis em -e (interesante)."})
N(G, "2.3", "El número del adjetivo", "Número do adjetivo", grupos="AC", resumo={
    "A1": "Plural em -s / -es (altos, fáciles)."})
N(G, "2.4", "Posición del adjetivo", "Posição do adjetivo", resumo={
    "A1": "Posposição dos especificativos (un chico guapo)."})
N(G, "2.5", "Grados del adjetivo", "Graus do adjetivo", resumo={
    "A1": "Superlativo com muy (muy guapo).",
    "A2": "Comparativos más/tan/menos… que/como; mejor, peor, mayor, menor.",
    "C1": "Superlativos irregulares (amabilísimo, óptimo, pésimo).",
    "C2": "Formas cultas (paupérrimo, celebérrimo); prefixo requete-."})
N(G, "2.6", "Metábasis del adjetivo", "Substantivação do adjetivo", grupos="BC", contr=["CT-LO-NEUTRO"], resumo={
    "B1": "Substantivação com determinante (el grande, el azul).",
    "B2": "Substantivação com lo neutro (lo interesante, lo bueno)."})
N(G, "3", "El artículo", "O artigo")
N(G, "3.1", "El artículo definido", "Artigo definido", contr=["CT-ARTIGO-POSSESSIVO", "CT-HAY-ESTA"], resumo={
    "A1": "el, la, los, las; al, del; primeiro no SN (la otra chica); nunca com possessivo ou demonstrativo antes (*la mi hermana); obrigatório com gustar (Me gusta la paella); incompatível com hay, compatível com está.",
    "A2": "el aula; segunda menção; posse inalienável (Me duele la cabeza); valor genérico; todos los libros; los dos amigos; jogar al tenis."})
N(G, "3.2", "El artículo indefinido", "Artigo indefinido", v=False, contr=["CT-ARTIGO-POSSESSIVO"],
  nota="Incluir 'otro' sem artigo (*un otro).")
N(G, "3.3", "Ausencia de determinación: los nombres escuetos", "Substantivos sem artigo", resumo={
    "A1": "Incompatível com gustar (*Me gusta paella); compatível com hay (Hay árboles).",
    "A2": "Quantidade inespecífica (Bebe agua); *Le encanta cine; Tiene casa / *Tiene palacio."})
N(G, "4", "Los demostrativos", "Os demonstrativos", v=False)
N(G, "5", "Los posesivos", "Os possessivos", v=False, contr=["CT-ARTIGO-POSSESSIVO"])
N(G, "6", "Los cuantificadores", "Os quantificadores", v=False, contr=["CT-MUY-MUCHO"])
N(G, "6.1", "Cuantificadores propios", "Quantificadores (números, mucho, poco, todo…)", resumo={"A1": "Cardinais com gênero nas centenas (doscientas personas); ordinais até 10.º; mucho, poco (com gênero e número), bastante.", "A2": "primer/tercer; todo + artigo (todos los días); otro, demasiado; nada, nadie; más, menos, tan, tanto… que/como."})
N(G, "6.2", "Cuantificadores focales o presuposicionales", "Quantificadores focais (también, solo, incluso)")
N(G, "6.3", "Estructuras cuantificadas", "Estruturas quantificadas", grupos="BC")
N(G, "7", "El pronombre", "O pronome")
N(G, "7.1", "El pronombre personal", "Pronome pessoal", contr=["CT-SUJEITO-NULO", "CT-OBJETO-RETOMADO", "CT-DUPLICACAO", "CT-COLOCACAO"])
N(G, "7.1.1", "Pronombre sujeto", "Pronome sujeito", contr=["CT-SUJEITO-NULO"], resumo={
    "A1": "Paradigma yo…ellos; vos e ustedes nas Américas; regra geral: sujeito omitido (Estudio español); presente só para contraste (Yo soy Clara, ¿y tú?).",
    "A2": "Presença para desfazer ambiguidade; ausente com verbos meteorológicos (Llueve); valor anafórico."})
N(G, "7.1.2", "Pronombres átonos de OD", "Pronomes átonos de objeto direto", contr=["CT-OBJETO-RETOMADO", "CT-COLOCACAO"], pre=["GRA-7.1.1"], resumo={
    "A1": "Ausência com hay e com substantivo sem determinante (¿Tienes coche? No, no tengo).",
    "A2": "me, te, nos, os; lo, la, los, las; lo neutro; preferência pelo átono (La vi / *Vi a ella); ênclise com imperativo e infinitivo (escríbelo); Voy a verlo / Lo voy a ver."})
N(G, "7.1.3", "Pronombres átonos de OI: serie me, te, le", "Pronomes átonos de objeto indireto", contr=["CT-DUPLICACAO", "CT-GUSTAR"], resumo={
    "A1": "me com gustar (Me gusta el cine).",
    "A2": "me, te, nos, os, le, les; le/les > se diante de lo (se lo dieron); duplicação obrigatória (Se lo doy a Luis); interesar, encantar."})
N(G, "7.1.4", "Valores de se", "Valores de se", contr=["CT-VERBOS-PRONOMINAIS", "CT-SE-IMPESSOAL"], resumo={
    "A1": "se reflexivo (levantarse, peinarse)."})
N(G, "7.1.6", "Pronombres tónicos complementos preposicionales", "Pronomes tônicos com preposição", contr=["CT-DUPLICACAO"], resumo={
    "A2": "mí, ti, conmigo, contigo; duplicação (A mí me gusta / *A mí gusta); valor contrastivo."})
N(G, "7.2", "Pronombres relativos", "Pronomes relativos", v=False)
N(G, "7.3", "Los interrogativos", "Palavras interrogativas", resumo={"A1": "qué, quién/quiénes, cuánto/a/os/as com acento e no início da pergunta.", "A2": "qué para sujeito, objeto e atributo; quiénes; ¿Cuánto pesas?"})
N(G, "8", "El adverbio y las locuciones adverbiales", "O advérbio e as locuções adverbiais", v=False, contr=["CT-MUY-MUCHO"])
N(G, "8.1", "Adverbios en -mente", "Advérbios em -mente")
N(G, "8.9", "Locuciones adverbiales", "Locuções adverbiais")
N(G, "8.8", "Adverbios relativos e interrogativos", "Advérbios relativos e interrogativos", resumo={
    "A1": "dónde, cómo no início da pergunta.", "A2": "cuándo.",
    "C1": "cuanto com indicativo e subjuntivo (Come cuanto te apetezca).",
    "C2": "¿Cómo que…? com valor de surpresa ou censura."})
N(G, "9", "El verbo", "O verbo", contr=["CT-SER-ESTAR"])
N(G, "9.1", "Tiempos verbales de indicativo", "Tempos do indicativo")
for ref, es, pt in [("9.1.1", "Presente", "Presente"), ("9.1.2", "Pretérito imperfecto", "Pretérito imperfeito"),
                    ("9.1.3", "Pretérito indefinido", "Pretérito indefinido (perfeito simples)"),
                    ("9.1.4", "Futuro imperfecto", "Futuro simples"), ("9.1.5", "Condicional simple", "Condicional simples (futuro do pretérito)"),
                    ("9.1.6", "Pretérito perfecto", "Pretérito perfeito composto (he cantado)"),
                    ("9.1.7", "Pretérito anterior", "Pretérito anterior"), ("9.1.8", "Pretérito pluscuamperfecto", "Mais-que-perfeito composto"),
                    ("9.1.9", "Futuro perfecto", "Futuro composto"), ("9.1.10", "Condicional compuesto", "Condicional composto")]:
    grupos = {"9.1.7": "C", "9.1.9": "BC", "9.1.10": "BC"}.get(ref, "ABC")
    contr = ["CT-PERFECTO-INDEFINIDO"] if ref in ("9.1.3", "9.1.6") else []
    N(G, ref, es, pt, grupos=grupos, v=ref in ("9.1.1", "9.1.2", "9.1.3", "9.1.6", "9.1.7", "9.1.8"), contr=contr,
      pre=["GRA-9.1.1"] if ref != "9.1.1" else [],
      resumo={"9.1.7": {"C2": "Forma e uso (anterioridade imediata, registro literário: En cuanto hubo saludado…)."},
              "9.1.1": {"C1": "Presente histórico (Colón llega a América en 1492).", "C2": "Presente com valor de ameaça; presente em legendas de foto."},
              "9.1.6": {"C1": "Na América e em zonas da Espanha, tendência a usar o indefinido no lugar do perfeito (Hoy llegué tarde)."}}.get(ref, {}),
      nota="Grupos de 9.1.9 e 9.1.10 a conferir." if ref in ("9.1.9", "9.1.10") else None)
N(G, "9.2", "Tiempos verbales de subjuntivo", "Tempos do subjuntivo", grupos="BC", pre=["GRA-9.1.1"])
for ref, es, pt, res in [
    ("9.2.1", "Presente", "Presente do subjuntivo", {
        "B1": "Formas regulares e irregulares; ojalá, quizá; Quiero que vengas; Es bueno que…; antes de que, cuando + futuro (Cuando llegues); para que.",
        "B2": "Que te vayas; valor de desconhecimento (Busco un libro que sea…); No creo que…; una vez que, hasta que, en cuanto; aunque; *Si llueva."}),
    ("9.2.2", "Pretérito imperfecto", "Imperfeito do subjuntivo", {
        "B2": "Formas em -ra e -se; ojalá com irrealidade; tal vez fuera; quisiera (cortesia); Dijo que fuera."}),
    ("9.2.3", "Pretérito perfecto", "Perfeito do subjuntivo", {"B2": "No es verdad que haya escrito…; Cuando se haya marchado…"}),
    ("9.2.4", "Pretérito pluscuamperfecto", "Mais-que-perfeito do subjuntivo", {"B2": "Orientado ao passado."})]:
    N(G, ref, es, pt, grupos="BC", resumo=res, pre=["GRA-9.2.1"] if ref != "9.2.1" else ["GRA-9.1.1"])
N(G, "9.3", "El imperativo", "O imperativo", contr=["CT-COLOCACAO"])
N(G, "9.4", "Formas no personales del verbo", "Formas nominais do verbo")
N(G, "9.4.1", "Infinitivo", "Infinitivo", resumo={"A1": "Infinitivo como sujeito (Estudiar español es divertido) e objeto (Quiero ir a España).", "A2": "Hay que + inf.; pronomes depois do infinitivo (Puedes usarla); antes de / después de + inf."})
N(G, "9.4.2", "Gerundio", "Gerúndio")
N(G, "9.4.3", "Participio", "Particípio")
N(G, "10", "El sintagma nominal", "O sintagma nominal")
N(G, "10.1", "El núcleo", "O núcleo do sintagma nominal")
N(G, "10.2", "Complementos y modificadores", "Complementos e modificadores do nome", resumo={
    "A1": "Adjetivos; de + nome (el libro de español, la clase de hoy); relativas especificativas em indicativo (la chica que lleva gafas).",
    "A2": "*la casa de mí / mi casa; particípios como adjetivo; aposição (mi hermano Juan, calle Alcalá)."})
N(G, "10.3", "Concordancia interna al SN", "Concordância dentro do sintagma nominal", grupos="AC")
N(G, "10.4", "Concordancia del SN con el verbo", "Concordância do sujeito com o verbo")
N(G, "10.5", "El vocativo", "O vocativo", grupos="AB")
N(G, "11", "El sintagma adjetival", "O sintagma adjetival")
N(G, "11.1", "El núcleo", "O núcleo do sintagma adjetival")
N(G, "11.2", "Complementos y modificadores", "Complementos do adjetivo")
N(G, "12", "El sintagma verbal", "O sintagma verbal")
N(G, "12.1", "El núcleo", "O núcleo do verbo: ser, estar, gustar e perífrases", contr=["CT-TENER-QUE-HAY-QUE", "CT-SER-ESTAR"], resumo={"A1": "gustar; ser sem adjetivo (identidade, origem, profissão, dia); estar sem adjetivo (lugar; bien/mal).", "A2": "Transitivos e intransitivos; encantar, doler; estar + gerúndio; ir a, acabar de, empezar a, volver a; poder, tener que, hay que; ser e estar com adjetivo."})
N(G, "12.2", "Complementos", "Complementos do verbo", contr=["CT-A-PESSOAL", "CT-OBJETO-RETOMADO", "CT-DUPLICACAO"], resumo={
    "A1": "Atributo (Mario es cocinero); OD de pessoa sem a (Tengo dos hermanos); OD oração (Creo que…); OI me com gustar.",
    "A2": "OD de pessoa com a (He visto a Almudena); Lo vi / *Vi a él; OI com a; dativo possessivo (Le rompieron las gafas a Ana); A mí me encanta…; ordem livre dos circunstanciais."})
N(G, "13", "La oración simple", "A oração simples")
N(G, "13.1", "Concordancia", "Concordância", resumo={"A1": "Sujeito–verbo e sujeito–atributo.", "A2": "Concordância com usted/ustedes."})
N(G, "13.2", "Orden de los constituyentes", "Ordem dos elementos da oração")
N(G, "13.3", "Tipos de oraciones simples", "Tipos de orações simples", contr=["CT-SE-IMPESSOAL", "CT-HAY-ESTA"], resumo={
    "A1": "Afirmativas e negativas; perguntas totais e parciais; hay impessoal (Hay tres personas); copulativas; transitivas e intransitivas.",
    "A2": "Perguntas disjuntivas, exclamativas, exortativas; reflexivas (Me ducho); Hace frío.",
    "B1": "Dubitativas com indicativo (A lo mejor viene); recíprocas; impessoais (Llueve); passivas reflexas (Se vende piso); desiderativas (¡Ojalá venga!).",
    "B2": "Dubitativas com subjuntivo (Quizá tengas razón); passivas perifrásticas (será expuesta)."})
N(G, "14", "Oraciones compuestas por coordinación", "Orações coordenadas")
N(G, "14.1", "Coordinación copulativa", "Coordenação aditiva (y, ni)", v=False)
N(G, "14.2", "Coordinación disyuntiva", "Coordenação alternativa (o)", v=False)
N(G, "14.3", "Coordinación adversativa", "Coordenação adversativa (pero, sino)", v=False)
N(G, "15", "Oraciones compuestas por subordinación", "Orações subordinadas")
N(G, "15.1", "Oraciones subordinadas sustantivas", "Subordinadas substantivas", pre=["GRA-9.4.1"], resumo={"A1": "De infinitivo como sujeito (Hablar español es útil; Me gusta estudiar) e objeto (Quiero ir); Creo que + indicativo.", "A2": "Le encanta ir al cine; Aprendo a hablar."})
N(G, "15.3", "Oraciones subordinadas adverbiales", "Subordinadas adverbiais")
N(G, "15.2", "Subordinadas de relativo", "Subordinadas relativas (adjetivas)", v=False)
for ref, es, pt in [("15.3.1", "Temporales", "Temporais"), ("15.3.2", "De lugar", "De lugar"), ("15.3.3", "Modales", "De modo"),
                    ("15.3.4", "Causales", "Causais"), ("15.3.5", "Finales", "Finais"), ("15.3.6", "Condicionales", "Condicionais"),
                    ("15.3.7", "Consecutivas", "Consecutivas"), ("15.3.8", "Comparativas", "Comparativas"), ("15.3.9", "Concesivas", "Concessivas")]:
    N(G, ref, "Subordinadas adverbiales: " + es.lower(), "Subordinadas adverbiais " + pt.lower(), v=ref not in ("15.3.2", "15.3.3", "15.3.9"),
      resumo={"15.3.4": {"A1": "porque depois da principal, sempre indicativo; por qué × porque.", "A2": "Trabajo por dinero; Como porque tengo hambre."},
              "15.3.5": {"A1": "para + infinitivo (Estudio español para trabajar en México; El boli es para escribir)."},
              "15.3.1": {"A2": "antes de / después de + inf.; cuando + presente habitual; desde, desde que, desde hace, hasta."},
              "15.3.6": {"A2": "si + presente, presente (Si quieres ir al cine, puedes…); si × sí."},
              "15.3.7": {"A2": "entonces, por eso."},
              "15.3.8": {"A2": "tan… como, tanto… como, más/menos… que; mejor, peor, mayor, menor; como."}}.get(ref, {}),
      nota=None if ref not in ("15.3.2", "15.3.3", "15.3.9") else "A conferir.")

# ---------------------------------------------------------------- PRONUNCIACIÓN (por fases)
P = "PRO"
N(P, "1", "La base de articulación", "A base de articulação")
N(P, "1.1", "Caracterización general del español", "Características gerais do espanhol", resumo={
    "A": "Vogais puras e tensas, sem nasalização relevante; tendência à sílaba aberta; noção de sotaque e variedades."})
N(P, "2", "La entonación", "A entonação")
N(P, "2.1", "Segmentación del discurso en unidades melódicas", "Grupos melódicos", resumo={
    "A": "Unidades de 7–8 sílabas; relação com a pontuação; enumerações e vocativo."})
N(P, "2.2", "Patrones melódicos de la entonación enunciativa", "Entonação das afirmações", resumo={
    "A": "Entonação sóbria; final descendente (cadência), anticadência e suspensão."})
N(P, "2.3", "Patrones melódicos de la entonación interrogativa", "Entonação das perguntas", resumo={
    "A": "Pergunta total × parcial; pergunta com pronome interrogativo."})
N(P, "2.4", "Patrones melódicos de los actos de habla", "Entonação dos atos de fala", resumo={
    "A": "Exclamações básicas; cumprimentos e cortesia (Muchas gracias, ¿Qué tal?)."})
N(P, "3", "La sílaba y el acento", "A sílaba e o acento", contr=["CT-HETEROTONICOS"])
N(P, "3.1", "Estructura silábica", "Estrutura da sílaba", resumo={
    "A": "Sílabas abertas e fechadas; ditongos e tritongos; ligação entre palavras (to-má-rál-go)."})
N(P, "3.2", "El acento", "O acento (sílaba tônica)", contr=["CT-HETEROTONICOS"], resumo={
    "A": "Acento livre com valor distintivo (caso/casó); agudas, graves, esdrúxulas; acento fixo no presente (trabajo… trabajáis)."})
N(P, "4", "El ritmo, las pausas y el tiempo", "Ritmo, pausas e tempo")
N(P, "4.1", "El ritmo", "O ritmo", resumo={
    "A": "Espanhol tem ritmo silábico; o português tem ritmo acentual: atenção a não 'engolir' vogais átonas."})
N(P, "4.2", "Las pausas y el grupo fónico", "Pausas e grupo fônico")
N(P, "5", "Los fonemas y sus variantes", "Os fonemas e suas variantes")
N(P, "5.1", "Fonemas vocálicos", "As cinco vogais", contr=["CT-VOGAIS-NASAIS"])
N(P, "5.2", "Fonemas consonánticos", "As consoantes", contr=["CT-B-V", "CT-LL-Y", "CT-R-RR", "CT-J-G"], resumo={
    "A": "pero/perro; som de j e g (gente, jefe); z interdental; distinção ll/y (conservação)."})
N(P, "5.3", "Sonidos agrupados: enlace", "Ligação entre palavras", resumo={
    "A": "el hombre bueno > elhombrebueno; casa de Paco; ha salido."})

# ---------------------------------------------------------------- ORTOGRAFÍA
O = "ORT"
N(O, "1", "Ortografía de letras y palabras", "Ortografia de letras e palavras")
N(O, "1.1", "Abecedario", "Alfabeto", grupos="A")
N(O, "1.2", "Vocales", "Vogais")
N(O, "1.3", "Consonantes", "Consoantes")
for ref, es, pt, c in [("1.3.1", "Letras b, v, w", "Letras b, v, w", ["CT-B-V"]), ("1.3.2", "Letras c, k, q, z; dígrafo ch", "Letras c, k, q, z e ch", []),
                       ("1.3.3", "Letras g, j", "Letras g e j", ["CT-J-G"]), ("1.3.4", "Letra h", "Letra h", []),
                       ("1.3.5", "Letra y, dígrafo ll", "Letra y e dígrafo ll", ["CT-LL-Y"]), ("1.3.6", "Letras m, n, ñ", "Letras m, n, ñ", ["CT-NH-N"]),
                       ("1.3.7", "Letra p", "Letra p", []), ("1.3.8", "Letra r, dígrafo rr", "Letra r e dígrafo rr", ["CT-R-RR"])]:
    N(O, ref, es, pt, v=True, contr=c, nota="Grupos por letra a conferir (o índice só mostra o grupo de 1.3).")
N(O, "1.4", "Letras mayúsculas", "Maiúsculas")
N(O, "1.5", "Letras minúsculas iniciales", "Minúsculas iniciais", nota="Dias, meses, nacionalidades e idiomas vão em minúscula, como em português.")
N(O, "1.6", "Tipos de letra", "Tipos de letra")
N(O, "1.7", "Ortografía de las palabras", "Ortografia das palavras (união, separação, números)")
N(O, "2", "Acentuación gráfica", "Acentuação gráfica", contr=["CT-ACENTO-GRAFICO"])
N(O, "2.1", "Reglas generales de acentuación", "Regras gerais de acentuação", resumo={
    "A1": "Tilde em interrogativos e exclamativos (¿Cómo te llamas?, ¡Qué bien!); tilde também em maiúscula (INÉS, Ángel).",
    "A2": "Regras de agudas, graves e esdrúxulas."})
N(O, "2.2", "Tilde diacrítica", "Acento diferencial (tú/tu, él/el, sí/si)")
N(O, "2.3", "Voces de otras lenguas", "Palavras de outras línguas", grupos="B")
N(O, "3", "Puntuación", "Pontuação", contr=["CT-PONTUACAO-INVERTIDA"])
for ref, es, pt, gr in [("3.1", "Punto", "Ponto", "ABC"), ("3.2", "Coma", "Vírgula", "ABC"), ("3.3", "Dos puntos", "Dois-pontos", "ABC"),
                        ("3.4", "Punto y coma", "Ponto e vírgula", "BC"), ("3.5", "Puntos suspensivos", "Reticências", "AB"),
                        ("3.6", "Signos de interrogación y exclamación (¿ ? ¡ !)", "Interrogação e exclamação (¿ ? ¡ !)", "AB"),
                        ("3.7", "Paréntesis", "Parênteses", "ABC"), ("3.12", "Barra", "Barra", "ABC"), ("3.13", "Asterisco", "Asterisco", "AC"),
                        ("3.14", "Diéresis", "Trema (pingüino)", "BC"), ("3.15", "Apóstrofo", "Apóstrofo", "C")]:
    N(O, ref, es, pt, grupos=gr, contr=["CT-PONTUACAO-INVERTIDA"] if ref == "3.6" else [],
      resumo={"3.1": {"B1": "Ponto e seguido, ponto parágrafo e ponto final na organização do texto.", "B2": "Sem ponto em títulos, datas e assinaturas."},
              "3.2": {"B1": "Sem vírgula na relativa especificativa; vocativo; datas em cartas; aposto; antes de aunque.", "B2": "Incisos, comentários, advérbios oracionais, verbo elidido."},
              "3.3": {"B1": "Citação em estilo direto.", "B2": "Esquemas, citações literárias, fechamento de enumeração."}}.get(ref, {}))
N(O, "3.8", "Corchetes", "Colchetes", grupos="BC")
N(O, "3.9", "Comillas", "Aspas (« »)")
N(O, "3.10", "Guion", "Hífen")
N(O, "3.11", "Raya", "Travessão")
N(O, "4", "Abreviaturas y siglas", "Abreviaturas e siglas", v=False)

# ---------------------------------------------------------------- FUNCIONES
F = "FUN"
N(F, "1", "Dar y pedir información", "Dar e pedir informação")
N(F, "1.1", "Identificar", "Identificar", contr=["CT-SUJEITO-NULO"], resumo={
    "A1": "Yo soy Laura, ¿y tú?; mi/tu/su + nome; este/ese/aquel; esto.",
    "A2": "El (jersey) azul; A mí me encanta…; A Mario y a Cristina."})
N(F, "1.2", "Pedir información", "Pedir informação", resumo={
    "A1": "¿Quién es?, ¿Qué es esto?, ¿Dónde vives?, ¿De dónde eres?, ¿A qué te dedicas?, ¿Cuántos años tienes?, ¿Por qué…?",
    "A2": "¿Con/Para quién…?, ¿De quién es…?, ¿Qué tipo de…?, ¿Cuándo…?, ¿Para qué…?, ¿Alguna vez…?, ¿Qué tal + SN?",
    "B1": "¿Sabes si/dónde…?, ¿Podrías decirme…?, ¿Cuál de estos…?, ¿Desde/Hasta cuándo…?",
    "B2": "Me gustaría saber si…; ¿Qué fue lo que pasó?; ¿Puedo hacerte una pregunta?"})
N(F, "1.3", "Dar información", "Dar informação", resumo={
    "A1": "Dados pessoais, lugar (Aquí, En la mesa), hora (Son las seis), finalidade (para + inf.), causa (porque); corrigir (No, no es alemana).",
    "A2": "Pessoa (Con mis padres), modo (En metro, Muy despacio), tempo e frequência (La semana pasada, nunca, desde hace dos años)."})
N(F, "1.4", "Pedir confirmación", "Pedir confirmação", v=False)
N(F, "2", "Expresar opiniones, actitudes y conocimientos", "Expressar opiniões, atitudes e conhecimentos")
N(F, "2.1", "Pedir opinión", "Pedir opinião", v=False)
N(F, "2.2", "Dar una opinión", "Dar opinião", v=False, nota="B2: No creo que + subjuntivo.")
N(F, "2.4", "Valorar", "Avaliar", resumo={
    "A1": "(Muy/Bastante) bien/mal; Es muy/bastante/un poco + adj.",
    "A2": "Está muy bien / no está mal; demasiado; no es nada + adj.; ¡Qué barato!; ¡Estupendo!"})
N(F, "2.5", "Expresar aprobación y desaprobación", "Aprovar e desaprovar", resumo={
    "A1": "¡Muy bien!, ¡Muy mal! e gestos.", "A2": "(Esto) está (muy) bien/mal."})
N(F, "2.6", "Posicionarse a favor o en contra", "Posicionar-se a favor ou contra", v=False)
N(F, "2.9", "Expresar acuerdo", "Concordar", resumo={
    "B1": "Tienes razón; Yo pienso lo mismo; A mí también/tampoco me parece…; Estoy de acuerdo con/en…",
    "B2": "Comparto tu opinión; Lo veo igual; Por supuesto que…; acordo parcial (En líneas generales…)."})
N(F, "2.10", "Expresar desacuerdo", "Discordar", v=False)
N(F, "2.12", "Presentar un contraargumento", "Apresentar um contra-argumento", resumo={"A1": "Sí, pero…; repetir a opinião + pero (Es muy bonito, pero muy caro).", "A2": "Sí, es verdad, pero…; Sí, estoy de acuerdo, pero…"})
N(F, "2.13", "Expresar certeza y evidencia", "Expressar certeza", v=False)
N(F, "2.16", "Expresar duda e incredulidad", "Expressar dúvida", v=False, pre=["GRA-9.2.1"])
N(F, "2.17", "Expresar obligación y necesidad", "Expressar obrigação e necessidade", contr=["CT-TENER-QUE-HAY-QUE"], resumo={
    "A2": "Tienes que + inf. (pessoal); Hay que + inf. (impessoal)."})
N(F, "2.18", "Expresar falta de obligación o de necesidad", "Expressar ausência de obrigação", resumo={
    "A2": "No tienes que…; No hay que…"})
N(F, "2.20", "Expresar conocimiento", "Expressar conhecimento", contr=["CT-A-PESSOAL"], resumo={
    "A1": "Sé + SN/inf.; Conozco Bolivia / Conozco a Leticia.",
    "A2": "Sé un poco de…; Sé que…; Conozco muy bien a…; He aprendido…"})
N(F, "2.21", "Expresar desconocimiento", "Dizer que não sabe ou não conhece", resumo={"A1": "No sé + SN/inf.; No conozco Granada / No conozco a Sonia.", "A2": "No conozco muy bien…; No conozco mucho a Pedro."})
N(F, "2.22", "Preguntar por la habilidad para hacer algo", "Perguntar se alguém sabe fazer algo", resumo={
    "A1": "¿Sabes griego? ¿Sabes tocar la guitarra?", "A2": "¿Sabes tocar bien…? ¿Puedes pronunciar…?"})
N(F, "2.23", "Expresar habilidad para hacer algo", "Dizer que sabe fazer algo", resumo={
    "A1": "Sé nadar.", "A2": "Sé cocinar bastante bien; Puedo ayudarte."})
N(F, "3", "Expresar gustos, deseos y sentimientos", "Expressar gostos, desejos e sentimentos", contr=["CT-GUSTAR"])
N(F, "3.2", "Expresar gustos e intereses", "Expressar gostos e interesses", contr=["CT-GUSTAR", "CT-DUPLICACAO"], pre=["GRA-7.1.3"], resumo={
    "A1": "(No) me gusta (mucho) + SN/inf. (só 1.ª pessoa).",
    "A2": "Paradigma completo (A nosotros no nos gusta nada…); me encanta; me interesa; ¡Qué interesante!"})
N(F, "3.4", "Preguntar por preferencias", "Perguntar preferências", resumo={
    "A1": "¿Té o café?", "A2": "¿Qué/Cuál prefieres…?; ¿Te gusta más…?; ¿Cuál es tu color favorito?"})
N(F, "3.5", "Expresar preferencia", "Expressar preferência", resumo={
    "A1": "Prefiero un café / bailar.", "A2": "Me gusta más el té que el café."})
N(F, "3.7", "Preguntar por deseos", "Perguntar desejos", resumo={"A2": "¿Quieres…?; ¿Te gustaría…?; ¿Qué quieres hacer?"})
N(F, "3.8", "Expresar deseos", "Expressar desejos", resumo={
    "A1": "Quiero + SN/inf.", "A2": "Me gustaría + inf.",
    "B1": "Quiero que + subj.; Tengo ganas de…; Espero que…; ¡A ver si…!; Ojalá; Que te mejores.",
    "B2": "Quisiera que + imperf. subj.; Me hace ilusión…; Ojalá pudiera…"})
N(F, "3.9", "Preguntar por planes e intenciones", "Perguntar por planos", resumo={"A1": "Presente + marcador de futuro (¿Trabajas mañana?).", "A2": "¿Vas a + inf.?"})
N(F, "3.14", "Expresar placer y diversión", "Expressar prazer e diversão", resumo={"A2": "¡Qué divertido!"})
N(F, "3.17", "Expresar enfado e indignación", "Expressar irritação", resumo={"A2": "Estoy (muy) enfadado."})
N(F, "3.30", "Expresar sensaciones físicas", "Expressar sensações físicas", contr=["CT-GUSTAR"], resumo={
    "A2": "Tengo sed/hambre/frío/sueño; Me duele la cabeza / Me duelen los pies; Estoy enfermo."})
N(F, "4", "Influir en el interlocutor", "Influenciar o interlocutor")
N(F, "4.1", "Dar una orden o instrucción", "Dar ordem ou instrução", pre=["GRA-9.3"], resumo={
    "A1": "¡Silencio, por favor! Más despacio, por favor. ¿Puedes repetir?",
    "A2": "Tienes que…; imperativo (Baja las escaleras); ¿Puedes + inf.?; Hay que…"})
N(F, "4.3", "Pedir objetos", "Pedir objetos", resumo={
    "A1": "Un café, por favor.", "A2": "¿Me das/traes…?; ¿Nos trae la cuenta?; No tengo bolígrafo (pedido indireto)."})
N(F, "4.4", "Pedir ayuda", "Pedir ajuda", resumo={"A1": "Por favor (com gesto).", "A2": "¡Socorro!; ¿Me ayudas?; Perdona, ¿puedes ayudarme?"})
N(F, "4.7", "Responder a una orden, petición o ruego", "Responder a ordens e pedidos", resumo={
    "A1": "Sí, sí / No.", "A2": "Sí, claro; Vale; Bueno, vale; No sé…; Lo siento, pero no puedo."})
N(F, "4.8", "Pedir permiso", "Pedir permissão", grupos="ABC", resumo={
    "B1": "¿Se puede…?; ¿Podría…?; ¿Te importa si…?; ¿Me dejas…?",
    "B2": "¿Te importaría que…?; ¿Sería posible…?; ¿Me das permiso para…?"})
N(F, "4.9", "Dar permiso", "Dar permissão", resumo={"A1": "Sí.", "A2": "Sí, claro; Sí, sí, ábrela."})
N(F, "4.10", "Denegar permiso", "Negar permissão", resumo={
    "A1": "No, lo siento.", "A2": "Perdona, pero…; No, está prohibido."})
N(F, "4.13", "Proponer y sugerir", "Propor e sugerir")
N(F, "4.14", "Ofrecer e invitar", "Oferecer e convidar")
N(F, "4.15", "Solicitar confirmación de una propuesta previa", "Confirmar uma proposta")
N(F, "4.16", "Aceptar una propuesta, ofrecimiento o invitación", "Aceitar proposta ou convite", resumo={
    "A1": "Sí, gracias.", "A2": "Vale, ¿por qué no?; De acuerdo; Sí, pero más tarde."})
N(F, "4.17", "Rechazar una propuesta, ofrecimiento o invitación", "Recusar proposta ou convite", resumo={"A1": "No, (muchas) gracias."})
N(F, "4.18", "Aconsejar", "Aconselhar", resumo={
    "A2": "Puedes…; Tienes que…; Hay que…; imperativo; ¿Por qué no…?; Es necesario…"})
N(F, "4.23", "Ofrecerse para hacer algo", "Oferecer-se para fazer algo", resumo={
    "B1": "¿Quieres que te + subj.?; Puedo + inf.", "B2": "¿Te echo una mano?; Déjame que te ayude."})
N(F, "4.24", "Tranquilizar y consolar", "Tranquilizar e consolar", grupos="BC")
N(F, "4.25", "Animar", "Animar", grupos="BC")
N(F, "5", "Relacionarse socialmente", "Relacionar-se socialmente")
N(F, "5.1", "Saludar", "Cumprimentar", resumo={
    "A1": "Hola; Buenos días/tardes/noches.", "A2": "Hola, ¿qué tal?; escrito: Querido Antonio:",
    "B1": "Escrito formal: Estimado Sr. Antúnez:", "B2": "¡Hombre, Pepe!; ¡Cuánto tiempo!"})
N(F, "5.2", "Responder a un saludo", "Responder a um cumprimento", resumo={"A1": "Hola; Buenos días/tardes/noches.", "A2": "(Muy) bien, gracias, ¿y tú/usted?", "C1": "No me puedo quejar; Aquí estamos; Tirando."})
N(F, "5.3", "Dirigirse a alguien", "Dirigir-se a alguém")
N(F, "5.4", "Presentar a alguien", "Apresentar alguém", resumo={
    "A1": "Esta es Ana; Hola, soy Pedro / me llamo…", "A2": "Te presento a…; Le presento a la Sra…",
    "B1": "Ven que te presente; Me gustaría presentarle a…", "B2": "¿Me permite presentarle a…?; Mi nombre es…"})
N(F, "5.5", "Responder a una presentación", "Responder a uma apresentação", resumo={"A1": "Encantado; Hola, ¿qué tal?", "A2": "Mucho gusto."})
N(F, "5.9", "Responder a una bienvenida", "Responder às boas-vindas")
N(F, "5.10", "Disculparse", "Pedir desculpas", resumo={"A1": "Perdón.", "A2": "Lo siento mucho; Perdona/Perdone; Siento llegar tarde.", "C1": "Mil perdones; Disculpa que no te haya saludado."})
N(F, "5.11", "Responder a una disculpa", "Responder a um pedido de desculpas")
N(F, "5.12", "Agradecer", "Agradecer", resumo={"A1": "(Muchas) gracias.", "C1": "Gracias de antemano; Muy amable de tu parte; Te debo una (C2)."})
N(F, "5.13", "Responder a un agradecimiento", "Responder a um agradecimento", resumo={"C1": "No hay de qué; Faltaría más.", "C2": "No se merecen; Para servirle."})
N(F, "5.14", "Dar el pésame", "Dar os pêsames")
N(F, "5.15", "Proponer un brindis", "Propor um brinde")
N(F, "5.16", "Felicitar", "Felicitar")
N(F, "5.17", "Formular buenos deseos", "Desejar coisas boas", pre=["GRA-9.2.1"], resumo={
    "B1": "Que te diviertas; Mucha suerte; Que te vaya bien; Que te mejores.",
    "B2": "Crucemos los dedos; Que te lo pases fenomenal; Que te pongas bien pronto."})
N(F, "5.21", "Despedirse", "Despedir-se", resumo={
    "A1": "¡Adiós!; Hasta mañana; Hasta el jueves; ¡Chao!", "A2": "¡Hasta luego!; escrito: Besos, Un abrazo.",
    "B1": "Hasta ahora; Hasta el próximo lunes; escrito: Un beso, Atentamente.",
    "B2": "A ver si nos vemos pronto; escrito formal: Sin otro particular, les saluda atentamente."})
N(F, "6", "Estructurar el discurso", "Estruturar a conversa")
N(F, "6.1", "Establecer la comunicación y reaccionar", "Iniciar o contato e reagir", resumo={
    "A1": "¡Eh!; Por favor; ¿Sí?", "A2": "Perdona/Perdone; Oye/Oiga; ¿Dígame? (telefone)."})
N(F, "6.2", "Saludar y responder a un saludo", "Cumprimentar e responder (na conversa)")
N(F, "6.3", "Preguntar por una persona y responder", "Perguntar por alguém (pessoalmente e ao telefone)", grupos="BC", resumo={
    "B1": "¿Podría hablar con…?; Ahora se pone; Se ha equivocado; ¿Quiere dejar un mensaje?",
    "B2": "¿Me pasas con…?; No se retire; Ahora le paso."})
N(F, "6.4", "Pedir una extensión o habitación y responder", "Pedir um ramal ou quarto")
N(F, "6.5", "Preguntar si se puede dejar un recado", "Perguntar se pode deixar recado")
N(F, "6.7", "Solicitar que comience un relato y reaccionar", "Pedir que alguém conte algo")
N(F, "6.8", "Introducir el tema del relato y reaccionar", "Começar a contar algo e reagir", resumo={
    "A2": "Sí, claro; ¿Sí?; Lo siento, es que tengo prisa.",
    "B1": "¿Sabes qué ha pasado?; Tengo que contarte una cosa; No, ¿qué pasó?",
    "B2": "¿Te has enterado de…?; ¿En serio?; ¡Vaya!, cuenta."})
N(F, "6.31", "Despedirse y responder a las despedidas", "Despedir-se e responder (na conversa)", grupos="AB")
N(F, "6.25", "Indicar que se desea continuar el discurso", "Indicar que quer continuar falando", grupos="BC")

# ---------------------------------------------------------------- TÁCTICAS Y ESTRATEGIAS PRAGMÁTICAS
T = "TAC"
N(T, "1", "Construcción e interpretación del discurso", "Construção e interpretação do discurso")
N(T, "1.1", "Mantenimiento del referente y del hilo discursivo", "Retomar o referente (pronomes, elipse)", contr=["CT-SUJEITO-NULO", "CT-OBJETO-RETOMADO"], resumo={
    "A1": "Retomar com pronomes, demonstrativos e possessivos; elipse do sujeito (Mi hermana se llama María y vive en Salamanca).",
    "A2": "Advérbios anafóricos (Allí viven sus padres); elipse do verbo; artigo definido na segunda menção."})
N(T, "1.2", "Marcadores del discurso", "Marcadores do discurso (conectores)", resumo={
    "A1": "y, también, pero, porque; tampoco; por ejemplo; ¿no?, ¿eh?",
    "A2": "por eso, entonces; primero, luego, después, por último; oye, mira.",
    "B1": "además, sobre todo, así que, por lo tanto, es que, aunque, sin embargo; en primer lugar…; o sea; en resumen; ¿sabes?",
    "B2": "no solo… sino también, de modo que, ya que, a pesar de, mientras que, de todos modos, mejor dicho, por cierto, respecto a…"})
N(T, "1.3", "La deixis", "Dêixis: aqui/ali, agora/amanhã, este/ese", resumo={"A1": "aquí, ahí, allí; ir/venir; este/ese/aquel; ahora, hoy, mañana; Yo me llamo Elena, ¿y tú?", "A2": "cerca, lejos, arriba, abajo; llevar/traer; después, ayer, anoche; Me duele la cabeza."})
N(T, "1.4", "Desplazamiento en el orden de los elementos oracionales", "Ordem das palavras: tema e rema", contr=["CT-DUPLICACAO"], resumo={
    "A1": "Sujeito posposto (Soy María; ¿Dónde está Rosa?); también/tampoco; Hay + indefinido (Hay un libro en la mesa).",
    "A2": "Anteposição com duplicação (A mí me encanta bailar); artigo definido na segunda menção."})
N(T, "1.5", "Cita y estilo indirecto", "Discurso direto e indireto", v=False, grupos="ABC")
N(T, "1.7", "La expresión de la negación", "Negar e corrigir", resumo={"A1": "No / No, soy italiano; negação repetida para corrigir (No, no está en la costa).", "A2": "todavía no; No ha venido en toda la semana."})
N(T, "1.6", "Valores ilocutivos de los enunciados interrogativos", "Perguntas que não são perguntas", resumo={
    "A1": "Pergunta real; saudação (¿Qué tal?).",
    "A2": "Pedido (¿Me das el pan?), oferta (¿Un café?), pergunta-eco, retórica.",
    "B1": "¿Te importa si…?; ¿Te ayudo?; controle de contato (¿eh?, ¿entiendes?).",
    "B2": "Ênfase (¿Quéee?); eco especificativo (¿Que cuándo me voy adónde?)."})
N(T, "1.8", "Significados interpretados", "Sentidos figurados", grupos="BC", resumo={
    "B2": "Comparações com animais (fuerte como un toro, está como una cabra); ponerse como un tomate."})
N(T, "2", "Modalización", "Modalização")
N(T, "2.1", "Intensificación y atenuación", "Intensificar e atenuar", v=False)
N(T, "2.3", "Focalización", "Focalização", grupos="BC")
N(T, "2.4", "Valores modales de la entonación", "Valores da entonação", resumo={
    "A1": "Final descendente na afirmação; ascendente na pergunta total; descendente na pergunta parcial.",
    "A2": "Pergunta parcial ascendente para mostrar interesse ou reclamar (¿Cuándo llegaste↑?)."})
N(T, "2.5", "Desplazamiento de la perspectiva temporal", "Tempos verbais com valor de atitude")
N(T, "3", "Conducta interaccional", "Cortesia e interação")
N(T, "3.1", "Cortesía verbal atenuadora", "Cortesia e atenuação", v=False)

# ---------------------------------------------------------------- GÉNEROS DISCURSIVOS
GE = "GEN"
N(GE, "1", "Géneros orales y escritos", "Gêneros orais e escritos")
N(GE, "1.3", "Géneros de transmisión escrita", "Gêneros escritos", resumo={
    "A1": "Ler bilhetes, cartazes, formulários de dados pessoais, folhetos turísticos, horários, menus, notas, postais e mensagens curtas (escrever formulários e postais).",
    "A2": "Ler anúncios, biografias curtas, cardápios, contos simplificados, rótulos, previsão do tempo, ofertas de emprego, receitas; escrever diários curtos, mensagens e cartas pessoais."})
N(GE, "2", "Muestras de géneros", "Modelos de textos", v=False)
N(GE, "3", "Macrofunciones", "Macrofunções textuais")
N(GE, "3.1", "Macrofunción descriptiva: personas", "Descrever pessoas", resumo={
    "B1": "Descrição objetiva e subjetiva com imperfeito; narrativa inserida.",
    "B2": "Descrição com comparações e expressões (Parece un palo)."})
N(GE, "3.2", "Macrofunción descriptiva: objetos", "Descrever objetos", resumo={
    "A1": "El tomate es rojo; frases de existência e qualidade.",
    "A2": "Descrição com partes, relações e uma pequena narrativa."})
N(GE, "3.3", "Macrofunción descriptiva: lugares", "Descrever lugares", resumo={
    "A1": "La casa de Andrea es grande. Hay un baño, una cocina…",
    "A2": "Percurso na casa (a la derecha, al fondo); comparação com outras casas."})
N(GE, "3.4", "Macrofunción narrativa", "Narrar", v=False)
N(GE, "3.5", "Macrofunción expositiva", "Expor", v=False)
N(GE, "3.6", "Macrofunción argumentativa", "Argumentar", v=False)

# ---------------------------------------------------------------- NOCIONES GENERALES
NG = "NG"
N(NG, "1", "Nociones existenciales", "Noções existenciais")
N(NG, "1.1", "Existencia, inexistencia", "Existência e inexistência", contr=["CT-HAY-ESTA"])
N(NG, "1.2", "Presencia, ausencia", "Presença e ausência")
N(NG, "2", "Nociones cuantitativas", "Noções quantitativas")
N(NG, "2.1", "Cantidad numérica", "Números e quantidade", resumo={
    "B1": "Ordinais 11.º–20.º; somar, subtrair; por ciento.", "B2": "cifra, millar, par/impar, porcentaje."})
N(NG, "2.2", "Cantidad relativa", "Quantidade relativa", contr=["CT-MUY-MUCHO"])
N(NG, "2.3", "Aumento, disminución", "Aumento e diminuição", grupos="BC")
N(NG, "2.4", "Proporción", "Proporção")
N(NG, "2.6", "Medidas", "Medidas (tamanho, distância, peso, temperatura)", v=False, resumo={
    "B1": "Medir, pesar, talla y número, a 100 km por hora, estamos a 18 grados.",
    "B2": "Largo, ancho, alto; frenar, acelerar; darse prisa."})
N(NG, "3", "Nociones espaciales", "Noções espaciais")
N(NG, "3.1", "Localización", "Localização", contr=["CT-HAY-ESTA"], resumo={
    "B1": "sitio, zona; en ninguna/todas partes.", "B2": "situado, aparcado; quedar; hallarse.",
    "C1": "ubicación, localizar.", "C2": "emplazamiento; esté donde esté; acá."})
N(NG, "3.2", "Posición", "Posição", v=False)
N(NG, "3.3", "Posición relativa", "Posição relativa (a la derecha, al fondo)")
N(NG, "3.4", "Distancia", "Distância")
N(NG, "3.6", "Orientación", "Orientação", v=False)
N(NG, "3.7", "Orden", "Ordem", grupos="ABC")
N(NG, "4", "Nociones temporales", "Noções temporais")
N(NG, "4.1", "Referencias generales", "Referências de tempo (horas, datas, estações)")
N(NG, "4.2", "Localización en el tiempo", "Localizar no tempo (presente, passado, futuro)", resumo={
    "B1": "llevar + gerundio; últimamente; ya / todavía no; por el momento.",
    "C1": "actualidad, de momento, de ahora en adelante.", "C2": "hoy por hoy, a día de hoy, en tiempos de Maricastaña."})
N(NG, "4.3", "Aspectos de desarrollo", "Duração, frequência, começo e fim, mudança")
N(NG, "5", "Nociones cualitativas", "Noções qualitativas (forma, cor, material…)", v=False)
N(NG, "5.12", "Color", "Cores", v=False)
N(NG, "6", "Nociones evaluativas", "Noções avaliativas")
N(NG, "6.3", "Atractivo", "Atrativo")
N(NG, "6.4", "Calidad", "Qualidade")
N(NG, "6.5", "Aceptabilidad", "Aceitabilidade")
N(NG, "6.6", "Adecuación", "Adequação")
N(NG, "7", "Nociones mentales", "Noções mentais (pensar, saber, lembrar)", v=False)

# ---------------------------------------------------------------- NOCIONES ESPECÍFICAS (20 temas)
E = "NE"
TEMAS = [
    ("1", "Individuo: dimensión física", "A pessoa: corpo e aparência", [("1.1", "Partes del cuerpo", "Partes do corpo"), ("1.2", "Características físicas", "Características físicas")]),
    ("2", "Individuo: dimensión perceptiva y anímica", "A pessoa: sentidos e emoções", []),
    ("3", "Identidad personal", "Identidade pessoal", []),
    ("4", "Relaciones personales", "Relações pessoais", [("4.3", "Celebraciones y actos familiares, sociales y religiosos", "Celebrações"), ("4.4", "Actitudes y formas de comportarse", "Atitudes e comportamento")]),
    ("5", "Alimentación", "Alimentação", [("5.1", "Dieta y nutrición", "Dieta e nutrição"), ("5.2", "Bebida", "Bebidas"), ("5.3", "Alimentos", "Alimentos"),
                                          ("5.4", "Recetas", "Receitas"), ("5.5", "Platos", "Pratos"), ("5.6", "Utensilios de cocina y mesa", "Utensílios de cozinha e mesa"), ("5.7", "Restaurante", "Restaurante")]),
    ("6", "Educación", "Educação", []),
    ("7", "Trabajo", "Trabalho", []),
    ("8", "Ocio", "Lazer", []),
    ("9", "Información y medios de comunicación", "Informação e meios de comunicação", []),
    ("10", "Vivienda", "Moradia", [("10.1", "Acciones relacionadas con la vivienda", "Ações ligadas à moradia"), ("10.2", "Características de la vivienda", "Características da moradia"),
                                    ("10.3", "Actividades domésticas", "Tarefas domésticas"), ("10.4", "Objetos domésticos", "Móveis e objetos da casa")]),
    ("11", "Servicios", "Serviços", []),
    ("12", "Compras, tiendas y establecimientos", "Compras e lojas", [("12.1", "Lugares, personas y actividades", "Lugares, pessoas e atividades"), ("12.2", "Ropa, calzado y complementos", "Roupas, calçados e acessórios"),
                                                                       ("12.3", "Alimentación", "Comprar comida"), ("12.4", "Pagos", "Pagamentos")]),
    ("13", "Salud e higiene", "Saúde e higiene", []),
    ("14", "Viajes, alojamiento y transporte", "Viagens, hospedagem e transporte", [("14.2", "Alojamiento", "Hospedagem")]),
    ("15", "Economía e industria", "Economia e indústria", []),
    ("16", "Ciencia y tecnología", "Ciência e tecnologia", []),
    ("17", "Gobierno, política y sociedad", "Governo, política e sociedade", []),
    ("18", "Actividades artísticas", "Atividades artísticas", []),
    ("19", "Religión y filosofía", "Religião e filosofia", []),
    ("20", "Geografía y naturaleza", "Geografia e natureza", []),
]
NE_RESUMO = {
    "1.1": {"A1": "pelo, ojo, nariz.", "A2": "cabeza, cara, brazo, mano, dedo, pierna, pie; oído, muela, garganta, estómago, espalda."},
    "5.1": {"A1": "desayuno, comida, merienda, cena e os verbos.", "A2": "tener hambre, ser vegetariano.",
            "C1": "alimento básico, ser de buen comer, hacerse la boca agua.", "C2": "atiborrarse, darse un atracón, matar el gusanillo."},
    "5.2": {"A1": "agua con/sin gas, leche, té, café solo/con leche/cortado, cerveza, vino blanco/tinto.", "A2": "zumo, infusión, botella, lata, tener sed, tomar algo."},
    "5.3": {"A1": "carne, pescado, fruta, verdura, huevos, pan, bocadillo.", "A2": "frutas, legumes, laticínios, peixes, arroz, temperos, jamón serrano.",
            "C1": "perdiz, centollo, acelgas, golosinas.", "C2": "requesón, cochinillo, níscalo, migaja."},
    "5.4": {"A2": "receta, ingrediente, cocinar, llevar (salsa)."},
    "5.5": {"A1": "primer/segundo plato, postre, sopa, ensalada, paella, tortilla.", "A2": "plato combinado, tapa, aperitivo, rico."},
    "5.6": {"A2": "plato, vaso, taza, botella, servilleta.", "C1": "vajilla, cubertería, cucharón, colador.", "C2": "espumadera, rallador, escurridor."},
    "5.7": {"A1": "bar, restaurante, camarero, mesa, el menú, la cuenta.", "A2": "cafetería, reservar una mesa, pedir la carta, el menú del día."},
    "10.2": {"A1": "casa, piso, habitación, cocina, baño, ascensor, terraza; viejo/nuevo, bien comunicado.", "A2": "edificio, pasillo, suelo, techo, pared; amueblado."},
    "10.4": {"A1": "mesa, silla, cama, sofá, armario, ducha; radio, televisión.", "A2": "nevera, lavadora, lavaplatos, microondas."},
    "12.3": {"A2": "docena, lata, paquete, caja, bote, litro, kilo, medio kilo, cien gramos; hacer la lista de la compra."},
    "14.2": {"A1": "hotel, habitación doble/individual, con baño.", "A2": "pensión completa, media pensión, hacer una reserva."},
}
for ref, es, pt, subs in TEMAS:
    N(E, ref, es, pt, v=True, contr=["CT-HETEROSEMANTICOS", "CT-HETEROGENERICOS"])
    for sref, ses, spt in subs:
        N(E, sref, ses, spt, resumo=NE_RESUMO.get(sref, {}), grupos="BC" if sref == "4.4" else "ABC")

# ---------------------------------------------------------------- CULTURA (fases)
R = "REF"
N(R, "1", "Conocimientos generales de los países hispanos", "Conhecimentos gerais dos países hispânicos")
N(R, "1.1", "Geografía física", "Geografia física", resumo={"A": "Estações (e sua ausência em alguns países); Andes, Amazonas, Pampa, Titicaca, estreito de Gibraltar; Celsius × Fahrenheit.", "B": "Rios, lagos, vulcões e desertos; fauna e flora (lhama, cóndor, lince ibérico).", "C": "Zonas climáticas; picos e cascatas; espécies ameaçadas."})
N(R, "1.9", "Medios de transporte", "Meios de transporte", resumo={"A": "Grandes aeroportos e companhias aéreas; redes de metrô e ônibus; Rodovia Pan-Americana.", "B": "Estações (Atocha, Retiro); Canal do Panamá; segurança viária.", "C": "Trens míticos; portos e estaleiros; pedágios."})
N(R, "2", "Acontecimientos y protagonistas del pasado y del presente", "Fatos e personagens do passado e do presente", v=False)
N(R, "3", "Productos y creaciones culturales", "Produtos e criações culturais", v=False)
S = "SAB"
N(S, "1", "Condiciones de vida y organización social", "Condições de vida e organização social")
N(S, "1.1", "Identificación personal", "Nomes, sobrenomes e documentos", resumo={"A": "Dois sobrenomes (paterno e materno); a mulher mantém os sobrenomes ao casar; nomes compostos com María; apelidos familiares (Mamen, Fran); DNI e passaporte.", "B": "Nomes regionais (Rocío, Covadonga); trâmites de documentos.", "C": "Origem dos nomes; apelidos e títulos."})
N(S, "1.13", "Viajes, alojamiento y transporte", "Viagens, hospedagem e transporte", resumo={"A": "Tipos de passagem (ida e volta); onde comprar; hotéis e hostales; metrô, ônibus e táxi: filas, pagar ao motorista, táxi branco em Madri.", "B": "Turismo rural, casas rurales; trens de alta velocidade (AVE); normas no transporte público.", "C": "Paradores; carteira por pontos."})
N(S, "1.4", "Comidas y bebidas", "Comidas e bebidas", resumo={
    "A": "Horários das refeições; tapa e merienda; ordem do menu (primero, segundo, postre); ¡Que aproveche!; tipos de bar e como pedir.",
    "B": "Produtos regionais e denominação de origem; ir de tapas; sobremesa; gorjeta e livro de reclamações.",
    "C": "Mudanças de hábitos; origem de pratos típicos; menu de Natal."})
N(S, "2", "Relaciones interpersonales", "Relações interpessoais", v=False)
N(S, "3", "Identidad colectiva y estilo de vida", "Identidade coletiva e estilo de vida", v=False)
N("INT", "1", "Configuración de una identidad cultural plural", "Identidade cultural plural", v=False)
N("INT", "2", "Asimilación de los saberes culturales", "Assimilar saberes culturais", v=False)
N("INT", "3", "Interacción cultural", "Interação cultural", v=False)
N("INT", "4", "Mediación intercultural", "Mediação intercultural", v=False)
N("APR", "1", "Procedimientos de aprendizaje", "Como aprender: planejar, monitorar, avaliar", v=False,
  nota="No app vira o painel de progresso e as dicas de estudo (revisão espaçada, recuperação ativa).")

# ---------------------------------------------------------------- ESTRUTURA DA FRASE (camada do app)
EF = "EF"
for ref, es, pt, gr, c, refs in [
    ("1", "Sujeto nulo", "Sujeito omitido", "A", ["CT-SUJEITO-NULO"], ["GRA-7.1.1", "TAC-1.1"]),
    ("2", "Objeto retomado con pronombre", "Objeto retomado por pronome (lo/la)", "A", ["CT-OBJETO-RETOMADO"], ["GRA-7.1.2", "GRA-12.2"]),
    ("3", "Duplicación de pronombres", "Duplicação de pronomes (le… a Juan; a mí me)", "A", ["CT-DUPLICACAO"], ["GRA-7.1.3", "GRA-7.1.6", "TAC-1.4"]),
    ("4", "Combinación y colocación de pronombres", "Combinar e posicionar pronomes (se lo, dámelo)", "AB", ["CT-COLOCACAO"], ["GRA-7.1.2", "GRA-7.1.3", "GRA-9.3"]),
    ("5", "Verbos pronominales", "Verbos pronominais (llamarse, irse, acordarse)", "AB", ["CT-VERBOS-PRONOMINAIS"], ["GRA-7.1.4"]),
    ("6", "Verbos como gustar", "Verbos como gustar (doler, encantar, parecer)", "A", ["CT-GUSTAR"], ["GRA-7.1.3", "FUN-3.2", "FUN-3.30"]),
    ("7", "Artículo y posesivo", "Artigo e possessivo (mi libro, otra vez)", "A", ["CT-ARTIGO-POSSESSIVO"], ["GRA-3.1", "GRA-3.2", "GRA-5"]),
    ("8", "Lo neutro y contracciones", "Lo neutro e contrações (del, al)", "AB", ["CT-LO-NEUTRO"], ["GRA-3.1", "GRA-2.6"]),
    ("9", "Elección del verbo", "Escolha do verbo (ser/estar, hay/está, tener que/hay que)", "AB", ["CT-SER-ESTAR", "CT-HAY-ESTA", "CT-TENER-QUE-HAY-QUE"], ["GRA-9", "GRA-12.1", "NG-1.1"]),
    ("10", "Preposiciones de régimen", "Preposições ('a' pessoal, en coche)", "AB", ["CT-A-PESSOAL"], ["GRA-12.2"]),
    ("11", "Se impersonal y pasivo", "Se impessoal e passivo (se alquila)", "B", ["CT-SE-IMPESSOAL"], ["GRA-7.1.4", "GRA-13.3"]),
]:
    N(EF, ref, es, pt, grupos=gr, v=True, contr=c, pre=refs, nota="Validado na pesquisa contrastiva (ver documento de fundamentos); remete às seções do PCIC em 'prerequisitos'.")

# ---------------------------------------------------------------- montagem
def node_id(inv, ref):
    return f"{inv}-{ref}"

def parent_ref(ref):
    return ref.rsplit(".", 1)[0] if "." in ref else None

def nivel_url(inv, grupos):
    if inv not in INV_URL:
        return PCIC + "indice.htm"
    t = INV_URL[inv]
    return PCIC + (t.format(g=GRUPO_URL[grupos[0]]) if "{g}" in t else t)

def main(out):
    ids = {node_id(n["inv"], n["ref"]) for n in NODES}
    nos = []
    for n in NODES:
        nid = node_id(n["inv"], n["ref"])
        pr = parent_ref(n["ref"])
        while pr and node_id(n["inv"], pr) not in ids:
            pr = parent_ref(pr)
        inv = INVENTARIOS[n["inv"]]
        por_fase = n["inv"] in ("PRO", "SAB", "REF", "INT")
        niveis = [lv for g in n["grupos"] for lv in NIVEIS[g]]
        inicio = n["inicio"] or next((lv for lv in niveis if lv in n["resumo"]), None) or niveis[0]
        nos.append({
            "id": nid,
            "inventario": n["inv"],
            "pcic_ref": None if n["inv"] == "EF" else n["ref"],
            "pai": node_id(n["inv"], pr) if pr else None,
            "profundidade": n["ref"].count(".") + 1,
            "titulo": {"es": n["es"], "pt": n["pt"]},
            "modulo": n["modulo"] or inv["modulo"],
            "componente": inv["componente"],
            "grupos": list(n["grupos"]),
            "niveis": niveis,
            "por_fase": por_fase,
            "nivel_inicio": inicio,
            "resumo": n["resumo"],
            "prerequisitos": [p for p in n["pre"] if p in ids or True],
            "contrastes": n["contr"],
            "verificado": n["v"],
            "fonte": None if n["inv"] == "EF" else nivel_url(n["inv"], n["grupos"]),
            "nota": n["nota"],
            "status": {lv: "estrutura" for lv in (["A", "B", "C"] if por_fase else niveis) if (lv in n["grupos"] if por_fase else True)},
        })
    mapa = {
        "versao": "1.0-etapa1",
        "gerado_em": "2026-11-14",
        "base": "Plan Curricular del Instituto Cervantes. Niveles de referencia para el español (2006/2007)",
        "base_url": PCIC + "indice.htm",
        "niveis": ["A1", "A2", "B1", "B2", "C1", "C2"],
        "inventarios": [{"id": k, **v} for k, v in INVENTARIOS.items()],
        "nos": nos,
    }
    Path(out).write_text(json.dumps(mapa, ensure_ascii=False, indent=1), encoding="utf-8")
    return mapa

if __name__ == "__main__":
    m = main(sys.argv[1] if len(sys.argv) > 1 else "mapa-a1-c2.json")
    print(len(m["nos"]), "nós")
