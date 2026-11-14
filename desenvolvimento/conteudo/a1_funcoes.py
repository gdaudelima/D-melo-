"""Fichas A1 — Funções comunicativas / expressões (Lote 2.3). Expoentes do A1 conferidos no inventário de Funciones A1-A2 do PCIC."""
from fichas_base import F, salvar

FUN = "https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/05_funciones_inventario_a1-a2.htm"
L = []
def X(no, es, pt, objetivo, regra, contraste, exemplos, erros, exs, **k):
    k.setdefault("fonte", FUN)
    L.append(F(no, es, pt, objetivo=objetivo, regra=regra, contraste=contraste, exemplos=exemplos, erros=erros, exs=exs, **k))

# ---- Relacionar-se socialmente (vem primeiro na trilha)
X("FUN-5.1", "Saludar", "Cumprimentar",
  "Sou capaz de cumprimentar a qualquer hora do dia.",
  "Hola (qualquer hora, informal). Buenos días (até o almoço, por volta das 14h na Espanha), buenas tardes (até escurecer), buenas noches (à noite, ao chegar e ao sair).",
  "Na Espanha a 'tarde' começa depois do almoço (14h–15h), não ao meio-dia. 'Bom dia' = Buenos días (no plural).",
  [("¡Hola!", "Oi!", "Hola"), ("Buenos días, señora.", "Bom dia, senhora.", "Buenos días"), ("Buenas noches.", "Boa noite.", "Buenas noches")],
  [("Buen día.", "Buenos días.", "Na Espanha o cumprimento vai no plural (Buen día se usa em partes da América).", None)],
  [("escolha-em-contexto", "entrada", "Imagem: relógio marcando 16h, Madri. Como cumprimentar?", "Buenas tardes", "Às 16h já é tarde na Espanha."),
   ("escolha-em-contexto", "entrada", "Imagem: 10h da manhã.", "Buenos días", None),
   ("producao-livre", "producao", "Grave como você cumprimenta o porteiro de manhã e à noite.", None, None)],
  imagem="relogio-saudacoes")

X("FUN-5.2", "Responder a un saludo", "Responder a um cumprimento",
  "Sou capaz de responder a um cumprimento.",
  "No A1 responde-se com a mesma fórmula: —Hola. —Hola. —Buenos días. —Buenos días. No A2: (Muy) bien, gracias, ¿y tú?",
  "Como no português.",
  [("—Buenos días. —Buenos días.", "—Bom dia. —Bom dia.", None), ("—Hola, ¿qué tal? —Bien, ¿y tú?", "—Oi, tudo bem? —Tudo, e você?", "¿y tú?")],
  [("—¿Qué tal? —Todo bien, ¿y tú? (traduzindo 'tudo bem')", "—¿Qué tal? —Bien, ¿y tú?", "'Tudo bem' não se traduz palavra por palavra; diga bien.", None)],
  [("escolha-em-contexto", "foco-na-forma", "—Buenas tardes. —___", "Buenas tardes.", None)])

X("FUN-5.4", "Presentarse y presentar a alguien", "Apresentar-se e apresentar alguém",
  "Sou capaz de me apresentar e apresentar alguém informalmente.",
  "Apresentar-se: Hola, soy… / Me llamo… + profissão (Soy estudiante de informática). Apresentar alguém: Este es Pedro / Esta es Ana (com gesto).",
  "Português: 'Esse é o Pedro'. Espanhol: Este es Pedro (sem artigo; este para quem está perto).",
  [("Hola, soy Pedro, ¿qué tal?", "Oi, sou o Pedro, tudo bem?", "soy"),
   ("Buenas tardes, me llamo Julio; soy estudiante.", "Boa tarde, meu nome é Julio; sou estudante.", "me llamo"),
   ("Esta es Ana.", "Essa é a Ana.", "Esta es")],
  [("Esta es la Ana.", "Esta es Ana.", "Nome próprio sem artigo.", None),
   ("Mi nombre es Pedro y yo soy profesor.", "Me llamo Pedro y soy profesor.", "Sem repetir yo.", "CT-SUJEITO-NULO")],
  [("montar-frase", "producao", "Monte: [me] [Ana] [y] [llamo] [soy] [enfermera]", "Me llamo Ana y soy enfermera.", None),
   ("producao-livre", "producao", "Apresente-se em 3 frases (nome, origem, profissão).", None, None)])

