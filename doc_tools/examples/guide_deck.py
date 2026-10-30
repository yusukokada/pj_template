"""説明資料「ひな型リポジトリによるプロジェクトの立上げと進め方」を作る（deck_lib の使い方の手本）。
python doc_tools/examples/guide_deck.py <テンプレート.pptx> <実物の画像のフォルダ>
テンプレートはプロジェクト計画書と同じ ITPMテンプレ.pptx（スライドマスタ・レイアウト・緑系の色をそのまま使う）。
実物の画像は ITマネジメント高度化の成果物の画面・シート（s1_memo.png など。リポジトリには入れない）。
出力：guide/【説明資料】ひな型リポジトリによるプロジェクトの立上げと進め方_v0.6.pptx（既にあれば止める）

ページごとに図の形を変え（集約・層・柱・流れ・ロードマップ・階段・左右対称・循環）、
1ページに1つ、目が行く場所（濃い緑・大きな文字・吹き出し）を作っている。"""
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "doc_tools"))
from deck_lib import *  # noqa: E402,F403

OUT = ROOT / "guide" / "【説明資料】ひな型リポジトリによるプロジェクトの立上げと進め方_v0.6.pptx"
TEMPLATE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "ITPMテンプレ.pptx"
assert TEMPLATE.exists(), f"テンプレートがない：{TEMPLATE}"
IMG = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "guide" / "img"
assert (IMG / "s1_memo.png").exists(), f"実物の画像がない：{IMG}"
assert not OUT.exists(), f"出力先が既にある：{OUT}"
TOP = 1.8
C, L, R = PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.RIGHT
M, T = MSO_ANCHOR.MIDDLE, MSO_ANCHOR.TOP
# 計画書と同じ緑系（テンプレートのテーマ色）
DG = RGBColor(0x04, 0x6A, 0x38)     # 濃い緑：注目させるもの
G2 = RGBColor(0x26, 0x89, 0x0D)     # 緑：番号・見出し
BG = RGBColor(0x86, 0xBC, 0x25)     # 明るい緑：矢印・線
LG = RGBColor(0xEC, 0xF4, 0xDD)     # 薄い緑：塗り
PALE = RGBColor(0xF6, 0xF9, 0xF0)   # さらに薄い緑
d = Deck("ひな型リポジトリ｜立上げと進め方", template=str(TEMPLATE), layout="（基本版）タイトルのみ_出所・脚注なし_16:9")


# ---------------------------------------------------------------- 部品
def circle(cx, cy, dia, fill=LG, line=None, paras=None, lw=1.75):
    return d.box(cx - dia / 2, cy - dia / 2, dia, dia, paras, fillc=fill, line=line, lw=lw, kind=MSO_SHAPE.OVAL, align=C, ins=(0, 0, 0, 0))


def num(cx, cy, n, dia=0.5, fill=G2, size=16):
    return circle(cx, cy, dia, fill, paras=[(str(n), True, size, WHITE)])


def arrow(p, q, color=BG, width=2.25, dashed=False):
    return d.line(p, q, color=color, width=width, arrow=True, dashed=dashed)


def label(x, y, w, h, paras, size=14, align=L, anchor=T, color=TXT):
    return d.text(x, y, w, h, paras, size=size, align=align, anchor=anchor, color=color)


# アイコン（中心 cx, cy、大きさ s）
def i_person(cx, cy, s=1.0, col=G2):
    d.box(cx - 0.17 * s, cy - 0.4 * s, 0.34 * s, 0.34 * s, None, fillc=col, line=None, kind=MSO_SHAPE.OVAL)
    d.box(cx - 0.3 * s, cy - 0.02 * s, 0.6 * s, 0.4 * s, None, fillc=col, line=None, kind=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)


def i_ai(cx, cy, s=1.0, col=G2):
    d.box(cx - 0.02 * s, cy - 0.46 * s, 0.04 * s, 0.14 * s, None, fillc=col, line=None)
    d.box(cx - 0.07 * s, cy - 0.54 * s, 0.14 * s, 0.14 * s, None, fillc=BG, line=None, kind=MSO_SHAPE.OVAL)
    d.box(cx - 0.36 * s, cy - 0.33 * s, 0.72 * s, 0.6 * s, [("AI", True, max(10, int(16 * s)), WHITE)], fillc=col, line=None,
          kind=MSO_SHAPE.ROUNDED_RECTANGLE, align=C, ins=(0, 0, 0, 0), round_adj=0.25)


def i_doc(cx, cy, s=1.0, col=G2):
    d.box(cx - 0.24 * s, cy - 0.3 * s, 0.48 * s, 0.6 * s, None, fillc=WHITE, line=col, lw=1.5, kind=MSO_SHAPE.FOLDED_CORNER)
    for k in range(3):
        d.box(cx - 0.15 * s, cy - 0.15 * s + k * 0.13 * s, 0.3 * s, 0.04 * s, None, fillc=col, line=None)


