"""Fichas A1 — Pronúncia (fase A), ortografia, gêneros textuais e cultura (Lote 2.5)."""
from fichas_base import F, salvar

PRO = "https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/03_pronunciacion_inventario_a1-a2.htm"
ORT = "https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/04_ortografia_inventario_a1-a2.htm"
GEN = "https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/07_generos_discursivos_inventario_a1-a2.htm"
SAB = "https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/11_saberes_y_comportamientos_inventario.htm"
REF = "https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/10_referentes_culturales_inventario.htm"
L = []
def P(*a, **k):
    L.append(F(*a, **k))

# ------------------------------------------------ PRONÚNCIA (fase A)
P("PRO-5.1", "Las cinco vocales", "As cinco vogais",
  objetivo="Sou capaz de pronunciar as cinco vogais puras, sem nasalizar e sem reduzir as átonas.",
  regra="O espanhol tem só 5 vogais: a, e, i, o, u. Sempre com o mesmo som, tônicas ou átonas, e sem nasalização. 'e' e 'o' são médias (nem abertas como é/ó, nem fechadas como ê/ô).",
  contraste="Brasileiros tendem a dizer 'leche' como 'lechi' e 'como' como 'comu', e a nasalizar 'cama'. Em espanhol: le-che, co-mo, ca-ma, todas plenas.",
  exemplos=[("leche", "leite", "e final plena"), ("como", "como", "o final plena"), ("cama", "cama", "a sem nasal")],
  erros=[("[ˈletʃi]", "[ˈletʃe]", "A vogal final não vira i.", "CT-VOGAIS-NASAIS"),
         ("[ˈkõmu]", "[ˈkomo]", "Sem nasalizar e sem reduzir o.", "CT-VOGAIS-NASAIS")],
  exs=[("pares-minimos", "entrada", "Ouça e escolha: peso / piso", "depende do áudio", "Treine ouvir e × i."),
       ("ditado", "foco-na-forma", "Ouça e escreva: noche, coche, leche", ["noche", "coche", "leche"], None),
       ("fluencia-cronometrada", "fluencia", "Leia 10 palavras terminadas em -e e -o, gravando-se, e compare com o modelo.", None, None)],
  fonte=PRO)

P("PRO-5.2", "Consonantes difíciles para brasileños", "Consoantes difíceis para brasileiros",
  objetivo="Sou capaz de distinguir r × rr, pronunciar j/g [x], z/c [θ] e ll/y.",
  regra="r entre vogais = toque simples (pero); r inicial e rr = vibrante múltipla (rosa, perro). j e ge/gi = som raspado na garganta [x] (jefe, gente). Na Espanha, z e ce/ci = som interdental [θ], como 'th' do inglês 'think' (zapato, cine); na América = s. ll e y soam parecido na maioria das regiões (calle, yo).",
  contraste="O r inicial do Brasil é gutural; em espanhol vibra a ponta da língua. j/g nunca soam como no português 'jeito', 'gente'. ll não é lh.",
  exemplos=[("pero / perro", "mas / cachorro", "r / rr"), ("jefe, gente", "chefe, gente", "j, g"), ("zapato, cine", "sapato, cinema", "z, c")],
  erros=[("rosa com r gutural", "rosa com r vibrante", "r inicial vibra na ponta da língua.", "CT-R-RR"),
         ("gente como no português", "gente com [x]", "g antes de e/i = [x].", "CT-J-G"),
         ("calle como 'calhe'", "calle como 'caye'", "ll não é lh.", "CT-LL-Y")],
  exs=[("pares-minimos", "entrada", "Ouça e escolha: pero / perro; caro / carro", "depende do áudio", None),
       ("ditado", "foco-na-forma", "Ouça e escreva: jamón, gente, ajo", ["jamón", "gente", "ajo"], None),
       ("producao-livre", "producao", "Grave: 'El perro de Roberto come arroz.' e compare com o modelo.", None, None)],
  fonte=PRO)

