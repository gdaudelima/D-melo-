"""Fichas A1 — Vocabulário por tema (Lote 2.4).
Listas A1 do inventário de Nociones específicas A1-A2 do PCIC. Itens com '+' no início são complemento do app (não listados no A1 do PCIC).
Formato de cada linha: lema | português | emoji (imagem OpenMoji) | alerta para brasileiros
Imagens: OpenMoji (openmoji.org), licença CC BY-SA 4.0 — uso pessoal com atribuição."""
import json
from pathlib import Path
from fichas_base import F, salvar

NE = "https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/09_nociones_especificas_inventario_a1-a2.htm"
OM = Path("/home/claude/vendor/om/package")
OM_IDX = {e["emoji"]: e["hexcode"] for e in json.loads((OM / "data/openmoji.json").read_text())}
FALTANDO = []

def img(emoji):
    if not emoji:
        return None
    for cand in (emoji, emoji + "️", emoji.replace("️", "")):
        if cand in OM_IDX and (OM / "color/svg" / f"{OM_IDX[cand]}.svg").exists():
            return "om:" + OM_IDX[cand]
    FALTANDO.append(emoji)
    return None

def itens(bloco):
    out = []
    for linha in bloco.strip().splitlines():
        p = [x.strip() for x in linha.split("|")] + ["", "", ""]
        lema, pt, emo, alerta = p[:4]
        comp = lema.startswith("+")
        lema = lema.lstrip("+").strip()
        art = lema.split(" ", 1)[0] if lema.split(" ", 1)[0] in ("el", "la", "los", "las") and " " in lema else None
        i = {"lema": lema, "artigo": art, "pt": pt, "concreto": bool(emo), "fonte_lexico": "complemento" if comp else "pcic"}
        im = img(emo)
        if im:
            i["imagem"] = im
        if alerta:
            i["alerta_pt"] = alerta
        out.append(i)
    return out

L = []
def V(no, es, pt, objetivo, bloco, exemplos, cena, fonte=NE, contrastes=None):
    voc = itens(bloco)
    conc = [v for v in voc if v.get("imagem")][:3]
    alertas = [v for v in voc if v.get("alerta_pt")][:2]
    exs = [("imagem-para-palavra", "foco-na-forma", f"Imagem → escreva com artigo: [{v['pt']}]", v["lema"], v.get("alerta_pt")) for v in conc]
    exs += [("escolha-em-contexto", "foco-na-forma", f"O que significa '{v['lema']}'?", v["pt"], v["alerta_pt"]) for v in alertas]
    exs += [("producao-livre", "producao", cena, None, None),
            ("fluencia-cronometrada", "fluencia", f"60 segundos: diga em voz alta o máximo de palavras de '{pt}' que lembrar, com artigo.", None, None)]
    erros = [(f"Entender '{v['lema']}' pelo português", f"'{v['lema']}' = {v['pt']}", v["alerta_pt"], None) for v in alertas]
    L.append(F(no, es, pt, objetivo=objetivo,
               regra="Aprenda cada substantivo com o artigo (a cor indica o gênero). Palavras concretas vêm com imagem; expressões, com uma frase.",
               contraste="Fique atento aos itens marcados com alerta: gênero diferente, falso amigo ou sílaba tônica diferente.",
               exemplos=exemplos, erros=erros, exs=exs, vocabulario=voc, fonte=fonte,
               contrastes=contrastes or ["CT-HETEROSEMANTICOS", "CT-HETEROGENERICOS"], modulo="vocabulario"))

V("NE-1", "Individuo: el cuerpo y el aspecto", "A pessoa: corpo e aparência",
  "Sou capaz de descrever a aparência de uma pessoa (altura, cabelo, olhos, óculos).", """
el pelo | cabelo | 💇
el ojo | olho | 👁️
la nariz | nariz | 👃 | Feminino em espanhol (o nariz → la nariz).
alto | alto
bajo | baixo
gordo | gordo
delgado | magro
guapo | bonito (pessoa) | | guapo = bonito, atraente.
feo | feio
rubio | loiro | | rubio = loiro; ruivo = pelirrojo.
moreno | moreno
la barba | barba | 🧔
el bigote | bigode | 🥸
las gafas | óculos | 👓 | Óculos = gafas (Espanha); na América, lentes/anteojos.
tener los ojos azules | ter olhos azuis
llevar gafas | usar óculos
tener el pelo rubio | ter cabelo loiro
""", [("Carlinhos es moreno, alto y tiene los ojos negros.", "Carlinhos é moreno, alto e tem olhos pretos.", "tiene los ojos"),
      ("Mi padre lleva gafas y bigote.", "Meu pai usa óculos e bigode.", "lleva gafas")],
  "Descreva uma pessoa da sua família: altura, cabelo, olhos.")