def i_sheet(cx, cy, s=1.0, col=G2):
    w, h = 0.62 * s, 0.5 * s
    d.box(cx - w / 2, cy - h / 2, w, h, None, fillc=WHITE, line=col, lw=1.5)
    d.box(cx - w / 2, cy - h / 2, w, 0.12 * s, None, fillc=col, line=None)
    for k in (1, 2):
        d.line((cx - w / 2 + k * w / 3, cy - h / 2 + 0.12 * s), (cx - w / 2 + k * w / 3, cy + h / 2), color=col, width=1)
    d.line((cx - w / 2, cy + 0.06 * s), (cx + w / 2, cy + 0.06 * s), color=col, width=1)


def i_json(cx, cy, s=1.0, col=G2):
    d.box(cx - 0.32 * s, cy - 0.26 * s, 0.64 * s, 0.52 * s, [("{ }", True, max(12, int(18 * s)), col)], fillc=WHITE, line=col, lw=1.5,
          kind=MSO_SHAPE.ROUNDED_RECTANGLE, align=C, ins=(0, 0, 0, 0))


def i_gear(cx, cy, s=1.0, col=G2):
    d.box(cx - 0.3 * s, cy - 0.3 * s, 0.6 * s, 0.6 * s, None, fillc=col, line=None, kind=MSO_SHAPE.GEAR_6)


def i_screen(cx, cy, s=1.0, col=G2):
    d.box(cx - 0.34 * s, cy - 0.28 * s, 0.68 * s, 0.44 * s, None, fillc=WHITE, line=col, lw=2)
    d.box(cx - 0.05 * s, cy + 0.16 * s, 0.1 * s, 0.1 * s, None, fillc=col, line=None)
    d.box(cx - 0.2 * s, cy + 0.26 * s, 0.4 * s, 0.05 * s, None, fillc=col, line=None)


def i_check(cx, cy, s=1.0, col=G2):
    d.line((cx - 0.24 * s, cy), (cx - 0.06 * s, cy + 0.19 * s), color=col, width=4.5 * s)
    d.line((cx - 0.06 * s, cy + 0.19 * s), (cx + 0.27 * s, cy - 0.2 * s), color=col, width=4.5 * s)


def i_sync(cx, cy, s=1.0, col=G2):
    arrow((cx - 0.12 * s, cy + 0.28 * s), (cx - 0.12 * s, cy - 0.28 * s), color=col, width=3)
    arrow((cx + 0.12 * s, cy - 0.28 * s), (cx + 0.12 * s, cy + 0.28 * s), color=col, width=3)


def i_folder(x, y, s=1.0, col=G2):
    d.box(x, y, 0.2 * s, 0.08 * s, None, fillc=col, line=None)
    d.box(x, y + 0.06 * s, 0.4 * s, 0.28 * s, None, fillc=col, line=None)


def icon_in_circle(fn, cx, cy, dia=1.1, s=1.0, fill=LG, line=None, col=G2):
    circle(cx, cy, dia, fill, line)
    fn(cx, cy, s, col)


def pill(x, y, w, n, name, fill=G2):
    """段階の札（番号と名前）"""
    return d.box(x, y, w, 0.42, [(f"{n}  {name}", True, 15, WHITE)], fillc=fill, line=None, kind=MSO_SHAPE.ROUNDED_RECTANGLE,
                 ins=(0.18, 0, 0.1, 0), round_adj=0.5)


def framed(name, x, y, w, h, line=None, lw=3.0):
    """薄い緑の枠の中に、縦横比を保って画像を最大に置く"""
    from PIL import Image
    d.box(x, y, w, h, None, fillc=PALE, line=line, lw=lw)
    iw, ih = Image.open(IMG / name).size
    pad = 0.12
    sc = min((w - 2 * pad) / iw, (h - 2 * pad) / ih)
    pw, ph = iw * sc, ih * sc
    pic = d.s.shapes.add_picture(str(IMG / name), Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))
    pic.line.color.rgb = RGBColor(0xD0, 0xD0, 0xCE)
    pic.line.width = Pt(0.75)
    return pic


# ---------------------------------------------------------------- 表紙（計画書と同じ「タイトル ロゴ無」）
d.s = d.prs.slides.add_slide(d.lay["（基本版）タイトル ロゴ無_16:9"])
d.page = 1
for ph in list(d.s.placeholders):
    texts = {0: ["ひな型リポジトリによる", "プロジェクトの立上げと進め方"], 1: ["2026年10月30日（v0.6）"], 10: ["AI と進めるプロジェクトの共通の土台"]}
    idx = ph.placeholder_format.idx
    if idx not in texts:
        ph._element.getparent().remove(ph._element)
        continue
    tf = ph.text_frame
    tf.clear()
    for k, t in enumerate(texts[idx]):
        para = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        r = para.add_run()
        r.text = t
        rPr = r._r.get_or_add_rPr()
        rPr.set("lang", "ja-JP"); rPr.set("altLang", "en-US"); rPr.set("dirty", "0")
CX, CY = 9.55, 2.75
SAT = [(6.95, 1.17, i_doc, "ルール・手順書", 5.75, 1.83), (12.1, 1.17, i_gear, "決まった道具", 10.75, 1.83),
       (12.1, 4.97, i_check, "確認の道具", 10.75, 5.63)]
for sx, sy, *_ in SAT:   # 点線は円の下に描き、中央の円で隠す
    d.line((sx, sy), (CX, CY), color=BG, width=1.5, dashed=True)