P("PRO-3.2", "El acento: la sílaba fuerte", "O acento: a sílaba forte",
  objetivo="Sou capaz de identificar a sílaba tônica e pronunciar corretamente palavras que mudam de tônica do português.",
  regra="O acento pode mudar o sentido (caso / casó). Agudas: última sílaba forte (trabajar); graves: penúltima (niño); esdrúxulas: antepenúltima (música). No presente, a tônica fica no radical (TRAbajo, traBAjas), menos vosotros (trabaJÁIS).",
  contraste="Algumas palavras mudam de tônica: ni-VEL (PT ní-vel), te-LÉ-fo-no (PT te-le-FO-ne), a-ca-DE-mia (PT a-ca-de-MI-a), de-mo-CRA-cia, ce-RE-bro.",
  exemplos=[("caso / casó", "caso / casou", "CA-so / ca-SÓ"), ("teléfono", "telefone", "te-LÉ-fo-no"), ("nivel", "nível", "ni-VEL")],
  erros=[("NÍ-vel", "ni-VEL", "Tônica diferente do português.", "CT-HETEROTONICOS"),
         ("de-mo-cra-CÍ-a", "de-mo-CRA-cia", "Tônica diferente do português.", "CT-HETEROTONICOS")],
  exs=[("silaba-tonica", "foco-na-forma", "Marque a sílaba forte: teléfono, nivel, música, ciudad", ["te-LÉ-fo-no", "ni-VEL", "MÚ-si-ca", "ciu-DAD"], None),
       ("pares-minimos", "entrada", "Ouça: ¿'trabajo' ou 'trabajó'?", "depende do áudio", None)],
  fonte=PRO)

P("PRO-2.3", "Entonación: afirmar y preguntar", "Entonação: afirmar e perguntar",
  objetivo="Sou capaz de diferenciar pela entonação uma afirmação de uma pergunta.",
  regra="Afirmação: o tom cai no final (Es alemán↓). Pergunta de sim/não: o tom sobe no final (¿Eres alemán↑?). Pergunta com palavra interrogativa: em geral desce (¿Cómo te llamas↓?).",
  contraste="Parecido com o português; a entonação espanhola é mais 'sóbria', com menos subidas e descidas.",
  exemplos=[("Es alemán.", "Ele é alemão.", "↓"), ("¿Eres alemán?", "Você é alemão?", "↑"), ("¿Cómo te llamas?", "Como você se chama?", "↓")],
  erros=[],
  exs=[("pares-minimos", "entrada", "Ouça e marque: afirmação ou pergunta? 'Vives en Madrid'", "depende do áudio", None),
       ("producao-livre", "producao", "Grave a mesma frase como afirmação e como pergunta: Tienes hermanos.", None, None)],
  fonte="https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/06_tacticas_pragmaticas_inventario_a1-a2.htm")

P("PRO-5.3", "El enlace entre palabras", "A ligação entre palavras",
  objetivo="Sou capaz de ligar as palavras na fala como um nativo.",
  regra="Dentro de um grupo de palavras, a consoante final se liga à vogal seguinte: el hombre bueno → [elombrebueno]; dos amigos → [do-sa-mi-gos]; ha salido → [asalido].",
  contraste="O ritmo espanhol é silábico: cada sílaba tem duração parecida; não 'engula' vogais átonas como no português.",
  exemplos=[("tomar algo", "tomar algo", "to-ma-ral-go"), ("dos amigos", "dois amigos", "do-sa-mi-gos")],
  erros=[],
  exs=[("ditado", "entrada", "Ouça e separe as palavras: [elombrebueno]", "el hombre bueno", None)],
  fonte=PRO)

