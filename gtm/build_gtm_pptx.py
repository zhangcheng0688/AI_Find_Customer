#!/usr/bin/env python3
"""SLAM.SYSTEMS GTM plan — CN + EN. Strategy + seven engines."""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
from lxml import etree

INK = RGBColor(0x11, 0x11, 0x11)
MUTED = RGBColor(0x6B, 0x6B, 0x6B)
LINE = RGBColor(0xE6, 0xE6, 0xE6)
PAPER = RGBColor(0xFF, 0xFF, 0xFF)
WASH = RGBColor(0xF6, 0xF6, 0xF5)
MAGENTA = RGBColor(0xFF, 0x00, 0x4E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK = RGBColor(0x0B, 0x0B, 0x0C)
SOFT = RGBColor(0xC8, 0xC8, 0xC8)

W = Inches(13.333)
H = Inches(7.5)
ML = Inches(0.62)
TOTAL = 12


def set_run(run, size, color, bold=False, font_name="Calibri"):
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = font_name
    rPr = run._r.get_or_add_rPr()
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


def add_tf(
    slide,
    l,
    t,
    w,
    h,
    text,
    size,
    color,
    bold=False,
    font="Calibri",
    align=PP_ALIGN.LEFT,
    anchor=MSO_ANCHOR.TOP,
):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf._txBody.bodyPr.set(
            "anchor",
            {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}[anchor],
        )
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


def footer(slide, page, font, dark=False):
    c = SOFT if dark else MUTED
    line = RGBColor(0x2A, 0x2A, 0x2C) if dark else LINE
    add_tf(
        slide,
        ML,
        Inches(7.18),
        Inches(8),
        Inches(0.24),
        "SLAM.SYSTEMS  ·  GTM 2026 Q4 – 2027 Q1",
        10,
        c,
        False,
        font,
    )
    add_tf(
        slide,
        Inches(11.2),
        Inches(7.18),
        Inches(1.5),
        Inches(0.24),
        f"{page} / {TOTAL}",
        10,
        c,
        False,
        font,
        PP_ALIGN.RIGHT,
    )
    add_box(slide, ML, Inches(7.12), Inches(12.08), Pt(0.75), line)


def header(slide, kicker, title, font):
    add_tf(slide, ML, Inches(0.24), Inches(12), Inches(0.22), kicker, 11, MAGENTA, True, font)
    add_tf(slide, ML, Inches(0.46), Inches(12.1), Inches(0.42), title, 22, INK, True, font)
    add_box(slide, ML, Inches(0.92), Inches(0.42), Pt(3), MAGENTA)


def table_grid(slide, l, t, col_w, row_h, rows, font, header_row=True, size=11):
    for r, row in enumerate(rows):
        y = t + r * row_h
        bg = INK if (header_row and r == 0) else (WASH if r % 2 else PAPER)
        fg = WHITE if (header_row and r == 0) else INK
        for c, cell in enumerate(row):
            x = l + sum(col_w[:c])
            w = col_w[c]
            add_box(slide, x, y, w, row_h, bg, LINE)
            pad = Inches(0.08)
            is_head = header_row and r == 0
            add_tf(
                slide,
                x + pad,
                y + Inches(0.04),
                w - pad * 2,
                row_h - Inches(0.06),
                cell,
                size if not is_head else 11,
                fg,
                is_head or c == 0,
                font,
                PP_ALIGN.LEFT,
                MSO_ANCHOR.MIDDLE,
            )


CN = {
    "font": "PingFang SC",
    "file": "/workspace/gtm/SLAM.SYSTEMS_GTM_Plan_CN.pptx",
}

EN = {
    "font": "Calibri",
    "file": "/workspace/gtm/SLAM.SYSTEMS_GTM_Plan_EN.pptx",
}


def build(C, lang):
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    blank = prs.slide_layouts[6]
    font = C["font"]
    cn = lang == "cn"

    # ───────── 1 COVER ─────────
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, DARK)
    add_box(s, 0, 0, Inches(0.14), H, MAGENTA)
    add_tf(
        s,
        ML,
        Inches(1.28),
        Inches(12),
        Inches(0.28),
        "SLAM.SYSTEMS  ·  机密" if cn else "SLAM.SYSTEMS  ·  Confidential",
        13,
        MAGENTA,
        True,
        font,
    )
    add_tf(
        s,
        ML,
        Inches(1.72),
        Inches(12),
        Inches(0.95),
        "市场进入计划" if cn else "Go-to-Market",
        48,
        WHITE,
        True,
        font,
    )
    add_tf(
        s,
        ML,
        Inches(2.68),
        Inches(12),
        Inches(0.38),
        "整体战略  ·  2026 Q4 – 2027 Q1" if cn else "The operating strategy  ·  Q4 2026 – Q1 2027",
        18,
        SOFT,
        False,
        font,
    )
    add_box(s, ML, Inches(3.22), Inches(1.2), Pt(3.5), MAGENTA)
    add_tf(
        s,
        ML,
        Inches(3.50),
        Inches(11.6),
        Inches(1.35),
        (
            "欧洲现在卖项目。日本靠展会找经销商。\n"
            "线上五条线养管道。线下按展会出差——不参展，把人约出来。"
            if cn
            else "Sell projects in Europe now. Enter Japan through shows and dealers.\n"
            "Five online engines fill the pipe. Offline we travel the show calendar — no booth, meetings only."
        ),
        20,
        WHITE,
        False,
        font,
    )
    add_tf(
        s,
        ML,
        Inches(6.72),
        Inches(12),
        Inches(0.3),
        "12 页  ·  执行版  ·  2026.09" if cn else "12 slides  ·  Operating version  ·  September 2026",
        12,
        RGBColor(0x8A, 0x8A, 0x8A),
        False,
        font,
    )

    # ───────── 2 STRATEGY ─────────
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, DARK)
    add_box(s, 0, 0, Inches(0.14), H, MAGENTA)
    add_tf(
        s,
        ML,
        Inches(0.32),
        Inches(12),
        Inches(0.22),
        "01  /  整体战略" if cn else "01  /  The strategy",
        12,
        MAGENTA,
        True,
        font,
    )
    add_tf(
        s,
        ML,
        Inches(0.58),
        Inches(12.1),
        Inches(0.7),
        "一件事：让职业场馆用一套系统打完整场比赛。" if cn else "One job: one system that runs a professional match night.",
        24,
        WHITE,
        True,
        font,
    )
    pillars = (
        [
            ("01", "品牌资产", "独立站是总部。\nLinkedIn / Instagram / YouTube\n是仅有的三块招牌。\n所有邮件、展会、经销商\n都指回 slam.systems。"),
            ("02", "需求管道", "邮件获客、直接触达、\n线上封闭活动。\n名单驱动，不投广告。\n展会前后把同一批人再打一遍。"),
            ("03", "落地与规模", "线下按展会出差。\n不租展位，把人约到酒店。\n规模不靠加人，靠经销商\n和集成商把系统送进场馆。"),
        ]
        if cn
        else [
            ("01", "Brand asset", "The site is HQ.\nLinkedIn / Instagram / YouTube\nare the only three signs.\nMail, shows and dealers\nall point back to slam.systems."),
            ("02", "Demand pipe", "Email, direct outreach,\nclosed online briefings.\nNamed accounts, no ads.\nThe same names get hit\nbefore and after each show."),
            ("03", "Land & scale", "Travel the show calendar.\nNo booth — hotel meetings.\nScale is not headcount.\nDealers and integrators\nput the system in venues."),
        ]
    )
    for i, (n, title, body) in enumerate(pillars):
        x = ML + i * Inches(4.12)
        add_box(s, x, Inches(1.55), Inches(3.92), Inches(4.85), RGBColor(0x16, 0x16, 0x18))
        add_box(s, x, Inches(1.55), Inches(0.08), Inches(4.85), MAGENTA)
        add_tf(s, x + Inches(0.28), Inches(1.78), Inches(3.4), Inches(0.3), n, 14, MAGENTA, True, font)
        add_tf(s, x + Inches(0.28), Inches(2.18), Inches(3.4), Inches(0.45), title, 22, WHITE, True, font)
        add_tf(s, x + Inches(0.28), Inches(2.78), Inches(3.4), Inches(3.2), body, 15, SOFT, False, font)
    footer(s, 2, font, dark=True)

    # ───────── 3 MARKETS ─────────
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(
        s,
        "02  /  市场与客户" if cn else "02  /  Markets and buyers",
        "先打欧洲。日本用展会进。中国是工厂。" if cn else "Europe first. Japan through shows. China is the factory.",
        font,
    )
    if cn:
        rows = [
            ["市场", "角色", "现在做什么", "明确不做什么"],
            [
                "欧洲\nDACH + 职业俱乐部",
                "主战场",
                "立刻卖项目。独立站德文先上。\nSPORTEL、ISE 出差打集成商。",
                "不铺全欧广告。\n不先开英法意西站点。",
            ],
            [
                "日本",
                "第二市场",
                "今秋不卖散单。Inter BEE、\nSports Week 出差找经销商。",
                "不今秋做日语站。\n不在日本投流、不租展位。",
            ],
            [
                "韩国",
                "顺路",
                "2027.05 KOBA 可选。\n日本经销商能带路再去。",
                "不单开韩国战役。",
            ],
            [
                "中国",
                "工厂 / 研发",
                "深圳制造、软件、交付。",
                "不把小红书当欧洲获客渠道。",
            ],
        ]
        buyers = [
            ("场馆 / 俱乐部", "手球、冰球、足球的技术总监和场馆经理。买的是「一个人扛整场」。"),
            ("集成商 / 租赁商", "欧洲 AV、体育显示公司。把 COR + LED 打进项目。也是经销商苗子。"),
            ("联赛 / 转播", "要记分、数据和信号稳定。不跟观众做品牌。"),
        ]
    else:
        rows = [
            ["Market", "Role", "Do now", "Do not"],
            [
                "Europe\nDACH + pro clubs",
                "Primary",
                "Sell projects now. German site first.\nTravel SPORTEL and ISE.",
                "No pan-EU ads.\nNo FR/IT/ES sites first.",
            ],
            [
                "Japan",
                "Second",
                "Do not sell parts this autumn.\nInter BEE + Sports Week for dealers.",
                "No JP site this autumn.\nNo ads, no booth.",
            ],
            [
                "Korea",
                "Optional",
                "KOBA May 2027 only if a Japan\ndealer can open the door.",
                "No standalone Korea campaign.",
            ],
            [
                "China",
                "Factory / R&D",
                "Shenzhen builds, codes, ships.",
                "Xiaohongshu is not a Europe channel.",
            ],
        ]
        buyers = [
            ("Venues / clubs", "Technical directors in handball, ice hockey, football. They buy one operator for a full match."),
            ("Integrators / rental", "European AV and sports-display firms. They bundle COR + LED — and are dealer candidates."),
            ("Leagues / broadcast", "Score, data, stable signal. We do not advertise to fans."),
        ]
    table_grid(s, ML, Inches(1.12), [Inches(2.35), Inches(1.7), Inches(4.35), Inches(3.65)], Inches(0.64), rows, font, True, 11)
    add_tf(
        s,
        ML,
        Inches(4.42),
        Inches(12),
        Inches(0.28),
        "卖给谁（就这三类）" if cn else "Who we sell to (only these three)",
        12,
        MAGENTA,
        True,
        font,
    )
    for i, (title, body) in enumerate(buyers):
        x = ML + i * Inches(4.1)
        add_box(s, x, Inches(4.76), Inches(3.92), Inches(2.10), WASH)
        add_tf(s, x + Inches(0.18), Inches(4.90), Inches(3.55), Inches(0.32), title, 15, INK, True, font)
        add_tf(s, x + Inches(0.18), Inches(5.26), Inches(3.55), Inches(1.42), body, 13, MUTED, False, font)
    footer(s, 3, font)

    # ───────── 4 SEVEN ENGINES ─────────
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(
        s,
        "03  /  作战地图" if cn else "03  /  Operating map",
        "线上五条，线下两条。同时转，不互相替代。" if cn else "Five online. Two offline. They run together.",
        font,
    )
    if cn:
        online = [
            ("01  独立站", "slam.systems 是总部。德文先上，英/中补齐。所有渠道的落地页。"),
            ("02  社交媒体", "只做 LinkedIn、Instagram、YouTube。获客、证据、可被搜到。"),
            ("03  邮件获客", "对名单发序列：介绍 → 现场片 → 展会约见。不群发行业通讯。"),
            ("04  直接触达", "Peter + Linda 点名 40 家欧洲场馆/集成商。每周 8 家。"),
            ("05  线上活动", "封闭简报，不是公开网红直播。每月一场，给集成商和经销商苗子。"),
        ]
        offline = [
            ("06  展会出差", "按欧洲、日本节点出动。不参展。展前约人，展中见面，展后跟进。"),
            ("07  经销商", "规模从这里来。欧洲在 ISE 扩集成商。日本用 Inter BEE 找一家。"),
        ]
        note = "原则：线上把人养熟，线下按展会把人见掉。经销商是规模，不是今年秋天的招商大会。"
    else:
        online = [
            ("01  Site", "slam.systems is HQ. German first, EN/ZH next. Every channel lands here."),
            ("02  Social", "LinkedIn, Instagram, YouTube only. Sell, prove, be searchable."),
            ("03  Email", "Sequences to the named list: intro → film → show meeting. No industry newsletter."),
            ("04  Direct", "Peter + Linda name 40 EU venues/integrators. Eight a week."),
            ("05  Online events", "Closed briefings, not public livestreams. Monthly, for integrators and dealer candidates."),
        ]
        offline = [
            ("06  Show travel", "Move on the Europe and Japan calendar. No booth. Book, meet, follow up."),
            ("07  Dealers", "This is scale. Add EU integrators at ISE. Find one Japan partner at Inter BEE."),
        ]
        note = "Rule: online warms the names. Offline closes them at shows. Dealers are scale — not an autumn franchise conference."
    add_box(s, ML, Inches(1.14), Inches(7.55), Inches(5.22), WASH)
    add_tf(s, ML + Inches(0.22), Inches(1.28), Inches(7.1), Inches(0.28), "线上  ·  一直在转" if cn else "Online  ·  always on", 13, MAGENTA, True, font)
    for i, (t, b) in enumerate(online):
        y = Inches(1.64) + i * Inches(0.90)
        add_tf(s, ML + Inches(0.22), y, Inches(7.1), Inches(0.28), t, 15, INK, True, font)
        add_tf(s, ML + Inches(0.22), y + Inches(0.30), Inches(7.1), Inches(0.52), b, 13, MUTED, False, font)
    add_box(s, Inches(8.40), Inches(1.14), Inches(4.30), Inches(5.22), INK)
    add_tf(s, Inches(8.62), Inches(1.28), Inches(3.9), Inches(0.28), "线下  ·  按节点出动" if cn else "Offline  ·  on the nodes", 13, MAGENTA, True, font)
    for i, (t, b) in enumerate(offline):
        y = Inches(1.78) + i * Inches(2.05)
        add_tf(s, Inches(8.62), y, Inches(3.9), Inches(0.4), t, 16, WHITE, True, font)
        add_tf(s, Inches(8.62), y + Inches(0.48), Inches(3.9), Inches(1.4), b, 14, SOFT, False, font)
    add_tf(s, ML, Inches(6.48), Inches(12.1), Inches(0.45), note, 13, INK, True, font)
    footer(s, 4, font)

    # ───────── 5 SITE ─────────
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(
        s,
        "04  /  独立站" if cn else "04  /  The site",
        "德文先上 slam.systems。三语两周内补齐。" if cn else "German live on slam.systems first. EN/ZH within two weeks.",
        font,
    )
    if cn:
        nodes = [
            ("9/22", "定稿", "德文 v2.2.6 冻结。修首页假视频、手机菜单缺 Peripherals、表单不能只靠 mailto。"),
            ("9/29", "上线", "slam.systems 切新站。德文可对外。i@slam.systems 人工 48 小时必回。"),
            ("10/13", "三语", "EN/ZH 导航和首页可用。中文首页不允许仍是英文。"),
            ("10/20", "弹药", "7 秒 SCORE 片播完跳转表单（主题 Scoreboard Handball）。再加系统片 / LED 片和项目 PDF。"),
        ]
        must_t, must_b = "上线当天必须为真", "· 德文全站可点\n· Start Your Project 能变成询盘\n· 瑞士 + 深圳地址正确\n· 手球 hero 仍是原片"
        wait_t, wait_b = "上线当天可以还没做", "· 日文 / 韩文\n· 六个社媒图标全亮\n· 复杂表单后台\n· 案例页 20 张大图"
    else:
        nodes = [
            ("22 Sep", "Freeze", "Lock German v2.2.6. Fix fake Watch-video, missing Peripherals in mobile nav, mailto-only forms."),
            ("29 Sep", "Go live", "Cut slam.systems to the new site. German is public. i@slam.systems answered in 48 hours."),
            ("13 Oct", "3 languages", "EN/ZH nav and home work. Chinese home must not stay English."),
            ("20 Oct", "Ammunition", "7s SCORE film ends on the form (subject Scoreboard Handball). Then system/LED films and a project PDF."),
        ]
        must_t, must_b = "Must be true on go-live", "· Full German site clickable\n· Start Your Project produces an enquiry\n· Swiss + Shenzhen addresses correct\n· Handball hero stays the original still"
        wait_t, wait_b = "Allowed to wait", "· Japanese / Korean\n· All six social icons live\n· A heavy form backend\n· A 20-image case gallery"
    for i, (date, tag, body) in enumerate(nodes):
        y = Inches(1.14) + i * Inches(1.18)
        add_box(s, ML, y, Inches(8.35), Inches(1.06), WASH)
        add_tf(s, ML + Inches(0.2), y + Inches(0.14), Inches(1.5), Inches(0.3), date, 16, MAGENTA, True, font)
        add_tf(s, ML + Inches(1.7), y + Inches(0.14), Inches(2.4), Inches(0.3), tag, 16, INK, True, font)
        add_tf(s, ML + Inches(0.2), y + Inches(0.50), Inches(7.95), Inches(0.46), body, 13, MUTED, False, font)
    add_box(s, Inches(9.15), Inches(1.14), Inches(3.55), Inches(2.55), INK)
    add_tf(s, Inches(9.33), Inches(1.30), Inches(3.2), Inches(0.32), must_t, 13, MAGENTA, True, font)
    add_tf(s, Inches(9.33), Inches(1.70), Inches(3.2), Inches(1.8), must_b, 14, WHITE, False, font)
    add_box(s, Inches(9.15), Inches(3.86), Inches(3.55), Inches(2.00), WASH)
    add_tf(s, Inches(9.33), Inches(4.00), Inches(3.2), Inches(0.32), wait_t, 13, INK, True, font)
    add_tf(s, Inches(9.33), Inches(4.38), Inches(3.2), Inches(1.35), wait_b, 14, MUTED, False, font)
    footer(s, 5, font)

    # ───────── 6 SOCIAL ─────────
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(
        s,
        "05  /  社交媒体" if cn else "05  /  Social",
        "先开两家验证。瑞士独立号注册。发现场，不发参数。" if cn else "Prove two channels first. Swiss SIM. Post the match, not the spec.",
        font,
    )
    if cn:
        rows = [
            ["渠道", "阶段", "发什么", "频率", "谁"],
            ["LinkedIn", "现在开\n商务获客主场", "一人操作系统、场馆夜、\n展会约见。德语母版。", "2–3 天一条\n展会周加倍", "Peter\nLinda 转评"],
            ["Instagram", "现在开\n画面即证据", "Reels：控制室、LED 近景、\n比赛夜。不发参数表。", "2–3 天一条", "Eva\n现场素材"],
            ["X / Twitter", "两家跑通再开\n图文与行业动态", "一句现场、一张图、一个链。\n对标 Stramatel：装机与比赛夜。", "有事才发", "Peter"],
            ["YouTube", "两家跑通再开\n可被搜到", "7 秒 SCORE + 60 秒系统片\n+ 教程长视频。", "2 条/月", "Jürg\nDonglin"],
        ]
        films = "注册：买一个全新瑞士手机号，账号不绑私人号。热点只蹭职业比赛夜和展会周，不蹭 iPhone 级消费发布会。"
        no = "Facebook 只做竞品观察，不日常运营。TikTok / 小红书不对欧洲获客。文案可用 AI 起草，人必须改完再发。"
    else:
        rows = [
            ["Channel", "Phase", "What", "Cadence", "Who"],
            ["LinkedIn", "Open now\nBuyer home", "One-operator system, match night,\nshow meeting. German master.", "Every 2–3 days\nDouble in show week", "Peter\nLinda comments"],
            ["Instagram", "Open now\nPicture is proof", "Reels: control room, LED, match night.\nNo spec sheets.", "Every 2–3 days", "Eva\nSite footage"],
            ["X / Twitter", "After the two work\nShort news", "One line, one still, one link.\nLike Stramatel: install + match night.", "When there is news", "Peter"],
            ["YouTube", "After the two work\nSearch", "7s SCORE + 60s system\n+ longer how-to.", "2 / month", "Jürg\nDonglin"],
        ]
        films = "Register on a new Swiss mobile number. Accounts stay off personal SIMs. Newsjack match nights and show weeks, not consumer gadget launches."
        no = "Facebook is for watching competitors, not a daily channel. No TikTok / Xiaohongshu for Europe. AI may draft copy. A person publishes."
    table_grid(s, ML, Inches(1.12), [Inches(1.85), Inches(2.35), Inches(3.35), Inches(2.15), Inches(2.35)], Inches(0.82), rows, font, True, 11)
    add_box(s, ML, Inches(5.38), Inches(12.08), Inches(0.72), INK)
    add_tf(s, ML + Inches(0.2), Inches(5.48), Inches(11.7), Inches(0.52), films, 13, WHITE, False, font, PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
    add_tf(s, ML, Inches(6.22), Inches(12.1), Inches(0.68), no, 13, MUTED, False, font)
    footer(s, 6, font)

    # ───────── 7 EMAIL + DIRECT ─────────
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(
        s,
        "06  /  邮件获客  ·  直接触达" if cn else "06  /  Email  ·  Direct outreach",
        "名单驱动。先欧洲 40 家。展会是约见由头。" if cn else "Named accounts. Forty in Europe first. Shows are the reason to meet.",
        font,
    )
    if cn:
        cols = [
            ("邮件三封", "① 介绍：一人操作系统，链到独立站。\n② 证据：嵌 60 秒系统片。\n③ 约见：用最近一场展会当由头。\n德语母版，英语备份。不群发。"),
            ("直接触达", "Peter + Linda 点名 40 家：德瑞奥俱乐部、场馆、集成商。\n每周 8 家，电话 / LinkedIn / 邮件同一周打完。\nROUNDS 本季另带 5 个瑞士/南德机会。"),
            ("询盘纪律", "i@slam.systems 48 小时人回。\n一张表，每周一过。\n有效对话才计数，点赞不算。\n展会周把回信改成「现场见」。"),
        ]
        seq = [
            ("T-21", "展前三周", "对将出现的人发第③封，锁 8–12 个会。"),
            ("T-7", "展前一周", "确认时间、酒店、一页 PDF。"),
            ("T+3", "展后三天", "纪要、片子、下一步。项目和经销商分两条跟。"),
        ]
    else:
        cols = [
            ("Three emails", "1 Intro: one-operator system, link the site.\n2 Proof: embed the 60s film.\n3 Meeting: the next show is the reason.\nGerman master, English backup. No blast."),
            ("Direct", "Peter + Linda name 40: DACH clubs, arenas, integrators.\nEight a week — phone, LinkedIn, mail in the same week.\nROUNDS brings five more Swiss / south-German chances."),
            ("Inbound discipline", "i@slam.systems, human reply in 48h.\nOne sheet, reviewed Mondays.\nOnly real conversations count.\nIn show week, replies become “see you there”."),
        ]
        seq = [
            ("T-21", "Three weeks out", "Send email 3 to people who will be there. Lock 8–12 meetings."),
            ("T-7", "One week out", "Confirm time, hotel, one-pager."),
            ("T+3", "Three days after", "Notes + film + next step. Project track or dealer track."),
        ]
    for i, (t, b) in enumerate(cols):
        x = ML + i * Inches(4.1)
        add_box(s, x, Inches(1.14), Inches(3.92), Inches(3.15), WASH)
        add_tf(s, x + Inches(0.2), Inches(1.28), Inches(3.52), Inches(0.36), t, 16, INK, True, font)
        add_tf(s, x + Inches(0.2), Inches(1.72), Inches(3.52), Inches(2.35), b, 13, MUTED, False, font)
    for i, (k, t, b) in enumerate(seq):
        x = ML + i * Inches(4.1)
        add_box(s, x, Inches(4.46), Inches(3.92), Inches(2.40), PAPER, LINE)
        add_tf(s, x + Inches(0.2), Inches(4.60), Inches(3.52), Inches(0.28), k, 12, MAGENTA, True, font)
        add_tf(s, x + Inches(0.2), Inches(4.90), Inches(3.52), Inches(0.32), t, 15, INK, True, font)
        add_tf(s, x + Inches(0.2), Inches(5.28), Inches(3.52), Inches(1.35), b, 13, MUTED, False, font)
    footer(s, 7, font)

    # ───────── 8 ONLINE EVENTS ─────────
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(
        s,
        "07  /  事件营销  ·  线上活动" if cn else "07  /  Events  ·  Online briefings",
        "不做公开大会。把正确的人关进一间小房间。" if cn else "No public festival. Put the right people in a small room.",
        font,
    )
    if cn:
        items = [
            ("每月封闭简报", "30 分钟。一人操作系统 + 一支片子。邀请 8–12 个集成商或经销商苗子。从 11 月起，Linda 主持。"),
            ("展会前夜会", "ISE / Inter BEE 前一晚，酒店 90 分钟。已约到的人再加 4 个当地名字。不办酒会。"),
            ("比赛夜远程看", "有现场时，给短名单开 20 分钟控制室窗口。证据比幻灯片强。Jürg 在场。"),
            ("经销商私董", "日本、欧洲各一场。讲授权范围、项目支持和 48 小时工厂响应。不讲招商政策。"),
        ]
        kill = "不做：粉丝直播、公开 Webinar 拉新、六国同传、为办活动而办活动。"
        out = "每次活动的产出只有三样：到场名单、2 个下一步会议、1 条可发 LinkedIn 的现场句。没有第四样。"
    else:
        items = [
            ("Monthly closed briefing", "30 minutes. One-operator system + one film. Invite 8–12 integrators or dealer candidates. From November, Linda hosts."),
            ("Night-before the show", "90 minutes in the hotel the evening before ISE / Inter BEE. The booked names plus four local adds. Not a drinks party."),
            ("Match-night window", "When we have a live job, open a 20-minute control-room view for the shortlist. Proof beats slides. Jürg on the call."),
            ("Dealer roundtable", "One Europe, one Japan. Territory, project support, 48h factory. Not a franchise pitch."),
        ]
        kill = "Do not: fan livestreams, public lead-gen webinars, six-language simulcast, events for their own sake."
        out = "Each event produces only three things: the attendance list, two next meetings, one LinkedIn line from the room. Nothing else."
    for i, (t, b) in enumerate(items):
        x = ML + (i % 2) * Inches(6.2)
        y = Inches(1.14) + (i // 2) * Inches(2.15)
        add_box(s, x, y, Inches(5.95), Inches(2.00), WASH)
        add_tf(s, x + Inches(0.22), y + Inches(0.18), Inches(5.5), Inches(0.36), t, 16, INK, True, font)
        add_tf(s, x + Inches(0.22), y + Inches(0.62), Inches(5.5), Inches(1.2), b, 14, MUTED, False, font)
    add_tf(s, ML, Inches(5.55), Inches(12.1), Inches(0.4), kill, 13, INK, True, font)
    add_box(s, ML, Inches(6.05), Inches(12.08), Inches(0.85), INK)
    add_tf(s, ML + Inches(0.22), Inches(6.18), Inches(11.6), Inches(0.6), out, 14, WHITE, False, font, PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
    footer(s, 8, font)

    # ───────── 9 SHOW CALENDAR ─────────
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(
        s,
        "08  /  展会节点" if cn else "08  /  Show calendar",
        "不参展。按节点出差。欧洲打项目，日本找经销商。" if cn else "No booth. Travel the nodes. Europe for projects, Japan for a dealer.",
        font,
    )
    if cn:
        rows = [
            ["时间", "展会", "城市", "打什么人", "怎么打"],
            ["2026.10.19–21", "SPORTEL", "摩纳哥", "联赛 / 转播 / 体育科技", "本季欧洲第一仗。参观 + 8 场会。"],
            ["2026.11.18–20", "Inter BEE", "千叶", "广电 / 系统商", "日本第一仗。找经销商，不卖散单。"],
            ["2027.01.27–29", "Japan Sports Week", "千叶", "球队 / 场馆设施", "经销商短名单。第二次日本出差。"],
            ["2027.02.01–02", "Sports World Congress", "巴塞罗那", "场馆运营商", "与 ISE 同城一周，场馆侧。"],
            ["2027.02.02–05", "ISE", "巴塞罗那", "欧洲集成商", "本季欧洲主攻。项目 + 经销商苗子。"],
            ["2027.05.11–14", "KOBA", "首尔", "韩国广电（可选）", "日本经销商能带路才去。"],
        ]
        play = "打法：2 人出差（商务 + 技术）。不租展位。展前 21 天锁 8–12 个会，住会场附近，早餐和晚间约人。每天 4 个有效会面。展后 7 天全跟完，分「项目」和「经销商」两条漏斗。IBC 阿姆斯特丹 2026.09 已过，本季不补位。FSB 科隆 2027.10 先占位，不进本季考核。"
    else:
        rows = [
            ["When", "Show", "City", "Who", "How we play"],
            ["19–21 Oct 2026", "SPORTEL", "Monaco", "Leagues / broadcast / sports tech", "First Europe trip. Visitor + 8 meetings."],
            ["18–20 Nov 2026", "Inter BEE", "Chiba", "Broadcast / system houses", "First Japan trip. Hunt a dealer, no parts sales."],
            ["27–29 Jan 2027", "Japan Sports Week", "Chiba", "Teams / venue facilities", "Dealer shortlist. Second Japan trip."],
            ["1–2 Feb 2027", "Sports World Congress", "Barcelona", "Venue operators", "Same week as ISE. Venue side."],
            ["2–5 Feb 2027", "ISE", "Barcelona", "European integrators", "Main Europe strike. Projects + dealer seeds."],
            ["11–14 May 2027", "KOBA", "Seoul", "Korea broadcast (optional)", "Only if a Japan dealer opens the door."],
        ]
        play = "Play: two people travel (commercial + technical). No booth. Twenty-one days out, lock 8–12 meetings near the hall — breakfast and evening. Four real meetings a day. Seven days after, every name followed, split into project vs dealer. IBC Amsterdam Sep 2026 has passed; we do not backfill. FSB Cologne Oct 2027 is a hold, not a Q1 KPI."
    table_grid(s, ML, Inches(1.10), [Inches(1.95), Inches(2.55), Inches(1.55), Inches(2.75), Inches(3.25)], Inches(0.62), rows, font, True, 11)
    add_box(s, ML, Inches(5.58), Inches(12.08), Inches(1.32), WASH)
    add_tf(s, ML + Inches(0.2), Inches(5.70), Inches(11.7), Inches(1.1), play, 13, INK, False, font)
    footer(s, 9, font)

    # ───────── 10 DEALERS ─────────
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(
        s,
        "09  /  经销商" if cn else "09  /  Dealers",
        "要规模，就要做经销商。展会是找人的地方。" if cn else "Scale needs dealers. Shows are where we find them.",
        font,
    )
    if cn:
        why = (
            "一家公司盖不住德瑞奥俱乐部和日本场馆。加人填不满。\n"
            "经销商和集成商把 COR + LED 送进项目，我们保交付和 48 小时工厂响应。"
        )
        cards = [
            ("欧洲", "ROUNDS 是现在的瑞士/南德入口。\nISE 再找 2 家能打包场馆项目的集成商（德、荷或北欧）。\n本季目标：对话，不签 20 家。"),
            ("日本", "必须有一家本地伙伴才进场。\nInter BEE 开谈，Sports Week 收短名单，\n2027.03 目标一份 LOI。今秋不卖散单。"),
            ("给什么", "德/英资料包、三支片子、项目 PDF、\n48 小时工厂支持、一场远程演示。\n不给消费品牌授权，不开招商会。"),
        ]
        rules = "规则：宁缺毋滥。欧洲增量 2 家，日本 1 家。先看他们有没有场馆项目，再谈授权。展会上交换名片不算经销商。"
    else:
        why = (
            "One company cannot cover DACH clubs and Japanese venues. Hiring will not close the gap.\n"
            "Dealers and integrators put COR + LED into projects. We keep delivery and a 48-hour factory."
        )
        cards = [
            ("Europe", "ROUNDS is the Swiss / south-German door now.\nISE: two more integrators who can package a venue (DE, NL or Nordic).\nThis season: conversations, not twenty contracts."),
            ("Japan", "We do not enter without one local partner.\nInter BEE opens talks, Sports Week shortlists,\nLOI target March 2027. No parts sales this autumn."),
            ("What they get", "DE/EN pack, three films, project PDF,\n48h factory, one remote demo.\nNo consumer franchise. No dealer conference."),
        ]
        rules = "Rule: few and real. Two incremental in Europe, one in Japan. Venue projects first, paper second. A badge scan is not a dealer."
    add_tf(s, ML, Inches(1.14), Inches(12.1), Inches(0.85), why, 16, INK, False, font)
    for i, (t, b) in enumerate(cards):
        x = ML + i * Inches(4.1)
        add_box(s, x, Inches(2.15), Inches(3.92), Inches(3.55), WASH)
        add_box(s, x, Inches(2.15), Inches(3.92), Pt(4), MAGENTA)
        add_tf(s, x + Inches(0.22), Inches(2.40), Inches(3.5), Inches(0.4), t, 18, INK, True, font)
        add_tf(s, x + Inches(0.22), Inches(2.90), Inches(3.5), Inches(2.55), b, 14, MUTED, False, font)
    add_box(s, ML, Inches(5.88), Inches(12.08), Inches(1.02), INK)
    add_tf(s, ML + Inches(0.22), Inches(6.04), Inches(11.6), Inches(0.72), rules, 14, WHITE, False, font, PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
    footer(s, 10, font)

    # ───────── 11 SLAM AGENT ─────────
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(
        s,
        "10  /  Slam Agent" if cn else "10  /  Slam Agent",
        "今秋仍卖项目。Agent 是 2027 的差异化叙事，不是现在的交货清单。" if cn else "This autumn we still sell projects. Agent is the 2027 story, not this quarter’s SKU.",
        font,
    )
    if cn:
        cards = [
            ("定位升级", "从「硬件 + 软件」讲成 Slam Agent：\n一场比赛的智能代理，而不只是记分屏。\n用来区别同质化记分/LED 竞品。"),
            ("技术路径", "开源 Linux 网关底座。\n语音切灯光 / 广告方案。\n自然语言交代「下一球暂停广告」。\n能演示再写进官网，不能演示就先别写。"),
            ("场景互动", "现场氛围感知：掌声分贝触发灯光秀。\n参考互动应用，不做粉丝玩具。\n给集成商看「整场系统会自己反应」。"),
            ("需求入口", "Solutions 页加 Custom AI Solution。\n请客户写下：自动统计、售票、灯光编排。\n用来收集需求，不假装功能已经交付。"),
        ]
        rule = "纪律：德文主站今秋主诉仍是一人操作系统 + SCORE / LED。Agent 只出现在简报、LinkedIn 和封闭活动，不替代现有产品名。"
    else:
        cards = [
            ("The shift", "Package hardware + software as Slam Agent:\nthe intelligent proxy for a match night,\nnot just a scoreboard. This is how we\nleave commodity LED behind."),
            ("The path", "Open Linux gateway. Voice to lights\nand ad playlists. Natural language:\n“hold the next timeout ad.”\nDemo first. Then put it on the site."),
            ("The room", "Sense the arena: applause triggers a light cue.\nNot a fan toy. Show integrators the system\nreacts to the match."),
            ("The intake", "A Custom AI Solution door on Solutions.\nAsk for stats, ticketing, lighting plots.\nCollect demand. Do not fake shipping."),
        ]
        rule = "Rule: the German site this autumn still sells one-operator SCORE + LED. Agent lives in briefings, LinkedIn and closed rooms — it does not replace product names."
    for i, (t, b) in enumerate(cards):
        x = ML + (i % 4) * Inches(3.08)
        add_box(s, x, Inches(1.18), Inches(2.92), Inches(4.55), WASH)
        add_tf(s, x + Inches(0.16), Inches(1.34), Inches(2.6), Inches(0.4), t, 16, MAGENTA, True, font)
        add_tf(s, x + Inches(0.16), Inches(1.82), Inches(2.6), Inches(3.7), b, 13, MUTED, False, font)
    add_box(s, ML, Inches(5.92), Inches(12.08), Inches(0.98), INK)
    add_tf(s, ML + Inches(0.2), Inches(6.06), Inches(11.7), Inches(0.72), rule, 14, WHITE, False, font, PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
    footer(s, 11, font)

    # ───────── 12 SCOREBOARD ─────────
    s = prs.slides.add_slide(blank)
    add_box(s, 0, 0, W, H, PAPER)
    header(
        s,
        "11  /  九十天必须交出来的东西" if cn else "11  /  What must be done in 90 days",
        "日期、负责人、数字。没有第三种状态。" if cn else "Date, owner, number. No third status.",
        font,
    )
    if cn:
        rows = [
            ["日期", "必须交付", "战线", "负责人", "数字"],
            ["9/29", "slam.systems 德文上线", "独立站", "Linda", "1 个域名"],
            ["10/13", "EN+ZH 首页 / LI+IG 首发", "独立站 · 社媒", "Eva + Peter", "2 个账号先活"],
            ["10/20", "7 秒 SCORE 片 + 表单跳转", "独立站 · 视频", "Jürg", "7s → 表单"],
            ["10/21", "SPORTEL 出差完成", "展会 · 直达", "Linda + Peter", "8 场会"],
            ["11/20", "Inter BEE 经销商开谈", "展会 · 经销商", "Linda + Jürg", "6 家面谈"],
            ["11/30", "欧洲名单全部触达", "邮件 · 直达", "Peter + Linda", "40 家"],
            ["12/20", "有效对话（不是点赞）", "直达", "Linda", "8 次"],
            ["1/29", "日本经销商短名单", "经销商", "Linda", "3 家"],
            ["2/05", "ISE + SWC 巴塞罗那", "展会 · 经销商", "Linda + Jürg", "12 场会"],
            ["3/31", "日本 LOI 或明确放弃", "经销商", "Linda", "1 份"],
        ]
        bottom = "下周一开始：冻结德文缺陷清单，列出欧洲 40 家和 SPORTEL 会谈名单。日本进展会表，不进今秋销售表。"
    else:
        rows = [
            ["Date", "Must ship", "Engine", "Owner", "Number"],
            ["29 Sep", "German live on slam.systems", "Site", "Linda", "1 domain"],
            ["13 Oct", "EN+ZH home / LI+IG first posts", "Site · Social", "Eva + Peter", "2 accounts live"],
            ["20 Oct", "7s SCORE film + form jump", "Site · Video", "Jürg", "7s → form"],
            ["21 Oct", "SPORTEL trip done", "Show · Direct", "Linda + Peter", "8 meetings"],
            ["20 Nov", "Inter BEE dealer talks open", "Show · Dealer", "Linda + Jürg", "6 meetings"],
            ["30 Nov", "Full Europe list reached", "Email · Direct", "Peter + Linda", "40 accounts"],
            ["20 Dec", "Real conversations (not likes)", "Direct", "Linda", "8"],
            ["29 Jan", "Japan dealer shortlist", "Dealer", "Linda", "3 names"],
            ["5 Feb", "ISE + SWC Barcelona", "Show · Dealer", "Linda + Jürg", "12 meetings"],
            ["31 Mar", "Japan LOI or a clear no", "Dealer", "Linda", "1 paper"],
        ]
        bottom = "Start next Monday: freeze the German defect list, draft the 40 EU names and the SPORTEL meeting list. Japan is on the show calendar, not on this autumn’s sales sheet."
    table_grid(s, ML, Inches(1.08), [Inches(1.35), Inches(4.05), Inches(2.35), Inches(2.15), Inches(2.15)], Inches(0.48), rows, font, True, 11)
    add_box(s, ML, Inches(6.42), Inches(12.08), Inches(0.52), MAGENTA)
    add_tf(s, ML + Inches(0.18), Inches(6.48), Inches(11.7), Inches(0.4), bottom, 13, WHITE, True, font, PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
    footer(s, 12, font)

    prs.save(C["file"])
    print("wrote", C["file"])


if __name__ == "__main__":
    build(CN, "cn")
    build(EN, "en")
