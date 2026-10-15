#!/usr/bin/env python3
"""bio.cmdspace.work/agents 생성기 — 에이전트와 하네스 소개 페이지.

수치와 문구는 아래 DATA 가 정본이다. 고친 뒤 실행하면 agents.html 을 다시 쓴다.
    python3 scripts/build-agents.py
수치 재측정 방법은 docs/06-worklog.md 2026-10-15 항목 참조 (에이전트 정의 수, 리그 수, 스킬 수, 정기 작업 수, Zotero 서지 수).
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEASURED = "2026-10-15"

HERO = {
    "kicker": ("에이전트와 하네스", "Agents & Harness"),
    "title": ("연구와 일을 운영하는<br>에이전트 시스템", "An agent system that<br>runs research and work"),
    "lead": (
        "구요한이 매일 쓰는 에이전트 시스템의 구조와 규모, 대표작입니다. 원문은 Zotero에서 시작하고, 에이전트는 하네스 위에서 일하며, 바꾸는 일은 사람이 승인한 뒤에만 합니다.",
        "The structure, scale and highlights of the agent system Yohan Koo runs every day. Sources start in Zotero, agents work on a harness, and nothing changes without human approval.",
    ),
}

# 1. 앞단: Zotero 연결
ZOTERO = {
    "title": ("1. 원문은 Zotero에서 시작합니다", "1. Sources start in Zotero"),
    "desc": (
        "논문 서지, PDF, 하이라이트는 Zotero 한 곳에 둡니다. 볼트와 위키는 서지를 복사하지 않고 인용 키로 원문을 가리킵니다. 에이전트도 Zotero를 읽기만 합니다.",
        "Citations, PDFs and highlights live in Zotero alone. The vault and wiki point to sources by citekey instead of copying them, and agents only read Zotero.",
    ),
    "steps": [
        (("Zotero", "Zotero"), ("서지, PDF, 하이라이트의 원본", "The original citations, PDFs and highlights")),
        (("인용 키", "Citekey"), ("Better BibTeX가 논문마다 바뀌지 않는 키를 붙입니다", "Better BibTeX gives each paper a stable key")),
        (("CMDS Zotero 플러그인", "CMDS Zotero plugin"), ("인용 넣기, 주석 가져오기, PDF 해당 쪽 열기. 직접 만들어 공개했습니다", "Insert citations, import annotations, jump to the PDF page. Built and open-sourced by me")),
        (("볼트와 위키", "Vault and wiki"), ("본문에는 인용 키만 두고, 에이전트는 키로 원문 위치를 확인합니다", "Notes keep only the citekey; agents check the source location by key")),
    ],
    "stats": [
        ("453", ("Zotero 서지", "Zotero items")),
        ("137", ("Zotero 주석", "Annotations")),
        ("0.6.3", ("플러그인 공개 판", "Plugin release")),
    ],
    "links": [
        (("CMDS Zotero (GitHub)", "CMDS Zotero (GitHub)"), "https://github.com/johnfkoo951/cmds-zotero"),
        (("사용 설명서", "User guide"), "https://apps.cmdspace.work/plugins/cmds-zotero/?lang=ko"),
    ],
}

# 2. 규모
SCALE = {
    "title": ("2. 규모", "2. Scale"),
    "desc": (f"{MEASURED} 실측입니다. 에이전트와 스킬과 하네스를 따로 셉니다.", f"Measured {MEASURED}. Agents, skills and harnesses are counted separately."),
    "stats": [
        ("9 + 1", ("전문 에이전트와 지휘", "Specialists + conductor")),
        ("8", ("작업 리그", "Work rigs")),
        ("120+", ("스킬(절차 패키지)", "Skills (procedures)")),
        ("16", ("정기 작업", "Scheduled jobs")),
        ("10,000+", ("볼트 노트", "Vault notes")),
        ("1,100+", ("LLM Wiki 페이지", "LLM Wiki pages")),
    ],
}

# 3. 구조
LAYERS = {
    "title": ("3. 구조", "3. Structure"),
    "desc": ("아래 층일수록 오래 바뀌지 않습니다. 에이전트라고 부르는 것은 가운데 두 층뿐입니다.", "Lower layers change least. Only the two middle layers are called agents."),
    "rows": [
        (("하네스", "Harness"), ("Claude Code, Codex", "Claude Code, Codex"),
         ("반복 실행, 도구, 맥락, 권한을 주는 실행 환경입니다. 맥 두 대에 OpenRig 작업 리그 8종을 나눠 둡니다(리서치, 블라인드 판정, 덱 제작, 구현과 리뷰 등).",
          "The runtime that provides the loop, tools, context and permissions. Eight OpenRig work rigs are split across two Macs (research, blind review, decks, build and review, and more).")),
        (("지휘 에이전트", "Conductor agent"), ("9요한", "9Yohan"),
         ("일을 나누고 합치며, 밖으로 나가는 결과는 사람의 확인을 거칩니다.", "Splits and merges work; anything going out passes human review.")),
        (("전문 에이전트", "Specialist agents"), ("9개", "9"),
         ("연구, 글쓰기, 교육, 창작, 분석, 관계, 개발, 커뮤니티, 자문. 각자 자기 맥락에서 일하고 결과만 돌려줍니다.",
          "Research, writing, teaching, media, analytics, partnerships, engineering, community, advisory. Each works in its own context and returns results.")),
        (("스킬", "Skills"), ("120여 개", "120+"),
         ("에이전트가 필요할 때 꺼내 읽는 절차서입니다. 덱 제작, 논문 반입, 질문 수신함 처리 등. 스킬은 에이전트가 아닙니다.",
          "Procedures an agent loads when needed: decks, paper intake, inbox handling. A skill is not an agent.")),
        (("규칙 파일", "Rule files"), ("CLAUDE.md, AGENTS.md 외", "CLAUDE.md, AGENTS.md, more"),
         ("모든 에이전트가 먼저 읽는 공개 규칙입니다. 하네스가 바뀌어도 그대로 남습니다.", "Public rules every agent reads first. They stay when the harness changes.")),
    ],
}

# 4. 대표작
WORKS = {
    "title": ("4. 대표작", "4. Highlights"),
    "items": [
        (("과학기술정책연구원 기획연구 지원", "STEPI policy-study support"),
         ("에이전트가 숫자 하나에서 원문 초록까지 근거를 짚고, 판단은 연구진이 확정했습니다. 판마다 기록을 남긴 공개 아카이브.", "Agents traced evidence from a single number back to source abstracts; researchers made the calls. Public archive with every version kept."),
         "https://labs.cmdspace.work/stepi-2045/"),
        (("다중 모델 블라인드 판정", "Blind multi-model review"),
         ("같은 후보를 이름을 가린 채 Claude, GPT, Gemini, Grok 판정석이 따로 판정합니다. 평균을 내지 않고 이견을 사람에게 올립니다.", "Claude, GPT, Gemini and Grok judges score the same anonymized candidates separately. Disagreements go to a human instead of being averaged."),
         None),
        (("매일 브리핑과 주간 회고", "Daily briefings and weekly reviews"),
         ("정기 작업 16개가 데일리 노트, 주간 회고, 작업 기록, 모델 정보 갱신을 남깁니다. 사람은 결정 한 줄만 씁니다.", "Sixteen scheduled jobs write daily notes, weekly reviews, work logs and model updates. The human writes one decision line."),
         None),
        (("질문 창구 Ask", "Ask, the question desk"),
         ("공개 자료를 근거로 답하는 상시 질문 창구입니다. 들어온 질문은 볼트 노트가 되고, 에이전트가 답변 초안을 채웁니다.", "An always-on question desk that answers from public material. Each question becomes a vault note, and an agent drafts the reply."),
         "https://ask.cmdspace.work"),
        (("AKM Index", "AKM Index"),
         ("에이전틱 지식관리 자가 평가 루브릭과 공개 보드. 제출은 30분마다 회수해 점검합니다.", "A self-assessment rubric and public board for agentic knowledge management. Submissions are collected and checked every 30 minutes."),
         "https://akm.cmdspace.work"),
        (("모델 지도", "Model map"),
         ("네 회사 공식 문서에서 매일 모델 정보를 가져와 정리합니다.", "Pulls model information from four vendors' official docs every day."),
         "https://models.cmdspace.work"),
    ],
}

# 5. 원칙
RULES = {
    "title": ("5. 지키는 원칙", "5. Principles"),
    "items": [
        ("읽기는 맡기고, 쓰기는 승인 뒤에만 허락합니다.", "Agents may read freely; writing needs approval."),
        ("만든 에이전트와 검증하는 에이전트를 나눕니다.", "The agent that makes is not the agent that checks."),
        ("원문은 고치지 않고, 무엇을 왜 바꿨는지 기록을 남깁니다.", "Sources stay untouched, and every change is logged with its reason."),
        ("에이전트를 만들기 전에 반복되는 절차부터 스킬로 적습니다.", "Before building an agent, write the repeated procedure down as a skill."),
    ],
}

GLOSSARY = {
    "title": ("용어", "Terms"),
    "items": [
        (("에이전트", "Agent"), ("모델 + 하네스. 자기 맥락을 가지고 계획하고 도구를 쓰며 반복 실행하는 단위", "Model + harness: a unit with its own context that plans, uses tools and runs in a loop")),
        (("하네스", "Harness"), ("모델이 실제로 일하게 하는 반복 실행, 도구, 맥락 관리, 권한", "The loop, tools, context management and guardrails that make a model work")),
        (("스킬", "Skill"), ("에이전트가 불러 쓰는 절차 패키지. 스스로 실행하지 않음", "A procedure package an agent loads; it does not run on its own")),
    ],
    "sources": [
        ("Anthropic: Agent harness design", "https://claude.com/blog/harnessing-claudes-intelligence"),
        ("Claude Code: Skills", "https://code.claude.com/docs/en/skills"),
        ("Claude Code: Subagents", "https://code.claude.com/docs/en/sub-agents"),
    ],
}

RELATED = [
    (("9요한 에이전트 설계", "9Yohan agent design"), "https://9yohan.cmdspace.work"),
    (("CMDS 시스템 파일", "CMDS System Files"), "https://system.cmdspace.work"),
    (("LLM Wiki", "LLM Wiki"), "https://llm-wiki.cmdspace.work"),
    (("CMDSPACE Labs", "CMDSPACE Labs"), "https://labs.cmdspace.work"),
]


def t(pair, tag="span", cls=None, html=False):
    ko, en = pair
    c = f' class="{cls}"' if cls else ""
    if html:
        return f'<{tag}{c} data-ko-html="{escape(ko)}" data-en-html="{escape(en)}">{ko}</{tag}>'
    return f'<{tag}{c} data-ko="{escape(ko)}" data-en="{escape(en)}">{escape(ko)}</{tag}>'


def ext(href, inner, cls="ext"):
    return f'<a class="{cls}" href="{href}" target="_blank" rel="noopener">{inner}</a>'


def stats(items):
    return '<div class="stats">' + "".join(
        f'<div class="stat"><span class="num">{escape(n)}</span>{t(lbl, cls="lbl")}</div>' for n, lbl in items) + "</div>"


def section(sid, title, body, desc=None):
    d = t(desc, "p", "desc") if desc else ""
    return f'<section id="{sid}" aria-labelledby="{sid}-t"><h2 id="{sid}-t" data-ko="{escape(title[0])}" data-en="{escape(title[1])}">{escape(title[0])}</h2>{d}{body}</section>'


def build():
    z = ZOTERO
    zsteps = "<ol class=\"flow\">" + "".join(
        f'<li><span class="n">{i:02d}</span><div>{t(h, "strong")}{t(b, "p")}</div></li>' for i, (h, b) in enumerate(z["steps"], 1)) + "</ol>"
    zlinks = '<div class="chips">' + "".join(ext(u, t(l)) for l, u in z["links"]) + "</div>"
    s1 = section("zotero", z["title"], zsteps + stats(z["stats"]) + zlinks, z["desc"])
    s2 = section("scale", SCALE["title"], stats(SCALE["stats"]), SCALE["desc"])
    rows = "".join(
        f'<div class="layer"><div class="lh">{t(name, "strong")}{t(what, "span", "what")}</div>{t(desc, "p")}</div>'
        for name, what, desc in LAYERS["rows"])
    s3 = section("structure", LAYERS["title"], f'<div class="layers">{rows}</div>', LAYERS["desc"])
    cards = ""
    for name, desc, url in WORKS["items"]:
        inner = f'{t(name, "strong")}{t(desc, "p")}'
        if url:
            inner += f'<span class="url">{escape(url.replace("https://", "").rstrip("/"))}</span>'
            cards += ext(url, inner, "work")
        else:
            cards += f'<div class="work">{inner}</div>'
    s4 = section("works", WORKS["title"], f'<div class="works">{cards}</div>')
    s5 = section("rules", RULES["title"], "<ul class=\"rules\">" + "".join(f"<li>{t(r)}</li>" for r in RULES["items"]) + "</ul>")
    gl = "<dl class=\"gloss\">" + "".join(f"<div>{t(k, 'dt')}{t(v, 'dd')}</div>" for k, v in GLOSSARY["items"]) + "</dl>"
    gl += '<p class="src">' + " · ".join(ext(u, escape(l)) for l, u in GLOSSARY["sources"]) + "</p>"
    s6 = section("terms", GLOSSARY["title"], gl)
    rel = '<div class="chips">' + "".join(ext(u, t(l)) for l, u in RELATED) + "</div>"
    page = TEMPLATE.format(
        kicker=t(HERO["kicker"], "p", "kicker"), title=t(HERO["title"], "h1", html=True), lead=t(HERO["lead"], "p", "lead"),
        body=s1 + s2 + s3 + s4 + s5 + s6, related=rel, measured=MEASURED)
    (ROOT / "agents.html").write_text(page, encoding="utf-8")
    print("wrote", ROOT / "agents.html")


TEMPLATE = """<!DOCTYPE html>
<html lang="ko" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>에이전트와 하네스 · 구요한 (Yohan Koo) · CMDSPACE</title>
    <meta name="description" content="구요한(CMDSPACE)이 운영하는 에이전트 시스템의 구조, 규모, 대표작. Zotero 원문 연결부터 하네스, 9요한 전문 에이전트, 스킬, 정기 작업까지.">
    <meta name="author" content="구요한 (Yohan Koo)">
    <meta name="theme-color" content="#134538" media="(prefers-color-scheme: light)">
    <meta name="theme-color" content="#06080a" media="(prefers-color-scheme: dark)">
    <link rel="icon" type="image/png" href="/assets/cmds-logo-round.png">
    <link rel="canonical" href="https://bio.cmdspace.work/agents">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="구요한 · CMDSPACE">
    <meta property="og:title" content="에이전트와 하네스 — 구요한 · CMDSPACE">
    <meta property="og:description" content="Zotero 원문 연결, 하네스, 9요한 전문 에이전트, 스킬 120여 개, 정기 작업 16개. 구조와 규모, 대표작.">
    <meta property="og:url" content="https://bio.cmdspace.work/agents">
    <meta property="og:image" content="https://bio.cmdspace.work/assets/og-bio.png">
    <meta name="twitter:card" content="summary_large_image">
    <script>
        (function () {{
            try {{
                var saved = localStorage.getItem("bio-theme");
                var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
                document.documentElement.setAttribute("data-theme", saved || (prefersDark ? "dark" : "light"));
            }} catch (e) {{}}
        }})();
    </script>
    <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
    <style>
        :root {{
            --font-sans: "SF Pro Text", "SF Pro Display", "Pretendard Variable", "Pretendard", system-ui, sans-serif;
            --brand: #134538; --brand-bright: #22896a; --pink: #E985A2; --pink-light: #F4A4B8;
            --bg: #fbfbfa; --bg-elev: #ffffff; --bg-subtle: #f5f6f4;
            --fg: #0a0d0b; --fg-muted: #4a544f; --fg-subtle: #69726d;
            --border: #e6e8e6; --border-strong: #d0d3d0;
            --accent: var(--brand); --accent-strong: #0d3529; --accent-soft: #f1f7f4;
        }}
        [data-theme="dark"] {{
            --bg: #06080a; --bg-elev: #0d1411; --bg-subtle: #0a1110;
            --fg: #f2f4f3; --fg-muted: #9aa39d; --fg-subtle: #7f8883;
            --border: #1a231f; --border-strong: #26302a;
            --accent: var(--pink); --accent-strong: var(--pink-light); --accent-soft: #2b1922;
        }}
        *, *::before, *::after {{ box-sizing: border-box; }}
        * {{ margin: 0; padding: 0; }}
        html {{ -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }}
        body {{ font-family: var(--font-sans); color: var(--fg); background: var(--bg-elev); line-height: 1.55; -webkit-font-smoothing: antialiased; }}
        a {{ color: inherit; text-decoration: none; }}
        button {{ font: inherit; }}
        .page {{ width: min(100%, 596px); margin: 0 auto; padding: 0 16px 56px; }}
        .bar {{ display: flex; align-items: center; justify-content: space-between; gap: 8px; padding: 18px 0 8px; }}
        .back {{ font-size: 13px; font-weight: 750; color: var(--fg-muted); }}
        .back:hover {{ color: var(--accent); }}
        .tools {{ display: flex; gap: 6px; }}
        .tool {{ border: 1px solid var(--border); background: var(--bg-subtle); color: var(--fg-muted); border-radius: 999px; padding: 5px 11px; font-size: 12px; font-weight: 750; cursor: pointer; }}
        .tool:focus-visible, a:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
        header {{ padding: 26px 0 8px; }}
        .kicker {{ color: var(--accent); font-size: 12.5px; font-weight: 850; letter-spacing: .02em; }}
        h1 {{ margin-top: 8px; font-size: clamp(27px, 7vw, 34px); line-height: 1.22; font-weight: 880; letter-spacing: -0.01em; }}
        .lead {{ margin-top: 14px; color: var(--fg-muted); font-size: 15px; line-height: 1.7; }}
        section {{ padding-top: 34px; }}
        h2 {{ font-size: 18px; font-weight: 860; }}
        .desc {{ margin-top: 6px; color: var(--fg-muted); font-size: 14px; line-height: 1.65; }}
        .flow {{ list-style: none; margin-top: 14px; display: grid; gap: 8px; }}
        .flow li {{ display: grid; grid-template-columns: 34px 1fr; gap: 10px; padding: 12px 14px; border: 1px solid var(--border); border-radius: 14px; background: var(--bg); }}
        .flow .n {{ font: 800 12px/1.9 ui-monospace, "SF Mono", monospace; color: var(--accent); }}
        .flow strong {{ display: block; font-size: 15px; font-weight: 820; }}
        .flow p {{ color: var(--fg-muted); font-size: 13.5px; }}
        .stats {{ margin-top: 12px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; }}
        .stat {{ padding: 12px; border-radius: 14px; background: var(--accent-soft); }}
        .stat .num {{ display: block; font-size: 22px; font-weight: 880; color: var(--accent-strong); line-height: 1.2; }}
        .stat .lbl {{ display: block; margin-top: 2px; color: var(--fg-muted); font-size: 12px; font-weight: 650; }}
        .chips {{ margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; }}
        .chips .ext {{ border: 1px solid var(--border-strong); border-radius: 999px; padding: 6px 12px; font-size: 12.5px; font-weight: 760; color: var(--fg-muted); }}
        .chips .ext:hover {{ color: var(--accent); border-color: var(--accent); }}
        .chips .ext::after {{ content: " ↗"; }}
        .layers {{ margin-top: 14px; display: grid; gap: 0; border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }}
        .layer {{ padding: 13px 14px; background: var(--bg); }}
        .layer + .layer {{ border-top: 1px solid var(--border); }}
        .layer:nth-child(2), .layer:nth-child(3) {{ background: var(--accent-soft); }}
        .lh {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 10px; }}
        .lh strong {{ font-size: 15px; font-weight: 840; }}
        .lh .what {{ font-size: 12.5px; font-weight: 760; color: var(--accent); }}
        .layer p {{ margin-top: 4px; color: var(--fg-muted); font-size: 13.5px; }}
        .works {{ margin-top: 14px; display: grid; gap: 8px; }}
        .work {{ display: block; padding: 14px; border: 1px solid var(--border); border-radius: 14px; background: var(--bg); }}
        a.work:hover {{ border-color: var(--accent); }}
        .work strong {{ display: block; font-size: 15px; font-weight: 830; }}
        a.work strong::after {{ content: " ↗"; color: var(--fg-subtle); font-weight: 700; }}
        .work p {{ margin-top: 4px; color: var(--fg-muted); font-size: 13.5px; }}
        .work .url {{ display: block; margin-top: 6px; font: 600 11.5px ui-monospace, "SF Mono", monospace; color: var(--fg-subtle); }}
        .rules {{ margin-top: 12px; list-style: none; display: grid; gap: 6px; }}
        .rules li {{ position: relative; padding-left: 16px; font-size: 14.5px; font-weight: 650; }}
        .rules li::before {{ content: ""; position: absolute; left: 0; top: .62em; width: 7px; height: 7px; border-radius: 999px; background: var(--brand-bright); }}
        [data-theme="dark"] .rules li::before {{ background: var(--accent); }}
        .gloss {{ margin-top: 12px; display: grid; gap: 8px; }}
        .gloss dt {{ font-size: 14px; font-weight: 820; }}
        .gloss dd {{ color: var(--fg-muted); font-size: 13.5px; }}
        .src {{ margin-top: 10px; font-size: 12px; color: var(--fg-subtle); }}
        .src a {{ border-bottom: 1px dotted var(--border-strong); }}
        .src a:hover {{ color: var(--accent); }}
        footer {{ margin-top: 40px; padding-top: 18px; border-top: 1px solid var(--border); color: var(--fg-subtle); font-size: 12px; }}
        footer a {{ color: var(--fg-muted); border-bottom: 1px dotted var(--border-strong); }}
        @media (max-width: 380px) {{ .stats {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
    </style>
    <script>window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};</script>
    <script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
    <main class="page">
        <div class="bar">
            <a class="back" href="/" data-ko="← 구요한 bio" data-en="← Yohan Koo bio">← 구요한 bio</a>
            <div class="tools">
                <button class="tool" id="langBtn" type="button">EN</button>
                <button class="tool" id="themeBtn" type="button" aria-label="다크 모드 전환">◐</button>
            </div>
        </div>
        <header>{kicker}{title}{lead}</header>
        {body}
        <section id="related" aria-labelledby="related-t"><h2 id="related-t" data-ko="함께 보기" data-en="See also">함께 보기</h2>{related}</section>
        <footer><span data-ko="수치 실측 {measured} · 외부 표기는 반올림" data-en="Measured {measured} · public figures rounded">수치 실측 {measured} · 외부 표기는 반올림</span> · <a href="/">bio.cmdspace.work</a> · <a href="https://cmdspace.work">cmdspace.work</a></footer>
    </main>
    <script>
        (function () {{
            var root = document.documentElement;
            var lang = "ko";
            try {{ lang = localStorage.getItem("bio-lang") || "ko"; }} catch (e) {{}}
            var langBtn = document.getElementById("langBtn");
            var themeBtn = document.getElementById("themeBtn");
            function apply(l) {{
                lang = l === "en" ? "en" : "ko";
                root.setAttribute("lang", lang);
                try {{ localStorage.setItem("bio-lang", lang); }} catch (e) {{}}
                document.querySelectorAll("[data-ko][data-en]").forEach(function (el) {{ el.textContent = el.getAttribute(lang === "en" ? "data-en" : "data-ko"); }});
                document.querySelectorAll("[data-ko-html][data-en-html]").forEach(function (el) {{ el.innerHTML = el.getAttribute(lang === "en" ? "data-en-html" : "data-ko-html"); }});
                langBtn.textContent = lang === "en" ? "KO" : "EN";
                langBtn.setAttribute("aria-label", lang === "en" ? "한국어로 전환" : "Switch to English");
            }}
            langBtn.addEventListener("click", function () {{ apply(lang === "en" ? "ko" : "en"); }});
            themeBtn.addEventListener("click", function () {{
                var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
                root.setAttribute("data-theme", next);
                try {{ localStorage.setItem("bio-theme", next); }} catch (e) {{}}
            }});
            apply(lang);
        }})();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
