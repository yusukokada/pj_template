"""資料を作る環境の確認。docs/ のファイルは書き換えない。
python doc_tools/check_env.py
結果は画面と doc_tools/render/check_env.txt に出す。"""
import importlib
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
DOCS = HERE.parent / "docs"
OUT = HERE / "render"
OUT.mkdir(exist_ok=True)
log = []


def step(name):
    def wrap(fn):
        try:
            log.append(f"OK  {name}：{fn()}")
        except Exception as e:
            log.append(f"NG  {name}：{type(e).__name__}: {e}")
            log.append("    " + traceback.format_exc().strip().splitlines()[-1])
        return fn
    return wrap


@step("ライブラリ")
def _():
    v = []
    for m in ("pptx", "openpyxl", "lxml", "win32com"):
        mod = importlib.import_module(m)
        v.append(f"{m} {getattr(mod, '__version__', '')}".strip())
    return "、".join(v)


@step("データ定義書を読んで点検する")
def _():
    from definition import check, load
    hit = [p for p in DOCS.glob("【データ定義書】*.xlsx") if not p.name.startswith("~$")]
    assert len(hit) == 1, f"docs/ の【データ定義書】が {len(hit)} 件（1つだけ置く）"
    d = load(hit[0])
    err, warn = check(d)
    assert not err, f"誤り {len(err)} 件（python doc_tools/definition.py check で中身を見る）"
    return f"{hit[0].name}：{len(d['tables'])} テーブル、気づき {len(warn)} 件"


@step("Excel（COM）を開いて閉じる")
def _():
    import pythoncom
    import win32com.client as win32
    pythoncom.CoInitialize()
    xl = win32.DispatchEx("Excel.Application")
    try:
        return f"Excel {xl.Version}"
    finally:
        xl.Quit()


@step("deck_lib で試しの1ページを作り、PowerPoint（COM）で PNG に書き出す")
def _():
    from deck_lib import Deck
    from render_pptx import render
    d = Deck("動作確認")
    d.slide("動作確認のページ", "deck_lib と PowerPoint の確認")
    d.text(0.6, 1.8, 12.0, 0.6, ["このページは doc_tools/check_env.py が作った"], size=14)
    f = OUT / "check_env.pptx"
    d.save(str(f))
    render(f, [1])
    return "doc_tools/render/check_env/p01.png"


if __name__ == "__main__":
    text = "\n".join(log)
    (OUT / "check_env.txt").write_text(text + "\n", encoding="utf-8")
    print(text)
    sys.exit(1 if any(x.startswith("NG") for x in log) else 0)
