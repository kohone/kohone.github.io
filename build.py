#!/usr/bin/env python3
"""Сборка сайта kohone.net (GitHub Pages): одна витрина для всех приложений, на английском.

    python3.14 build.py   # нужен Python 3.12+ (f-строки с обратной косой)

Новое приложение — запись в APPS и функция страниц (как nardy_pages). HTML пишется в корень репозитория,
GitHub Pages отдаёт его как есть. Без сервера, без трекеров, без внешних скриптов.
"""
import html
import os

SITE = "https://kohone.net"
DEV = "Maks Beskrovnyi"
EMAIL = "support@kohone.net"
UPDATED = "2026-09-25"

APPS = [
    {"slug": "fair-dice", "icon": "/assets/fair-dice-icon.jpg",
     "name": {"en": "Backgammon: Fair Dice", "ru": "Нарды: длинные и короткие"},
     "tag": {"en": "Backgammon and long nardy with fair, verifiable dice",
             "ru": "Короткие и длинные нарды с честными проверяемыми костями"},
     "store": None},
    {"slug": "logbook", "icon": "/assets/logbook-icon.jpg",
     "name": {"en": "Pilot Logbook", "ru": "Pilot Logbook"},
     "tag": {"en": "A pilot logbook that counts currency and fills the 8710 grid",
             "ru": "Лётная книжка: считает допуски и заполняет сетку 8710"},
     "store": None},
    # Приложение со своим сайтом: карточка ведёт наружу, страниц здесь нет.
    {"slug": "cycleally", "icon": "/assets/cycleally-icon.jpg", "external": "https://cycleally.com",
     "name": {"en": "Cycle Ally", "ru": "Cycle Ally"},
     "tag": {"en": "A PCOS and PMOS log you can hand to your doctor",
             "ru": "Дневник СПКЯ, который можно показать врачу"},
     "store": None},
]

T = {
    "en": {"apps": "Apps", "home_lead": "Web developer and mobile app developer. I build apps and games for iPhone.",
           "overview": "Overview", "my_apps": "My apps",
           "soon": "Coming to the App Store", "privacy": "Privacy", "terms": "Terms", "support": "Support", "verify": "Verify the dice",
           "report": "Dice report", "lang": "Русский", "contact_soon": "A support e-mail will appear here soon.",
           "updated": "Last updated"},
    "ru": {"apps": "Приложения", "home_lead": "Делаю приложения и игры для iPhone.",
           "soon": "Скоро в App Store", "privacy": "Конфиденциальность", "terms": "Условия", "support": "Поддержка", "verify": "Проверка костей",
           "report": "Отчёт о костях", "lang": "English", "contact_soon": "Почта поддержки скоро появится здесь.",
           "updated": "Обновлено"},
}


def url(lang, path):
    return ("/ru" if lang == "ru" else "") + path


def page(lang, path, title, body, desc="", landing=False, sub=""):
    other = "en" if lang == "ru" else "ru"
    t = T[lang]
    doc = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc or title)}">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{url(lang, '/')}">{DEV}</a>
<nav><a href="{url(lang, '/')}">{t['apps']}</a></nav>
</div></header>
{('<div class="wrap subbar">' + sub + '</div>') if sub else ''}
{('<main class="landing">' + body + '</main>') if landing else ('<main><div class="wrap">' + body + '</div></main>')}
<footer><div class="wrap">
<nav><a href="/">Home</a><a href="/fair-dice/">Backgammon: Fair Dice</a><a href="/fair-dice/verify">Verify the dice</a><a href="/fair-dice/dice-report">Dice report</a><a href="/fair-dice/privacy">Privacy Policy</a><a href="/fair-dice/support">Support</a></nav>
<nav><a href="/logbook/">Pilot Logbook</a><a href="/logbook/privacy">Privacy Policy</a><a href="/logbook/terms">Terms of Use</a><a href="/logbook/support">Support</a></nav>
<p>Made by one person, {DEV}. Questions: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p class="muted" style="font-size:13px">Apple, iPhone, iCloud and App Store are trademarks of Apple Inc. These apps are independent and not affiliated with, endorsed by, or sponsored by Apple Inc.</p>
</div></footer>
</body>
</html>
"""
    rel = url(lang, path).lstrip("/")
    if rel == "" or rel.endswith("/"):
        rel += "index.html"
    elif not rel.endswith(".html"):
        rel += ".html"  # GitHub Pages отдаёт /nardy/verify из nardy/verify.html
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(doc)


def home(lang):
    t = T[lang]
    cards = "\n".join(
        f'<a class="app" href="{a.get("external") or url(lang, "/" + a["slug"] + "/")}"><img src="{a["icon"]}" alt="">'
        f'<div><b>{a["name"][lang]}</b><span>{a["tag"][lang]}</span></div></a>' for a in APPS)
    page(lang, "/", DEV + " — web and mobile developer", f"<section class=\"intro\"><h1>{DEV}</h1><p class=\"lead\">{t['home_lead']}</p></section>"
                          f"<h2>{t['my_apps']}</h2><div class=\"apps\">{cards}</div>")


def contact(lang):
    if EMAIL:
        return f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    return T[lang]["contact_soon"]


# ── Нарды ─────────────────────────────────────────────────────────────


def app_store_badge(link, on_dark=False):
    """Официальный значок Apple (скачан с toolbox.marketingtools.apple.com): чёрный на светлом, белый на тёмном."""
    if on_dark:
        return f'<a class="store" href="{link}"><img src="/assets/app-store-badge-white.svg" alt="Download on the App Store" height="44"></a>'
    return (f'<a class="store" href="{link}"><picture>'
            '<source srcset="/assets/app-store-badge-white.svg" media="(prefers-color-scheme: dark)">'
            '<img src="/assets/app-store-badge-black.svg" alt="Download on the App Store" height="44"></picture></a>')


def app_nav(lang, base, current, items=None):
    """Меню разделов приложения — над содержимым каждой его страницы. Пункты задаёт приложение."""
    t = T[lang]
    if items is None:
        items = [("", t["overview"]), ("verify", t["verify"]), ("dice-report", t["report"]),
                 ("privacy", t["privacy"]), ("support", t["support"])]
    links = "".join(f'<a href="{url(lang, base + slug)}"{" class=\"on\"" if slug == current else ""}>{name}</a>'
                    for slug, name in items)
    return f'<nav class="sub">{links}</nav>'


def nardy_pages(lang):
    a, t = APPS[0], T[lang]
    base = "/fair-dice/"
    store = app_store_badge(a["store"]) if a["store"] else f'<span class="badge">{t["soon"]}</span>'
    links = (f'<ul class="links"><li><a href="{url(lang, base + "verify")}">{t["verify"]}</a></li>'
             f'<li><a href="{url(lang, base + "dice-report")}">{t["report"]}</a></li>'
             f'<li><a href="{url(lang, base + "privacy")}">{t["privacy"]}</a></li>'
             f'<li><a href="{url(lang, base + "support")}">{t["support"]}</a></li></ul>')
    hero = f'<div class="hero"><img src="{a["icon"]}" alt=""><div><h1>{a["name"][lang]}</h1>{store}</div></div>'

    if lang == "en":
        # Значок App Store — только с настоящей ссылкой (правила Apple); до выхода — надпись «скоро».
        store_cta = app_store_badge(a["store"], on_dark=True) if a["store"] else '<span class="soon">Coming soon to the App Store</span>'
        img = lambda n, alt, cls="": f'<img class="{cls}" src="/assets/fair-dice/{n}.jpg" alt="{html.escape(alt)}" width="540" height="1174" loading="lazy">'
        body = f"""
