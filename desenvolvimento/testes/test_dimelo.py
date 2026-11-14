"""Testes automáticos do Dímelo (Playwright, tela de celular).

Uso: servir app/ em http://localhost:8765 e rodar  python3 testes/test_dimelo.py
Gera capturas em testes/capturas/.
"""
import asyncio, json, re, sys
from pathlib import Path
from playwright.async_api import async_playwright

URL = "http://localhost:8765/"
AQUI = Path(__file__).parent
CAP = AQUI / "capturas"; CAP.mkdir(exist_ok=True)
AXE = Path("/tmp/axe.min.js").read_text()
resultados = []

def ok(nome, cond, extra=""):
    resultados.append((nome, bool(cond), extra))
    print(("✔ " if cond else "✘ ") + nome + (f"  [{extra}]" if extra and not cond else ""))

async def novo(browser, largura=390, offline=False):
    ctx = await browser.new_context(viewport={"width": largura, "height": 844}, device_scale_factor=2, is_mobile=True,
                                    has_touch=True, locale="pt-BR", accept_downloads=True)
    pg = await ctx.new_page()
    pg.erros = []
    pg.on("pageerror", lambda e: pg.erros.append(str(e)))
    pg.on("console", lambda m: pg.erros.append(m.text) if m.type == "error" else None)
    return ctx, pg

async def clicar_e_esperar(pg, seletor):
    """Clica e espera a tela atual ser substituída (evita ler a tela velha)."""
    velho = await pg.query_selector(".tela")
    await pg.click(seletor)
    if velho:
        await pg.wait_for_function("(el) => !el.isConnected", arg=velho, timeout=5000)

async def item_atual(pg):
    return await pg.evaluate("""() => { const m = document.querySelector('main[data-item]'); if (!m) return null;
        const it = window.__dimelo.C.itemPorId.get(m.dataset.item); return JSON.parse(JSON.stringify(it)); }""")

async def responder(pg, certo=True):
    """Responde o item na tela. Devolve o tipo respondido."""
    it = await item_atual(pg)
    t = it["tipo"]
    if t == "vocab":
        await pg.fill("#r0", it["lema"] if certo else "xxx")
        await pg.click("#verificar")
    elif t == "digitar":
        for k, c in enumerate(it["campos"]):
            await pg.fill(f"#r{k}", c["resp"][0] if certo else "xxx")
        await pg.click("#verificar")
    elif t == "escolha":
        alvo = it["resp"] if certo else next(o for o in it["ops"] if o != it["resp"])
        await pg.locator(f'[data-op="{alvo}"]').first.click()
    elif t == "escolha-inline":
        grupos = [p for p in it["partes"] if isinstance(p, dict)]
        for k, g in enumerate(grupos):
            alvo = g["resp"] if certo else next(o for o in g["ops"] if o != g["resp"])
            await pg.locator(f'[data-grupo="{k}"] [data-op="{alvo}"]').click()
        await pg.click("#verificar")
    elif t == "montar":
        alvo = re.findall(r"[\wáéíóúñü]+", it["resp"].lower())
        pecas = [p.lower() for p in it["pecas"]]
        ordem = alvo if certo else list(reversed(alvo))
        usados = set()
        for w in ordem:
            k = next(i for i, p in enumerate(pecas) if p == w and i not in usados)
            usados.add(k)
            await pg.click(f'#banco [data-k="{k}"]')
        await pg.click("#verificar")
    elif t == "ouvir":
        # descobre qual opção foi sorteada pelo atributo do botão de áudio
        for k in range(len(it["grupos"])):
            fala = await pg.get_attribute(f'[data-grupo="{k}"] .audio.grande', "data-falar")
            rot = next(o["rotulo"] for o in it["grupos"][k] if o["fala"] == fala)
            if not certo: rot = next(o["rotulo"] for o in it["grupos"][k] if o["rotulo"] != rot)
            await pg.locator(f'[data-grupo="{k}"] [data-op="{rot}"]').click()
        await pg.click("#verificar")
    elif t == "tonica":
        for k, p in enumerate(it["palavras"]):
            j = p["forte"] if certo else (p["forte"] + 1) % len(p["silabas"])
            await pg.click(f'[data-palavra="{k}"] [data-j="{j}"]')
        await pg.click("#verificar")
    return t