# ------------------------------------------------ ORTOGRAFIA
P("ORT-1.1", "El abecedario", "O alfabeto",
  objetivo="Sou capaz de soletrar meu nome e meu sobrenome.",
  regra="27 letras: a, be, ce, de, e, efe, ge, hache, i, jota, ka, ele, eme, ene, eñe, o, pe, cu, erre, ese, te, u, uve, uve doble, equis, ye (i griega), zeta. ch e ll são dígrafos.",
  contraste="Nomes das letras diferentes: v = uve, w = uve doble, j = jota, y = ye, z = zeta, h = hache.",
  exemplos=[("—¿Cómo se escribe? —Uve, i, ce, te, o, erre.", "—Como se escreve? —Vê, i, cê, tê, ó, erre.", "uve"), ("Ñ = eñe", "Ñ = 'enhe'", "eñe")],
  erros=[("v = 've'", "v = uve", "Nome da letra em espanhol.", None)],
  exs=[("ditado", "entrada", "Ouça a soletração e escreva: jota, o, ese, e", "José", None),
       ("producao-livre", "producao", "Soletre seu nome e sobrenome em voz alta.", None, None)],
  fonte=ORT)

P("ORT-1.3.1", "b y v", "b e v",
  objetivo="Sou capaz de escrever com b ou v as palavras que mudam em relação ao português.",
  regra="b e v soam igual em espanhol; a escrita segue a origem. Imperfeito -aba sempre com b (hablaba). Palavras frequentes diferentes do português: gobierno, haber, deber, abogado, móvil.",
  contraste="Português 'governo, haver, dever, advogado' → espanhol gobierno, haber, deber, abogado.",
  exemplos=[("el gobierno", "o governo", "b"), ("deber", "dever", "b"), ("hablaba (A2)", "falava", "-aba")],
  erros=[("el govierno", "el gobierno", "Grafia diferente do português.", "CT-B-V")],
  exs=[("lacuna", "foco-na-forma", "Complete: ha_er, de_er, go_ierno", ["haber", "deber", "gobierno"], None)],
  fonte=ORT)

P("ORT-1.3.2", "c, qu, z", "c, qu, z",
  objetivo="Sou capaz de escrever o som [k] e o som [θ]/[s] corretamente.",
  regra="[k]: ca, co, cu, que, qui (casa, queso, quién). [θ] na Espanha / [s] na América: za, zo, zu, ce, ci (zapato, cena, cine). Plural de -z: luz → luces.",
  contraste="Igual ao português em qu; mas z antes de a/o/u (zapato) e c antes de e/i (cine) soam iguais.",
  exemplos=[("queso", "queijo", "qu"), ("zapato / cine", "sapato / cinema", "z / c"), ("luz → luces", "luz → luzes", "z → c")],
  erros=[("los lápizes", "los lápices", "z → c antes de e.", None)],
  exs=[("ditado", "foco-na-forma", "Ouça e escreva: cerveza, quiero, zumo", ["cerveza", "quiero", "zumo"], None)],
  fonte=ORT)

P("ORT-1.3.3", "g y j", "g e j",
  objetivo="Sou capaz de escrever g e j de acordo com o som.",
  regra="ja, jo, ju, je, ji e ge, gi = [x] (jamón, jefe, gente). ga, go, gu, gue, gui = [g] (gato, guitarra). Palavras terminadas em -aje levam j (viaje, garaje), enquanto em português levam g.",
  contraste="Português 'viagem, garagem' (g) → espanhol viaje, garaje (j).",
  exemplos=[("el viaje", "a viagem", "j"), ("el garaje", "a garagem", "j"), ("la guitarra", "o violão", "gui")],
  erros=[("el viage", "el viaje", "Terminação -aje com j.", "CT-J-G")],
  exs=[("lacuna", "foco-na-forma", "Complete: via_e, gara_e, _ente", ["viaje", "garaje", "gente"], None)],
  fonte=ORT)

P("ORT-1.3.4", "La h", "A letra h",
  objetivo="Sou capaz de escrever palavras com h, que não soa.",
  regra="O h não tem som (hola = [ola]). Muitas palavras com f no latim e h em espanhol: hacer (fazer), hijo (filho), hablar (falar), hoja (folha).",
  contraste="Correspondência útil: f do português → h do espanhol: fazer/hacer, filho/hijo, falar/hablar, formiga/hormiga.",
  exemplos=[("hacer", "fazer", "h"), ("el hijo", "o filho", "h"), ("hablar", "falar", "h")],
  erros=[("acer", "hacer", "Conserve o h, embora não soe.", None)],
  exs=[("ditado", "foco-na-forma", "Ouça e escreva: hola, hijo, hoy", ["hola", "hijo", "hoy"], None)],
  fonte=ORT)