<div class="lhero"><div class="wrap">
<div class="hero-text">
<div class="app-id"><img src="{a["icon"]}" alt=""><div><b>{a["name"]["en"]}</b><span>Backgammon &amp; long nardy for iPhone</span></div></div>
<h1>Dice you can check.</h1>
<p class="lede">Backgammon and long nardy against a strong computer or a friend on the same phone. The dice of every game are sealed before the first roll — after the game you get the key and check every roll yourself.</p>
<p class="for-whom">For anyone who has ever suspected an app of rigging the dice — and for anyone who simply wants a good game.</p>
<div class="cta">{store_cta}<a class="button" href="#how">See what it does</a></div>
<p class="small">Questions: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div>
{img("hint", "A game with the best move shown by arrows", "hero-shot")}
</div></div>

<section><div class="wrap"><div class="split">
<div>
<p class="statement">Sealed before the game. Opened after it.</p>
<p>Before the first roll the app shows a fingerprint of the whole dice sequence. You can add your own phrase, so the app cannot pick a convenient sequence in advance. After the game it reveals the key: recompute every roll in the app, on this site, in Python or in CyberChef — without trusting us.</p>
<p class="after-block"><a href="/fair-dice/verify">Check a game's dice →</a> &nbsp;·&nbsp; <a href="/fair-dice/dice-report">The 100-million-roll test →</a></p>
</div>
<figure>{img("verify", "Dice fingerprint, key and verification")}</figure>
</div></div></section>

<section class="band-soft"><div class="wrap">
<div class="measure">
<h2>A computer that explains, not just wins.</h2>
<p class="lede">Five levels from beginner to master, each calibrated by error rate. After a mistake the coach says what went wrong in plain words; after the game the review shows where it was decided.</p>
</div>
<div class="strip">
<figure><figcaption>Your error rate and the luck of both sides</figcaption>{img("review", "Game review")}</figure>
<figure><figcaption>Long nardy with its own neural network</figcaption>{img("long-nardy", "Long nardy game")}</figure>
<figure><figcaption>Your dice against the range of fair dice</figcaption>{img("dice-stats", "Dice statistics")}</figure>
</div>
</div></section>

<section id="how"><div class="wrap">
<div class="measure">
<h2>What it does</h2>
<p class="quiet">A quick game on the bus or a long match in the evening.</p>
</div>
<div class="grid">
<div class="tile"><h3>Two games, full rules</h3><p class="small">Backgammon with the doubling cube, Crawford and matches up to 11 points. Long nardy under standard tournament rules.</p></div>
<div class="tile"><h3>Against the computer or a friend</h3><p class="small">Five levels, or two players on one phone — the board can turn to whoever is on roll.</p></div>
<div class="tile"><h3>Learn as you play</h3><p class="small">Rules lessons on a live board, hints shown right on the board, a coach after mistakes.</p></div>
<div class="tile"><h3>Review and replay</h3><p class="small">Every game is saved. Review it move by move, or play any position again with the same dice.</p></div>
<div class="tile"><h3>Your own dice</h3><p class="small">Roll real dice and type the result. Replay a finished game with your own dice — the computer must play the same.</p></div>
<div class="tile"><h3>30 boards</h3><p class="small">Wood, stone, leather and regional styles, each with its own checkers and dice.</p></div>
</div>
</div></section>

<section class="band-soft"><div class="wrap"><div class="measure">
<p class="statement">What it never does</p>
<ul class="nots">
<li>Never changes the dice — not for the computer, not for a level, not for a purchase.</li>
<li>No coins, no boosts, nothing that buys a better roll.</li>
<li>No ads during a game.</li>
<li>No account and no sign-in.</li>
</ul>
<p class="small">The level changes only the computer's moves. The whole sequence of rolls is fixed before the game, and the key proves it afterwards.</p>
</div></div></section>

<section><div class="wrap"><div class="measure">
<h2>Your games stay yours</h2>
<p class="lede">There is no account to make and no server of ours to send anything to.</p>
<ul class="nots nots--yes">
<li>Games, history, statistics and settings are stored on your iPhone.</li>
<li>If you switch it on, a copy goes to your own iCloud so another iPhone can pick it up — we cannot see it.</li>
<li>The free version shows ads from Google AdMob between games; iOS asks your permission before any tracking. Pro removes ads completely.</li>
</ul>
<p class="after-block"><a href="/fair-dice/privacy">Privacy Policy</a> &nbsp;·&nbsp; <a href="/fair-dice/support">Support</a></p>
</div></div></section>

<section class="band-soft"><div class="wrap">
<div class="measure">
<h2>What it costs</h2>
<p class="quiet">Everything to play is free. Pro takes away the ads and the hint limit, never a feature.</p>
</div>
<div class="grid">
<div class="tile"><p class="price">Free</p><p class="small">Both games, all five levels, matches and the cube, dice verification, statistics, review, lessons, 6 boards. 3 hints a day against the computer, plus 3 for an optional video. A short ad after every second game — none in your first games, never during one.</p></div>
<div class="tile"><p class="price">Pro · one-time</p><p class="small">No ads and unlimited hints, forever. Bought once in the app through the App Store and restored on your other devices.</p></div>
<div class="tile"><p class="price">Boards</p><p class="small">24 more boards, each sold separately in the app, with a preview before you buy.</p></div>
</div>
</div></section>