X("FUN-5.5", "Responder a una presentación", "Responder a uma apresentação",
  "Sou capaz de reagir quando me apresentam alguém.",
  "Encantado (homem) / Encantada (mulher); Hola, ¿qué tal?",
  "Encantado concorda com quem fala, não com quem é apresentado.",
  [("—Esta es Ana. —Encantado.", "—Essa é a Ana. —Prazer.", "Encantado"), ("—Este es Luis. —Hola, ¿qué tal?", "—Esse é o Luis. —Oi, tudo bem?", None)],
  [("(mulher falando) Encantado.", "Encantada.", "Concorda com quem fala.", None)],
  [("escolha-em-contexto", "foco-na-forma", "Você (mulher/homem) responde a uma apresentação: ___", ["Encantada", "Encantado"], None)])

X("FUN-5.10", "Disculparse", "Pedir desculpas",
  "Sou capaz de pedir desculpas de forma simples.",
  "A1: Perdón. A2: Lo siento (mucho); Perdona/Perdone.",
  "'Desculpa' → Perdón / Perdona. Lo siento = sinto muito.",
  [("¡Ay, perdón!", "Ai, desculpa!", "perdón"), ("Lo siento mucho.", "Sinto muito.", "Lo siento")],
  [("Disculpa me.", "Perdón.", "Não traduza literalmente.", None)],
  [("escolha-em-contexto", "entrada", "Você esbarra em alguém no metrô.", "¡Perdón!", None)])

X("FUN-5.12", "Agradecer", "Agradecer",
  "Sou capaz de agradecer e responder ao agradecimento.",
  "(Muchas) gracias. Resposta comum: De nada.",
  "'Obrigado/obrigada' → gracias (não muda com o gênero).",
  [("Muchas gracias.", "Muito obrigado.", "Muchas"), ("—Gracias. —De nada.", "—Obrigada. —De nada.", "De nada")],
  [("Muy gracias.", "Muchas gracias.", "gracias é substantivo: muchas.", "CT-MUY-MUCHO")],
  [("lacuna", "foco-na-forma", "___ gracias por todo.", "Muchas", None)])

X("FUN-5.21", "Despedirse", "Despedir-se",
  "Sou capaz de me despedir indicando quando nos vemos.",
  "¡Adiós!; Adiós, buenas noches; Hasta mañana; Hasta el + dia da semana (Hasta el jueves); ¡Chao! (informal). A2: ¡Hasta luego!",
  "'Até quinta' → Hasta el jueves (com artigo antes do dia da semana).",
  [("Hasta mañana.", "Até amanhã.", "Hasta mañana"), ("Hasta el jueves.", "Até quinta.", "el jueves"), ("¡Adiós, buenas noches!", "Tchau, boa noite!", None)],
  [("Hasta jueves.", "Hasta el jueves.", "Dia da semana com artigo.", None)],
  [("lacuna", "foco-na-forma", "Hasta ___ lunes.", "el", None),
   ("producao-livre", "producao", "Despeça-se de um colega que você só verá na sexta.", "Hasta el viernes.", None)])

X("FUN-6.1", "Llamar la atención y reaccionar", "Chamar a atenção e reagir",
  "Sou capaz de chamar a atenção de alguém e reagir quando me chamam.",
  "A1: ¡Eh!; Por favor; o nome (¿María?); reagir: Hola, ¿Sí? A2: Perdona/Perdone, Oye/Oiga, ¿Dígame? (telefone).",
  "'Ô, moço!' → Perdone / Oiga (formal) ou Oye (informal).",
  [("Por favor, ¿la cuenta?", "Por favor, a conta?", "Por favor"), ("—¡María! —¿Sí?", "—Maria! —Oi?", "¿Sí?")],
  [],
  [("escolha-em-contexto", "entrada", "Você quer chamar o garçom educadamente.", "Por favor", None)])