circle(CX, CY, 4.5, PALE)
circle(CX, CY, 3.2, LG)
label(CX - 1.2, CY - 0.45, 2.4, 0.9, [("ひな型", True, 20, DG), ("リポジトリ", True, 14, DG)], align=C, anchor=M)
for sx, sy, fn, name, lx, ly in SAT:
    icon_in_circle(fn, sx, sy, 1.24, 1.0, WHITE, BG)
    label(lx, ly, 2.6, 0.3, [(name, True, 13, DG)], align=C)

# ---------------------------------------------------------------- 2 目的：集約の図
d.slide("AI の種類や担当者が変わっても、同じ手順・同じ確認方法でデータモデル設計から試作アプリ・説明資料まで進めるための共通の土台",
        "1｜ひな型の目的")
for k, (fn, name) in enumerate([(i_ai, "Copilot"), (i_ai, "Claude"), (i_person, "担当者")]):
    cy = 2.45 + k * 1.3
    icon_in_circle(fn, 1.2, cy, 0.95, 0.9)
    label(1.8, cy - 0.22, 1.6, 0.45, [(name, True, 16, DG)], anchor=M)
    arrow((3.25, cy), (4.45, 3.75 + (k - 1) * 0.6))
d.box(4.55, 2.15, 3.9, 3.2, [("ひな型", True, 30, WHITE), ("", False, 8), ("ルール", False, 16, WHITE), ("手順書", False, 16, WHITE),
                              ("決まった道具", False, 16, WHITE), ("確認の道具", False, 16, WHITE)],
      fillc=DG, line=None, align=C, anchor=M)
arrow((8.55, 3.75), (9.45, 3.75), width=3)
circle(10.15, 3.0, 1.1, LG)
i_check(10.15, 3.0, 1.3)
label(10.85, 2.55, 1.95, 0.9, [("同じ品質の", True, 18, DG), ("成果物", True, 18, DG)], anchor=M)
for k, (fn, name) in enumerate([(i_sheet, "データ定義書"), (i_screen, "試作アプリ"), (i_doc, "説明資料")]):
    fn(9.95, 4.0 + k * 0.5, 0.6)
    label(10.35, 3.82 + k * 0.5, 2.4, 0.36, [name], size=14, anchor=M)
d.box(X0, 5.85, W, 0.95, None, fillc=PALE, line=None)
label(X0 + 0.25, 5.85, 1.6, 0.95, [("解く課題", True, 16, DG)], anchor=M)
for k, t in enumerate(["AI は会話をまたいで記憶しない", "プロジェクト専用のスクリプトは使い回せない", "確認手段がないと出来がばらつく"]):
    label(2.1 + k * 3.6, 5.85, 3.5, 0.95, [t], size=14, anchor=M)

# ---------------------------------------------------------------- 3 構造：層の図＋誰が触るか
d.slide("AI への指示とルール・手順書、成果物、道具の3層で構成し、成果物は道具で作って道具で確かめるリポジトリの構造",
        "2｜リポジトリの構造")
SLX, SLW, LBW = X0, 8.95, 1.85
layers = [
    ("指示・ルール", PALE, DG, [(".github/", "AI への指示"), ("rules/", "作業ルール"), ("playbook/", "5段階の手順書")], 1.25,
     i_ai, "AI が最初に読む"),
    ("成果物", DG, WHITE, [("docs/", "定義書・資料の最新版"), ("app/", "試作アプリ・業務画面")], 1.55,
     i_person, "人がレビューする"),
    ("道具", PALE, DG, [("doc_tools/", "資料の道具"), ("app/tools/", "生成と確認"), ("check_all.py", "一括の確認")], 1.25,
     i_ai, "AI が使い、流す"),
]
y = TOP + 0.05
for name, fill, fg, chips, h, who, act in layers:
    d.box(SLX, y, SLW, h, None, fillc=fill, line=None)
    label(SLX + 0.2, y, LBW - 0.2, h, [(name, True, 18, fg)], anchor=M)
    cx0, cw = SLX + LBW, (SLW - LBW - 0.2 - 0.15 * (len(chips) - 1)) / len(chips)
    for j, (fname, desc) in enumerate(chips):
        x = cx0 + j * (cw + 0.15)
        d.box(x, y + 0.2, cw, h - 0.4, None, fillc=WHITE, line=None)
        i_folder(x + 0.15, y + h / 2 - 0.2, 1.0, G2)
        label(x + 0.65, y + 0.2, cw - 0.7, h - 0.4, [(fname, True, 15, DG), desc], size=14, anchor=M)
    icon_in_circle(who, 10.05, y + h / 2, 0.85, 0.8, fill=LG)
    label(10.6, y, 2.2, h, [(act, True, 16, DG)], anchor=M)
    y += h + 0.25

# ---------------------------------------------------------------- 4 考え方：4つの柱
d.slide("文書を正とし、事実の入力と計算による判断を分け、確認手段で品質を担保し、指摘をルールとして蓄積する4つの原則",
        "3｜ひな型の考え方")