<section><div class="wrap"><div class="measure center">
<h2>Questions people ask first</h2>
<details><summary>Are the dice really random?</summary><p>Yes, and you do not have to take our word for it. Every game's rolls come from a sealed sequence you can recompute after the game, and the same generator passed standard tests on 100 million rolls.</p></details>
<details><summary>Does the computer see my next roll?</summary><p>No. It chooses its move with the dice already on the board, like you. A replay with your own dice proves it: given the same rolls, it plays exactly the same moves.</p></details>
<details><summary>Does a harder level get better dice?</summary><p>No. The level changes only which moves the computer picks. The dice are the same sealed sequence whatever the level.</p></details>
<details><summary>Is it free?</summary><p>Yes — both games, all levels, verification, review and statistics. Pro is optional: no ads and unlimited hints.</p></details>
<details><summary>Which rules does long nardy use?</summary><p>Standard tournament rules: one checker from the head per turn (two on a first roll of 6-6, 4-4 or 3-3 for the second player), no six-point wall in front of all the opponent's checkers, mars counts 2 points.</p></details>
<details><summary>Does it work offline?</summary><p>Yes, everything works without the internet. Ads and the iCloud copy simply wait until you are online.</p></details>
<details><summary>How do I move my games to a new iPhone?</summary><p>Turn on Settings → Save progress to iCloud on both phones with the same Apple ID. Pro and boards are restored with Settings → Restore purchases.</p></details>
</div></div></section>
"""
        page(lang, base, a["name"][lang], body, a["tag"][lang], landing=True, sub=app_nav(lang, base, ""))
    else:
        about = """<p class="lead">Короткие и длинные нарды (турнирные правила) против сильного компьютера или вдвоём на одном телефоне. Работает без интернета.</p>
<ul>
<li><b>Честные кости, которые можно проверить.</b> Перед партией приложение запечатывает броски и показывает их отпечаток; после партии вы получаете ключ и пересчитываете каждый бросок — здесь, на Python или любым инструментом HMAC.</li>
<li><b>Компьютер, который объясняет.</b> Нейросеть играет на пяти уровнях, показывает лучший ход и объясняет ошибки простыми словами.</li>
<li><b>Разбор, статистика, уроки.</b> Разбор партии с оценкой ошибок, статистика костей против честных шансов, уроки правил на живой доске.</li>
<li><b>Без аккаунтов.</b> Партии и статистика остаются на вашем телефоне.</li>
</ul>"""
        page(lang, base, a["name"][lang], hero + about, a["tag"][lang], sub=app_nav(lang, base, ""))

    # Политика конфиденциальности
    if lang == "en":
        privacy = f"""<h1>Privacy Policy — {a['name']['en']}</h1>