# ---- Dar e pedir informação
X("FUN-1.1", "Identificar", "Identificar pessoas e coisas",
  "Sou capaz de dizer quem sou, de quem é algo e o que é algo.",
  "Yo + verbo para contrastar (Yo soy Laura, ¿y tú?); mi/tu/su + nome; este/ese/aquel + nome (com gesto); esto/eso (Esto, por favor); nome próprio.",
  "Sem artigo antes do possessivo e do nome de pessoa.",
  [("Yo soy Laura, ¿y tú?", "Eu sou a Laura, e você?", "Yo / tú"), ("Mi teléfono es el 699 705 388.", "Meu telefone é 699 705 388.", "Mi"), ("Estos son mis padres.", "Esses são meus pais.", "Estos")],
  [("El mi teléfono es…", "Mi teléfono es…", "Sem artigo antes do possessivo.", "CT-ARTIGO-POSSESSIVO")],
  [("producao-livre", "producao", "Mostre uma foto e identifique 3 pessoas: Este es… Esta es…", None, None)],
  imagem="foto-familia")

X("FUN-1.2", "Pedir información", "Pedir informação",
  "Sou capaz de perguntar nome, origem, endereço, profissão, idade, hora e motivo.",
  "¿Cómo te llamas? ¿De dónde eres? ¿Dónde vives? ¿A qué te dedicas? / ¿Qué haces? ¿Cuántos años tienes? ¿Qué hora es? ¿Por qué…? ¿Qué es esto? ¿Quién es? Alternativa: ¿Té o café?",
  "'Quantos anos você tem?' → ¿Cuántos años tienes? (tener para idade). 'Com o que você trabalha?' → ¿A qué te dedicas?",
  [("¿De dónde eres?", "De onde você é?", "De dónde eres"), ("¿A qué te dedicas?", "Você trabalha com o quê?", "A qué te dedicas"), ("¿Cuántos años tienes?", "Quantos anos você tem?", "tienes")],
  [("¿Cuántos años eres?", "¿Cuántos años tienes?", "Idade com tener.", None), ("¿Qué edad tú tienes?", "¿Cuántos años tienes?", "Ordem e sujeito.", "CT-SUJEITO-NULO")],
  [("montar-frase", "foco-na-forma", "Monte: [años] [cuántos] [tienes]", "¿Cuántos años tienes?", None),
   ("producao-livre", "producao", "Escreva 5 perguntas para conhecer um colega novo.", None, None),
   ("fluencia-cronometrada", "fluencia", "Faça as 7 perguntas básicas em 40 segundos.", None, None)])

X("FUN-1.3", "Dar información", "Dar informação",
  "Sou capaz de dar meus dados, dizer onde algo está, a hora, o motivo e a finalidade.",
  "Dados: —¿Cómo te llamas? —Mikel. Lugar: Aquí / En la mesa. Hora: Son las seis. Finalidade: para + inf. Causa: porque… Corrigir: No, no es alemana. Es austriaca.",
  "'São seis horas' → Son las seis (com artigo). 'É uma hora' → Es la una.",
  [("Son las seis.", "São seis horas.", "Son las"), ("Estudio español para trabajar en Chile.", "Estudo espanhol para trabalhar no Chile.", "para"), ("—Katrin es alemana. —No, no es alemana. Es austriaca.", "—A Katrin é alemã. —Não, não é alemã. É austríaca.", "No, no")],
  [("Son seis horas.", "Son las seis.", "Hora com artigo, sem 'horas'.", None)],
  [("lacuna", "foco-na-forma", "—¿Qué hora es? —___ las tres.", "Son", None),
   ("lacuna", "foco-na-forma", "—¿Qué hora es? —___ la una.", "Es", None)],
  imagem="relogio-horas")

X("FUN-2.4", "Valorar", "Avaliar algo",
  "Sou capaz de dizer se algo é bom, interessante ou difícil.",
  "(Muy/Bastante) bien/mal; Regular; Es (muy/bastante/un poco) + adjetivo: El Museo del Prado es muy interesante.",
  "'Um pouco difícil' → un poco difícil (igual); 'mais ou menos' → regular / así, así.",
  [("El ejercicio es un poco difícil.", "O exercício é um pouco difícil.", "un poco"), ("—¿Qué tal? —Regular.", "—Como foi? —Mais ou menos.", "Regular")],
  [("Es mucho interesante.", "Es muy interesante.", "Adjetivo: muy.", "CT-MUY-MUCHO")],
  [("producao-livre", "producao", "Avalie 3 coisas da sua cidade com muy / bastante / un poco.", None, None)])

