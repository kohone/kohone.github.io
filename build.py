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
           "soon": "Coming to the App Store", "privacy": "Privacy", "support": "Support", "verify": "Verify the dice",
           "report": "Dice report", "lang": "Русский", "contact_soon": "A support e-mail will appear here soon.",
           "updated": "Last updated"},
    "ru": {"apps": "Приложения", "home_lead": "Делаю приложения и игры для iPhone.",
           "soon": "Скоро в App Store", "privacy": "Конфиденциальность", "support": "Поддержка", "verify": "Проверка костей",
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


def app_nav(lang, base, current):
    """Меню разделов приложения — над содержимым каждой его страницы."""
    t = T[lang]
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


# Сайт только на английском; русские тексты в функциях оставлены на случай перевода.
for lang in ("en",):
    home(lang)
    nardy_pages(lang)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".nojekyll"), "w"):
    pass
print("готово")