V("NE-2", "Carácter y personalidad", "Personalidade",
  "Sou capaz de dizer como uma pessoa é (simpática, tímida…).", """
simpático | simpático
antipático | antipático
inteligente | inteligente
trabajador | trabalhador
alegre | alegre
serio | sério
tímido | tímido
sociable | sociável
""", [("Mi hermana es muy simpática.", "Minha irmã é muito simpática.", "simpática"),
      ("Soy un poco tímido.", "Sou um pouco tímido.", "tímido")],
  "Descreva o caráter de dois amigos com 2 adjetivos cada um.")

V("NE-3", "Identidad personal", "Identidade e dados pessoais",
  "Sou capaz de dar e pedir dados pessoais: nome, endereço, telefone, nacionalidade, idade, estado civil.", """
el nombre | nome
el apellido | sobrenome | | apellido = sobrenome; apelido (es) = apodo.
el señor / la señora | o senhor / a senhora
firmar | assinar | ✍️
llamarse | chamar-se
la dirección | endereço | | dirección = endereço (e também direção).
el correo electrónico | e-mail | 📧
la calle | rua
la avenida | avenida
la plaza | praça
el piso | apartamento; andar | | piso = apartamento ou andar; chão = suelo.
el número | número
el código postal | CEP
la casa | casa | 🏠
la habitación | quarto | 🛏️
el país | país
la ciudad | cidade | 🏙️
el pueblo | cidadezinha, vilarejo | | pueblo = cidade pequena (e também povo).
vivir | morar, viver
el número de teléfono | número de telefone | ☎️
el móvil | celular | 📱 | móvil = celular (Espanha); na América, celular.
la fecha de nacimiento | data de nascimento | 🎂
la nacionalidad | nacionalidade
extranjero | estrangeiro
español / española | espanhol / espanhola
alemán / alemana | alemão / alemã
mexicano / mexicana | mexicano / mexicana
japonés / japonesa | japonês / japonesa
la edad | idade
tener 30 años | ter 30 anos | | Idade com tener, como em português.
el niño / la niña | o menino / a menina | 🧒
el chico / la chica | o rapaz / a moça
joven | jovem
viejo | velho | 🧓
el hombre | homem | 👨
la mujer | mulher; esposa | 👩 | mujer = mulher e também esposa.
soltero | solteiro
casado | casado | | Estado civil vai com estar: Estoy casada.
divorciado | divorciado
el marido | marido
el pasaporte | passaporte | 🛂
el carné de identidad | carteira de identidade | 🪪
las llaves | chaves | 🔑
la cartera | carteira (de dinheiro) | 👛
el bolso | bolsa (de mão) | 👜 | bolso = bolsa; bolsa (es) = sacola.
la maleta | mala | 🧳
el reloj | relógio | ⌚
el ordenador | computador | 💻 | ordenador (Espanha) = computador; na América, computadora.
la tarjeta de crédito | cartão de crédito | 💳
""", [("Me llamo Ana Souza; mi apellido es Souza.", "Meu nome é Ana Souza; meu sobrenome é Souza.", "apellido"),
      ("Vivo en la calle Mayor, número 5, tercer piso.", "Moro na rua Mayor, número 5, terceiro andar.", "piso")],
  "Preencha uma ficha de hotel em espanhol: nombre, apellido, nacionalidad, dirección, teléfono.")

V("NE-4", "Relaciones personales: la familia", "Família e relações",
  "Sou capaz de falar da minha família e das pessoas próximas.", """
la familia | família | 👪
los padres | os pais (pai e mãe) | | padres = pai e mãe; parentes = parientes.
el padre | pai | 👨
la madre | mãe | 👩
el hijo / la hija | filho / filha
el hermano / la hermana | irmão / irmã
el tío / la tía | tio / tia
el sobrino / la sobrina | sobrinho / sobrinha
el abuelo / la abuela | avô / avó | 👴
el nieto / la nieta | neto / neta
el primo / la prima | primo / prima
el marido | marido
la mujer | esposa
la pareja | parceiro(a), casal
el novio / la novia | namorado / namorada | | novio = namorado (e noivo).
el amigo / la amiga | amigo / amiga
el jefe / la jefa | chefe
el compañero / la compañera | colega
la fiesta | festa | 🎉
""", [("Estos son mis padres y esta, mi hermana Carlota.", "Esses são meus pais e essa, minha irmã Carlota.", "padres"),
      ("Tengo dos hermanos y una sobrina.", "Tenho dois irmãos e uma sobrinha.", "hermanos")],
  "Mostre uma foto de família e apresente 4 pessoas.")

