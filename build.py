#!/usr/bin/env python3
"""Сборка сайта kohone.github.io: одна витрина для всех приложений, на английском.

    python3.14 build.py   # нужен Python 3.12+ (f-строки с обратной косой)

Новое приложение — запись в APPS и функция страниц (как nardy_pages). HTML пишется в корень репозитория,
GitHub Pages отдаёт его как есть. Без сервера, без трекеров, без внешних скриптов.
"""
import html
import os

SITE = "https://kohone.github.io"
DEV = "Maks Beskrovnyi"
EMAIL = None  # почта поддержки — будет позже
UPDATED = "2026-09-23"

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


def page(lang, path, title, body, desc=""):
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
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap">© 2026 {DEV}</div></footer>
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
    store = f'<a href="{a["store"]}">App Store</a>' if a["store"] else f'<span class="badge">{t["soon"]}</span>'
    links = (f'<ul class="links"><li><a href="{url(lang, base + "verify")}">{t["verify"]}</a></li>'
             f'<li><a href="{url(lang, base + "dice-report")}">{t["report"]}</a></li>'
             f'<li><a href="{url(lang, base + "privacy")}">{t["privacy"]}</a></li>'
             f'<li><a href="{url(lang, base + "support")}">{t["support"]}</a></li></ul>')
    hero = f'<div class="hero"><img src="{a["icon"]}" alt=""><div><h1>{a["name"][lang]}</h1>{store}</div></div>'

    if lang == "en":
        about = """<p class="lead">Backgammon and long nardy (Russian Nardy Federation rules) against a strong computer or a friend on the same phone. Works offline.</p>
<ul>
<li><b>Fair dice you can verify.</b> Before each game the app seals the rolls and shows their fingerprint; after the game you get the key and can recompute every roll — here, in Python, or with any HMAC tool.</li>
<li><b>A computer that explains.</b> A neural network plays at five levels, shows the best move and explains mistakes in plain words.</li>
<li><b>Review, statistics, lessons.</b> Game review with error rate, dice statistics against fair odds, interactive rules lessons.</li>
<li><b>No accounts.</b> Your games and statistics stay on your phone.</li>
</ul>"""
    else:
        about = """<p class="lead">Короткие и длинные нарды (правила Федерации нард России) против сильного компьютера или вдвоём на одном телефоне. Работает без интернета.</p>
<ul>
<li><b>Честные кости, которые можно проверить.</b> Перед партией приложение запечатывает броски и показывает их отпечаток; после партии вы получаете ключ и пересчитываете каждый бросок — здесь, на Python или любым инструментом HMAC.</li>
<li><b>Компьютер, который объясняет.</b> Нейросеть играет на пяти уровнях, показывает лучший ход и объясняет ошибки простыми словами.</li>
<li><b>Разбор, статистика, уроки.</b> Разбор партии с оценкой ошибок, статистика костей против честных шансов, уроки правил на живой доске.</li>
<li><b>Без аккаунтов.</b> Партии и статистика остаются на вашем телефоне.</li>
</ul>"""
    page(lang, base, a["name"][lang], app_nav(lang, base, "") + hero + about, a["tag"][lang])

    # Политика конфиденциальности
    if lang == "en":
        privacy = f"""<h1>Privacy Policy — {a['name']['en']}</h1>
<p class="muted">{t['updated']}: {UPDATED}</p>
<p><b>The app does not collect any data.</b> It has no accounts and no analytics, and it does not send your games or statistics anywhere.</p>
<h2>What stays on your device</h2>
<p>Your games, history, statistics and settings are stored only on your iPhone (the current game in the Keychain, the rest in the app's own storage). They are deleted when you delete the app. We never receive them.</p>
<h2>Purchases</h2>
<p>Optional boards are sold through the App Store. Payment is handled by Apple; we do not receive your payment details or personal information. Apple's privacy policy applies to purchases.</p>
<h2>Children</h2>
<p>The app does not collect data from anyone, including children.</p>
<h2>Changes and contact</h2>
<p>If this policy changes, the new version will be published on this page with a new date. Questions: {contact('en')}</p>"""
    else:
        privacy = f"""<h1>Политика конфиденциальности — {a['name']['ru']}</h1>
<p class="muted">{t['updated']}: {UPDATED}</p>
<p><b>Приложение не собирает никаких данных.</b> В нём нет аккаунтов, рекламы, аналитики и сторонних SDK, и оно не обращается к нашим серверам — их у нас нет.</p>
<h2>Что хранится на устройстве</h2>
<p>Партии, история, статистика и настройки хранятся только на вашем iPhone (текущая партия — в связке ключей, остальное — в хранилище приложения). Они удаляются вместе с приложением. Мы их не получаем.</p>
<h2>Покупки</h2>
<p>Дополнительные доски продаются через App Store. Оплату проводит Apple; мы не получаем ни платёжных, ни личных данных. К покупкам применяется политика конфиденциальности Apple.</p>
<h2>Дети</h2>
<p>Приложение не собирает данные ни у кого, в том числе у детей.</p>
<h2>Изменения и связь</h2>
<p>Если политика изменится, новая версия появится на этой странице с новой датой. Вопросы: {contact('ru')}</p>"""
    page(lang, base + "privacy", t["privacy"] + " — " + a["name"][lang], app_nav(lang, base, "privacy") + privacy)

    # Поддержка
    if lang == "en":
        support = f"""<h1>Support — {a['name']['en']}</h1>
<p>Write to us: {contact('en')}</p>
<h2>Frequently asked</h2>
<p><b>Are the dice really random?</b> Yes, and you can check it. See <a href="{url('en', base + 'verify')}">how to verify the dice</a> and the <a href="{url('en', base + 'dice-report')}">100-million-roll report</a>.</p>
<p><b>Does the level change the dice?</b> No. The level only changes the computer's moves; the rolls are sealed before the game.</p>
<p><b>I bought a board on another device.</b> Settings → Board → Restore purchases.</p>
<p><b>Which rules are used in long nardy?</b> The Russian Nardy Federation sport rules: one checker from the head per turn (except 6-6, 4-4, 3-3 on the first roll), no six-point wall in front of all opposing checkers, mars counts 2 points.</p>"""
    else:
        support = f"""<h1>Поддержка — {a['name']['ru']}</h1>
<p>Напишите нам: {contact('ru')}</p>
<h2>Частые вопросы</h2>
<p><b>Кости правда случайные?</b> Да, и это можно проверить. Смотрите <a href="{url('ru', base + 'verify')}">как проверить кости</a> и <a href="{url('ru', base + 'dice-report')}">отчёт о 100 млн бросков</a>.</p>
<p><b>Уровень влияет на кости?</b> Нет. Уровень меняет только ходы компьютера, броски запечатаны до партии.</p>
<p><b>Купил доску на другом устройстве.</b> Настройки → Доска → Восстановить покупки.</p>
<p><b>По каким правилам длинные нарды?</b> По спортивным правилам Федерации нард России: с головы одна шашка за ход (кроме 6-6, 4-4, 3-3 первым броском), нельзя ставить шесть пунктов подряд перед всеми шашками соперника, марс — 2 очка.</p>"""
    page(lang, base + "support", t["support"] + " — " + a["name"][lang], app_nav(lang, base, "support") + support)

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
    page(lang, base + "verify", L("Verify the dice", "Проверка костей") + " — Backgammon: Fair Dice", app_nav(lang, base, "verify") + body)


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
    page(lang, base + "dice-report", L("Dice report", "Отчёт о костях") + " — Backgammon: Fair Dice", app_nav(lang, base, "dice-report") + body)


# Сайт только на английском; русские тексты в функциях оставлены на случай перевода.
for lang in ("en",):
    home(lang)
    nardy_pages(lang)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".nojekyll"), "w"):
    pass
print("готово")
