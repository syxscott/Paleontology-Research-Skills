"""Generate 7 figures for the WeChat announcement - Paleontology Research Skills v1.0.0."""

import math
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial"]
plt.rcParams["font.monospace"] = ["Consolas", "Microsoft YaHei", "SimHei"]  # CJK fallback
plt.rcParams["axes.unicode_minus"] = False
import matplotlib  # noqa: E402 - imported after rcParams setup is intentional

matplotlib.rcParams["font.family"] = "sans-serif"

OUT = r"D:/GIthub/自制Claude Code skills/docs"
os.makedirs(OUT, exist_ok=True)

BG = "#F7F8FA"
TXT = "#2C2E33"
SUB = "#6B6F76"
B = "#5B8FF9"
G = "#5AD8A6"
ORANGE = "#E8B86E"
C = "#E8847C"
P = "#9B7FE8"
BRD = "#D9DCE0"
CLRS = [B, G, ORANGE, C, P, B, G, ORANGE, C, P, B, G]


def save(fig, name):
    fp = os.path.join(OUT, name)
    fig.savefig(fp, dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("[OK]", fp)


def hero():
    f, a = plt.subplots(figsize=(13, 9), facecolor=BG)
    a.set(xlim=(-7, 7), ylim=(-5, 5), aspect="equal")
    a.axis("off")
    a.text(0, 4.55, "Paleontology Research Skills", ha="center", fontsize=26, fontweight="bold", color=TXT)
    a.text(0, 4.05, "面向古生物研究的可复现工作流工具集  v1.0.0", ha="center", fontsize=13, color=SUB)
    a.add_patch(Circle((0, 0), 0.85, facecolor="#FFFFFF", edgecolor=B, linewidth=2.2, zorder=5))
    a.text(0, 0.22, "PRS", ha="center", va="center", fontsize=22, fontweight="bold", color=B, zorder=6)
    a.text(
        0,
        -0.32,
        "Parent Skill",
        ha="center",
        va="center",
        fontsize=10,
        color=TXT,
        fontweight="bold",
        zorder=6,
    )
    items = [
        "PBDB",
        "CrossRef",
        "Memory",
        "Session",
        "Profile",
        "GeoTime",
        "Taxonomy",
        "Strat",
        "Morpho",
        "Convert",
        "Assistant",
        "CN-News",
    ]
    zhs = [
        "化石查询",
        "文献检索",
        "本地记忆",
        "会话历史",
        "研究档案",
        "地质时间",
        "分类层级",
        "地层学",
        "形态计量",
        "格式转换",
        "研究编排",
        "中文新闻",
    ]
    names = [
        "paleo-pbdb",
        "paleo-crossref",
        "paleo-memory",
        "paleo-session",
        "paleo-profile",
        "paleo-geo-time",
        "paleo-taxonomy",
        "paleo-stratigraphy",
        "paleo-morphometric",
        "paleo-morpho-convert",
        "paleo-research-asst",
        "paleo-china-news",
    ]
    R_node = 2.30  # 节点环半径
    R_label = 3.40  # 外部标签环半径（避免顶部撞副标题、底部撞标语）
    r_circle = 0.46
    for i in range(12):
        ang = math.pi / 2 - i * (2 * math.pi / 12)
        cx, cy = math.cos(ang), math.sin(ang)
        # 节点位置
        x, y = R_node * cx, R_node * cy
        # 连线（从中心圆边缘到节点圆边缘）
        x0, y0 = 0.85 * cx, 0.85 * cy
        x1, y1 = (R_node - r_circle) * cx, (R_node - r_circle) * cy
        a.plot([x0, x1], [y0, y1], color=BRD, lw=1, zorder=1)
        # 节点圆
        a.add_patch(Circle((x, y), r_circle, facecolor="#FFFFFF", edgecolor=CLRS[i], lw=1.8, zorder=3))
        a.text(x, y + 0.10, items[i], ha="center", fontsize=8.5, fontweight="bold", color=CLRS[i], zorder=4)
        a.text(x, y - 0.18, zhs[i], ha="center", fontsize=9, color=TXT, zorder=4)
        # 外部标签：沿径向放置
        lx, ly = R_label * cx, R_label * cy
        # 根据角度选择对齐方式
        if abs(cx) < 0.2:  # 接近正上/正下
            ha = "center"
        elif cx > 0:
            ha = "left" if cx > 0.5 else "center"
        else:
            ha = "right" if cx < -0.5 else "center"
        a.text(lx, ly, names[i], ha=ha, va="center", fontsize=8.2, color=SUB, family="monospace")
    a.text(
        0,
        -4.75,
        "13 Skills  13 Slash Commands  MIT License  2026",
        ha="center",
        fontsize=10.5,
        color=SUB,
        style="italic",
    )
    save(f, "fig01_hero.png")


def arch():
    f, a = plt.subplots(figsize=(12, 9), facecolor=BG)
    a.set(xlim=(0, 12), ylim=(0, 9))
    a.axis("off")
    a.text(6, 8.55, "嵌套式 SKILL.md 架构", ha="center", fontsize=20, fontweight="bold", color=TXT)
    a.text(
        6,
        8.15,
        "递归发现机制：父技能（宽入口）+ 12 个子技能（精确触发）",
        ha="center",
        fontsize=11,
        color=SUB,
    )
    lines = [
        (".claude/", "b", B),
        ("  skills/", "b", B),
        ("    paleontology-research-skills/    ★ 父技能 SKILL.md（宽描述）", "p", ORANGE),
        ("      SKILL.md", "f", SUB),
        ("      scripts/      共享 Python 工具 (paleo_common.py)", "f", SUB),
        ("      data/         共享静态数据", "f", SUB),
        ("      references/   共享参考文档", "f", SUB),
        ("      templates/    Markdown 输出模板", "f", SUB),
        ("      ", "f", SUB),
        ("      paleo-pbdb/                  PBDB 化石查询", "c", G),
        ("      paleo-crossref/              文献检索 (CrossRef + S2 + arXiv)", "c", G),
        ("      paleo-memory/                本地研究记忆", "c", G),
        ("      paleo-session/               会话历史", "c", G),
        ("      paleo-profile/               双层 profile", "c", G),
        ("      paleo-geo-time/              ICS 地质时间", "c", G),
        ("      paleo-taxonomy/              分类层级", "c", G),
        ("      paleo-stratigraphy/          地层学", "c", G),
        ("      paleo-morphometric/          几何形态计量地标", "c", G),
        ("      paleo-morphometric-convert/  地标格式互转", "c", G),
        ("      paleo-research-assistant/    五阶段研究编排", "c", G),
        ("      paleo-china-news/            中文古生物新闻", "c", G),
        ("    commands/                      13 个斜杠命令（手动入口）", "b", B),
    ]
    y = 7.4
    for text, kd, cl in lines:
        w = "bold" if kd in ("p", "b") else "normal"
        a.text(0.6, y, text, ha="left", va="center", fontsize=10.2, color=cl, fontweight=w)
        y -= 0.32
    a.add_patch(
        FancyBboxPatch(
            (8.6, 1.0),
            3.2,
            2.4,
            boxstyle="round,pad=0.06,rounding_size=0.15",
            facecolor="#FFFFFF",
            edgecolor=B,
            lw=1.5,
        )
    )
    a.text(10.2, 3.15, "设计要点", ha="center", fontsize=11.5, fontweight="bold", color=B)
    for i, n in enumerate(
        [
            " 父技能：宽 description",
            "  接住模糊提示",
            " 子技能：窄 description",
            "  精确匹配触发",
            " 共享 scripts / data / refs",
            " 子技能间无循环依赖",
        ]
    ):
        a.text(8.8, 2.85 - i * 0.28, n, ha="left", fontsize=9.2, color=TXT)
    save(f, "fig02_architecture.png")


def grid():
    f, a = plt.subplots(figsize=(13, 8), facecolor=BG)
    a.set(xlim=(0, 13), ylim=(0, 8))
    a.axis("off")
    a.text(6.5, 7.55, "十二个能力子模块", ha="center", fontsize=22, fontweight="bold", color=TXT)
    a.text(
        6.5,
        7.15,
        "覆盖：数据查询  文献检索  本地记忆  数据治理  研究编排",
        ha="center",
        fontsize=11,
        color=SUB,
    )
    items = [
        ("PBDB", "paleo-pbdb", "PBDB 化石产出查询", "1.5M+ 条产出  200K+ 分类", B),
        ("CrossRef", "paleo-crossref", "跨源文献检索", "CrossRef + S2 + arXiv", G),
        ("Memory", "paleo-memory", "本地研究记忆", "384 维哈希向量检索", ORANGE),
        ("Session", "paleo-session", "会话历史与恢复", "list/show/search/resume", C),
        ("Profile", "paleo-profile", "双层研究 profile", "soul.md + user.md", P),
        ("GeoTime", "paleo-geo-time", "ICS 地质时间表", "2023-09 彩色版离线副本", B),
        ("Taxonomy", "paleo-taxonomy", "分类层级 + 跨库交叉", "PBDB + NCBI + Wikidata", G),
        ("Strat", "paleo-stratigraphy", "地层学查询", "PBDB colls + Macrostrat", ORANGE),
        ("Morpho", "paleo-morphometric", "几何形态计量地标", "Moore 追踪 + 弧长重采样", C),
        ("Convert", "paleo-morphometric-convert", "地标格式互转", "TPS/NTS/CSV/JSON/Excel", P),
        ("Assistant", "paleo-research-assistant", "五阶段研究编排", "Markdown 综述 + JSON", B),
        ("CN-News", "paleo-china-news", "中文古生物新闻", "nkocs / 古学会 / IVPP", G),
    ]
    cw, ch, gx, gy = 2.95, 1.85, 0.15, 0.25
    x0, y0 = 0.6, 5.1
    for i, (tag, name, zh, sub, cl) in enumerate(items):
        c, r = i % 4, i // 4
        x = x0 + c * (cw + gx)
        y = y0 - r * (ch + gy)
        a.add_patch(
            FancyBboxPatch(
                (x, y),
                cw,
                ch,
                boxstyle="round,pad=0.04,rounding_size=0.10",
                facecolor="#FFFFFF",
                edgecolor=cl,
                lw=1.6,
            )
        )
        a.add_patch(Rectangle((x, y), 0.10, ch, facecolor=cl, edgecolor="none"))
        a.text(
            x + 0.30, y + ch - 0.30, tag, ha="left", va="center", fontsize=11.5, color=cl, fontweight="bold"
        )
        a.text(
            x + 1.30, y + ch - 0.32, name, ha="left", va="center", fontsize=9.5, color=SUB, family="monospace"
        )
        a.text(
            x + 0.25, y + ch - 0.78, zh, ha="left", va="center", fontsize=12.5, color=TXT, fontweight="bold"
        )
        a.text(x + 0.25, y + 0.35, sub, ha="left", va="center", fontsize=9.5, color=SUB)
    save(f, "fig03_modules_grid.png")


def princ():
    f, a = plt.subplots(figsize=(13, 7.5), facecolor=BG)
    a.set(xlim=(0, 13), ylim=(0, 7.5))
    a.axis("off")
    a.text(6.5, 7.05, "六条统一工程约定", ha="center", fontsize=22, fontweight="bold", color=TXT)
    a.text(6.5, 6.65, "可审计  可复现  失败优雅  跨平台", ha="center", fontsize=11, color=SUB)
    items = [
        ("统一 JSON 输出", "每个脚本输出一个 JSON 对象\nsource / query / count / records", B),
        ("失败不抛栈", "网络/IO/解析错误一律捕获\n转为 JSON.error 字段返回", G),
        ("零运行时依赖", "Python 3.9+ 标准库\nPillow/openpyxl 仅形态计量可选", ORANGE),
        ("科学诚信优先", "拒绝虚构物种/DOI/产地\nPBDB 404 友好提示而非 stack", C),
        ("可复现性", "查询参数完整回显\nMakefile: test/lint/validate/smoke", P),
        ("跨平台兼容", "subprocess 显式 UTF-8\n解决 Windows GBK/CJK 路径问题", B),
    ]
    cw, ch, gx, gy = 4.0, 2.4, 0.25, 0.30
    x0, y0 = 0.5, 3.6
    for i, (title, body, cl) in enumerate(items):
        c, r = i % 3, i // 3
        x = x0 + c * (cw + gx)
        y = y0 - r * (ch + gy)
        a.add_patch(
            FancyBboxPatch(
                (x, y),
                cw,
                ch,
                boxstyle="round,pad=0.04,rounding_size=0.12",
                facecolor="#FFFFFF",
                edgecolor=cl,
                lw=1.7,
            )
        )
        a.add_patch(Circle((x + 0.45, y + ch - 0.42), 0.30, facecolor=cl, edgecolor="none"))
        a.text(
            x + 0.45,
            y + ch - 0.42,
            str(i + 1),
            ha="center",
            va="center",
            fontsize=13,
            color="white",
            fontweight="bold",
        )
        a.text(
            x + 0.95, y + ch - 0.42, title, ha="left", va="center", fontsize=14, color=TXT, fontweight="bold"
        )
        a.text(x + 0.45, y + 0.75, body, ha="left", va="top", fontsize=10.5, color=SUB, linespacing=1.5)
    save(f, "fig04_principles.png")


def workflow():
    f, a = plt.subplots(figsize=(13, 7), facecolor=BG)
    a.set(xlim=(0, 13), ylim=(0, 7))
    a.axis("off")
    a.text(6.5, 6.55, "可复现工作流示例", ha="center", fontsize=22, fontweight="bold", color=TXT)
    a.text(
        6.5,
        6.15,
        "案例：辽西下白垩统义县组今鸟型类（Ornithuromorpha）化石多样性与文献热度",
        ha="center",
        fontsize=11,
        color=SUB,
    )
    steps = [
        ("1", "profile_init", "初始化 profile", "soul.md + user.md", P),
        ("2", "stratigraphy_query", "义县组地层查询", "PBDB + Macrostrat", ORANGE),
        ("3", "taxonomy_query", "分类层级核实", "Ornithuromorpha 全谱", G),
        ("4", "pbdb_query", "PBDB 产出记录", "respect-profile 限速", B),
        ("5", "crossref_search", "近 25 年文献", "rows=30  from=2000", C),
    ]
    n = len(steps)
    y_step = 4.2
    bw, bh = 2.05, 1.55
    tw = n * bw + (n - 1) * 0.45
    x0 = (13 - tw) / 2
    for i, (idx, name, zh, sub, cl) in enumerate(steps):
        x = x0 + i * (bw + 0.45)
        a.add_patch(
            FancyBboxPatch(
                (x, y_step),
                bw,
                bh,
                boxstyle="round,pad=0.04,rounding_size=0.10",
                facecolor="#FFFFFF",
                edgecolor=cl,
                lw=1.8,
            )
        )
        a.add_patch(Circle((x + bw / 2, y_step + bh - 0.30), 0.22, facecolor=cl, edgecolor="none"))
        a.text(
            x + bw / 2,
            y_step + bh - 0.30,
            idx,
            ha="center",
            va="center",
            fontsize=14,
            color="white",
            fontweight="bold",
        )
        a.text(
            x + bw / 2,
            y_step + bh - 0.78,
            zh,
            ha="center",
            va="center",
            fontsize=12,
            color=TXT,
            fontweight="bold",
        )
        a.text(
            x + bw / 2,
            y_step + 0.45,
            name + ".py",
            ha="center",
            va="center",
            fontsize=9.5,
            color=SUB,
            family="monospace",
        )
        a.text(x + bw / 2, y_step + 0.18, sub, ha="center", va="center", fontsize=8.5, color=SUB)
        if i < n - 1:
            a.add_patch(
                FancyArrowPatch(
                    (x + bw + 0.05, y_step + bh / 2),
                    (x + bw + 0.40, y_step + bh / 2),
                    arrowstyle="->",
                    mutation_scale=15,
                    color=SUB,
                    lw=1.6,
                )
            )
    a.annotate("", xy=(6.5, 2.2), xytext=(6.5, 4.05), arrowprops=dict(arrowstyle="->", lw=2, color=B))
    a.text(
        6.85, 3.25, "research_assistant.py", ha="left", va="center", fontsize=10, color=B, family="monospace"
    )
    a.text(6.85, 2.95, "5 阶段编排", ha="left", va="center", fontsize=10, color=B)
    a.add_patch(
        FancyBboxPatch(
            (4.0, 0.55),
            5.0,
            1.55,
            boxstyle="round,pad=0.06,rounding_size=0.15",
            facecolor="#FFFFFF",
            edgecolor=B,
            lw=2,
        )
    )
    a.text(
        6.5,
        1.75,
        "七章节 Markdown 报告 + JSON manifest",
        ha="center",
        va="center",
        fontsize=12,
        color=TXT,
        fontweight="bold",
    )
    a.text(
        6.5,
        1.35,
        "Overview  Literature  Taxonomy  Occurrences",
        ha="center",
        va="center",
        fontsize=9.5,
        color=SUB,
    )
    a.text(
        6.5, 1.10, "Stratigraphy  References  Limitations", ha="center", va="center", fontsize=9.5, color=SUB
    )
    a.text(
        6.5, 0.78, "网络可用条件下 3090 秒完成", ha="center", va="center", fontsize=9, color=B, style="italic"
    )
    save(f, "fig05_workflow.png")


def moore():
    f, axes = plt.subplots(1, 2, figsize=(13, 6.5), facecolor=BG)
    f.suptitle("Moore 邻域边界追踪 + 累积弧长等距重采样", fontsize=18, fontweight="bold", color=TXT, y=0.98)
    ax = axes[0]
    ax.set_facecolor(BG)
    ax.set(xlim=(-2.5, 2.5), ylim=(-2.5, 2.5), aspect="equal")
    ax.axis("off")
    ax.set_title("(a) 8 方向 Moore 邻域", fontsize=13, color=TXT, pad=14)
    for i in range(-2, 3):
        for j in range(-2, 3):
            ax.add_patch(Rectangle((i - 0.5, j - 0.5), 1, 1, facecolor="#FFFFFF", edgecolor=BRD, lw=0.8))
    ax.add_patch(Rectangle((-0.5, -0.5), 1, 1, facecolor=C, edgecolor=C, lw=1, alpha=0.85))
    ax.text(0, 0, "P", ha="center", va="center", fontsize=14, fontweight="bold", color="white")
    dirs = [
        (0, 1, "0"),
        (1, 1, "1"),
        (1, 0, "2"),
        (1, -1, "3"),
        (0, -1, "4"),
        (-1, -1, "5"),
        (-1, 0, "6"),
        (-1, 1, "7"),
    ]
    for dx, dy, lbl in dirs:
        ax.add_patch(Rectangle((dx - 0.5, dy - 0.5), 1, 1, facecolor=B, edgecolor=B, alpha=0.20))
        ax.text(dx, dy, lbl, ha="center", va="center", fontsize=12, color=B, fontweight="bold")
    for k in range(8):
        x1, y1, _ = dirs[k]
        x2, y2, _ = dirs[(k + 1) % 8]
        ax.annotate(
            "",
            xy=(x2 * 0.62, y2 * 0.62),
            xytext=(x1 * 0.62, y1 * 0.62),
            arrowprops=dict(arrowstyle="->", lw=1, color=G, alpha=0.7),
        )
    ax.text(0, -2.15, "顺时针扫描  寻找下一个前景像素", ha="center", fontsize=10, color=SUB)
    ax = axes[1]
    ax.set_facecolor(BG)
    ax.set(xlim=(-1.4, 1.4), ylim=(-1.2, 1.2), aspect="equal")
    ax.axis("off")
    ax.set_title("(b) 弧长等距重采样（N=24，演示用）", fontsize=13, color=TXT, pad=14)
    t = np.linspace(0, 2 * np.pi, 400)
    r = 1 + 0.18 * np.sin(3 * t) - 0.08 * np.cos(2 * t)
    cx, cy = r * np.cos(t), r * np.sin(t)
    ax.plot(cx, cy, color=TXT, lw=1.6, label="原始轮廓")
    dx = np.diff(cx)
    dy = np.diff(cy)
    seg = np.sqrt(dx * dx + dy * dy)
    cum = np.concatenate([[0], np.cumsum(seg)])
    total = cum[-1]
    targets = np.linspace(0, total, 24, endpoint=False)
    px = np.interp(targets, cum, cx)
    py = np.interp(targets, cum, cy)
    ax.scatter(px, py, s=55, color=C, zorder=5, edgecolors="white", lw=1.2, label="弧长等距 semilandmark")
    idx = np.linspace(0, len(cx) - 1, 24, endpoint=False).astype(int)
    ax.scatter(cx[idx], cy[idx], s=22, color=B, zorder=4, alpha=0.55, label="按索引等距（疏密不均）")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.18), ncol=3, fontsize=9, frameon=False)
    plt.subplots_adjust(top=0.88, bottom=0.10)
    save(f, "fig06_moore_arc.png")


