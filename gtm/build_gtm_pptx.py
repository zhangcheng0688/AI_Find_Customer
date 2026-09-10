#!/usr/bin/env python3
"""SLAM.SYSTEMS GTM plan — restrained 8-slide decks, CN + EN."""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import nsmap, qn
from pptx.util import Emu, Inches, Pt
from pptx.oxml import parse_xml
from copy import deepcopy
from lxml import etree

INK = RGBColor(0x11, 0x11, 0x11)
MUTED = RGBColor(0x6B, 0x6B, 0x6B)
LINE = RGBColor(0xE6, 0xE6, 0xE6)
PAPER = RGBColor(0xFF, 0xFF, 0xFF)
WASH = RGBColor(0xF6, 0xF6, 0xF5)
MAGENTA = RGBColor(0xFF, 0x00, 0x4E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK = RGBColor(0x0B, 0x0B, 0x0C)

W = Inches(13.333)
H = Inches(7.5)
ML = Inches(0.62)
MR = Inches(12.70)


def set_run(run, size, color, bold=False, font_name="Calibri"):
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = font_name
    rPr = run._r.get_or_add_rPr()
    # East Asian font for Chinese glyphs
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = etree.SubElement(rPr, qn("a:ea"))
    ea.set("typeface", font_name)


def add_box(slide, l, t, w, h, fill, line=None):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(0.75)
    sh.shadow.inherit = False
    return sh


def add_tf(slide, l, t, w, h, text, size, color, bold=False, font="Calibri", align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}[anchor])
    except Exception:
        pass
    chunks = text.split("\n") if text else [""]
    for i, chunk in enumerate(chunks):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_before = Pt(0)
        p.space_after = Pt(0)
        run = p.add_run()
        run.text = chunk
        set_run(run, size, color, bold, font)
    return box


def add_lines(slide, l, t, w, h, lines, size, color, font, bold=False, leading=1.15):
    """lines: list of str or (str, bold, color) tuples."""
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_before = Pt(0)
        p.space_after = Pt(2)
        p.line_spacing = leading
        if isinstance(item, tuple):
            text, is_bold, col = item
        else:
            text, is_bold, col = item, bold, color
        run = p.add_run()
        run.text = text
        set_run(run, size, col, is_bold, font)
    return box


def footer(slide, page, total, font, right):
    add_tf(slide, ML, Inches(7.18), Inches(6), Inches(0.24), "SLAM.SYSTEMS  ·  GTM 2026 Q4–2027 Q1", 10, MUTED, False, font)
    add_tf(slide, Inches(11.2), Inches(7.18), Inches(1.5), Inches(0.24), f"{page} / {total}", 10, MUTED, False, font, PP_ALIGN.RIGHT)
    add_box(slide, ML, Inches(7.12), Inches(12.08), Pt(0.75), LINE)


def header(slide, kicker, title, font):
    add_tf(slide, ML, Inches(0.28), Inches(12), Inches(0.22), kicker, 11, MAGENTA, True, font)
    add_tf(slide, ML, Inches(0.50), Inches(12.1), Inches(0.42), title, 22, INK, True, font)
    add_box(slide, ML, Inches(0.96), Inches(0.42), Pt(3), MAGENTA)


def card(slide, l, t, w, h, kicker, title, body, font, accent=False):
    add_box(slide, l, t, w, h, WASH if not accent else INK)
    kc = MAGENTA if not accent else MAGENTA
    tc = INK if not accent else WHITE
    bc = MUTED if not accent else RGBColor(0xC8, 0xC8, 0xC8)
    add_tf(slide, l + Inches(0.18), t + Inches(0.14), w - Inches(0.32), Inches(0.22), kicker, 10, kc, True, font)
    add_tf(slide, l + Inches(0.18), t + Inches(0.36), w - Inches(0.32), Inches(0.36), title, 16, tc, True, font)
    add_tf(slide, l + Inches(0.18), t + Inches(0.76), w - Inches(0.32), h - Inches(0.92), body, 12, bc, False, font)