PW = (W - 3 * 0.35) / 4
for k, (fn, key, body) in enumerate([
        (i_sheet, ["定義書が正", "アプリは生成物"], "項目の追加・変更は定義書を直してアプリを作り直し。アプリのコードだけで辻褄を合わせる変更の禁止"),
        (i_gear, ["人は事実を入力", "判断は計算"], "遅れ・良否などの判定の値を人に入力させず、閾値はマスタに保持。全件を同じ基準で比較"),
        (i_check, ["確認手段が", "品質を決定"], "AI の出来は正解と比べる手段の有無で変動。点検・全画面の確認・PNG に合格するまで AI が自ら修正"),
        (i_doc, ["ルールのファイルが", "記憶の代わり"], "AI は会話をまたいで記憶しないため、指摘と理由を rules/ に記録し、次の作業から適用")]):
    x = X0 + k * (PW + 0.35)
    cx = x + PW / 2
    label(x, TOP + 0.05, PW, 0.4, [(f"0{k + 1}", True, 16, BG)], align=C)
    icon_in_circle(fn, cx, TOP + 1.15, 1.35, 1.35)
    label(x, TOP + 2.0, PW, 0.95, [(key[0], True, 20, DG), (key[1], True, 20, DG)], align=C)
    d.line((x + 0.3, TOP + 3.1), (x + PW - 0.3, TOP + 3.1), color=BG, width=1.5)
    label(x + 0.1, TOP + 3.25, PW - 0.2, 1.8, [body], size=14)

# ---------------------------------------------------------------- 5 流れ：パイプライン
d.slide("AI は JSON を直してスクリプトで定義書を作り、定義書からアプリを生成するため、体裁と構造が毎回同一になる仕組み",
        "4｜定義書からアプリまでの流れ")
nodes = [(i_sheet, "定義書", "人が直す正本"), (i_json, "JSON", "AI が修正"), (i_sheet, "新しい版", "build で作成"), (i_check, "点検", "誤り0件"),
         (i_gear, "生成", "モデル・管理画面"), (i_screen, "試作アプリ", "業務画面を追加"), (i_check, "確認", "全画面・文言")]
NY, SP = 3.35, W / 7
xs = [X0 + SP * (k + 0.5) for k in range(7)]
d.line((xs[0], NY), (xs[-1], NY), color=BG, width=4)
for lo, hi, name in [(0, 3, "定義書を作る（doc_tools/definition.py）"), (4, 6, "アプリを作る（app/tools/）")]:
    x1, x2 = xs[lo] - SP / 2 + 0.1, xs[hi] + SP / 2 - 0.1
    d.line((x1, 2.25), (x2, 2.25), color=G2, width=1.5)
    for xx in (x1, x2):
        d.line((xx, 2.25), (xx, 2.45), color=G2, width=1.5)
    label(x1, 1.85, x2 - x1, 0.4, [(name, True, 16, G2)], align=C)
for k, (fn, name, desc) in enumerate(nodes):
    icon_in_circle(fn, xs[k], NY, 1.1, 1.05, fill=WHITE if k == 0 else LG)
    label(xs[k] - SP / 2, NY + 0.75, SP, 0.4, [(name, True, 16, DG)], align=C)
    label(xs[k] - SP / 2, NY + 1.15, SP, 0.4, [desc], size=14, align=C)
d.box(xs[0] - 0.62, NY - 0.62, 1.24, 1.24, None, fillc=None, line=DG, lw=3, kind=MSO_SHAPE.OVAL)   # 正本を濃い緑の輪で強調
yb = 5.55
d.polyline([(xs[5], NY + 1.6), (xs[5], yb), (xs[0], yb)], color=DG, width=2, dashed=True)
arrow((xs[0], yb), (xs[0], NY + 1.6), color=DG, width=2, dashed=True)
label(xs[0] + 0.3, yb + 0.1, xs[5] - xs[0] - 0.6, 0.5, [("業務画面の作成で見つかった定義書の不足は、定義書の版上げで反映", True, 16, DG)], align=C)

# ---------------------------------------------------------------- 6 進め方：ロードマップと合意のゲート
d.slide("事象と課題から To-Be像・データモデル・試作アプリ・資料へ5段階で進め、各段階の確認と人の合意を次段階への移行条件とする進め方",
        "5｜5段階の進め方")
LY = 2.95
sx = [1.1 + k * 2.36 for k in range(5)]
d.line((sx[0], LY), (sx[-1] + 1.18, LY), color=BG, width=4)
stages = [("事象と課題", ["目指す姿・事象・", "課題・解きたい判断"]), ("To-Be像", ["領域別の", "To-Be像"]), ("データモデル", ["データ定義書"]),
          ("試作アプリ", ["業務画面", "ダミーデータ"]), ("資料", ["説明資料"])]