def hashvec():
    f, a = plt.subplots(figsize=(13, 6), facecolor=BG)
    a.set(xlim=(0, 13), ylim=(0, 6))
    a.axis("off")
    a.text(
        6.5,
        5.55,
        "384 维哈希技巧伪向量  零外部依赖的语义检索",
        ha="center",
        fontsize=18,
        fontweight="bold",
        color=TXT,
    )
    a.text(
        6.5,
        5.15,
        "Signed Random Projection 极简实现  MD5 决定维度索引与符号",
        ha="center",
        fontsize=11,
        color=SUB,
    )
    stages = [
        ("文本输入", "义县组今鸟型类\n化石多样性", B),
        ("分词", "tokens = [Yixian,\nOrnithuromorpha, ...]", G),
        ("MD5 摘要", "md5(token)\n→ 16 bytes", ORANGE),
        ("维度索引", "前 8 字节\n% 384 = dim", C),
        ("符号决定", "第 9-10 字节\n奇偶 → +1/-1", P),
        ("384 维向量", "vec[dim] += sign\nL2 归一化", B),
    ]
    n = len(stages)
    bw, bh = 1.85, 1.35
    gap = 0.13
    tw = n * bw + (n - 1) * gap
    x0 = (13 - tw) / 2
    y = 2.55
    for i, (title, body, cl) in enumerate(stages):
        x = x0 + i * (bw + gap)
        a.add_patch(
            FancyBboxPatch(
                (x, y),
                bw,
                bh,
                boxstyle="round,pad=0.04,rounding_size=0.10",
                facecolor="#FFFFFF",
                edgecolor=cl,
                lw=1.6,
            )
        )
        a.text(
            x + bw / 2,
            y + bh - 0.25,
            title,
            ha="center",
            va="center",
            fontsize=11.5,
            color=cl,
            fontweight="bold",
        )
        a.text(x + bw / 2, y + 0.50, body, ha="center", va="center", fontsize=9, color=TXT, linespacing=1.4)
        if i < n - 1:
            a.add_patch(
                FancyArrowPatch(
                    (x + bw + 0.005, y + bh / 2),
                    (x + bw + gap - 0.005, y + bh / 2),
                    arrowstyle="->",
                    mutation_scale=12,
                    color=SUB,
                    lw=1.4,
                )
            )
    a.add_patch(
        FancyBboxPatch(
            (1.0, 0.55),
            11.0,
            1.45,
            boxstyle="round,pad=0.05,rounding_size=0.12",
            facecolor="#FFFFFF",
            edgecolor=BRD,
            lw=1,
        )
    )
    a.text(1.3, 1.65, "优势", ha="left", fontsize=11, fontweight="bold", color=G)
    a.text(
        1.3,
        1.30,
        " 不调用任何嵌入 API（OpenAI/Cohere/SentenceTransformers 全部豁免）",
        ha="left",
        fontsize=9.5,
        color=TXT,
    )
    a.text(
        1.3,
        1.05,
        " 仅依赖 hashlib（标准库），可在受限网络 / 内网开发机直接运行",
        ha="left",
        fontsize=9.5,
        color=TXT,
    )
    a.text(
        1.3, 0.80, " 自相似度恒等于 1，跨主题相似度 < 0.5（tests 已验证）", ha="left", fontsize=9.5, color=TXT
    )
    a.text(7.6, 1.65, "适用范围", ha="left", fontsize=11, fontweight="bold", color=ORANGE)
    a.text(7.6, 1.30, " 1000 量级以下记忆条目质量可接受", ha="left", fontsize=9.5, color=TXT)
    a.text(7.6, 1.05, " 命中阈值：cosine similarity > 0.2", ha="left", fontsize=9.5, color=TXT)
    a.text(7.6, 0.80, " 可平滑替换为本地 embedding（API 一致）", ha="left", fontsize=9.5, color=TXT)
    save(f, "fig07_hashing_vector.png")


if __name__ == "__main__":
    hero()
    arch()
    grid()
    princ()
    workflow()
    moore()
    hashvec()
    print("[Done] all 7 figures generated in", OUT)
