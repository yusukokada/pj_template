"""画面の文言の点検：業務画面の文字を洗い、動詞で終わる文・あいまい語・比喩を出す（rules/business-doc-writing.md）。
python tools/audit_wording.py   （見つかったものを出すだけ。直すかどうかは文脈で決める）"""
import re
from html.parser import HTMLParser

from pages import setup, work_urls

c = setup()

VERB_END = re.compile(r"(する|できる|ている|ていない|られる|れる|しない|ない|た|だ|う|く|ぐ|す|つ|ぬ|ぶ|む|る)[。]?$")
BANNED = ["扱い", "適切", "効率的", "推進", "強化", "徹底", "重心", "主体性", "実質", "見直す", "回す", "積み上が", "圧迫", "言い値"]
OK_END = ("ない（", "なし", "以内", "以下", "以上")


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, a):
        if tag in ("script", "style"):
            self.skip += 1
        self.out += [v for k, v in a if k in ("title", "placeholder") and v]

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, d):
        if not self.skip and d.strip():
            self.out.append(d.strip())


hits = {}
for u in work_urls():
    t = Text()
    t.feed(c.get(u).content.decode("utf-8"))
    for s in t.out:
        if not re.search(r"[ぁ-んァ-ン一-龥]", s):
            continue
        for piece in s.split("。"):
            p = piece.strip().rstrip("）)」 ")
            if len(p) >= 6 and VERB_END.search(p) and not p.endswith(OK_END):
                hits.setdefault(("動詞で終わる", piece.strip()), u)
        for b in BANNED:
            if b in s:
                hits.setdefault((b, s[:80]), u)
for (k, s), u in sorted(hits.items()):
    print(f"[{k}] {s}   <{u}>")
print(f"{len(hits)} 件")