gates = ["課題と判断の一覧", "To-Be像", "テーブル一覧と1行の単位", "画面一覧と閾値", "ページ構成"]
for k, (name, made) in enumerate(stages):
    label(sx[k] - 1.15, TOP + 0.05, 2.3, 0.45, [(name, True, 18, DG)], align=C)
    num(sx[k], LY, k + 1, 0.8, G2, 20)
    label(sx[k] - 1.1, LY + 0.55, 2.2, 0.8, made, size=14, align=C)
    gx = sx[k] + 1.18
    d.box(gx - 0.42, LY - 0.42, 0.84, 0.84, [("合意", True, 13, WHITE)], fillc=DG, line=None, kind=MSO_SHAPE.DIAMOND, align=C, ins=(0, 0, 0, 0))
    d.line((gx, LY + 0.45), (gx, 4.6), color=DG, width=1.25, dashed=True)
    d.box(gx - 1.05, 4.6, 2.1, 0.95, [gates[k]], fillc=PALE, line=DG, lw=1.25, size=14, align=C, ins=(0.08, 0.04, 0.08, 0.04))
d.box(X0 + 0.05, 6.12, 0.46, 0.46, None, fillc=DG, line=None, kind=MSO_SHAPE.DIAMOND)
label(X0 + 0.7, 5.95, W - 0.7, 0.8, [[("人の合意が、次の段階に進む条件", True, 18, DG), ("　確認方法は playbook/ の各段階に記載", False, 14, NOTE)]],
      anchor=M)

# ---------------------------------------------------------------- 7 成果物の実物（段階1〜3）：4つの枠と大きな文字
d.slide("ITマネジメント高度化では、事象62件の課題から領域別の To-Be像を描き、それを実現する84テーブル・786項目のデータ定義書まで作成",
        "6｜成果物の実物（段階1〜3）")
FW4 = (W - 3 * 0.22) / 4
pill(X0, TOP, FW4, 1, "事象と課題")
pill(X0 + FW4 + 0.22, TOP, FW4, 2, "To-Be像", fill=DG)
pill(X0 + 2 * (FW4 + 0.22), TOP, 2 * FW4 + 0.22, 3, "データモデル")
for k, (img, big, cap) in enumerate([
        ("s1_memo_c.png", "62件", "現場の事象を8領域で整理し、課題と解きたい判断を導出"),
        ("s2_tobe.png", "8領域", "判断・データ・自動化の形で書いた領域別の To-Be像"),
        ("s2_concept_c.png", "領域ごとの図", "テーブルの親子関係を描いた概念データモデル"),
        ("s2_def_c.png", "84テーブル", "786項目の型・キー・参照先まで定めたデータ定義書")]):
    x = X0 + k * (FW4 + 0.22)
    framed(img, x, TOP + 0.6, FW4, 2.9, line=DG if k == 1 else None)
    label(x, TOP + 3.65, FW4, 0.55, [(big, True, 24, DG)])
    label(x, TOP + 4.2, FW4, 0.9, [cap], size=14)

# ---------------------------------------------------------------- 8 成果物の実物（段階4・5）：大きな画面と2つの小さな画面
d.slide("データ定義書から生成した器の上に、判断に必要な形の業務画面を業務の単位で作り、その画面を使って1件1ページの説明資料まで作成",
        "7｜成果物の実物（段階4・5）")
RX0 = X0 + 7.35
pill(X0, TOP, XE - X0, 4, "試作アプリ（業務画面）", fill=DG)
framed("s4_project.png", X0, TOP + 0.55, 7.0, 4.0, line=DG)
label(X0, TOP + 4.65, 7.0, 0.5, [[("9画面", True, 26, DG), ("　定義書から生成した器の上に、業務の単位で作成", False, 14, TXT)]], anchor=M)
framed("s4_review.png", RX0, TOP + 0.55, 2.85, 1.75)
label(RX0 + 3.0, TOP + 0.6, XE - RX0 - 3.0, 1.7, [("判断が必要な事項", True, 16, DG), "見直し候補の自動抽出と推奨"], size=14, anchor=M)
pill(RX0, TOP + 2.6, XE - RX0, 5, "資料")
framed("s5_dp.png", RX0, TOP + 3.15, 2.85, 1.75)
label(RX0 + 3.0, TOP + 3.2, XE - RX0 - 3.0, 1.7, [("1件1ページ", True, 20, DG), "データ → ロジック → 画面の順に説明"], size=14, anchor=M)

# ---------------------------------------------------------------- 7 立上げ：階段
d.slide("ひな型からリポジトリを作り、メンバー・環境・初期設定を整えたうえで、手順書の第1段階から AI に依頼する立上げの手順",
        "8｜プロジェクトの立上げ手順")
steps = [("リポジトリの作成", "「Use this template」で private のリポジトリ"),
         ("メンバーの追加", "チームに Write の権限。Copilot は各自のライセンス"),
         ("環境の準備", "clone・pip install・check_all.py の全 OK"),
         ("初期設定", "README とシステム名の変更"),
         ("AI への最初の依頼", "手順書の第1段階からの依頼"),
         ("サンプルの削除", "自分の定義書と画面の完成後")]
STW, BASE = (W - 5 * 0.06) / 6, 6.75
for k, (t, b) in enumerate(steps):
    x, h = X0 + k * (STW + 0.06), 1.0 + 0.4 * k
    focus = k == 4
    d.box(x, BASE - h, STW, h, [(str(k + 1), True, 28, WHITE if focus else G2)], fillc=DG if focus else LG, line=None,
          align=C, anchor=T, ins=(0, 0.08, 0, 0))
    label(x, BASE - h - 1.3, STW, 1.25, [(t, True, 16, DG), b], size=14)