X("FUN-2.5", "Aprobar y desaprobar", "Aprovar e desaprovar",
  "Sou capaz de aprovar ou desaprovar de forma simples.",
  "¡Muy bien! / ¡Muy mal! e gestos com a cabeça.",
  "Como no português.",
  [("¡Muy bien!", "Muito bem!", None), ("¡Muy mal!", "Muito mal!", None)],
  [],
  [("escolha-em-contexto", "entrada", "Seu colega acerta todas as respostas.", "¡Muy bien!", None)])

X("FUN-2.12", "Contraargumentar: sí, pero", "Concordar em parte: sí, pero",
  "Sou capaz de concordar e acrescentar uma objeção.",
  "Sí, pero…; repetir a avaliação + pero: Es muy bonito, pero muy caro.",
  "'Mas' → pero (não más).",
  [("—Es muy difícil. —Sí, pero es muy interesante.", "—É muito difícil. —Sim, mas é muito interessante.", "Sí, pero"), ("Es muy bonito, pero muy caro.", "É muito bonito, mas muito caro.", "pero")],
  [("Sí, más es interesante.", "Sí, pero es interesante.", "'Mas' = pero.", None)],
  [("producao-livre", "producao", "Responda com 'Sí, pero…': —Vivir en el centro es caro.", None, None)])

X("FUN-2.20", "Expresar conocimiento: saber y conocer", "Saber e conhecer",
  "Sou capaz de dizer o que sei e quem/o que conheço.",
  "saber + informação ou habilidade (Sé los números; Sé decir 'hola' en alemán). conocer + lugar ou pessoa (Conozco Bolivia; Conozco a Leticia: pessoa com a).",
  "Português: 'conheço a Letícia' (o 'a' é artigo). Espanhol: Conozco a Leticia (o a é preposição obrigatória com pessoa).",
  [("Sé griego.", "Sei grego.", "Sé"), ("Conozco Bolivia.", "Conheço a Bolívia.", "Conozco"), ("Conozco a Leticia.", "Conheço a Letícia.", "a Leticia")],
  [("Conozco Leticia.", "Conozco a Leticia.", "Pessoa: conocer a.", "CT-A-PESSOAL"), ("Conozco nadar.", "Sé nadar.", "Habilidade: saber.", None)],
  [("escolha-em-contexto", "foco-na-forma", "(Sé / Conozco) a tu hermano.", "Conozco", None),
   ("escolha-em-contexto", "foco-na-forma", "(Sé / Conozco) cocinar.", "Sé", None)])

X("FUN-2.21", "Expresar desconocimiento", "Dizer que não sabe ou não conhece",
  "Sou capaz de dizer que não sei algo ou não conheço alguém.",
  "No sé + SN/inf. (No sé pronunciar «perro»); No conozco + lugar / a + pessoa.",
  "'Não sei' → No sé (com acento: sé = verbo saber).",
  [("No sé pronunciar «perro».", "Não sei pronunciar 'perro'.", "No sé"), ("No conozco a Sonia.", "Não conheço a Sônia.", "a Sonia")],
  [("No se.", "No sé.", "Verbo saber leva acento.", "CT-ACENTO-GRAFICO")],
  [("producao-livre", "producao", "Diga duas coisas que você não sabe fazer em espanhol ainda.", None, None)])

X("FUN-2.22", "Preguntar por habilidades", "Perguntar o que alguém sabe fazer",
  "Sou capaz de perguntar se alguém sabe fazer algo.",
  "¿Sabes + língua/infinitivo? ¿Sabes griego? ¿Sabes tocar la guitarra?",
  "'Você sabe tocar violão?' → ¿Sabes tocar la guitarra? (guitarra = violão).",
  [("¿Sabes tocar la guitarra?", "Você sabe tocar violão?", "Sabes"), ("¿Sabes inglés?", "Você sabe inglês?", None)],
  [], [("producao-livre", "producao", "Faça 3 perguntas a um colega com ¿Sabes…?", None, None)])

X("FUN-2.23", "Expresar habilidades", "Dizer o que sabe fazer",
  "Sou capaz de dizer o que sei fazer.",
  "Sé + infinitivo/língua: Sé nadar. Pepa no sabe alemán.",
  "Igual ao português.",
  [("Sé nadar.", "Sei nadar.", "Sé"), ("Pepa no sabe alemán.", "A Pepa não sabe alemão.", "no sabe")],
  [("Yo sé de nadar.", "Sé nadar.", "Sem 'de'.", None)],
  [("producao-livre", "producao", "Diga 3 coisas que você sabe fazer.", None, None)])