P("ORT-1.3.6", "La ñ", "A letra ñ",
  objetivo="Sou capaz de escrever o som 'nh' com ñ.",
  regra="ñ corresponde ao nh do português: España, año, niño, mañana.",
  contraste="nh → ñ: Espanha/España, ano/año (atenção: sem ñ, 'ano' tem outro sentido!).",
  exemplos=[("España", "Espanha", "ñ"), ("el año", "o ano", "ñ"), ("mañana", "amanhã", "ñ")],
  erros=[("Espanha", "España", "nh → ñ.", "CT-NH-N"), ("Tengo 30 anos.", "Tengo 30 años.", "Sem ñ a palavra muda de sentido.", "CT-NH-N")],
  exs=[("lacuna", "foco-na-forma", "Complete: ni_o, ma_ana, Espa_a", ["niño", "mañana", "España"], None)],
  fonte=ORT)

P("ORT-1.4", "Mayúsculas", "Maiúsculas",
  objetivo="Sou capaz de usar maiúscula no início da frase e em nomes próprios.",
  regra="Maiúscula no início da frase e em nomes de pessoas, cidades e países. Dias, meses, nacionalidades e idiomas vão em minúscula: lunes, enero, español. Maiúscula também leva acento: Ángel, ÁFRICA.",
  contraste="Igual ao português (dias e meses em minúscula).",
  exemplos=[("Ángel vive en Perú.", "Ângelo mora no Peru.", "Á"), ("Hoy es lunes, 3 de enero.", "Hoje é segunda, 3 de janeiro.", "lunes / enero")],
  erros=[("Angel", "Ángel", "Maiúscula também leva acento.", "CT-ACENTO-GRAFICO"), ("Hablo Español.", "Hablo español.", "Idiomas em minúscula.", None)],
  exs=[("achar-o-erro", "foco-na-forma", "Mi amiga Ines es Argentina y habla Español.", "Mi amiga Inés es argentina y habla español.", None)],
  fonte=ORT)

P("ORT-2.1", "Tildes básicas", "Acentos básicos",
  objetivo="Sou capaz de acentuar palavras interrogativas e exclamativas e maiúsculas.",
  regra="A1: qué, quién, cuánto, dónde, cómo, por qué levam acento em perguntas e exclamações (¿Cómo te llamas? ¡Qué bien!). O espanhol só usa acento agudo (´). A2: regras de agudas, graves e esdrúxulas.",
  contraste="Não existe ^ nem ~ como acento: 'você' não tem correspondente; 'português' → portugués.",
  exemplos=[("¿Dónde vives?", "Onde você mora?", "Dónde"), ("¡Qué bien!", "Que bom!", "Qué"), ("portugués", "português", "é")],
  erros=[("português", "portugués", "Só existe acento agudo.", "CT-ACENTO-GRAFICO"), ("¿Que es esto?", "¿Qué es esto?", "Interrogativo leva acento.", "CT-ACENTO-GRAFICO")],
  exs=[("achar-o-erro", "foco-na-forma", "¿Como te llamas? ¿De donde eres?", "¿Cómo te llamas? ¿De dónde eres?", None)],
  fonte="https://cvc.cervantes.es/ensenanza/biblioteca_ele/sicele/sicele03/009_diez.htm")

P("ORT-3.6", "¿ ? y ¡ !", "Sinais ¿ ? e ¡ !",
  objetivo="Sou capaz de escrever perguntas e exclamações com sinal de abertura.",
  regra="Pergunta e exclamação abrem com sinal invertido: ¿Vienes? ¡Hola! Se a pergunta começa no meio da frase, o sinal vai ali: Y tú, ¿de dónde eres?",
  contraste="Em português só há o sinal final.",
  exemplos=[("¿Vienes mañana?", "Você vem amanhã?", "¿"), ("Y tú, ¿de dónde eres?", "E você, de onde é?", "¿"), ("¡Qué bonito!", "Que bonito!", "¡")],
  erros=[("Vienes mañana?", "¿Vienes mañana?", "Falta o sinal de abertura.", "CT-PONTUACAO-INVERTIDA")],
  exs=[("transformar", "foco-na-forma", "Pontue: que hora es", "¿Qué hora es?", None)],
  fonte=ORT)

