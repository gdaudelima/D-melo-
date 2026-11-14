"""Fichas A1 — Estrutura da frase (Lote 2.2): camada contrastiva + táticas discursivas do A1.
Os temas EF-2 (lo/la), EF-3 (duplicação), EF-4 (se lo, dámelo) e EF-8 (lo neutro) entram no A2, onde o PCIC os introduz."""
from fichas_base import F, salvar

TAC = "https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/06_tacticas_pragmaticas_inventario_a1-a2.htm"
L = []
def E(*a, **k):
    L.append(F(*a, **k))

E("EF-1", "Sujeto nulo", "Sujeito omitido",
  objetivo="Sou capaz de falar de mim e dos outros sem repetir o pronome sujeito.",
  regra="Em espanhol a terminação do verbo já diz quem faz a ação. O pronome só aparece para contrastar (Yo soy de Brasil, y ella, de Chile) ou para desfazer dúvida. Dentro de uma mesma frase, nunca se repete.",
  contraste="Português do Brasil: 'Eu acordo cedo, eu tomo café e eu vou trabalhar.' Espanhol: Me levanto temprano, desayuno y voy a trabajar.",
  exemplos=[("Me levanto temprano, desayuno y voy a trabajar.", "Eu acordo cedo, tomo café e vou trabalhar.", "Me levanto / desayuno / voy"),
            ("Mi hermana se llama María y vive en Salamanca.", "Minha irmã se chama Maria e mora em Salamanca.", "vive"),
            ("Yo soy de Brasil y ella es de Chile.", "Eu sou do Brasil e ela é do Chile.", "Yo / ella")],
  erros=[("Yo vivo en Recife y yo trabajo en un hospital.", "Vivo en Recife y trabajo en un hospital.", "O verbo já indica a pessoa.", "CT-SUJEITO-NULO"),
         ("Ella es mi amiga. Ella se llama Lía. Ella es médica.", "Es mi amiga. Se llama Lía y es médica.", "Depois da primeira menção, o sujeito some.", "CT-SUJEITO-NULO")],
  exs=[("achar-o-erro", "foco-na-forma", "Toque nos pronomes que sobram: Yo tengo 30 años. Yo soy profesora y yo vivo en Curitiba.", "Tengo 30 años. Soy profesora y vivo en Curitiba.", "Só use o pronome para contrastar."),
       ("escolha-em-contexto", "foco-na-forma", "—¿Quién habla inglés aquí? —(Hablo / Yo hablo) inglés.", "Yo hablo", "Aqui yo responde 'quem': é contraste."),
       ("producao-livre", "producao", "Grave 30 segundos apresentando um amigo sem repetir 'él/ella'.", None, None),
       ("fluencia-cronometrada", "fluencia", "Leia em voz alta 5 frases e corte os pronomes em tempo real.", None, None)],
  fonte=TAC)

E("EF-5", "Verbos pronominales básicos", "Verbos pronominais básicos",
  objetivo="Sou capaz de usar me llamo, me levanto, me ducho sem esquecer o pronome.",
  regra="Alguns verbos sempre levam o pronome da mesma pessoa: llamarse, levantarse, ducharse, acostarse. me/te/se/nos/os/se vêm antes do verbo conjugado.",
  contraste="No Brasil o pronome desses verbos cai ('levanto às 7', 'chamo Ana'); em espanhol ele é obrigatório.",
  exemplos=[("Me llamo Lucas.", "Meu nome é Lucas.", "Me"),
            ("¿A qué hora te levantas?", "A que horas você levanta?", "te"),
            ("Nos acostamos tarde.", "A gente vai dormir tarde.", "Nos")],
  erros=[("Levanto a las siete.", "Me levanto a las siete.", "levantarse é pronominal.", "CT-VERBOS-PRONOMINAIS"),
         ("Llamo Lucas.", "Me llamo Lucas.", "llamarse é pronominal.", "CT-VERBOS-PRONOMINAIS")],
  exs=[("lacuna", "foco-na-forma", "Mis hijos ___ duchan por la noche.", "se", None),
       ("montar-frase", "producao", "Monte: [las] [me] [a] [levanto] [ocho]", "Me levanto a las ocho.", None),
       ("producao-livre", "producao", "Descreva sua rotina da manhã com 3 verbos pronominais.", None, None)],
  fonte="https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/02_gramatica_inventario_a1-a2.htm")