bub = d.box(X0, TOP, 7.45, 0.85, [("「playbook に沿って、1. 事象と課題から始めたい。テーマは〜」", True, 16, WHITE)],
            fillc=G2, line=None, kind=MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT, align=C, ins=(0.2, 0.05, 0.2, 0.05))
bub.adjustments[0], bub.adjustments[1] = 0.6, 0.85

# ---------------------------------------------------------------- 10・11 依頼の型：段階ごとの依頼文と、伝えること
PROMPTS = [
    (1, "事象と課題", "「playbook の『1. 事象と課題』で進めたい。テーマは〈テーマ〉、対象は〈業務・組織〉。気づいていない事象の候補を領域ごとに出してほしい。起きているかは私が答える。To-Be像にはまだ進まないで」",
     ["対象の範囲", "候補を出させ、人が答える", "先に進ませない"]),
    (2, "To-Be像", "「私が実現したいことは〈実現したいこと〉。合意した課題と目指す姿を突き合わせて、領域ごとの To-Be像を『どの判断を、どのデータで、どう自動化するか』の形で書いて。データモデルにはまだ進まないで」",
     ["実現したいこと（人が示す）", "判断・データ・自動化の形", "先に進ませない"]),
    (3, "データモデル", "「合意した To-Be像から、データ定義書のテーブル一覧を作って。各テーブルに層・1行の単位・正とする所を書き、項目はキーだけでよい。definition.py check で誤り0件にしてから見せて」",
     ["テーブル単位から", "書いてほしい欄", "確認方法"]),
    (4, "試作アプリ", "「定義書から器を作ったうえで、〈業務〉で〈誰〉が〈何〉を判断する画面を作りたい。まず画面一覧（使う人・場面・判断）を出して。画面には問い・診断・原因・推奨を置き、判定が出るダミーデータも作って。定義書に無いデータは仮置きして一覧にして」",
     ["判断する人と判断", "画面一覧を先に", "不足の一覧"]),
    (5, "資料", "「〈会議〉は〈イメージ合わせ〉の段階。rules の資料の書き方を全部読んでから、各ページのリード文だけの構成案を先に出して。体裁は docs の〈テンプレート〉に合わせ、作ったら全ページを PNG で確かめて」",
     ["会議の段階", "構成案を先に", "体裁と確認方法"]),
]


def runs_with_slots(text):
    """〈〉の差し替える部分だけを緑の太字にした文字の連なり"""
    out = []
    for part in re.split(r"(〈[^〉]+〉)", text):
        if part:
            out.append((part, part.startswith("〈"), 14, G2 if part.startswith("〈") else TXT))
    return [out]


def prompt_row(y, n, name, text, points, h=1.4):
    d.box(X0, y + h / 2 - 0.23, 1.75, 0.46, [(f"{n}  {name}", True, 14, WHITE)], fillc=G2, line=None,
          kind=MSO_SHAPE.ROUNDED_RECTANGLE, ins=(0.15, 0, 0.08, 0), round_adj=0.5)
    b = d.box(2.5, y, 6.75, h, runs_with_slots(text), fillc=WHITE, line=G2, lw=1.5, kind=MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT,
              anchor=M, ins=(0.18, 0.06, 0.15, 0.06))
    b.adjustments[0], b.adjustments[1] = -0.54, 0.0
    for j, t in enumerate(points):
        yy = y + 0.12 + j * 0.42
        i_check(9.62, yy + 0.17, 0.55)
        label(9.9, yy, XE - 9.9, 0.38, [(t, True, 14, DG)], anchor=M)


def prompt_header():
    icon_in_circle(i_person, 2.85, TOP + 0.22, 0.46, 0.42)
    label(3.2, TOP, 4.0, 0.45, [[("依頼の例", True, 14, DG), ("（〈〉は差し替える部分）", False, 14, NOTE)]], anchor=M)
    label(9.45, TOP, 3.0, 0.45, [("伝えること", True, 14, DG)], anchor=M)


d.slide("段階ごとに範囲・成果物の単位・確認方法・止める所を伝える依頼の型で、AI の先走りと手戻りを防止",
        "9｜AI への依頼の型（段階1〜3）")
prompt_header()
for k, (n, name, text, pts) in enumerate(PROMPTS[:3]):
    prompt_row(TOP + 0.6 + k * 1.58, n, name, text, pts)

d.slide("試作アプリは判断する人と判断から、資料は会議の段階から頼み、どの段階でもルールの読み込みと結果の原文での報告を添える依頼の型",
        "10｜AI への依頼の型（段階4・5と共通の一言）")
prompt_header()
for k, (n, name, text, pts) in enumerate(PROMPTS[3:]):
    prompt_row(TOP + 0.6 + k * 1.58, n, name, text, pts)