# ------------------------------------------------ GÊNEROS TEXTUAIS
P("GEN-1.3", "Textos del A1: formularios, postales, mensajes", "Textos do A1: formulários, postais, mensagens",
  objetivo="Sou capaz de ler cartazes, horários e menus simples e preencher formulários e escrever postais curtos.",
  regra="No A1 você lê: passagens, cartazes de lojas, formulários, folhetos turísticos, horários, menus e notas curtas. Escreve: formulários de dados pessoais, postais e mensagens breves.",
  contraste="Formulários espanhóis pedem dois sobrenomes (primer apellido, segundo apellido) e o DNI/pasaporte.",
  exemplos=[("Nombre: Ana. Primer apellido: Souza. Nacionalidad: brasileña.", "Nome: Ana. Primeiro sobrenome: Souza. Nacionalidade: brasileira.", "Primer apellido"),
            ("¡Hola, Marta! Estoy en Sevilla. Hace mucho calor. Un beso, Ana.", "Oi, Marta! Estou em Sevilha. Faz muito calor. Beijo, Ana.", "Un beso")],
  erros=[],
  exs=[("producao-livre", "producao", "Preencha um formulário de inscrição numa academia (nome, sobrenomes, endereço, telefone, e-mail).", None, None),
       ("producao-livre", "producao", "Escreva um postal de 3 linhas para um amigo contando onde você está.", None, None),
       ("escolha-em-contexto", "entrada", "Cartaz: 'Horario: de lunes a viernes, de 9:00 a 14:00'. A loja abre no sábado?", "No", None)],
  fonte=GEN)

P("GEN-3.1", "Describir a una persona", "Descrever uma pessoa",
  objetivo="Sou capaz de descrever uma pessoa em um parágrafo curto.",
  regra="Do geral ao particular: quem é (Carlinhos es un estudiante brasileño) → aparência (Es moreno, alto…) → roupa (Hoy lleva…) → caráter (Es muy simpático).",
  contraste="Roupa que se está usando: llevar (Hoy lleva una camiseta roja), não 'usar'.",
  exemplos=[("Carlinhos es un estudiante brasileño. Es moreno, alto y tiene los ojos negros.", "Carlinhos é um estudante brasileiro. É moreno, alto e tem olhos pretos.", "Es / tiene"),
            ("Hoy lleva unos pantalones blancos y una camiseta roja.", "Hoje está usando uma calça branca e uma camiseta vermelha.", "lleva")],
  erros=[("Hoy usa una camiseta roja.", "Hoy lleva una camiseta roja.", "Roupa que se veste: llevar.", None)],
  exs=[("producao-livre", "producao", "Descreva um colega da escola em 4 frases (quem é, aparência, roupa, caráter).", None, None)],
  fonte=GEN)

P("GEN-3.3", "Describir un lugar", "Descrever um lugar",
  objetivo="Sou capaz de descrever uma casa ou um lugar simples.",
  regra="Visão geral (La casa de Andrea es grande) → o que há (Hay un baño, una cocina…) → detalhes (La habitación es un poco pequeña, pero hay una cama…).",
  contraste="Use hay para listar o que existe e es/está para características e localização.",
  exemplos=[("La casa de Andrea es grande. Hay un baño, una cocina y un salón.", "A casa da Andrea é grande. Tem um banheiro, uma cozinha e uma sala.", "Hay"),
            ("El armario es blanco y muy grande.", "O armário é branco e muito grande.", "es")],
  erros=[("Tiene un baño y una cocina. (descrevendo a casa sem sujeito)", "Hay un baño y una cocina.", "Para listar o que existe: hay.", "CT-HAY-ESTA")],
  exs=[("producao-livre", "producao", "Descreva seu quarto em 4 frases.", None, None)],
  fonte=GEN)