E("EF-6", "Gustar: la cosa es el sujeto", "Gustar: quem 'manda' no verbo é a coisa",
  objetivo="Sou capaz de montar frases com gustar sem a estrutura do português.",
  regra="Pense em gustar como 'agradar': Me gusta el café = O café me agrada. Por isso: sem 'de', com artigo, e o verbo concorda com a coisa (me gustan los perros).",
  contraste="'Eu gosto de café' → Me gusta el café. 'Eu gosto de cachorros' → Me gustan los perros.",
  exemplos=[("Me gusta el café.", "Gosto de café.", "gusta el café"),
            ("Me gustan los perros.", "Gosto de cachorros.", "gustan los perros"),
            ("Me gusta mucho bailar.", "Gosto muito de dançar.", "gusta… bailar")],
  erros=[("Yo gusto de los perros.", "Me gustan los perros.", "A coisa é o sujeito; sem 'de'.", "CT-GUSTAR"),
         ("Me gusta los perros.", "Me gustan los perros.", "Plural da coisa → gustan.", "CT-GUSTAR"),
         ("Me gusta de bailar.", "Me gusta bailar.", "Sem 'de'.", "CT-GUSTAR")],
  exs=[("transformar", "foco-na-forma", "Passe para espanhol: Eu gosto de livros.", "Me gustan los libros.", None),
       ("montar-frase", "producao", "Monte: [gustan] [no] [me] [las] [discotecas]", "No me gustan las discotecas.", None),
       ("producao-livre", "producao", "Conte do que você gosta na sua cidade (3 frases).", None, None)],
  fonte="https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/05_funciones_inventario_a1-a2.htm")

E("EF-7", "Artículo y posesivo; otro", "Artigo com possessivo e com otro",
  objetivo="Sou capaz de usar possessivos e otro sem artigo.",
  regra="Antes do nome, possessivo e demonstrativo substituem o artigo: mi casa, este libro. otro também não leva un: otro día. O artigo definido vem antes de otro: la otra chica.",
  contraste="Português: 'a minha casa', 'um outro dia'. Espanhol: mi casa, otro día.",
  exemplos=[("Mi casa es pequeña.", "A minha casa é pequena.", "Mi"),
            ("Este libro es muy bueno.", "Este livro é muito bom.", "Este"),
            ("Otro día, por favor.", "Um outro dia, por favor.", "Otro"),
            ("La otra chica es mi prima.", "A outra moça é minha prima.", "La otra")],
  erros=[("La mi casa es pequeña.", "Mi casa es pequeña.", "Sem artigo antes do possessivo.", "CT-ARTIGO-POSSESSIVO"),
         ("Quiero un otro café.", "Quiero otro café.", "otro sem un.", "CT-ARTIGO-POSSESSIVO"),
         ("el este libro", "este libro", "Demonstrativo sem artigo.", None)],
  exs=[("achar-o-erro", "foco-na-forma", "Mi hermano vive con la su novia.", "Mi hermano vive con su novia.", None),
       ("achar-o-erro", "foco-na-forma", "Necesito una otra silla.", "Necesito otra silla.", None)],
  fonte="https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/02_gramatica_inventario_a1-a2.htm")

E("EF-9", "Elegir el verbo: ser, estar, hay", "Escolher o verbo: ser, estar, hay",
  objetivo="Sou capaz de escolher entre ser, estar e hay para identificar, localizar e dizer que algo existe.",
  regra="ser = o que/quem é (Es un banco; Soy profesora). estar = onde está algo já conhecido (El banco está en la esquina). hay = existe algo novo, sem artigo definido (Hay un banco en mi calle). tener nunca indica existência.",
  contraste="Português: 'Tem um banco na minha rua' e 'o banco fica na esquina'. Espanhol: Hay un banco en mi calle; El banco está en la esquina.",
  exemplos=[("Hay un banco en mi calle.", "Tem um banco na minha rua.", "Hay un"),
            ("El banco está en la esquina.", "O banco fica na esquina.", "El banco está"),
            ("Es un banco muy grande.", "É um banco muito grande.", "Es")],
  erros=[("Tiene un banco en mi calle.", "Hay un banco en mi calle.", "Existência: hay, não tener.", "CT-HAY-ESTA"),
         ("Hay el banco en la esquina.", "El banco está en la esquina.", "Algo já conhecido: está.", "CT-HAY-ESTA"),
         ("El banco es en la esquina.", "El banco está en la esquina.", "Lugar de algo: estar.", "CT-SER-ESTAR")],
  exs=[("escolha-em-contexto", "foco-na-forma", "En mi barrio (hay / está / tiene) un parque.", "hay", None),
       ("escolha-em-contexto", "foco-na-forma", "¿Dónde (hay / está) la estación?", "está", "A estação é conhecida: está."),
       ("escolha-em-contexto", "foco-na-forma", "¿(Hay / Está) una farmacia cerca?", "Hay", None),
       ("producao-livre", "producao", "Descreva seu bairro: 3 frases com hay e 2 com está.", None, None)],
  imagem="cena-bairro",
  fonte="https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/02_gramatica_inventario_a1-a2.htm")

E("EF-10", "Preposiciones básicas: ir a, en coche, de", "Preposições básicas: ir a, en coche, de",
  objetivo="Sou capaz de dizer aonde vou e em que meio de transporte.",
  regra="Destino: ir a + lugar (Voy a Madrid; Voy al trabajo). Meio de transporte: en (en coche, en tren, en metro); exceção: a pie. Origem: ser de (Soy de Brasil).",
  contraste="Português: 'vou de carro'. Espanhol: voy en coche. 'Vou no mercado' → voy al mercado.",
  exemplos=[("Voy a trabajar en coche.", "Vou trabalhar de carro.", "en coche"),
            ("Voy al mercado.", "Vou ao mercado.", "al"),
            ("Voy a pie.", "Vou a pé.", "a pie")],
  erros=[("Voy de coche.", "Voy en coche.", "Transporte: en.", None),
         ("Voy en el mercado.", "Voy al mercado.", "Destino: a.", None)],
  exs=[("lacuna", "foco-na-forma", "Vengo a clase ___ metro.", "en", None),
       ("lacuna", "foco-na-forma", "Los sábados voy ___ gimnasio.", "al", None)],
  fonte=TAC)