<p class="muted">{t['updated']}: {UPDATED}</p>
<p>The game itself needs no account and sends your games nowhere. The only third party in the app is advertising (Google AdMob), described below.</p>
<h2>What stays on your device</h2>
<p>Your games, history, statistics and settings are stored on your iPhone (the current game in the Keychain, the rest in the app's own storage). We have no servers and never receive them.</p>
<h2>iCloud (optional)</h2>
<p>If you turn on “Save progress to iCloud”, your history, statistics, dice log and settings are copied to your own private iCloud storage so they appear on your other devices. This copy is handled by Apple under your Apple ID; we cannot see it. You can turn it off in Settings at any time.</p>
<h2>Advertising</h2>
<p>The free version shows ads between games and optional videos that give extra hints. Ads are served by Google AdMob, which may collect device identifiers, approximate location (from the IP address), and information about ad views and clicks, to show and measure ads and to prevent fraud.</p>
<ul>
<li>Before any personalized ads, iOS asks whether the app may track you (App Tracking Transparency). If you decline, Google shows only non-personalized ads.</li>
<li>In the EEA, the UK and Switzerland you are asked for consent first (Google's consent form).</li>
<li>Google's policy: <a href="https://policies.google.com/technologies/partner-sites">How Google uses information from apps that use its services</a>.</li>
</ul>
<p>Ads never affect the dice or the computer. Pro removes ads completely.</p>
<h2>How long data is kept and how to delete it</h2>
<ul>
<li><b>On your device:</b> kept until you delete it. Deleting the app deletes your history, statistics and settings; the unfinished game is kept in the Keychain and is removed when you start a new game or reset the device.</li>
<li><b>In your iCloud:</b> kept until you turn off “Save progress to iCloud” and delete the app's data in iPhone Settings → your name → iCloud → Manage Storage.</li>
<li><b>By Google (ads):</b> kept under Google's own retention rules, described in its privacy policy.</li>
</ul>
<h2>Your choices</h2>
<ul>
<li>Allow or deny tracking at any time: iPhone Settings → Privacy &amp; Security → Tracking.</li>
<li>In the EEA, the UK and Switzerland you can change or withdraw your consent to ads in the app: Settings → Ad privacy choices.</li>
<li>Turn the iCloud copy on or off in the app's Settings.</li>
<li>Buy Pro to stop ads completely.</li>
</ul>
<h2>Purchases</h2>
<p>Pro and optional boards are sold through the App Store. Payment is handled by Apple; we do not receive your payment details or personal information.</p>
<h2>Children</h2>
<p>The app is not directed at children under 13 and we do not knowingly collect their data.</p>
<h2>Changes and contact</h2>
<p>If this policy changes, the new version will be published on this page with a new date. Questions: {contact('en')}</p>"""
    else:
        privacy = f"""<h1>Политика конфиденциальности — {a['name']['ru']}</h1>
<p class="muted">{t['updated']}: {UPDATED}</p>
<p>Для игры не нужен аккаунт, и партии никуда не отправляются. Единственная сторонняя служба в приложении — реклама Google AdMob, о ней ниже.</p>
<h2>Что хранится на устройстве</h2>
<p>Партии, история, статистика и настройки хранятся на вашем iPhone (текущая партия — в связке ключей, остальное — в хранилище приложения). Своих серверов у нас нет, и мы эти данные не получаем.</p>
<h2>iCloud (по желанию)</h2>
<p>Если включить «Сохранять прогресс в iCloud», история, статистика, журнал бросков и настройки копируются в ваше личное хранилище iCloud, чтобы появиться на других ваших устройствах. Копию хранит Apple под вашим Apple ID; мы её не видим. Выключается в настройках в любой момент.</p>
<h2>Реклама</h2>
<p>В бесплатной версии между партиями показывается реклама, а за ролик по желанию даются подсказки. Рекламу показывает Google AdMob. Для показа, подсчёта и защиты от мошенничества он может собирать идентификаторы устройства, примерное местоположение (по IP-адресу) и сведения о просмотрах и нажатиях.</p>
<ul>
<li>Перед персонализированной рекламой iOS спрашивает разрешение на отслеживание (App Tracking Transparency). Если отказаться, Google показывает только неперсонализированную рекламу.</li>
<li>В ЕЭЗ, Великобритании и Швейцарии сначала запрашивается согласие (форма Google).</li>
<li>Политика Google: <a href="https://policies.google.com/technologies/partner-sites">как Google использует данные из приложений партнёров</a>.</li>
</ul>
<p>Реклама никогда не влияет на кости и компьютер. Pro убирает рекламу полностью.</p>
<h2>Покупки</h2>
<p>Pro и дополнительные доски продаются через App Store. Оплату проводит Apple; мы не получаем ни платёжных, ни личных данных.</p>
<h2>Дети</h2>
<p>Приложение не предназначено для детей младше 13 лет, и мы сознательно не собираем их данные.</p>
<h2>Изменения и связь</h2>
<p>Если политика изменится, новая версия появится на этой странице с новой датой. Вопросы: {contact('ru')}</p>"""
    page(lang, base + "privacy", t["privacy"] + " — " + a["name"][lang], privacy, sub=app_nav(lang, base, "privacy"))

    # Поддержка
    if lang == "en":
        support = f"""<h1>Support — {a['name']['en']}</h1>
<p>Write to us: {contact('en')}</p>
<h2>Frequently asked</h2>
<p><b>Are the dice really random?</b> Yes, and you can check it. See <a href="{url('en', base + 'verify')}">how to verify the dice</a> and the <a href="{url('en', base + 'dice-report')}">100-million-roll report</a>.</p>
<p><b>Does the level change the dice?</b> No. The level only changes the computer's moves; the rolls are sealed before the game.</p>
<p><b>I bought Pro or a board on another device.</b> Settings → Restore purchases.</p>
<p><b>What does Pro include?</b> No ads and unlimited hints, forever. Everything else in the game is free.</p>
<p><b>How many hints are free?</b> 3 a day against the computer, plus 3 more for each video you choose to watch. Games with a friend have no hints.</p>
<p><b>My games on a new iPhone.</b> Turn on Settings → Save progress to iCloud on both phones with the same Apple ID.</p>
<p><b>Which rules are used in long nardy?</b> Standard tournament rules: one checker from the head per turn (except 6-6, 4-4, 3-3 on the first roll), no six-point wall in front of all opposing checkers, mars counts 2 points.</p>"""
    else:
        support = f"""<h1>Поддержка — {a['name']['ru']}</h1>
<p>Напишите нам: {contact('ru')}</p>
<h2>Частые вопросы</h2>
<p><b>Кости правда случайные?</b> Да, и это можно проверить. Смотрите <a href="{url('ru', base + 'verify')}">как проверить кости</a> и <a href="{url('ru', base + 'dice-report')}">отчёт о 100 млн бросков</a>.</p>
<p><b>Уровень влияет на кости?</b> Нет. Уровень меняет только ходы компьютера, броски запечатаны до партии.</p>
<p><b>Купил Pro или доску на другом устройстве.</b> Настройки → Восстановить покупки.</p>
<p><b>Что даёт Pro?</b> Без рекламы и подсказки без ограничений — навсегда. Всё остальное в игре бесплатно.</p>
<p><b>Сколько подсказок бесплатно?</b> 3 в день в игре против компьютера и ещё 3 за каждый ролик по желанию. В игре вдвоём подсказок нет.</p>
<p><b>Мои партии на новом iPhone.</b> Включите «Настройки → Сохранять прогресс в iCloud» на обоих телефонах с одним Apple ID.</p>
<p><b>По каким правилам длинные нарды?</b> По турнирным правилам: с головы одна шашка за ход (кроме 6-6, 4-4, 3-3 первым броском), нельзя ставить шесть пунктов подряд перед всеми шашками соперника, марс — 2 очка.</p>"""
    page(lang, base + "support", t["support"] + " — " + a["name"][lang], support, sub=app_nav(lang, base, "support"))

    verify_page(lang, base)
    report_page(lang, base)


def verify_page(lang, base):
    ru = lang == "ru"
    L = (lambda en, r: r if ru else en)
    body = f"""<h1>{L('Verify the dice', 'Проверка костей')}</h1>
<p class="muted">{L('Everything runs in your browser. Nothing is sent anywhere. You can save this page and use it offline.',
                     'Всё считается в вашем браузере, ничего никуда не отправляется. Страницу можно сохранить и открыть без интернета.')}</p>
<label>{L('Fingerprint shown before the game', 'Отпечаток, показанный до партии')} <input id="c" placeholder="64 hex"></label>
<label>{L('Key shown after the game', 'Ключ, показанный после партии')} <input id="k" placeholder="64 hex"></label>
<label>{L('Phrase', 'Фраза')} <input id="p"></label>
<label>{L('Number of rolls', 'Сколько бросков')} <input id="n" type="number" value="60"></label>
<button id="go">{L('Verify', 'Проверить')}</button>
<p id="verdict"></p>
<pre id="out" hidden></pre>

<h2>{L('How the dice work', 'Как устроены кости')}</h2>
<ol>
<li>{L('<b>Key.</b> Before the game the app takes 32 random bytes from the phone\'s cryptographic generator. This is the secret key of the game.',
       '<b>Ключ.</b> Перед партией приложение берёт 32 случайных байта из криптографического генератора телефона. Это секретный ключ партии.')}</li>
<li>{L('<b>Fingerprint.</b> Before the first roll the app shows SHA-256 of the key — a sealed envelope. Finding another key with the same fingerprint is practically impossible, so the rolls cannot be changed afterwards.',
       '<b>Отпечаток.</b> До первого броска приложение показывает SHA-256 ключа — запечатанный конверт. Подобрать другой ключ с тем же отпечатком практически невозможно, поэтому броски нельзя подменить.')}</li>
<li>{L('<b>Roll number <i>i</i></b> (from 0, the opening roll included) = HMAC-SHA256(key, <code>narde-v1|phrase|i</code>). Bytes 252–255 are skipped; every other byte <i>b</i> gives a die <code>b mod 6 + 1</code>, so all six faces are exactly equally likely. The first two dice are the roll. If a block has fewer than two usable bytes (chance ≈ 10<sup>−55</sup>), the next one is <code>…|i|1</code>.',
       '<b>Бросок номер <i>i</i></b> (с нуля, включая розыгрыш первого хода) = HMAC-SHA256(ключ, <code>narde-v1|фраза|i</code>). Байты 252–255 пропускаются; каждый остальной байт <i>b</i> даёт кость <code>b mod 6 + 1</code>, поэтому все шесть граней ровно равновероятны. Первые две кости — бросок. Если в блоке меньше двух годных байт (вероятность ≈ 10<sup>−55</sup>), берётся <code>…|i|1</code>.')}</li>
<li>{L('<b>After the game</b> the key is revealed. Its SHA-256 must equal the fingerprint, and the rolls computed from it must equal the roll log in the app. The computer\'s level never touches the dice.',
       '<b>После партии</b> ключ раскрывается. Его SHA-256 должен совпасть с отпечатком, а броски из него — с журналом бросков в приложении. Уровень компьютера на кости не влияет.')}</li>
</ol>

<h2>{L('Check without our site', 'Проверка без нашего сайта')}</h2>
<p>{L('You do not have to trust this page. The algorithm uses only standard SHA-256 and HMAC, available in every programming language.',
      'Этой странице можно не доверять. Алгоритм использует только стандартные SHA-256 и HMAC, они есть в любом языке программирования.')}</p>
<p><b>Python</b> {L('(any computer, nothing to install):', '(на любом компьютере, ничего ставить не нужно):')}</p>
<pre>import hashlib, hmac
key = bytes.fromhex("{L('PASTE THE KEY', 'ВСТАВЬТЕ КЛЮЧ')}")
phrase = "{L('PASTE THE PHRASE', 'ВСТАВЬТЕ ФРАЗУ')}"
print(hashlib.sha256(key).hexdigest())   # {L('must equal the fingerprint', 'должен совпасть с отпечатком')}
for i in range(60):
    mac = hmac.new(key, f"narde-v1|{{phrase}}|{{i}}".encode(), hashlib.sha256).digest()
    print(i, [b % 6 + 1 for b in mac if b &lt; 252][:2])</pre>
<p><b>CyberChef</b> — {L('an open tool by GCHQ that runs in the browser', 'открытый инструмент британской GCHQ, работает в браузере')}: <a href="https://gchq.github.io/CyberChef/">gchq.github.io/CyberChef</a>.
{L('Add the operation <i>HMAC</i>, key type <i>Hex</i>, paste the key, function <i>SHA256</i>; type <code>narde-v1|phrase|0</code> as input. Read the result two hex digits at a time: skip fc, fd, fe, ff; convert the rest to a number, take the remainder after dividing by 6 and add 1.',
   'Добавьте операцию <i>HMAC</i>, тип ключа <i>Hex</i>, вставьте ключ, функция <i>SHA256</i>; на вход — <code>narde-v1|фраза|0</code>. Читайте результат по две hex-цифры: fc, fd, fe, ff пропускайте; остальные переведите в число, возьмите остаток от деления на 6 и прибавьте 1.')}</p>

<h2>{L('Test example', 'Проверочный пример')}</h2>
<p>{L('Key', 'Ключ')} <code>000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f</code>, {L('phrase', 'фраза')} <code>test</code>:</p>
<pre>{L('fingerprint', 'отпечаток')} 630dcd2966c4336691125448bbb25b4ff412a49c732db2c8abc1b8581bd710dd
{L('roll', 'бросок')} 0: HMAC c0a03654… → c0 = 192 → 192 mod 6 + 1 = 1; a0 = 160 → 5   → 1-5
{L('roll', 'бросок')} 1: HMAC 1b6b74e5… → 1b = 27 → 4;  6b = 107 → 6                  → 4-6
{L('roll', 'бросок')} 2: HMAC 32c986d4… → 32 = 50 → 3;  c9 = 201 → 4                  → 3-4</pre>
<p class="muted">{L("The same example is checked by the app's automated tests, so the app, this page and the Python script always agree.",
                    'Этот же пример проверяют автоматические тесты приложения, поэтому приложение, эта страница и скрипт всегда совпадают.')}</p>

<script>
const hex = s => new Uint8Array((s.trim().match(/../g) || []).map(h => parseInt(h, 16)));
const toHex = b => [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, "0")).join("");
async function roll(key, phrase, i) {{
  for (const suffix of ["", "|1", "|2"]) {{
    const mac = new Uint8Array(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(`narde-v1|${{phrase}}|${{i}}${{suffix}}`)));
    const dice = [...mac].filter(b => b < 252).map(b => b % 6 + 1).slice(0, 2);
    if (dice.length === 2) return dice;
  }}
}}
document.getElementById("go").onclick = async () => {{
  const raw = hex(document.getElementById("k").value);
  const v = document.getElementById("verdict"), out = document.getElementById("out");
  if (raw.length !== 32) {{ v.className = "bad"; v.textContent = "{L('The key must be 64 hex characters.', 'Ключ — 64 hex-символа.')}"; return; }}
  const fp = toHex(await crypto.subtle.digest("SHA-256", raw));
  const expected = document.getElementById("c").value.trim().toLowerCase();
  const ok = fp === expected;
  v.className = ok ? "ok" : "bad";
  v.textContent = ok ? "{L('The key matches the fingerprint: the rolls were fixed before the game.', 'Ключ совпал с отпечатком: броски были зафиксированы до партии.')}"
                     : "{L('The key does NOT match the fingerprint.', 'Ключ НЕ совпадает с отпечатком.')}";
  const key = await crypto.subtle.importKey("raw", raw, {{ name: "HMAC", hash: "SHA-256" }}, false, ["sign"]);
  const phrase = document.getElementById("p").value, n = Math.min(1000, +document.getElementById("n").value || 0);
  const lines = [];
  for (let i = 0; i < n; i++) lines.push(`${{i}}  ${{(await roll(key, phrase, i)).join("-")}}`);
  out.hidden = false;
  out.textContent = "{L('Compare with the roll log in the app:', 'Сравните с журналом бросков в приложении:')}\\n" + lines.join("\\n");
}};
</script>"""
    page(lang, base + "verify", L("Verify the dice", "Проверка костей") + " — Backgammon: Fair Dice", body, sub=app_nav(lang, base, "verify"))


def report_page(lang, base):
    ru = lang == "ru"
    L = (lambda en, r: r if ru else en)
    rows = [("21 roll types", "21 тип броска", 31.0, 20, 0.055),
            ("36 ordered pairs", "36 упорядоченных пар", 39.4, 35, 0.279),
            ("first die, 6 faces", "первая кость, 6 граней", 9.7, 5, 0.084),
            ("second die, 6 faces", "вторая кость, 6 граней", 1.2, 5, 0.946),
            ("opening roll of a game", "первый бросок партии", 41.7, 35, 0.202),
            ("independence of consecutive rolls (21×21)", "независимость соседних бросков (21×21)", 406.2, 400, 0.404)]
    table = "".join(f"<tr><td>{L(e, r)}</td><td>{c}</td><td>{df}</td><td>{p}</td></tr>" for e, r, c, df, p in rows)
    body = f"""<h1>{L('Fair dice: 100 million rolls', 'Честность костей: 100 млн бросков')}</h1>