# ---- Gostos, desejos, planos
X("FUN-3.2", "Expresar gustos", "Dizer do que gosta",
  "Sou capaz de dizer do que gosto e do que não gosto (eu).",
  "(No) me gusta (mucho) + substantivo com artigo / infinitivo; me gustan + plural.",
  "Português 'Eu gosto de…' → Me gusta… (ver Estrutura da frase: gustar).",
  [("No me gustan las discotecas.", "Não gosto de baladas.", "gustan"), ("Me gusta mucho bailar.", "Gosto muito de dançar.", "gusta mucho")],
  [("Me gusta mucho de bailar.", "Me gusta mucho bailar.", "Sem 'de'.", "CT-GUSTAR")],
  [("producao-livre", "producao", "Diga 3 gostos e 2 não-gostos.", None, None)], pre=["GRA-7.1.3", "EF-6"])

X("FUN-3.4", "Preguntar por preferencias", "Perguntar preferências",
  "Sou capaz de oferecer duas opções.",
  "¿Té o café?",
  "Igual ao português.",
  [("¿Té o café?", "Chá ou café?", "o"), ("¿Agua o vino?", "Água ou vinho?", None)],
  [], [("producao-livre", "producao", "Ofereça duas opções de bebida a um convidado.", None, None)])

X("FUN-3.5", "Expresar preferencia", "Dizer o que prefere",
  "Sou capaz de dizer o que prefiro.",
  "Prefiero + substantivo/infinitivo: Prefiero un café. Prefiero bailar.",
  "preferir é irregular: prefiero (e → ie).",
  [("Prefiero un café.", "Prefiro um café.", "Prefiero"), ("Prefiero bailar.", "Prefiro dançar.", None)],
  [("Prefero un café.", "Prefiero un café.", "e → ie: prefiero.", None)],
  [("lacuna", "foco-na-forma", "—¿Té o café? —___ (preferir) té.", "Prefiero", None)])

X("FUN-3.8", "Expresar deseos: quiero", "Dizer o que quer",
  "Sou capaz de dizer o que quero.",
  "Quiero + substantivo/infinitivo: Quiero una bicicleta nueva. Quiero aprender español.",
  "querer é irregular: quiero (e → ie).",
  [("Quiero aprender español.", "Quero aprender espanhol.", "Quiero"), ("Quiero una bicicleta nueva.", "Quero uma bicicleta nova.", None)],
  [("Quero aprender.", "Quiero aprender.", "e → ie: quiero.", None)],
  [("producao-livre", "producao", "Diga 3 coisas que você quer fazer este ano.", None, None)])

X("FUN-3.9", "Preguntar por planes", "Perguntar por planos",
  "Sou capaz de perguntar sobre planos com o presente.",
  "Presente + marcador de futuro: ¿Trabajas mañana? ¿Qué haces el sábado?",
  "Como no português falado ('Você trabalha amanhã?').",
  [("¿Trabajas mañana?", "Você trabalha amanhã?", "mañana"), ("¿Qué haces el sábado?", "O que você vai fazer no sábado?", "el sábado")],
  [("¿Qué haces en el sábado?", "¿Qué haces el sábado?", "Dia da semana: el, sem en.", None)],
  [("producao-livre", "producao", "Pergunte a um amigo sobre os planos do fim de semana.", None, None)])

# ---- Influenciar
X("FUN-4.1", "Pedir que alguien haga algo (A1)", "Pedir que alguém faça algo",
  "Sou capaz de pedir silêncio, que falem mais devagar ou repitam.",
  "Sem verbo + por favor: ¡Silencio, por favor! Más despacio, por favor. ¿Puedes repetir?",
  "Muito útil em aula: 'Mais devagar, por favor' → Más despacio, por favor.",
  [("Más despacio, por favor.", "Mais devagar, por favor.", "Más despacio"), ("¿Puedes repetir?", "Você pode repetir?", "Puedes")],
  [("Más devagar, por favor.", "Más despacio, por favor.", "'Devagar' em espanhol é despacio.", None)],
  [("escolha-em-contexto", "entrada", "O professor fala rápido demais.", "Más despacio, por favor.", None)])