# ------------------------------------------------ CULTURA (fase A)
P("SAB-1.1", "Nombres, apellidos y documentos", "Nomes, sobrenomes e documentos",
  objetivo="Sou capaz de entender como funcionam nomes e sobrenomes no mundo hispânico.",
  regra="Cada pessoa tem dois sobrenomes: o primeiro do pai e o segundo da mãe (Ana García López). A mulher não muda de sobrenome ao casar. Muitos nomes femininos compostos com María (María José). Apelidos familiares: Mamen, Fran, Toni. Documento: DNI.",
  contraste="No Brasil a ordem costuma ser mãe + pai e é comum adotar o sobrenome do marido; na Espanha, pai + mãe e sem mudança no casamento.",
  exemplos=[("Me llamo Ana García López.", "Meu nome é Ana García López.", "García López"), ("Mi DNI es 12345678A.", "Meu RG é 12345678A.", "DNI")],
  erros=[],
  exs=[("escolha-em-contexto", "entrada", "Pedro Martínez Ruiz: qual é o sobrenome do pai?", "Martínez", None)],
  fonte=SAB)

P("SAB-1.4", "Comidas y horarios en España", "Refeições e horários na Espanha",
  objetivo="Sou capaz de entender os horários e as convenções das refeições na Espanha.",
  regra="Desayuno leve de manhã; comida (almoço) entre 14h e 15h30, a refeição principal; merienda à tarde; cena (jantar) por volta das 21h–22h. Menú del día: primer plato, segundo plato, postre, bebida e pão. Tapa: pequena porção, às vezes grátis com a bebida. Na mesa: ¡Que aproveche!",
  contraste="Os horários são mais tardios que no Brasil: almoçar às 12h ou jantar às 19h é cedo na Espanha.",
  exemplos=[("Comemos a las tres.", "Almoçamos às três.", "a las tres"), ("¡Que aproveche!", "Bom apetite!", "Que aproveche")],
  erros=[],
  exs=[("escolha-em-contexto", "entrada", "São 14h30 em Madri. Que refeição as pessoas fazem?", "La comida", None)],
  fonte=SAB)

P("SAB-1.13", "Transporte y viajes", "Transporte e viagens",
  objetivo="Sou capaz de entender como comprar passagens e usar o transporte público.",
  regra="Passagens: sencillo (ida) ou de ida y vuelta, na bilheteria (taquilla), em máquinas, em agências ou pela internet. Ônibus: fila no ponto, pagar ao motorista ou validar o bilhete. Táxi: na rua levantando o braço ou no ponto; em Madri é branco.",
  contraste="Na Espanha: bilhete de metrô = billete; ônibus = autobús; ponto = parada.",
  exemplos=[("Un billete sencillo, por favor.", "Uma passagem só de ida, por favor.", "sencillo"), ("¿Dónde está la parada del autobús?", "Onde fica o ponto de ônibus?", "parada")],
  erros=[],
  exs=[("escolha-em-contexto", "entrada", "Você quer ir e voltar de Toledo. Que passagem pede?", "Un billete de ida y vuelta", None)],
  fonte=SAB)

P("REF-1.1", "Geografía de los países hispanos", "Geografia dos países hispânicos",
  objetivo="Sou capaz de reconhecer grandes referências geográficas do mundo hispânico.",
  regra="Os Andes, o Amazonas, a Pampa, o lago Titicaca, o estreito de Gibraltar. As estações não existem da mesma forma em todos os países, e alguns usam Celsius e outros Fahrenheit.",
  contraste="O Brasil faz fronteira com sete países hispânicos e compartilha com eles a Amazônia.",
  exemplos=[("El lago Titicaca está entre Perú y Bolivia.", "O lago Titicaca fica entre o Peru e a Bolívia.", "está entre"), ("Los Andes están en América del Sur.", "Os Andes ficam na América do Sul.", "están")],
  erros=[],
  exs=[("escolha-em-contexto", "entrada", "Onde está o estreito de Gibraltar?", "Entre España y África", None)],
  fonte=REF)

if __name__ == "__main__":
    salvar(L, "a1-pronuncia-ortografia-cultura.json")