<p class="lead">{L("We ran the app's real dice generator: 1,000,000 new games of 100 rolls, each with a fresh key from the system's cryptographic generator — exactly as in a game.",
                   'Мы прогнали настоящий генератор костей приложения: 1 000 000 новых партий по 100 бросков, у каждой свой ключ из системного криптогенератора — как в игре.')}</p>
<h2>{L('Results', 'Результат')}</h2>
<ul>
<li>{L('Doubles: 16.6620% (expected 16.6667%; deviation −1.26 σ — ordinary chance).', 'Дубли: 16.6620% при ожидании 16.6667% (отклонение −1.26 σ — обычная случайность).')}</li>
<li>{L('Pips per roll: 8.1669 (expected 8.1667).', 'Очки за бросок: 8.1669 при ожидании 8.1667.')}</li>
<li>{L('Longest run of doubles in a row: 9. Runs of 3, 4 and 5 doubles: 315,515, 51,911 and 8,610 — each longer run about 6 times rarer, as it should be.',
       'Самая длинная серия дублей подряд: 9. Серий по 3, 4 и 5 дублей: 315 515, 51 911 и 8 610 — каждая следующая длина реже примерно в 6 раз, как и должно быть.')}</li>
</ul>
<h2>{L('Chi-square tests', 'Критерии χ²')}</h2>
<p class="muted">{L('p is the chance that perfect dice deviate as much or more. Anything above 0.01 means no deviation.',
                     'p — вероятность, что идеальные кости отклонятся так же или сильнее. Всё выше 0.01 — отклонений нет.')}</p>