X("FUN-4.3", "Pedir cosas", "Pedir coisas",
  "Sou capaz de pedir algo num bar ou loja.",
  "El/Un + substantivo + por favor: Un café, por favor. La cuenta, por favor.",
  "Mais direto que no português ('Me vê um café?'); com 'por favor' é educado.",
  [("Un café, por favor.", "Um café, por favor.", "Un café"), ("La cuenta, por favor.", "A conta, por favor.", "La cuenta")],
  [], [("producao-livre", "producao", "Peça uma água sem gás e a conta.", "Un agua sin gas, por favor. La cuenta, por favor.", None)])

X("FUN-4.4", "Pedir ayuda", "Pedir ajuda",
  "Sou capaz de pedir ajuda de forma simples.",
  "A1: Por favor + gesto. A2: ¿Me ayudas? / Perdona, ¿puedes ayudarme?",
  "Igual ao português.",
  [("Por favor… (mostrando a mala)", "Por favor… (mostrando a mala)", None), ("Perdona, ¿puedes ayudarme?", "Desculpa, pode me ajudar?", "ayudarme")],
  [], [("escolha-em-contexto", "entrada", "Você não consegue abrir a porta.", "Por favor, ¿me ayudas?", None)])

X("FUN-4.7", "Responder a peticiones", "Responder a pedidos",
  "Sou capaz de aceitar ou recusar um pedido.",
  "Aceitar: Sí, sí. Recusar: No.",
  "Igual ao português.",
  [("—¿Puedes dejarme tu bolígrafo? —Sí, sí.", "—Pode me emprestar sua caneta? —Claro.", "Sí, sí"), ("—¿Me ayudas? —No.", "—Você me ajuda? —Não.", "No")],
  [],
  [("escolha-em-contexto", "entrada", "—¿Puedes cerrar la ventana?", "Sí, sí.", None)])

X("FUN-4.9", "Dar permiso", "Dar permissão",
  "Sou capaz de dar permissão.",
  "A1: Sí. A2: Sí, claro; Sí, sí, ábrela.",
  "Igual ao português.",
  [("—¿Puedo pasar? —Sí.", "—Posso entrar? —Pode.", "Sí"), ("—¿Puedo abrir la ventana? —Sí, claro. (A2)", "—Posso abrir a janela? —Claro.", "Sí, claro")],
  [],
  [("escolha-em-contexto", "entrada", "—¿Puedo abrir la ventana?", "Sí.", None)])

X("FUN-4.10", "Denegar permiso", "Negar permissão",
  "Sou capaz de negar permissão de forma educada.",
  "No; No, lo siento; No. Perdón.",
  "Igual ao português.",
  [("—¿Puedo fumar? —No, lo siento.", "—Posso fumar? —Não, sinto muito.", "No, lo siento"), ("—¿Puedo usar tu móvil? —No. Perdón.", "—Posso usar seu celular? —Não. Desculpa.", "No. Perdón")],
  [], [("escolha-em-contexto", "entrada", "—¿Puedo fumar aquí?", "No, lo siento.", None)])

X("FUN-4.16", "Aceptar una invitación", "Aceitar um convite",
  "Sou capaz de aceitar uma oferta.",
  "Sí, gracias.",
  "Igual ao português.",
  [("—¿Un café? —Sí, gracias.", "—Um café? —Sim, obrigado.", "Sí, gracias"), ("—¿Quieres un poco de pan? —Sí, gracias.", "—Quer um pouco de pão? —Quero, obrigada.", "Sí, gracias")],
  [], [("escolha-em-contexto", "entrada", "—¿Quieres agua?", "Sí, gracias.", None)])

X("FUN-4.17", "Rechazar una invitación", "Recusar um convite",
  "Sou capaz de recusar uma oferta.",
  "No, (muchas) gracias.",
  "Igual ao português.",
  [("—¿Un café? —No, gracias.", "—Um café? —Não, obrigado.", "No, gracias"), ("—¿Más agua? —No, muchas gracias.", "—Mais água? —Não, muito obrigado.", "No, muchas gracias")],
  [], [("escolha-em-contexto", "entrada", "—¿Más pan?", "No, muchas gracias.", None)])

if __name__ == "__main__":
    salvar(L, "a1-funcoes.json")