E("TAC-1.2", "Conectores básicos: y, también, pero, porque", "Conectores básicos",
  objetivo="Sou capaz de ligar ideias com y, también, tampoco, pero, porque e por ejemplo.",
  regra="y soma; también concorda com algo afirmativo (Yo también); tampoco com algo negativo (Yo tampoco); pero opõe; porque explica; por ejemplo concretiza; ¿no? no fim pede confirmação.",
  contraste="'Eu também não' → Yo tampoco (uma palavra só).",
  exemplos=[("—No me gusta el té. —A mí tampoco.", "—Não gosto de chá. —Eu também não.", "tampoco"),
            ("Tengo un hijo, pero no estoy casado.", "Tenho um filho, mas não sou casado.", "pero"),
            ("Vives en Madrid, ¿no?", "Você mora em Madri, né?", "¿no?")],
  erros=[("Yo también no.", "Yo tampoco.", "Negativo: tampoco.", None)],
  exs=[("escolha-em-contexto", "foco-na-forma", "—No hablo alemán. —Yo (también / tampoco).", "tampoco", None),
       ("producao-livre", "producao", "Escreva 3 frases sobre seus gostos usando pero e porque.", None, None)],
  fonte=TAC)

E("TAC-1.3", "Deixis: aquí, ahí, allí; ir y venir", "Aqui, aí, ali; ir e vir",
  objetivo="Sou capaz de indicar lugares e tempo em relação a mim: aquí, allí, hoy, mañana.",
  regra="aquí (perto de mim), ahí (perto de você), allí (longe). ir = movimento para longe de quem fala; venir = para onde está quem fala. Tempo: ahora, hoy, mañana.",
  contraste="Como no português 'ir/vir'; na América prefere-se acá e allá.",
  exemplos=[("Voy a trabajar en coche.", "Vou trabalhar de carro.", "Voy"),
            ("Mañana es mi cumpleaños.", "Amanhã é meu aniversário.", "Mañana"),
            ("¿Qué es eso? —Un rotulador.", "O que é isso? —Uma caneta marcadora.", "eso")],
  erros=[],
  exs=[("lacuna", "foco-na-forma", "¿Vienes a mi casa? —Sí, ___ ahora.", "voy", "Do ponto de vista de quem responde, é ir."),
       ("escolha-em-contexto", "foco-na-forma", "El libro está (aquí / allí), en mi mano.", "aquí", None)],
  fonte=TAC)

E("TAC-1.4", "Información nueva: hay + indefinido; también/tampoco", "Ordem da informação: novo e conhecido",
  objetivo="Sou capaz de apresentar algo novo com hay + un/una e retomar com el/la.",
  regra="Informação nova: Hay + un/una + lugar (Hay un libro en la mesa) ou Es + una… (Es una película muy interesante). Ao falar dela de novo: el/la (El libro es de Ana).",
  contraste="Mesma lógica do português, mas com hay no lugar de 'tem'.",
  exemplos=[("Hay un libro en la mesa. El libro es de Ana.", "Tem um livro na mesa. O livro é da Ana.", "un → El"),
            ("Soy María.", "Sou a Maria.", "Soy María")],
  erros=[("Tiene un libro en la mesa.", "Hay un libro en la mesa.", "Existência: hay.", "CT-HAY-ESTA")],
  exs=[("lacuna", "foco-na-forma", "Hay ___ gato en el jardín. ___ gato es negro.", ["un", "El"], None)],
  fonte=TAC)

E("TAC-1.7", "La negación", "Negar e corrigir",
  objetivo="Sou capaz de responder 'não' e corrigir uma informação.",
  regra="No antes do verbo. Para corrigir, repete-se o no: —Madrid está en la costa. —No, no está en la costa. Para concordar com uma negação: —No es difícil. —No, no es difícil.",
  contraste="Igual ao português; a dupla negação também existe ('Não, não está').",
  exemplos=[("—¿Eres griego? —No, soy italiano.", "—Você é grego? —Não, sou italiano.", "No"),
            ("—Madrid está en la costa. —No, no está en la costa.", "—Madri fica no litoral. —Não, não fica no litoral.", "No, no")],
  erros=[("Soy no español.", "No soy español.", "no vai antes do verbo.", None)],
  exs=[("transformar", "foco-na-forma", "Corrija: —Lima está en Chile.", "No, no está en Chile. Está en Perú.", None)],
  fonte=TAC)

if __name__ == "__main__":
    salvar(L, "a1-estrutura-da-frase.json")