<table><tr><th>{L('Test', 'Проверка')}</th><th>χ²</th><th>{L('d.f.', 'ст. св.')}</th><th>p</th></tr>{table}</table>
<p>{L('Conclusion: faces, pairs and roll types are uniform, consecutive rolls are independent, and the opening roll is no different from the others. The generator behaves like perfect dice.',
      'Вывод: грани, пары и типы броска распределены равномерно, соседние броски независимы, первый бросок партии не отличается от остальных. Генератор ведёт себя как идеальные кости.')}</p>
<p><a href="{url(lang, base + 'verify')}">{L('Verify the dice of your own game →', 'Проверить кости своей партии →')}</a></p>"""
    page(lang, base + "dice-report", L("Dice report", "Отчёт о костях") + " — Backgammon: Fair Dice", body, sub=app_nav(lang, base, "dice-report"))




# ── Лётная книжка ─────────────────────────────────────────────────────


def logbook_nav(lang, base, current):
    t = T[lang]
    return app_nav(lang, base, current, items=[("", t["overview"]), ("privacy", t["privacy"]),
                                               ("terms", t["terms"]), ("support", t["support"])])


def logbook_pages(lang):
    """Страницы Pilot Logbook. Рынок США — тексты только на английском."""
    if lang != "en":
        return
    a, t = next(x for x in APPS if x["slug"] == "logbook"), T[lang]
    base = "/logbook/"
    store = app_store_badge(a["store"]) if a["store"] else f'<span class="badge">{t["soon"]}</span>'
    hero = f'<div class="hero"><img src="{a["icon"]}" alt=""><div><h1>{a["name"]["en"]}</h1>{store}</div></div>'

    shot = lambda n, cap: (f'<figure><img src="/assets/logbook/{n}.jpg" alt="{html.escape(cap)}" '
                           f'width="368" height="800" loading="lazy"><figcaption>{cap}</figcaption></figure>')
    feature = lambda title, text: f"<div><b>{title}</b><p>{text}</p></div>"
    features = "".join(feature(*f) for f in [
        ("Entry in seconds", "A new flight opens with the aircraft, route and distance of the last one. Repeat a flight or reverse the route in one tap; “Save and next” keeps the form open for a day of pattern work."),
        ("Whole minutes", "Time is kept in minutes, not decimal hours. Three legs of 40 minutes add up to 2:00, not to 2:01."),
        ("Totals that match", "PIC, SIC, solo, dual received, dual given, night, actual and simulated instrument — in total, over the last 12 months and over any period, split by class and by type."),
        ("Cross-country, all seven ways", "14 CFR 61.1 defines cross-country seven times: 50, 25 and 15 nautical miles and no distance at all. Pick what you are counting toward and the app counts that one."),
        ("Currency", "Three takeoffs and landings in 90 days per category and class, the night window of 61.57(b) with full-stop landings, and instrument currency with the six-month window of 61.57(d) and the IPC after it."),
        ("Deadlines", "Medical duration by class, age at the exam and kind of operation (61.23(d)); flight review through the 24th calendar month (61.56). Reminders 60, 30 and 7 days before."),
        ("Form 8710-1", "The Record of Pilot Time grid, filled from your flights — the part of the application people recount by hand."),
        ("Progress to a rating", "Hours against 61.109 for private, 61.65 for instrument and 61.129 for commercial: what is covered and what is left."),
        ("Import and export", "Files from ForeFlight, LogTen and MyFlightbook come in; CSV and a printable PDF go out. The import shows what will be added, updated and skipped before it writes anything."),
        ("Instructor signatures", "An instructor signs on the phone with a finger or an Apple Pencil; the entry then locks, and editing it takes removing the signature, which is recorded."),
        ("Night time suggested", "Civil twilight for your route and date, computed on the device from the airport database. The suggestion is editable."),
        ("Works with no signal", "Airports ship with the app. Entry, totals, currency and export need no connection, no account and no server — only buying goes through the App Store."),
        ("A copy in your iCloud", "With the full version the logbook is copied to your own iCloud Drive after every change, as one CSV file you can open in Files. A new phone or a reinstall offers to restore it. It is a copy, not a sync between two devices — merging two logbooks is where other apps lose entries."),
    ])
    plans = ("<div class=\"plans\">"
             "<div><h3>Free</h3><ul><li>The first 25 flights you type in</li>"
             "<li>Imported flights do not use up the 25</li>"
             "<li>Totals, currency and CSV export included</li></ul></div>"
             "<div><h3>$24.99 a year</h3><ul><li>Unlimited flights</li><li>Copy in your iCloud Drive</li>"
             "<li>Renews yearly until cancelled</li></ul></div>"
             "<div><h3>$59.99 once</h3><ul><li>Unlimited flights</li><li>Copy in your iCloud Drive</li>"
             "<li>One payment, no renewal</li></ul></div>"
             "<p class=\"note\">Prices are in US dollars and may differ in your country's App Store.</p></div>")

    body = f"""{hero}