V("NE-5", "Alimentación", "Comida e bebida",
  "Sou capaz de nomear refeições, alimentos e bebidas básicos e pedir num bar.", """
el desayuno | café da manhã | ☕
la comida | almoço; comida | 🍽️ | Na Espanha, comida = almoço (refeição principal, 14h–15h).
la merienda | lanche da tarde
la cena | jantar | | cena = jantar (cena de filme = escena).
desayunar | tomar café da manhã
comer | almoçar; comer
cenar | jantar
el agua | água | 💧 | Feminino, mas usa el no singular: el agua fría.
el agua con gas / sin gas | água com gás / sem gás
la leche | leite | 🥛 | Feminino em espanhol (o leite → la leche).
el té | chá | 🍵
el café solo / con leche / cortado | café puro / com leite / pingado | ☕
la cerveza | cerveja | 🍺
el vino blanco / tinto | vinho branco / tinto | 🍷
beber | beber
la carne | carne | 🥩
el pescado | peixe (comida) | 🐟 | pescado = peixe para comer; pez = peixe vivo.
la fruta | fruta | 🍎
la verdura | verdura | 🥦
los huevos | ovos | 🥚
el pan | pão | 🍞
el bocadillo | sanduíche de baguete | 🥖 | bocadillo = sanduíche no pão francês.
el sándwich | sanduíche (pão de forma) | 🥪
la hamburguesa | hambúrguer | 🍔
el primer plato | primeiro prato
el segundo plato | segundo prato
el postre | sobremesa | 🍮 | postre = sobremesa (doce); sobremesa (es) = conversa depois da refeição.
la sopa | sopa | 🍲
la ensalada | salada | 🥗
la paella | paella | 🥘
la tortilla | omelete de batata | 🍳 | Na Espanha, tortilla = omelete de batata; no México, massa de milho.
el bar | bar
el restaurante | restaurante | 🍽️
el camarero | garçom | | camarero = garçom.
la mesa | mesa
el menú | menu (do dia)
la cuenta | conta | 🧾
""", [("Un café con leche y un bocadillo, por favor.", "Um café com leite e um sanduíche, por favor.", "café con leche"),
      ("De primer plato, sopa; de segundo, pescado; y de postre, fruta.", "De entrada, sopa; de prato principal, peixe; e de sobremesa, fruta.", "postre")],
  "Peça o 'menú del día' completo: primer plato, segundo plato, postre e bebida.")

V("NE-7", "Trabajo", "Trabalho",
  "Sou capaz de dizer onde e com que trabalho.", """
la empresa | empresa | 🏢
la oficina | escritório | 🏢 | oficina = escritório; oficina mecânica = taller.
la tienda | loja | 🏪
internet | internet | 🌐
el teléfono | telefone | ☎️
el trabajo | trabalho
la profesión | profissão
trabajar | trabalhar
dedicarse a | trabalhar com | | ¿A qué te dedicas? = Com o que você trabalha?
comprar | comprar
vender | vender
+el profesor / la profesora | professor / professora | 🧑‍🏫
+el médico / la médica | médico / médica | 🧑‍⚕️
+el estudiante / la estudiante | estudante | 🧑‍🎓
+el enfermero / la enfermera | enfermeiro / enfermeira
""", [("Trabajo en una oficina.", "Trabalho num escritório.", "oficina"),
      ("—¿A qué te dedicas? —Soy profesora.", "—Com o que você trabalha? —Sou professora.", "Soy profesora")],
  "Diga onde você trabalha e o que faz lá.")

V("NE-8", "Ocio", "Lazer e esporte",
  "Sou capaz de falar do meu tempo livre e dos esportes que pratico.", """
las vacaciones | férias | 🏖️ | Sempre no plural: las vacaciones.
el turista | turista
viajar | viajar | ✈️
leer el periódico | ler o jornal | 📰
leer un libro | ler um livro | 📖
leer una revista | ler uma revista
ver la televisión | ver televisão | 📺
ver una película | ver um filme | 🎬 | película = filme.
escuchar música | ouvir música | 🎵
escuchar la radio | ouvir rádio | 📻
ir al cine | ir ao cinema | 🎦
ir al teatro | ir ao teatro | 🎭
ir al parque | ir ao parque
ir a un museo | ir a um museu | 🏛️
ir a una discoteca | ir a uma balada | 🪩
cantar | cantar | 🎤
bailar | dançar | 💃
correr | correr | 🏃
nadar | nadar | 🏊
esquiar | esquiar | ⛷️
hacer deporte | fazer esporte
jugar al fútbol | jogar futebol | ⚽ | jugar al + esporte (com artigo).
jugar al baloncesto | jogar basquete | 🏀
jugar al tenis | jogar tênis | 🎾
el juego | jogo | 🎲
""", [("Los sábados juego al fútbol.", "Aos sábados jogo futebol.", "juego al fútbol"),
      ("Me gusta ver películas y escuchar música.", "Gosto de ver filmes e ouvir música.", "ver películas")],
  "Conte o que você faz no fim de semana (4 atividades).")