def table_grid(slide, l, t, col_w, row_h, rows, font, header=True):
    """rows: list of list of str. First row header."""
    n_cols = len(rows[0])
    n_rows = len(rows)
    for r, row in enumerate(rows):
        y = t + r * row_h
        bg = INK if (header and r == 0) else (WASH if r % 2 else PAPER)
        fg = WHITE if (header and r == 0) else INK
        for c, cell in enumerate(row):
            x = l + sum(col_w[:c])
            w = col_w[c]
            add_box(slide, x, y, w, row_h, bg, LINE)
            pad = Inches(0.08)
            is_head = header and r == 0
            add_tf(
                slide,
                x + pad,
                y + Inches(0.06),
                w - pad * 2,
                row_h - Inches(0.08),
                cell,
                10 if not is_head else 10,
                fg if not (not is_head and c == 0) else INK,
                is_head or c == 0,
                font,
                PP_ALIGN.LEFT,
                MSO_ANCHOR.MIDDLE,
            )


def gantt(slide, l, t, labels, bars, weeks, font, now_label):
    """
    labels: row names
    bars: list of (start_week_index, span, kind) kind in {now, later, done}
    weeks: list of week labels
    """
    label_w = Inches(2.15)
    chart_w = Inches(9.9)
    row_h = Inches(0.38)
    head_h = Inches(0.32)
    n = len(weeks)
    cell = chart_w / n

    add_box(slide, l, t, label_w + chart_w, head_h + row_h * len(labels), PAPER, LINE)
    add_box(slide, l, t, label_w, head_h, INK)
    add_tf(slide, l + Inches(0.1), t + Inches(0.04), label_w - Inches(0.15), head_h, now_label, 10, WHITE, True, font, PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)

    for i, wlab in enumerate(weeks):
        x = l + label_w + i * cell
        add_box(slide, x, t, cell, head_h, INK)
        add_tf(slide, x, t + Inches(0.04), cell, head_h, wlab, 9, WHITE, False, font, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    colors = {
        "now": MAGENTA,
        "work": INK,
        "later": RGBColor(0xC4, 0xC4, 0xC4),
    }
    for r, lab in enumerate(labels):
        y = t + head_h + r * row_h
        bg = WASH if r % 2 == 0 else PAPER
        add_box(slide, l, y, label_w, row_h, bg, LINE)
        add_tf(slide, l + Inches(0.1), y, label_w - Inches(0.14), row_h, lab, 11, INK, True, font, PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
        for i in range(n):
            add_box(slide, l + label_w + i * cell, y, cell, row_h, bg, LINE)
        start, span, kind = bars[r]
        bx = l + label_w + start * cell + Inches(0.06)
        bw = span * cell - Inches(0.12)
        by = y + Inches(0.10)
        bh = row_h - Inches(0.20)
        add_box(slide, bx, by, bw, bh, colors[kind])


CN = {
    "font": "PingFang SC",
    "file": "/workspace/gtm/SLAM.SYSTEMS_GTM_Plan_CN.pptx",
    "cover_kicker": "SLAM.SYSTEMS  ·  机密",
    "cover_title": "市场进入计划",
    "cover_sub": "Go-to-Market  ·  2026 Q4 – 2027 Q1",
    "cover_line": "先打欧洲职业体育场馆。日韩明年进。社媒只做三家。获客靠名单，不靠广告。",
    "cover_meta": "8 页  ·  直接执行版  ·  2026.09",
    "s2k": "01  /  打哪个市场",
    "s2t": "先打欧洲。日韩排明年。中国是工厂，不是主战场。",
    "s3k": "02  /  卖给谁",
    "s3t": "卖给场馆和集成商，不卖给观众。",
    "s4k": "03  /  接下来 16 周",
    "s4t": "一张图看完：网站何时上线，获客何时开始。",
    "s5k": "04  /  网站上线节点",
    "s5t": "德文先上 slam.systems。三语两周内补齐。",
    "s6k": "05  /  社媒只做这三家",
    "s6t": "LinkedIn 获客。Instagram 证明画面。YouTube 能被搜到。",
    "s7k": "06  /  视频怎么做，客户怎么来",
    "s7t": "三支片子循环用。获客四条线，每周盯数字。",
    "s8k": "07  /  90 天必须交出来的东西",
    "s8t": "日期、负责人、数字。没有第三种状态。",
}

EN = {
    "font": "Calibri",
    "file": "/workspace/gtm/SLAM.SYSTEMS_GTM_Plan_EN.pptx",
    "cover_kicker": "SLAM.SYSTEMS  ·  Confidential",
    "cover_title": "Go-to-Market Plan",
    "cover_sub": "Q4 2026 – Q1 2027",
    "cover_line": "Europe first. Korea and Japan next year. Three social channels only. Named accounts, not ads.",
    "cover_meta": "8 slides  ·  Operating version  ·  September 2026",
    "s2k": "01  /  Where we play",
    "s2t": "Europe now. Korea / Japan in 2027. China is the factory, not the brand battlefield.",
    "s3k": "02  /  Who we sell to",
    "s3t": "Venues and integrators. Not spectators.",
    "s4k": "03  /  Next 16 weeks",
    "s4t": "One chart: when the site goes live, when outreach starts.",
    "s5k": "04  /  Website launch",
    "s5t": "German goes live on slam.systems first. EN/ZH within two weeks.",
    "s6k": "05  /  Three channels only",
    "s6t": "LinkedIn to sell. Instagram for proof. YouTube so buyers can find us.",
    "s7k": "06  /  Video and pipeline",
    "s7t": "Three films, reused everywhere. Four acquisition lines, reviewed weekly.",
    "s8k": "07  /  What must be done in 90 days",
    "s8t": "Date, owner, number. No third status.",
}


def build(C, lang):
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    blank = prs.slide_layouts[6]
    font = C["font"]
    is_cn = lang == "cn"

    # ——— 0 COVER ———
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, DARK)
    add_box(s, 0, 0, Inches(0.12), H, MAGENTA)
    add_tf(s, ML, Inches(1.55), Inches(12), Inches(0.3), C["cover_kicker"], 13, MAGENTA, True, font)
    add_tf(s, ML, Inches(2.05), Inches(12), Inches(0.9), C["cover_title"], 44, WHITE, True, font)
    add_tf(s, ML, Inches(2.95), Inches(12), Inches(0.4), C["cover_sub"], 18, RGBColor(0xB8, 0xB8, 0xB8), False, font)
    add_box(s, ML, Inches(3.50), Inches(1.1), Pt(3.5), MAGENTA)
    add_tf(s, ML, Inches(3.75), Inches(11.2), Inches(1.1), C["cover_line"], 18, WHITE, False, font)
    add_tf(s, ML, Inches(6.85), Inches(12), Inches(0.3), C["cover_meta"], 12, RGBColor(0x8A, 0x8A, 0x8A), False, font)

    # ——— 1 MARKETS ———
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(s, C["s2k"], C["s2t"], font)
    if is_cn:
        rows = [
            ["市场", "现在做什么", "为什么", "明确不做什么"],
            ["欧洲\nDACH + 职业俱乐部", "主战场。立刻打。", "瑞士主体、德文母版、Bülach 地址、\nROUNDS、已有手球/冰球/足球现场。", "不铺全欧广告。\n不先开英法意西站点。"],
            ["韩国 / 日本", "2027 Q1 找代理。\n今年不卖。", "场馆舍得为系统付钱，\n但必须有本地伙伴和语言。", "不今秋做日韩语网站。\n不投流。"],
            ["中国", "研发、制造、交付。", "深圳工厂和软件团队在这里。\n不是欧洲买家看的主场。", "不把小红书当欧洲获客渠道。"],
        ]
        note = "一句话：今秋只打欧洲。日韩是明年的第二场，不是现在的第二优先。"
    else:
        rows = [
            ["Market", "Do now", "Why", "Do not"],
            ["Europe\nDACH + pro clubs", "Primary battlefield.\nStart immediately.", "Swiss entity, German master copy,\nBülach, ROUNDS, live handball /\nice hockey / football proof.", "No pan-Europe ads.\nNo FR/IT/ES sites first."],
            ["Korea / Japan", "Find partners in Q1 2027.\nDo not sell this autumn.", "Arenas pay for systems —\nbut only with a local partner\nand language.", "No JP/KR website this autumn.\nNo paid social."],
            ["China", "R&D, manufacture, delivery.", "Shenzhen is the factory and\nsoftware bench — not the\nEuropean buying stage.", "Xiaohongshu is not a Europe\nacquisition channel."],
        ]
        note = "One line: this autumn we only fight in Europe. Korea/Japan is next year’s second campaign, not this quarter’s second priority."
    # custom 4-col cards instead of cramped table
    col_w = [Inches(1.9), Inches(3.15), Inches(3.55), Inches(3.4)]
    table_grid(s, ML, Inches(1.18), col_w, Inches(1.28), rows, font, True)
    add_box(s, ML, Inches(6.45), Inches(12.08), Inches(0.52), WASH)
    add_tf(s, ML + Inches(0.18), Inches(6.54), Inches(11.7), Inches(0.36), note, 13, INK, True, font, PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
    footer(s, 2, 8, font, "")

    # ——— 2 WHO ———
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(s, C["s3k"], C["s3t"], font)
    if is_cn:
        buyers = [
            ("01", "场馆 / 俱乐部", "手球、冰球、足球的技术总监、场馆经理。他们买的是「一个人能扛整场比赛」。"),
            ("02", "系统集成商 / 租赁商", "欧洲 AV、体育显示集成商。他们把 COR + LED 打包进项目。"),
            ("03", "联赛 / 转播相关方", "要数据、记分、信号稳定。不跟观众做品牌广告。"),
        ]
        offer_k = "卖什么（就这三样）"
        offers = [
            ("Media Playout", "COR 家族：一人操作系统。主推 SCORE + DECK。"),
            ("LED Video", "围栏、记分、室内外屏。用已有 UEFA 级现场做证据。"),
            ("项目制", "不卖散件目录。卖一场比赛能跑起来的整套。"),
        ]
        kill = "不做：C 端粉丝运营、电商品牌、全国经销商大会、六国语言同时上。"
    else:
        buyers = [
            ("01", "Venues / clubs", "Technical directors and arena managers in handball, ice hockey, football. They buy “one operator, one match”."),
            ("02", "Integrators / rental", "European AV and sports-display firms who bundle COR + LED into a project."),
            ("03", "Leagues / broadcast", "They need data, scoring, stable signal. We do not advertise to fans."),
        ]
        offer_k = "What we sell (only these three)"
        offers = [
            ("Media Playout", "COR family: one-operator system. Lead with SCORE + DECK."),
            ("LED Video", "Perimeter, scoreboard, indoor/outdoor. Proof is existing UEFA-grade jobs."),
            ("Projects", "Not a parts catalogue. A system that runs a match night."),
        ]
        kill = "Not this: consumer fandom, ecommerce, a dealer conference, six languages at once."
    for i, (n, title, body) in enumerate(buyers):
        x = ML + i * Inches(4.1)
        add_box(s, x, Inches(1.18), Inches(3.92), Inches(2.15), WASH)
        add_tf(s, x + Inches(0.2), Inches(1.32), Inches(3.5), Inches(0.28), n, 12, MAGENTA, True, font)
        add_tf(s, x + Inches(0.2), Inches(1.62), Inches(3.5), Inches(0.36), title, 16, INK, True, font)
        add_tf(s, x + Inches(0.2), Inches(2.05), Inches(3.5), Inches(1.1), body, 13, MUTED, False, font)
    add_tf(s, ML, Inches(3.50), Inches(12), Inches(0.3), offer_k, 12, MAGENTA, True, font)
    for i, (title, body) in enumerate(offers):
        x = ML + i * Inches(4.1)
        add_box(s, x, Inches(3.85), Inches(3.92), Inches(1.55), PAPER, LINE)
        add_tf(s, x + Inches(0.2), Inches(3.98), Inches(3.5), Inches(0.32), title, 14, INK, True, font)
        add_tf(s, x + Inches(0.2), Inches(4.32), Inches(3.5), Inches(0.9), body, 12, MUTED, False, font)
    add_tf(s, ML, Inches(5.60), Inches(12.1), Inches(0.4), kill, 13, INK, True, font)
    footer(s, 3, 8, font, "")

    # ——— 3 GANTT ———
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(s, C["s4k"], C["s4t"], font)
    weeks = ["9/15", "9/22", "9/29", "10/6", "10/13", "10/20", "10/27", "11/3", "11/10", "11/17", "11/24", "12/1", "12/15", "1/26"] if not is_cn else ["9/15", "9/22", "9/29", "10/6", "10/13", "10/20", "10/27", "11/3", "11/10", "11/17", "11/24", "12/1", "12/15", "1月"]
    if is_cn:
        labels = ["网站德文定稿+修缺陷", "英/中文首页与导航", "slam.systems 切正式站", "三社媒账号+首发", "三支视频成片", "欧洲 40 家名单触达", "日韩代理摸底"]
        gantt_note = "红条 = 必须在该周完成。灰条 = 启动但不作为本季考核。9/29 是网站德文上线日。"
    else:
        labels = ["DE site freeze + fixes", "EN/ZH home + nav", "Cut over slam.systems", "3 social accounts + first posts", "3 films locked", "40 EU accounts reached", "KR/JP partner mapping"]
        gantt_note = "Magenta = must finish that week. Grey = started, not a Q4 KPI. 29 Sep is German go-live on slam.systems."
    bars = [
        (0, 2, "now"),
        (1, 3, "work"),
        (2, 2, "now"),
        (3, 2, "now"),
        (2, 5, "work"),
        (3, 8, "work"),
        (10, 4, "later"),
    ]
    gantt(s, ML, Inches(1.18), labels, bars, weeks, font, "工作流" if is_cn else "Workstream")
    add_tf(s, ML, Inches(6.45), Inches(12.1), Inches(0.45), gantt_note, 13, MUTED, False, font)
    footer(s, 4, 8, font, "")

    # ——— 4 WEBSITE ———
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(s, C["s5k"], C["s5t"], font)
    if is_cn:
        nodes = [
            ("9/22", "定稿", "德文 v2.2.6 冻结。修：首页假视频按钮、手机菜单缺 Peripherals、表单不能只靠 mailto。"),
            ("9/29", "上线", "slam.systems 切到新站。德文可对外发。i@slam.systems 人工 48 小时必回。"),
            ("10/13", "三语", "EN/ZH 导航和首页可用。内页允许英德混合，但不允许中文首页仍是英文。"),
            ("10/20", "证据", "挂上 3 支视频、1 份项目 PDF、LinkedIn 可点回网站。"),
        ]
        left_t = "上线当天必须为真"
        left_b = "· 德文全站可点\n· Start Your Project 能发来询盘\n· 瑞士 + 深圳地址正确\n· 手球 hero 仍是原片，不重做"
        right_t = "上线当天可以还没做"
        right_b = "· 日文 / 韩文\n· 六个社媒图标全亮\n· 复杂表单后台\n· 案例页 20 张大图"
    else:
        nodes = [
            ("22 Sep", "Freeze", "Lock German v2.2.6. Fix: fake Watch-video button, missing Peripherals in mobile nav, forms that are not mailto-only."),
            ("29 Sep", "Go live", "Cut slam.systems to the new site. German is public. i@slam.systems answered in 48 hours."),
            ("13 Oct", "3 languages", "EN/ZH nav and home work. Interior pages may mix EN/DE. Chinese home must not stay English."),
            ("20 Oct", "Proof", "Three films, one project PDF, LinkedIn clicks back to the site."),
        ]
        left_t = "Must be true on go-live"
        left_b = "· Full German site clickable\n· Start Your Project produces an enquiry\n· Swiss + Shenzhen addresses correct\n· Handball hero stays the original still"
        right_t = "Allowed to wait"
        right_b = "· Japanese / Korean\n· All six social icons live\n· A heavy form backend\n· A 20-image case gallery"
    for i, (date, tag, body) in enumerate(nodes):
        y = Inches(1.18) + i * Inches(0.95)
        add_box(s, ML, y, Inches(8.35), Inches(0.86), WASH)
        add_tf(s, ML + Inches(0.18), y + Inches(0.12), Inches(1.4), Inches(0.28), date, 14, MAGENTA, True, font)
        add_tf(s, ML + Inches(1.55), y + Inches(0.12), Inches(2.2), Inches(0.28), tag, 14, INK, True, font)
        add_tf(s, ML + Inches(0.18), y + Inches(0.42), Inches(8.0), Inches(0.38), body, 12, MUTED, False, font)
        if i < 3:
            add_box(s, ML + Inches(0.42), y + Inches(0.86), Pt(2), Inches(0.09), MAGENTA)
    add_box(s, Inches(9.15), Inches(1.18), Inches(3.55), Inches(2.35), INK)
    add_tf(s, Inches(9.33), Inches(1.32), Inches(3.2), Inches(0.3), left_t, 12, MAGENTA, True, font)
    add_tf(s, Inches(9.33), Inches(1.68), Inches(3.2), Inches(1.7), left_b, 13, WHITE, False, font)
    add_box(s, Inches(9.15), Inches(3.68), Inches(3.55), Inches(2.15), WASH)
    add_tf(s, Inches(9.33), Inches(3.82), Inches(3.2), Inches(0.3), right_t, 12, INK, True, font)
    add_tf(s, Inches(9.33), Inches(4.18), Inches(3.2), Inches(1.5), right_b, 13, MUTED, False, font)
    footer(s, 5, 8, font, "")

    # ——— 5 SOCIAL ———
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(s, C["s6k"], C["s6t"], font)
    if is_cn:
        rows = [
            ["渠道", "为什么只选它", "发什么", "频率", "谁来发"],
            ["LinkedIn", "买家在这里。\n获客主场。", "一人操作系统、场馆夜、\n项目询盘入口。", "2 条/周", "Peter\nLinda 转评"],
            ["Instagram", "画面即证据。\n给集成商转发。", "控制室 15 秒、LED 近景、\n比赛夜。不发参数表。", "3 条/周", "Eva\n素材来自现场"],
            ["YouTube", "能被搜到。\n官网和邮件都嵌。", "60 秒系统片 + SCORE/LED\n各一支 30 秒。", "2 条/月", "Jürg 定调\nDonglin 协助"],
        ]
        no = "明确不做：TikTok、Pinterest、小红书（对欧洲获客）、Facebook 日常运营。账号可以占着，但不排期、不考核。"
        how = "怎么发：同一条内容先出德语母版，再出英语。每周三定三条，周五发 LinkedIn，周末发 IG。所有帖带 slam.systems 和 i@slam.systems。"
    else:
        rows = [
            ["Channel", "Why only this", "What we post", "Cadence", "Who"],
            ["LinkedIn", "Buyers live here.\nPrimary acquisition.", "One-operator system, match\nnight, enquiry link.", "2 / week", "Peter\nLinda comments"],
            ["Instagram", "Picture is proof.\nIntegrators forward it.", "15s control room, LED close-up,\nmatch night. No spec sheets.", "3 / week", "Eva\nfootage from site"],
            ["YouTube", "Searchable.\nEmbed on site + mail.", "60s system film + 30s SCORE\nand 30s LED.", "2 / month", "Jürg directs\nDonglin assists"],
        ]
        no = "Do not: TikTok, Pinterest, Xiaohongshu for Europe, Facebook as a daily channel. Accounts may exist. They are not scheduled or scored."
        how = "How: German master first, then English. Lock three posts every Wednesday. LinkedIn Friday. Instagram weekend. Every post carries slam.systems and i@slam.systems."
    table_grid(s, ML, Inches(1.18), [Inches(1.7), Inches(2.55), Inches(3.35), Inches(1.7), Inches(2.75)], Inches(0.95), rows, font, True)
    add_box(s, ML, Inches(5.15), Inches(12.08), Inches(0.72), INK)
    add_tf(s, ML + Inches(0.18), Inches(5.28), Inches(11.7), Inches(0.5), no, 13, WHITE, False, font, PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
    add_tf(s, ML, Inches(6.00), Inches(12.1), Inches(0.85), how, 13, MUTED, False, font)
    footer(s, 6, 8, font, "")

    # ——— 6 VIDEO + ACQ ———
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(s, C["s7k"], C["s7t"], font)
    if is_cn:
        films = [
            ("片子 A  ·  60 秒", "系统片", "一人、一场、整晚。用手球 hero 同场景延伸现有 6 秒片。官网首页、YouTube、询盘页都用这一支。10/20 交片。"),
            ("片子 B  ·  30 秒", "SCORE", "记分界面特写 + 场边大屏。只讲「一个人改比分」。LinkedIn / IG 主用。"),
            ("片子 C  ·  30 秒", "LED", "围栏和记分屏在比赛里的样子。给集成商转发，不讲像素间距。"),
        ]
        acq_t = "获客就四条线"
        acqs = [
            ("1  名单", "Peter + Linda 列出 40 家：德瑞奥俱乐部、场馆、集成商。每周触达 8 家。"),
            ("2  伙伴", "ROUNDS 本季带 5 个瑞士/南德机会。不新开一堆经销商。"),
            ("3  询盘", "网站表单 + i@slam.systems，48 小时内人回。记进一张表，每周一过。"),
            ("4  展会", "只准备一场：ISE Barcelona 2027.02。今秋不另开欧洲巡展。"),
        ]
    else:
        films = [
            ("Film A  ·  60s", "System", "One operator, one match, full night. Extend the existing 6s handball intro. Home, YouTube, enquiry page. Due 20 Oct."),
            ("Film B  ·  30s", "SCORE", "Score UI close-up + fascia. Only one point: one person changes the score. LinkedIn / IG."),
            ("Film C  ·  30s", "LED", "Perimeter and scoreboard in a live match. For integrators. No pixel-pitch lecture."),
        ]
        acq_t = "Four acquisition lines only"
        acqs = [
            ("1  List", "Peter + Linda name 40: DACH clubs, arenas, integrators. Eight reached each week."),
            ("2  Partner", "ROUNDS brings five Swiss / southern-German opportunities this season. No new dealer army."),
            ("3  Inbound", "Site form + i@slam.systems, human reply in 48h. One sheet, reviewed Mondays."),
            ("4  Show", "One show only: ISE Barcelona, Feb 2027. No extra autumn tour."),
        ]
    for i, (k, t, b) in enumerate(films):
        y = Inches(1.16) + i * Inches(1.05)
        add_box(s, ML, y, Inches(6.15), Inches(0.96), WASH)
        add_tf(s, ML + Inches(0.18), y + Inches(0.1), Inches(5.8), Inches(0.24), k, 11, MAGENTA, True, font)
        add_tf(s, ML + Inches(0.18), y + Inches(0.34), Inches(5.8), Inches(0.24), t, 14, INK, True, font)
        add_tf(s, ML + Inches(0.18), y + Inches(0.58), Inches(5.8), Inches(0.32), b, 11, MUTED, False, font)
    add_tf(s, Inches(7.05), Inches(1.16), Inches(5.6), Inches(0.3), acq_t, 14, INK, True, font)
    for i, (k, b) in enumerate(acqs):
        y = Inches(1.52) + i * Inches(1.05)
        add_box(s, Inches(7.05), y, Inches(5.65), Inches(0.96), PAPER, LINE)
        add_tf(s, Inches(7.22), y + Inches(0.1), Inches(5.3), Inches(0.26), k, 13, MAGENTA, True, font)
        add_tf(s, Inches(7.22), y + Inches(0.40), Inches(5.3), Inches(0.48), b, 12, MUTED, False, font)
    footer(s, 7, 8, font, "")

    # ——— 7 SCOREBOARD ———
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(s, C["s8k"], C["s8t"], font)
    if is_cn:
        rows = [
            ["日期", "必须交付", "负责人", "数字"],
            ["9/29", "slam.systems 德文上线", "Linda / 网站", "1 个可对外域名"],
            ["10/13", "EN+ZH 首页与导航", "Eva / 网站", "3 个语言可切换"],
            ["10/13", "LinkedIn / IG / YouTube 首发", "Peter + Eva", "3 个账号各 ≥1 条"],
            ["10/20", "三支视频可嵌官网", "Jürg", "60s + 30s + 30s"],
            ["11/30", "欧洲名单全部触达", "Peter + Linda", "40 家"],
            ["12/20", "有效对话（不是点赞）", "Linda", "8 次"],
            ["1/31", "现场演示或场馆走访", "Linda + Jürg", "2 次"],
        ]
        bottom = "下周一开始执行：冻结德文缺陷清单，列出 40 家欧洲名单初稿。日韩不进这张表。"
    else:
        rows = [
            ["Date", "Must ship", "Owner", "Number"],
            ["29 Sep", "German live on slam.systems", "Linda / web", "1 public domain"],
            ["13 Oct", "EN+ZH home and nav", "Eva / web", "3 languages switch"],
            ["13 Oct", "LinkedIn / IG / YouTube first posts", "Peter + Eva", "≥1 post per channel"],
            ["20 Oct", "Three films on the site", "Jürg", "60s + 30s + 30s"],
            ["30 Nov", "Full Europe list reached", "Peter + Linda", "40 accounts"],
            ["20 Dec", "Real conversations (not likes)", "Linda", "8"],
            ["31 Jan", "On-site demo or venue walk", "Linda + Jürg", "2"],
        ]
        bottom = "Start next Monday: freeze the German defect list, draft the 40-name Europe list. Korea/Japan stay off this scoreboard."
    table_grid(s, ML, Inches(1.18), [Inches(1.55), Inches(4.55), Inches(3.2), Inches(2.75)], Inches(0.58), rows, font, True)
    add_box(s, ML, Inches(6.05), Inches(12.08), Inches(0.85), MAGENTA)
    add_tf(s, ML + Inches(0.22), Inches(6.22), Inches(11.6), Inches(0.55), bottom, 15, WHITE, True, font, PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
    footer(s, 8, 8, font, "")

    prs.save(C["file"])
    print("wrote", C["file"])


if __name__ == "__main__":
    build(CN, "cn")
    build(EN, "en")