<p class="lead">A logbook for US pilots. You log the flight; the app keeps the totals, the 90-day and instrument currency, the medical and flight-review dates, and the Record of Pilot Time grid of FAA Form 8710-1.</p>
<div class="shots">{shot('flights', 'The book: a flight is a line, a tap opens it')}{shot('totals', 'Totals by role and condition, by class and by type')}{shot('currency', 'Currency with the date each one runs out')}{shot('f8710', 'The 8710-1 Record of Pilot Time grid')}</div>
<h2>What it does</h2>
<div class="features">{features}</div>
<h2>Price</h2>
{plans}
<h2>Your data stays yours</h2>
<p>There is no account and no server of ours. The book is stored on your device; with the full version a copy also goes to your own iCloud Drive, where only you can read it. There is no analytics and no advertising code. The rest of the network traffic is Apple's own: the App Store, asked for the price and for whether you have bought. Details are on the <a href="{url(lang, base + 'privacy')}">privacy page</a>.</p>
<p class="muted">You are responsible for your own logbook and for meeting the regulations that apply to you. The app computes from what you enter, following 14 CFR part 61; it does not replace the regulations, your instructor or your own check. This app is independent and is not affiliated with or endorsed by the Federal Aviation Administration.</p>"""
    page(lang, base, a["name"]["en"] + " — a pilot logbook for iPhone and iPad", body,
         desc="A pilot logbook for iPhone: totals, 90-day and instrument currency, medical and flight review dates, and the FAA Form 8710-1 Record of Pilot Time.",
         sub=logbook_nav(lang, base, ""))

    privacy = f"""<h1>Privacy Policy — {a['name']['en']}</h1>
<p class="muted">{t['updated']}: {UPDATED}</p>
<h2>The short version</h2>
<p>The app collects nothing. It has no account and no server of ours, and it never sends your logbook to us or to anyone else. The book is stored on your device; with the full version a copy is also written to your own iCloud Drive, under your Apple Account, where only you can read it.</p>
<h2>What is stored, and where</h2>
<ul>
<li><b>Your logbook</b> — flights, aircraft, instructor signatures, your certificates, medical and flight review dates, and the settings of the app. All of it lives in the app's own storage on the device.</li>
<li><b>Backup copies</b> — on launch the app writes a copy of the book as a CSV file inside its own storage and keeps the five most recent ones. These stay on the device.</li>
<li><b>The iCloud copy</b> — with the full version the app also writes the book to your own iCloud Drive, after every change, as a single CSV file you can see in Files. It goes to your Apple Account, not to us; we have no access to it and no way to read it. Turn it off in iPhone Settings → your Apple Account → iCloud → Apps Using iCloud, and the app keeps working with the local copies.</li>
<li><b>Airports</b> — the airport database ships inside the app; nothing is looked up online.</li>
</ul>
<h2>What is not there</h2>
<ul>
<li>No analytics, no crash reporting service, no advertising, no third-party SDKs.</li>
<li>No server of ours: there is nowhere for your flights to be sent, and nothing to hack into.</li>
<li>No tracking, in the sense of Apple's App Tracking Transparency: nothing to permit, because nothing is collected.</li>
<li>No location access: night time is computed from the airports you enter, not from where the phone is.</li>
<li>No e-mail address, name or password is asked for.</li>
</ul>
<h2>When data does leave the device — because you send it</h2>
<ul>
<li><b>Export.</b> CSV and PDF files go where you send them: a file you save, a message you write, a printer. We do not see them.</li>
<li><b>Import.</b> A file you choose is read on the device.</li>
<li><b>Device backup.</b> If you have iCloud Backup or an encrypted computer backup turned on, iOS includes the app's data in it, under Apple's terms.</li>
<li><b>iCloud Drive.</b> The copy described above is stored by Apple in your own iCloud, under Apple's privacy policy and your Apple Account. Deleting the file in Files deletes the copy.</li>
<li><b>Purchases.</b> The subscription and the one-time unlock are sold by Apple. To show the price and to know whether you have bought, the app asks Apple's StoreKit, which talks to the App Store — that is the only network traffic in the app, it carries no logbook data, and it is covered by Apple's privacy policy. Apple processes the payment and tells the app only whether the purchase is active; we receive no payment details and no identity from it.</li>
<li><b>Reminders.</b> Notifications about your medical and flight review are local to the device; no reminder is sent through any server.</li>
</ul>
<h2>How long it is kept, and how to delete it</h2>
<p>Everything is kept for as long as the app is on your device, because it is on your device. Delete a flight and it is gone from the book; delete the app and iOS removes its storage, including the local backup copies. The iCloud copy stays in your iCloud Drive until you delete the file yourself — that is the point of it, and it is deleted like any other file in Files. There is nothing on our side to request or to erase. Export your book first if you want to keep it.</p>
<h2>Children</h2>
<p>The app is a tool for pilots and is not directed to children under 13. It collects nothing from anyone.</p>
<h2>Changes and contact</h2>
<p>If this policy changes, the new version appears on this page with a new date. Questions: {contact('en')}</p>"""
    page(lang, base + "privacy", t["privacy"] + " — " + a["name"]["en"], privacy,
         desc="Privacy policy for Pilot Logbook: no collection, no network calls, no account.",
         sub=logbook_nav(lang, base, "privacy"))

    terms = f"""<h1>Terms of Use — {a['name']['en']}</h1>