V("NE-10", "Vivienda", "A casa",
  "Sou capaz de descrever minha casa: tipo, cômodos e móveis.", """
la casa | casa | 🏠
el piso | apartamento | 🏢 | Na Espanha, piso = apartamento.
el apartamento | apartamento pequeno
el estudio | quitinete
la habitación | quarto
el ascensor | elevador | 🛗
la escalera | escada | 🪜
la terraza | terraço, varanda
el jardín | jardim | 🏡
la ventana | janela | 🪟
la puerta | porta | 🚪
el salón | sala | 🛋️
el dormitorio | quarto de dormir | 🛏️
la cocina | cozinha | 🍳 | cocina = cozinha e também fogão.
el baño | banheiro | 🛁 | baño = banheiro e banho.
el garaje | garagem | 🚗
viejo / nuevo | velho / novo
céntrico | central
bien comunicado | bem servido de transporte
la mesa | mesa
la silla | cadeira | 🪑
la cama | cama | 🛏️
el sofá | sofá | 🛋️
el sillón | poltrona
el armario | armário, guarda-roupa
la estantería | estante | 📚
la ducha | chuveiro | 🚿 | ducha = chuveiro / ducha; ducharse = tomar banho.
el lavabo | pia do banheiro | | lavabo = pia; também banheiro (em restaurantes).
la televisión | televisão | 📺
""", [("Mi piso tiene dos habitaciones, un salón y una cocina.", "Meu apartamento tem dois quartos, uma sala e uma cozinha.", "piso"),
      ("En mi habitación hay una cama, una mesa y una silla.", "No meu quarto tem uma cama, uma mesa e uma cadeira.", "hay")],
  "Descreva sua casa com hay e está (5 frases).")

V("NE-11", "Servicios: salud", "Serviços de saúde",
  "Sou capaz de falar de hospital, médico e enfermeira.", """
el hospital | hospital | 🏥
el médico / la médica | médico / médica | 🧑‍⚕️
el enfermero / la enfermera | enfermeiro / enfermeira
""", [("Daniel trabaja en un hospital.", "Daniel trabalha num hospital.", "hospital"),
      ("Mi madre es enfermera.", "Minha mãe é enfermeira.", "enfermera")],
  "Diga se você conhece alguém que trabalha num hospital.")

V("NE-12", "Compras y ropa", "Compras e roupa",
  "Sou capaz de nomear lojas, roupas básicas e falar de comprar e vender.", """
el supermercado | supermercado | 🛒
el mercado | mercado
la tienda | loja | 🏪
la salida | saída | 🚪
la información | informação | ℹ️
comprar | comprar
vender | vender
los pantalones | calça | 👖 | Plural em espanhol: los pantalones.
los vaqueros | jeans
la falda | saia | | falda = saia.
la camisa | camisa | 👔
el jersey | suéter, blusa de frio | 🧥 | jersey (Espanha) = suéter.
los zapatos | sapatos | 👞
el bolso | bolsa | 👜
""", [("Necesito unos pantalones y unos zapatos.", "Preciso de uma calça e de sapatos.", "unos pantalones"),
      ("La salida está a la derecha.", "A saída fica à direita.", "salida")],
  "Diga que roupa você está usando hoje (Hoy llevo…).")

V("NE-14", "Viajes y alojamiento", "Viagens e hospedagem",
  "Sou capaz de comprar uma passagem, pedir um quarto e falar de destinos.", """
el pasaporte | passaporte | 🛂
la maleta | mala | 🧳
el plano | mapa da cidade | 🗺️
el mapa | mapa | 🗺️ | Masculino: el mapa.
el billete de ida | passagem de ida | 🎫 | billete = passagem; bilhete; cédula.
el billete de ida y vuelta | passagem de ida e volta | 🎫
el horario | horário | 🕒
la oficina de turismo | posto de informação turística
ir a la playa | ir à praia | 🏖️
ir a la montaña | ir à montanha | ⛰️
ir al campo | ir ao campo
el hotel | hotel | 🏨
la habitación doble | quarto duplo | 🛏️
la habitación individual | quarto individual
con baño | com banheiro | 🛁
el camping | camping | ⛺
""", [("Un billete de ida y vuelta a Sevilla, por favor.", "Uma passagem de ida e volta para Sevilha, por favor.", "billete de ida y vuelta"),
      ("Quiero una habitación doble con baño.", "Quero um quarto duplo com banheiro.", "habitación doble")],
  "Faça a reserva de um quarto: tipo de quarto e número de noites.")

