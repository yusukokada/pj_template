"""pptx の資料を作る部品。体裁のルールは rules/pptx-format.md。

  from deck_lib import *
  d = Deck("フッターの文字", template="docs/テンプレート.pptx")   # template を省くと白紙の 16:9
  d.slide("リード文（体言止め・2行まで）", "小見出し")
  d.box(0.6, 1.7, 4, 1.2, ["本文 14pt"], size=14)
  d.save("docs/【資料】…_v0.1.pptx")

会社・顧客のテンプレートがあれば docs/ に置き、template と layout に名前を渡す。
色は下の定数で決める（既定は紺・グレー。見た目重視の資料はテンプレートの色に替える）。"""
import re
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

G1 = RGBColor(0x5B, 0x7F, 0xC7)   # 線・強調の薄い色
G2 = RGBColor(0x01, 0x21, 0x69)   # 見出しの色（紺）
G3 = RGBColor(0x01, 0x21, 0x69)   # 表の見出し行・線（紺）
LG = RGBColor(0xE8, 0xED, 0xF6)   # 薄い塗り
PG = RGBColor(0xF5, 0xF7, 0xFB)   # さらに薄い塗り
GRAY = RGBColor(0x75, 0x78, 0x7B)
LGRAY = RGBColor(0xD0, 0xD0, 0xCE)
TXT = RGBColor(0x22, 0x22, 0x22)
NOTE = RGBColor(0x66, 0x66, 0x66)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
JA = re.compile(r"[\u3000-\u30ff\u3400-\u9fff\uff00-\uffef]")
X0, XE = 0.52, 12.81
W = XE - X0