<p class="muted">{t['updated']}: {UPDATED}</p>
<p>The app is licensed to you under Apple's <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Standard Licensed Application End User License Agreement</a>. These terms add what is specific to this app.</p>
<h2>What the app is</h2>
<p>Pilot Logbook records flights and computes from them: totals, cross-country under the definitions of 14 CFR 61.1, recent flight experience under 61.57, the deadlines of 61.23(d) and 61.56, progress toward the aeronautical experience of 61.109, 61.65 and 61.129, and the Record of Pilot Time grid of FAA Form 8710-1.</p>
<h2>Your logbook is yours to keep correct</h2>
<p>Logging flight time and meeting the requirements that apply to you are your responsibility as a pilot. The app computes from the data you enter; wrong or missing entries give wrong results, and rules change. Check what the app tells you against the regulations and, where it matters, with your instructor or examiner. The app does not give regulatory or legal advice and is not a substitute for the current text of the regulations.</p>
<h2>Independence</h2>
<p>This app is made by one developer. It is not affiliated with, endorsed by or sponsored by the Federal Aviation Administration, and it is not connected with ForeFlight, LogTen or MyFlightbook — importing their files does not imply any relationship.</p>
<h2>Purchases</h2>
<ul>
<li><b>Free.</b> The first 25 flights you enter by hand are free, and flights brought in by import do not use them up. Reading, totals, currency and CSV export work in the free version.</li>
<li><b>Subscription.</b> $24.99 per year, charged to your Apple Account at confirmation of purchase. It renews automatically for another year unless you turn off auto-renewal at least 24 hours before the current period ends; the renewal is charged within 24 hours before that. Manage or cancel it in Settings → your Apple Account → Subscriptions.</li>
<li><b>One-time unlock.</b> $59.99 once, for the same features, with nothing to renew.</li>
<li>Prices are in US dollars; your App Store may show a different price and currency. Apple processes payments, renewals and refunds under its own rules. Restore a purchase on another device with Settings → Restore purchases in the app.</li>
</ul>
<h2>Data</h2>
<p>Your book stays on your device, and with the full version a copy is written to your own iCloud Drive (see the <a href="{url(lang, base + 'privacy')}">privacy page</a>). That copy is a copy, not a sync: the app writes it and never merges two devices. Keeping your own copies is up to you as well — the app writes local backups on launch and exports CSV and PDF at any time, including in the free version.</p>
<h2>No warranty</h2>
<p>The app is provided “as is”, without warranties of any kind. We work to keep the calculations right and test them against the text of the regulations, but we do not warrant that the app is free of errors or fit for any particular purpose, and we are not liable for decisions made from its output.</p>
<h2>Changes and contact</h2>
<p>If these terms change, the new version is published on this page with a new date. Questions: {contact('en')}</p>"""
    page(lang, base + "terms", t["terms"] + " — " + a["name"]["en"], terms,
         desc="Terms of use for Pilot Logbook, including subscription and one-time purchase terms.",
         sub=logbook_nav(lang, base, "terms"))

    support = f"""<h1>Support — {a['name']['en']}</h1>
<p>Write to us: {contact('en')}. One person reads that mailbox, and answers in a day or two. A screenshot and your iOS version help.</p>
<h2>Frequently asked</h2>
<p><b>How do I move my logbook in?</b> Settings → Import, then pick a file exported from ForeFlight, LogTen or MyFlightbook. You see how many entries will be added, updated and skipped, and why, before anything is written. Importing the same file twice does not duplicate flights.</p>
<p><b>What is free?</b> The first 25 flights you type in yourself. Flights that come in by import do not use them up, and reading, totals, currency and CSV export keep working.</p>
<p><b>I bought on another device.</b> Settings → Restore purchases.</p>
<p><b>How do I cancel the subscription?</b> In iOS Settings → your Apple Account → Subscriptions, at least 24 hours before the year ends. Cancelling leaves the book on your device.</p>
<p><b>My totals differ from my old logbook by a minute or two.</b> This app keeps time in whole minutes and converts to decimal hours only for display and export. Apps that store decimal hours round every leg, and the rounding adds up.</p>
<p><b>Which cross-country does it count?</b> The one you choose. 14 CFR 61.1 has seven definitions with different distances, so the answer depends on what the time is for; the totals screen lets you pick.</p>
<p><b>Why is a flight not counting toward night currency?</b> 61.57(b) uses the window from one hour after sunset to one hour before sunrise and requires landings to a full stop — a different window from the night flight time of 1.1, which uses civil twilight. The app counts both, separately.</p>
<p><b>Can my instructor sign on the phone?</b> Yes — open the flight, Sign, and the instructor signs with a finger or an Apple Pencil and enters their name and certificate number. The entry is then locked; to edit it, remove the signature, which is recorded.</p>
<p><b>How do I get a paper copy?</b> Export → PDF gives printable spreads with carried-forward totals, page numbers and room for signatures. Export → CSV gives the data itself.</p>
<p><b>What happens to my logbook on a new phone?</b> With the full version the book is copied to your own iCloud Drive after every change. Install the app on the new phone, and it offers to restore from that copy — you see how many entries will be added before anything is written. It is a copy for moving and for reinstalls, not a sync: the app does not merge two devices editing at once.</p>
<p><b>How do I delete my data?</b> Delete flights in the app, or delete the app. The iCloud copy is a file in your own iCloud Drive — delete it in Files. Nothing is stored anywhere else.</p>
<p><b>Does it need a connection?</b> Not for flying or for logging. Airports ship with the app; entry, totals, currency and export all work in airplane mode. A connection is needed only to buy or to restore a purchase, because that goes through the App Store.</p>"""
    page(lang, base + "support", t["support"] + " — " + a["name"]["en"], support,
         desc="Support and frequently asked questions for Pilot Logbook.",
         sub=logbook_nav(lang, base, "support"))


# Сайт только на английском; русские тексты в функциях оставлены на случай перевода.
for lang in ("en",):
    home(lang)
    nardy_pages(lang)
    logbook_pages(lang)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".nojekyll"), "w"):
    pass
print("готово")