V("NE-20", "Geografía, tiempo y naturaleza", "Geografia, tempo e natureza",
  "Sou capaz de falar de lugares, do clima e das estações.", """
el mapa | mapa | 🗺️
el país | país
la ciudad | cidade | 🏙️
la capital | capital
el norte / el sur / el este / el oeste | norte / sul / leste / oeste | 🧭
la montaña | montanha | ⛰️
el mar | mar | 🌊
el río | rio
la playa | praia | 🏖️
la primavera | primavera | 🌸
el verano | verão | ☀️ | verano = verão; invierno = inverno.
el otoño | outono | 🍂
el invierno | inverno | ❄️
llover | chover | 🌧️
nevar | nevar | 🌨️
hace frío | está frio | 🥶 | Clima com hacer: hace frío, hace calor.
hace calor | está calor | 🥵
hace sol | faz sol | 🌞
hace viento | está ventando | 💨
hace buen tiempo / mal tiempo | o tempo está bom / ruim
el animal | animal
la planta | planta | 🪴
la flor | flor | 🌼
el árbol | árvore | 🌳 | Masculino em espanhol (a árvore → el árbol).
""", [("En verano hace mucho calor.", "No verão faz muito calor.", "hace mucho calor"),
      ("Barcelona está en el noreste de España, cerca del mar.", "Barcelona fica no nordeste da Espanha, perto do mar.", "cerca del mar")],
  "Descreva o clima da sua cidade em cada estação.", contrastes=["CT-HETEROSEMANTICOS", "CT-HETEROGENERICOS", "CT-HAY-ESTA"])

V("NG-5.12", "Los colores", "Cores",
  "Sou capaz de dizer as cores básicas e concordá-las com o substantivo.", """
+blanco | branco | ⚪
+negro | preto | ⚫ | negro = preto.
+rojo | vermelho | 🔴 | rojo = vermelho; roxo = morado.
+azul | azul | 🔵
+verde | verde | 🟢
+amarillo | amarelo | 🟡
+marrón | marrom | 🟤
+gris | cinza
+rosa | rosa
+naranja | laranja | 🟠
""", [("Tengo un coche rojo.", "Tenho um carro vermelho.", "rojo"),
      ("Las camisas blancas son bonitas.", "As camisas brancas são bonitas.", "blancas")],
  "Descreva a roupa que você está usando com cores.",
  fonte="https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/08_nociones_generales_inventario_a1-a2.htm")

V("NG-4.1", "El tiempo: días, meses, partes del día", "Tempo: dias, meses, partes do dia",
  "Sou capaz de dizer o dia da semana, o mês e a parte do dia.", """
+el lunes | segunda-feira | | Dias da semana sem 'feira': lunes, martes…
+el martes | terça-feira
+el miércoles | quarta-feira
+el jueves | quinta-feira
+el viernes | sexta-feira
+el sábado | sábado
+el domingo | domingo
+enero, febrero, marzo… | janeiro, fevereiro, março… | 📅 | Meses em minúscula, como em português.
+la mañana | a manhã | 🌅 | mañana = manhã e também amanhã.
+mañana | amanhã
+la tarde | a tarde | | Na Espanha, a tarde vai do almoço até escurecer.
+la noche | a noite | 🌙
+hoy | hoje
+la semana | semana
+el fin de semana | fim de semana
""", [("Hoy es lunes.", "Hoje é segunda-feira.", "lunes"),
      ("Mañana por la mañana tengo clase.", "Amanhã de manhã tenho aula.", "Mañana… mañana")],
  "Diga o que você faz em cada dia da semana.",
  fonte="https://cvc.cervantes.es/ensenanza/biblioteca_ele/plan_curricular/niveles/08_nociones_generales_inventario_a1-a2.htm")

if __name__ == "__main__":
    salvar(L, "a1-vocabulario.json")
    tot = sum(len(f["vocabulario"]) for f in L)
    com_img = sum(1 for f in L for v in f["vocabulario"] if v.get("imagem"))
    print(f"palavras/expressões: {tot}; com imagem: {com_img}; emojis sem imagem: {FALTANDO}")