d.box(X0, TOP + 3.85, W, 1.25, None, fillc=DG, line=None)
label(X0 + 0.2, TOP + 3.85, 2.3, 1.25, [("どの段階でも", True, 16, WHITE), ("添える一言", True, 16, WHITE)], anchor=M)
CW3 = (W - 2.6 - 2 * 0.2) / 3
for j, t in enumerate([["「作業の前に rules/README.md と", "関係するルールを読んで」"], ["「終わったら check_all.py の結果を", "そのまま報告して」"],
                       ["「今の指摘を、理由つきで", "rules/ に書いて」"]]):
    d.box(X0 + 2.5 + j * (CW3 + 0.2), TOP + 4.0, CW3, 0.95, [(x, True, 14, DG) for x in t], fillc=WHITE, line=None, anchor=M, align=C,
          ins=(0.12, 0.04, 0.12, 0.04))

# ---------------------------------------------------------------- 8 役割分担：左右対称
d.slide("業務の判断は人が決め、作成と確認は AI が担う役割分担により、AI のもっともらしい決定による手戻りを防止",
        "11｜人と AI の役割分担")
MX, MW = 5.4, 2.5
icon_in_circle(i_person, 4.6, 2.3, 0.95, 0.9)
label(X0, 2.0, 3.55, 0.6, [("人：決める", True, 24, DG)], align=R, anchor=M)
icon_in_circle(i_ai, 8.7, 2.3, 0.95, 0.85)
label(9.3, 2.0, 3.5, 0.6, [("AI：作る・確かめる", True, 24, G2)], anchor=M)
rows = [("事象と課題", "事象の有無の回答、課題と判断の合意", "事象の候補の提示、目指す姿の仮置き"),
        ("To-Be像", "実現したいことの提示、To-Be像の合意", "To-Be像の案の作成、目指す姿との突き合わせ"),
        ("データモデル", "テーブルの切り方・1行の単位・正とする所", "定義書の作成・点検"),
        ("試作アプリ", "画面一覧・閾値・判断の読み取りやすさ", "器の生成、計算・画面・ダミーデータの実装"),
        ("資料", "会議の段階・ページ構成・色の使用", "スクリプトでの作成、PNG での確認"),
        ("全段階", "削除・外部送信の可否、指摘", "確認結果の原文での報告、指摘のルール化")]
for k, (st, h_, a_) in enumerate(rows):
    y = 3.1 + k * 0.62
    d.line((X0, y + 0.59), (XE, y + 0.59), color=LG, width=1)
    d.box(MX, y + 0.06, MW, 0.46, [(st, True, 14, WHITE)], fillc=G2, line=None, kind=MSO_SHAPE.ROUNDED_RECTANGLE, align=C,
          ins=(0, 0, 0, 0), round_adj=0.5)
    label(X0, y, MX - X0 - 0.2, 0.58, [h_], size=14, align=R, anchor=M)
    label(MX + MW + 0.2, y, XE - MX - MW - 0.2, 0.58, [a_], size=14, anchor=M)

# ---------------------------------------------------------------- 9 品質：ロードマップに点検の印
d.slide("AI の出来を左右するのは人のレビューであり、段階の飛ばし・単位の曖昧さ・判断の丸投げ・確認の省略を止める6つの点検ポイント",
        "12｜品質を守るために人が押さえるポイント")
RY = 2.75
rx = [1.6 + k * 2.4 for k in range(5)]
d.line((rx[0], RY), (rx[-1], RY), color=BG, width=4)
for k, name in enumerate(["事象と課題", "To-Be像", "データモデル", "試作アプリ", "資料"]):
    circle(rx[k], RY, 0.42, G2)
    label(rx[k] - 1.1, RY + 0.28, 2.2, 0.4, [(name, True, 14, G2)], align=C)
for n, px in [(1, (rx[1] + rx[2]) / 2), (2, rx[2]), (5, rx[3] - 0.45), (3, rx[3] + 0.45)]:
    d.line((px, 2.25), (px, RY - 0.2), color=DG, width=2)
    num(px, 2.0, n, 0.52, DG)
d.line((rx[0], 3.55), (rx[-1], 3.55), color=DG, width=2)
for xx in (rx[0], rx[-1]):
    d.line((xx, 3.4), (xx, 3.55), color=DG, width=2)
num(rx[2] - 0.35, 3.55, 4, 0.48, DG)
num(rx[2] + 0.35, 3.55, 6, 0.48, DG)
label(rx[2] + 0.7, 3.6, 1.5, 0.4, [("全段階", True, 14, DG)], anchor=M)
pts = [("段階の飛ばしの禁止", "課題と To-Be像の合意前にデータモデルに着手させない"),
       ("単位と正とする所の確認", "二重計上と、正とする値をめぐる対立の防止"),
       ("判定・閾値・色の人による決定", "AI の仮置きの値をそのまま採用しない"),
       ("確認結果の原文での報告", "NG の放置と「OK」への言い換えの確認"),
       ("定義書を正とする変更", "アプリだけで辻褄を合わせた変更の差し戻し"),
       ("指摘のルール化", "指摘と理由を rules/ に記録させ、索引を確認")]