async def axe(pg, nome):
    await pg.add_script_tag(content=AXE)
    r = await pg.evaluate("""async () => { const r = await axe.run(document, { resultTypes: ['violations'] });
        return r.violations.filter(v => ['serious','critical'].includes(v.impact)).map(v => v.id + ': ' + v.nodes.length + ' ' + (v.nodes[0]?.target||''));}""")
    ok(f"acessibilidade sem violações graves: {nome}", not r, "; ".join(r))

async def sem_rolagem_lateral(pg, nome):
    w = await pg.evaluate("() => [document.documentElement.scrollWidth, window.innerWidth]")
    ok(f"sem rolagem horizontal: {nome}", w[0] <= w[1], str(w))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx, pg = await novo(b)

        # 1. abertura
        await pg.goto(URL); await pg.wait_for_selector("h1")
        ok("abre na tela Hoje", (await pg.inner_text("h1")) == "Sua sessão de hoje")
        await pg.screenshot(path=CAP / "01-hoje.png", full_page=True)
        await axe(pg, "Hoje"); await sem_rolagem_lateral(pg, "Hoje")
        await pg.evaluate("() => navigator.serviceWorker.ready")
        await pg.wait_for_function("() => !!navigator.serviceWorker.controller", timeout=10000)
        ok("service worker controla a página", True)

        # 2. unidade completa (Saludar): entrada, foco, prática, produção
        await pg.click("#comecar"); await pg.wait_for_selector(".barra")
        ok("etapa 1 mostra objetivo", "Objetivo" in await pg.inner_text("main"))
        await pg.screenshot(path=CAP / "02-entrada.png", full_page=True)
        await axe(pg, "Entrada")
        await pg.click("#seguir"); await pg.wait_for_selector("text=Entendi, praticar")
        await pg.screenshot(path=CAP / "03-regra.png", full_page=True)
        await axe(pg, "Regra")
        await pg.click("#seguir"); await pg.wait_for_selector("main[data-item]")
        await pg.screenshot(path=CAP / "04-pratica.png", full_page=True)
        tipos, n, errou_uma = set(), 0, False
        while await pg.locator("main[data-item]").count() and n < 40:
            if not errou_uma:
                t = await responder(pg, certo=False); errou_uma = True
                await pg.wait_for_selector("#continuar")
                txt = await pg.inner_text("#resultado")
                ok("erro mostra explicação 'Por quê'", "Por quê" in txt)
                await pg.screenshot(path=CAP / "05-erro.png", full_page=True)
                await axe(pg, "Correção")
                await clicar_e_esperar(pg, "#continuar")
            else:
                t = await responder(pg, certo=True)
                await pg.wait_for_selector("[data-nota]")
                if n == 1: await pg.screenshot(path=CAP / "06-certo.png", full_page=True)
                await clicar_e_esperar(pg, '[data-nota="Bom"]')
            tipos.add(t); n += 1
            await pg.wait_for_timeout(60)
        ok("prática termina", n < 40, f"{n} respostas")
        ok("item errado volta na mesma sessão (passo curto do FSRS)", n > 0)
        if await pg.locator("#feito").count():
            await pg.screenshot(path=CAP / "07-producao.png", full_page=True)
            while await pg.locator("#feito").count():
                await pg.click("#feito"); await pg.wait_for_timeout(60)
        await pg.wait_for_selector("text=Unidade concluída")
        await pg.screenshot(path=CAP / "08-concluida.png", full_page=True)
        ok("unidade concluída", True)
        cartoes = await pg.evaluate("() => window.__dimelo.S.cartoes.size")
        ok("respostas viraram cartões FSRS", cartoes > 0, str(cartoes))

        # 3. persistência após recarregar
        await pg.goto(URL + "#eu"); await pg.reload(); await pg.wait_for_selector("text=Sou capaz de")
        txt = await pg.inner_text("main")
        ok("progresso persiste após recarregar (Sou capaz de…)", "cumprimentar" in txt.lower(), txt[:200])
        await pg.screenshot(path=CAP / "09-eu.png", full_page=True)
        await axe(pg, "Eu")

        # 4. revisão: simula cartões vencidos (avaliados há 10 dias)
        await pg.evaluate("""async () => { const {S} = window.__dimelo; const {db} = await import('./js/db.js');
            for (const c of [...S.cartoes.values()].slice(0, 3)) { c.fsrs.due = new Date(Date.now() - 864e5); await db.gravar('cartoes', c); } }""")
        await pg.goto(URL + "#hoje"); await pg.reload(); await pg.wait_for_selector("h1")
        txt = await pg.inner_text("main")
        ok("cartões vencidos aparecem como revisões", re.search(r"\d+ revis", txt) is not None, txt[:120])
        await pg.click("#comecar"); await pg.wait_for_selector("main[data-item]")
        rot = await pg.inner_text(".barra .rotulo")
        ok("sessão começa pelas revisões", rot.startswith("Revisão"), rot)
        await pg.screenshot(path=CAP / "10-revisao.png", full_page=True)
        await pg.click("[data-sair]")

        # 5. mapa e ficha
        await pg.goto(URL + "#mapa"); await pg.wait_for_selector("text=Painel do A1")
        await pg.screenshot(path=CAP / "11-mapa.png", full_page=True)
        await axe(pg, "Mapa"); await sem_rolagem_lateral(pg, "Mapa")
        n_az = await pg.locator(".azulejo-btn").count()
        ok("mapa A1 mostra 107 azulejos", n_az == 107, str(n_az))
        await pg.click('[data-nivel="B1"]'); await pg.wait_for_selector("text=Painel do B1")
        ok("mapa B1 mostra a estrutura", "seções" in await pg.inner_text("main"))
        await pg.goto(URL + "#ficha:NE-1@A1"); await pg.wait_for_selector("#estudar")
        await pg.screenshot(path=CAP / "12-ficha.png", full_page=True)
        await pg.click("#pular"); await pg.wait_for_selector("main[data-item]")
        it = await item_atual(pg)
        ok("'Já conheço' vai direto à prática", it is not None)
        if it["tipo"] == "vocab" and it.get("img"):
            carregou = await pg.evaluate("() => { const i = document.querySelector('.ilustra'); return i && i.complete && i.naturalWidth > 0; }")
            ok("ilustração OpenMoji carrega", carregou)
            await pg.screenshot(path=CAP / "13-vocab.png", full_page=True)
            await axe(pg, "Vocabulário")
            await pg.fill("#r0", it["lema"].split(" ", 1)[-1])  # sem artigo
            await pg.click("#verificar"); await pg.wait_for_selector("#continuar")
            ok("sem artigo é corrigido com aviso de artigo", "artigo" in (await pg.inner_text("#resultado")).lower())
            await pg.screenshot(path=CAP / "14-sem-artigo.png", full_page=True)
            await clicar_e_esperar(pg, "#continuar")
        # percorre a unidade de vocabulário inteira (todos os tipos de exercício)
        n = 0
        while await pg.locator("main[data-item]").count() and n < 80:
            it = await item_atual(pg)
            t = await responder(pg, True); tipos.add(t); n += 1
            await pg.wait_for_selector("[data-nota], #continuar")
            if await pg.locator("#continuar").count():
                ok(f"resposta certa aceita (NE-1, {t})", False, json.dumps(it, ensure_ascii=False)[:300] + " => " + (await pg.inner_text("#resultado"))[:200])
                await clicar_e_esperar(pg, "#continuar"); continue
            await clicar_e_esperar(pg, '[data-nota="Bom"]'); await pg.wait_for_timeout(40)
        await pg.click("[data-sair]")

        # 6. contrastes
        await pg.goto(URL + "#contrastes"); await pg.wait_for_selector("text=Onde o português engana")
        await pg.screenshot(path=CAP / "15-contrastes.png", full_page=True)
        await axe(pg, "Contrastes")
        await pg.click('[data-eixo="pronuncia-e-escuta"]')
        ok("filtro de contrastes funciona", await pg.locator("article").count() < 26)

        # 7. todos os tipos de exercício respondem certo
        for fid in ["PRO-3.2@A1", "PRO-5.2@A1", "EF-6@A1", "ORT-1.3.6@A1", "GRA-1.3@A1", "FUN-5.5@A1", "PRO-2.3@A1", "EF-9@A1", "GRA-13.3@A1"]:
            await pg.goto(URL + f"#ficha:{fid}"); await pg.wait_for_selector("#estudar")
            await pg.click("#pular" if await pg.locator("#pular").count() else "#estudar")
            await pg.wait_for_selector("main[data-item]")
            k = 0
            while await pg.locator("main[data-item]").count() and k < 30:
                t = await responder(pg, True); tipos.add(t); k += 1
                await pg.wait_for_selector("[data-nota], #continuar", timeout=3000)
                if await pg.locator("#continuar").count():
                    ok(f"resposta certa aceita ({fid}, {t})", False, await pg.inner_text("#resultado")); break
                await clicar_e_esperar(pg, '[data-nota="Bom"]'); await pg.wait_for_timeout(40)
            await pg.goto(URL + "#hoje")
        ok("todos os tipos de exercício foram respondidos", {"vocab", "digitar", "escolha", "escolha-inline", "montar", "ouvir", "tonica"} <= tipos, str(tipos))

        # 8. backup: exportar e restaurar
        await pg.goto(URL + "#eu"); await pg.wait_for_selector("#exportar")
        async with pg.expect_download() as dl:
            await pg.click("#exportar")
        caminho = await (await dl.value).path()
        dados = json.loads(Path(caminho).read_text())
        ok("cópia de segurança exportada", dados.get("app") == "dimelo" and len(dados["cartoes"]) > 0)
        await pg.click("#apagar"); await pg.click("#confirmar"); await pg.wait_for_timeout(200)
        ok("apagar zera o progresso", await pg.evaluate("() => window.__dimelo.S.cartoes.size") == 0)
        await pg.set_input_files("#importar", caminho); await pg.wait_for_timeout(500)
        ok("restaurar recupera o progresso", await pg.evaluate("() => window.__dimelo.S.cartoes.size") == len(dados["cartoes"]))

        # 9. offline: sem rede, o app abre e navega
        await ctx.set_offline(True)
        await pg.goto(URL + "#hoje"); await pg.reload(); await pg.wait_for_selector("h1")
        ok("abre sem internet", "Dímelo" in await pg.inner_text("header"))
        await pg.goto(URL + "#mapa"); await pg.wait_for_selector("text=Painel do A1")
        img_ok = await pg.evaluate("""async () => { const r = await caches.match('img/om/1F95B.svg'); return !!r; }""")
        ok("ilustrações guardadas para uso offline", img_ok)
        await ctx.set_offline(False)
        ok("sem erros de JavaScript", not pg.erros, "; ".join(pg.erros[:5]))
        await ctx.close()

        # 10. tela estreita (360px) e movimento reduzido
        ctx, pg = await novo(b, largura=360)
        await pg.emulate_media(reduced_motion="reduce")
        for h in ["#hoje", "#mapa", "#contrastes", "#eu"]:
            await pg.goto(URL + h); await pg.wait_for_selector("h1")
            await sem_rolagem_lateral(pg, f"{h} em 360px")
        await pg.goto(URL + "#ficha:EF-6@A1"); await pg.wait_for_selector("#pular"); await pg.click("#pular")
        await pg.wait_for_selector("main[data-item]")
        await sem_rolagem_lateral(pg, "exercício em 360px")
        await pg.screenshot(path=CAP / "16-360px.png", full_page=True)
        await ctx.close(); await b.close()

    falhas = [r for r in resultados if not r[1]]
    print(f"\n{len(resultados) - len(falhas)} de {len(resultados)} verificações passaram.")
    (AQUI / "resultado.json").write_text(json.dumps([{"teste": n, "passou": p, "detalhe": e} for n, p, e in resultados], ensure_ascii=False, indent=1))
    sys.exit(1 if falhas else 0)

asyncio.run(main())