class Deck:
    def __init__(self, foot, template=None, layout=None):
        """template：テンプレートの pptx（中のスライドは消して、レイアウトだけ使う）。layout：使うレイアウトの名前"""
        self.prs = Presentation(template) if template else Presentation()
        self.blank = not template
        if self.blank:
            self.prs.slide_width, self.prs.slide_height = Inches(13.333), Inches(7.5)
        sl = self.prs.slides._sldIdLst
        for sid in list(sl):
            self.prs.part.drop_rel(sid.rId)
            sl.remove(sid)
        self.lay = {l.name: l for l in self.prs.slide_layouts}
        self.layout = layout or ("Title Only" if "Title Only" in self.lay else list(self.lay)[0])
        self.foot = foot
        self.s = None
        self.page = 0

    # ---------------- 文字
    @staticmethod
    def style_run(r, size, bold=False, color=TXT):
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
        rPr = r._r.get_or_add_rPr()
        if JA.search(r.text):
            rPr.set("lang", "ja-JP")
            rPr.set("altLang", "en-US")
        else:
            rPr.set("lang", "en-US")
            rPr.set("altLang", "ja-JP")
            rPr.set("noProof", "1")
        rPr.set("dirty", "0")

    def fill(self, tf, paras, size=12, color=TXT, align=PP_ALIGN.LEFT, spacing=None, after=0):
        """paras：各段落＝文字列 / (文字列, 太字[, 大きさ, 色]) / それらのリスト（1段落内の複数の連なり）"""
        tf.clear()
        for i, p in enumerate(paras):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = align
            if spacing:
                para.line_spacing = spacing
            if after:
                para.space_after = Pt(after)
            runs = p if isinstance(p, list) else [p]
            for r_ in runs:
                if isinstance(r_, str):
                    r_ = (r_, False)
                t, b = r_[0], r_[1]
                sz = r_[2] if len(r_) > 2 else size
                col = r_[3] if len(r_) > 3 else color
                if not t:
                    continue
                r = para.add_run()
                r.text = t
                self.style_run(r, sz, b, col)

    @staticmethod
    def insets(tf, l=0.06, r=0.04, t=0.02, b=0.02):
        tf.margin_left, tf.margin_right, tf.margin_top, tf.margin_bottom = Inches(l), Inches(r), Inches(t), Inches(b)
        tf.word_wrap = True

    def text(self, x, y, w, h, paras, size=12, color=TXT, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, after=0, spacing=None):
        t = self.s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = t.text_frame
        self.insets(tf, 0.04, 0.04, 0.0, 0.0)
        tf.vertical_anchor = anchor
        self.fill(tf, paras, size, color, align, spacing, after)
        return t

    # ---------------- 図形
    def box(self, x, y, w, h, paras=None, fillc=WHITE, line=GRAY, lw=1.0, size=12, color=TXT, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE,
            kind=MSO_SHAPE.RECTANGLE, dashed=False, ins=(0.08, 0.06, 0.04, 0.04), after=0, round_adj=0.06):
        sh = self.s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
        if fillc is None:
            sh.fill.background()
        else:
            sh.fill.solid()
            sh.fill.fore_color.rgb = fillc
        if line is None:
            sh.line.fill.background()
        else:
            sh.line.color.rgb = line
            sh.line.width = Pt(lw)
            if dashed:
                sh.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        sh.shadow.inherit = False
        if kind == MSO_SHAPE.ROUNDED_RECTANGLE:
            sh.adjustments[0] = round_adj
        if paras:
            tf = sh.text_frame
            self.insets(tf, *ins)
            tf.vertical_anchor = anchor
            self.fill(tf, paras, size, color, align, after=after)
        return sh

    def line(self, p, q, color=G3, width=1.0, dashed=False, arrow=False, head=False):
        c = self.s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(p[0]), Inches(p[1]), Inches(q[0]), Inches(q[1]))
        c.line.color.rgb = color
        c.line.width = Pt(width)
        ln = c.line._get_or_add_ln()
        if dashed:
            etree.SubElement(ln, qn("a:prstDash")).set("val", "sysDash")
        if head:
            e = etree.SubElement(ln, qn("a:headEnd"))
            e.set("type", "triangle")
        if arrow:
            e = etree.SubElement(ln, qn("a:tailEnd"))
            e.set("type", "triangle")
            e.set("w", "med")
            e.set("len", "med")
        return c

    def polyline(self, points, color=G3, width=3.0, dashed=False):
        E = 914400
        fb = self.s.shapes.build_freeform(int(points[0][0] * E), int(points[0][1] * E), scale=1.0)
        fb.add_line_segments([(int(x * E), int(y * E)) for x, y in points[1:]], close=False)
        sh = fb.convert_to_shape()
        sh.fill.background()
        sh.line.color.rgb = color
        sh.line.width = Pt(width)
        sh.shadow.inherit = False
        if dashed:
            etree.SubElement(sh.line._get_or_add_ln(), qn("a:prstDash")).set("val", "dash")
        return sh

    def heading(self, x, y, w, label, color=G2, size=14, rule=True):
        """小見出し（緑の文字と下線）"""
        self.text(x, y, w, 0.3, [(label, True, size, color)], anchor=MSO_ANCHOR.BOTTOM)
        if rule:
            self.line((x, y + 0.33), (x + w, y + 0.33), color=G1, width=1.5)

    # ---------------- 表
    def table(self, x, y, widths, rows, header=True, size=12, row_h=0.3, head_fill=G3, first_col_fill=None, first_col_bold=True, valign=MSO_ANCHOR.MIDDLE,
              heights=None, zebra=False, align_cols=None):
        nr, nc = len(rows), len(widths)
        gs = self.s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(sum(widths)), Inches(row_h * nr))
        tbl = gs.table
        tblPr = tbl._tbl.tblPr
        for k in list(tblPr):
            if k.tag == qn("a:tableStyleId"):
                tblPr.remove(k)
        tblPr.set("firstRow", "0")
        tblPr.set("bandRow", "0")
        for j, wd in enumerate(widths):
            tbl.columns[j].width = Inches(wd)
        for i in range(nr):
            tbl.rows[i].height = Inches((heights[i] if heights else row_h))
            for j in range(nc):
                c = tbl.cell(i, j)
                v = rows[i][j]
                is_head = header and i == 0
                c.fill.solid()
                if is_head:
                    c.fill.fore_color.rgb = head_fill
                elif first_col_fill is not None and j == 0:
                    c.fill.fore_color.rgb = first_col_fill
                elif zebra and i % 2 == 0:
                    c.fill.fore_color.rgb = PG
                else:
                    c.fill.fore_color.rgb = WHITE
                c.margin_left = c.margin_right = Inches(0.06)
                c.margin_top = c.margin_bottom = Inches(0.03)
                c.vertical_anchor = valign
                tf = c.text_frame
                tf.word_wrap = True
                paras = v if isinstance(v, list) else [v if v is not None else ""]
                al = PP_ALIGN.CENTER if is_head else ((align_cols or {}).get(j, PP_ALIGN.LEFT))
                if is_head:
                    paras = [(p if isinstance(p, str) else p[0], True, size, WHITE) for p in paras]
                elif j == 0 and first_col_bold:
                    paras = [(p, True) if isinstance(p, str) else p for p in paras]
                self.fill(tf, paras, size, TXT, al)
                # 罫線（白地の表は薄いグレーの線）
                tcPr = c._tc.get_or_add_tcPr()
                for k_, tag in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
                    ln = etree.Element(qn(tag))
                    tcPr.insert(k_, ln)
                    ln.set("w", "9525")
                    sf = etree.SubElement(ln, qn("a:solidFill"))
                    etree.SubElement(sf, qn("a:srgbClr")).set("val", "D0D0CE")
        return gs

    # ---------------- スライド
    def slide(self, title, sub=None, layout=None, title_size=20, sub_idx=15):
        """title：リード文。sub：小見出し（テンプレートに idx=sub_idx の枠があればそこへ、なければ文字の箱で置く）"""
        self.s = self.prs.slides.add_slide(self.lay[layout or self.layout])
        self.page += 1
        placed = False
        for ph in list(self.s.placeholders):
            idx = ph.placeholder_format.idx
            if idx == 0:
                if self.blank:   # 白紙のときだけ位置を決める。テンプレートの位置は動かさない
                    ph.left, ph.top, ph.width, ph.height = Inches(X0), Inches(0.3), Inches(W), Inches(0.8)
                self.fill(ph.text_frame, [(title, True)], size=title_size)
            elif idx == sub_idx:
                placed = True
                if sub:   # 文字だけを入れ、書式（緑・18pt・太字）はスライドマスタのプレースホルダーのものを使う
                    tf = ph.text_frame
                    tf.clear()
                    r = tf.paragraphs[0].add_run()
                    r.text = sub
                    rPr = r._r.get_or_add_rPr()
                    rPr.set("lang", "ja-JP"); rPr.set("altLang", "en-US"); rPr.set("dirty", "0")
                else:
                    ph._element.getparent().remove(ph._element)
            else:
                ph._element.getparent().remove(ph._element)
        if sub and not placed:
            self.text(X0, 1.22, W, 0.4, [(sub, True, 18, G2)])
        for x, w, t in [(0.80, 7.0, self.foot), (0.42, 0.40, str(self.page))]:
            tb = self.s.shapes.add_textbox(Inches(x), Inches(7.2), Inches(w), Inches(0.19))
            tf = tb.text_frame
            self.insets(tf, 0.06, 0.06, 0.04, 0)
            self.fill(tf, [(t, False)], size=9, color=NOTE)
        return self.s

    def save(self, path):
        self.prs.save(path)