for k, (t, b) in enumerate(pts):
    x, y = X0 + (k // 3) * 6.25, 4.15 + (k % 3) * 0.9
    num(x + 0.27, y + 0.4, k + 1, 0.5, DG)
    label(x + 0.7, y, 5.4, 0.85, [(t, True, 16, DG), b], size=14, anchor=M)

# ---------------------------------------------------------------- 10 運用：循環
d.slide("依頼から確認・レビュー・ルール化までを1回の作業の単位として回し、指摘をルールに蓄積してひな型ごと育てる運用",
        "13｜作業の回し方とチームでの運用")
CCX, CCY, RX_, RY_ = 3.55, 4.35, 2.15, 1.85
circle(CCX, CCY, 2.0, PALE)
label(CCX - 1.0, CCY - 0.4, 2.0, 0.8, [("1回の", True, 18, DG), ("作業", True, 18, DG)], align=C, anchor=M)
cyc = ["作業の依頼", "ルールの読込", "AI による作成", "check_all.py", "結果の報告", "レビュー・ルール化"]
pos = [(CCX + RX_ * math.cos(math.radians(-90 + k * 60)), CCY + RY_ * math.sin(math.radians(-90 + k * 60))) for k in range(6)]
for k in range(6):
    (x1, y1), (x2, y2) = pos[k], pos[(k + 1) % 6]
    dx, dy = x2 - x1, y2 - y1
    ln = math.hypot(dx, dy)
    arrow((x1 + dx / ln * 0.75, y1 + dy / ln * 0.42), (x2 - dx / ln * 0.75, y2 - dy / ln * 0.42), width=2.25)
for k, t in enumerate(cyc):
    x, y = pos[k]
    focus = k == 5
    d.box(x - 0.98, y - 0.3, 1.96, 0.6, [(t, focus, 14, WHITE if focus else TXT)], fillc=DG if focus else LG, line=None,
          kind=MSO_SHAPE.ROUNDED_RECTANGLE, align=C, ins=(0.04, 0, 0.04, 0), round_adj=0.5)
label(7.2, TOP + 0.05, 5.6, 0.45, [("チームでの運用", True, 18, DG)])
for k, (fn, t, b) in enumerate([
        (i_sync, "作業の前の Pull、直後の Push", "同じファイルの同時編集の衝突を防止"),
        (i_sheet, "Excel・pptx の同時編集の回避", "変更を混ぜられないため、担当者を決めてから編集"),
        (i_doc, "ひな型への還元", "汎用的な指摘と道具の改良をひな型に反映")]):
    y = 2.55 + k * 1.45
    icon_in_circle(fn, 7.65, y + 0.5, 0.95, 0.9)
    label(8.35, y, 4.45, 1.1, [(t, True, 16, DG), b], size=14, anchor=M)

# ---------------------------------------------------------------- 14 指摘がルールになった実例：吹き出し → rules/ の帯
d.slide("ユーザーの指摘を理由つきで rules/ に記録し、次の作業からはどの AI も同じ指摘を受けずに済む、指摘がルールになった実例",
        "14｜指摘がルールになった実例")
QW4 = (W - 3 * 0.25) / 4
quotes = [("「K1とかK2とかってなんですっけ、意味がないなら消して」", "説明資料の文章 9", "内部の番号・対応づけの注記を出さない"),
          ("「全体的にフォントサイズが小さくなってきている」", "pptx の体裁 2", "本文は14pt を基本にし、収まらなければ折り返す"),
          ("「いかにもAI感が出る」", "説明資料の文章 7", "ページ下部の注記・補足の一文を入れない"),
          ("「どこに注目すべきなのか、ぱっと視覚的に理解できるか」", "pptx の体裁 9", "ページごとに図の形を変え、注目点を1つ作る")]
label(X0, TOP, 3.0, 0.4, [("ユーザーの指摘", True, 16, DG)])
for k, (q, rule, body) in enumerate(quotes):
    x = X0 + k * (QW4 + 0.25)
    b = d.box(x, TOP + 0.45, QW4, 1.2, [(q, True, 15, DG)], fillc=LG, line=None, kind=MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT,
              align=C, anchor=M, ins=(0.15, 0.05, 0.15, 0.05))
    b.adjustments[0], b.adjustments[1] = 0.0, 0.75
    arrow((x + QW4 / 2, TOP + 2.0), (x + QW4 / 2, TOP + 2.45), color=DG, width=2.5)
d.box(X0, TOP + 2.5, W, 1.75, None, fillc=DG, line=None)
label(X0 + 0.2, TOP + 2.55, 4.0, 0.4, [("rules/ に記録（理由つき）", True, 15, WHITE)])
for k, (q, rule, body) in enumerate(quotes):
    x = X0 + k * (QW4 + 0.25)
    d.box(x + 0.12, TOP + 3.0, QW4 - 0.24, 1.1, [(rule, True, 14, DG), (body, False, 14, TXT)], fillc=WHITE, line=None,
          anchor=M, ins=(0.12, 0.04, 0.1, 0.04))
for k in range(3):
    i_ai(X0 + 0.45 + k * 0.85, TOP + 4.85, 0.75)
label(X0 + 2.75, TOP + 4.5, W - 2.75, 0.7, [("次の作業から、どの AI も同じルールで作成", True, 20, DG)], anchor=M)

OUT.parent.mkdir(exist_ok=True)
d.save(str(OUT))
print(f"作った：{OUT}（{len(d.prs.slides)} ページ）")
