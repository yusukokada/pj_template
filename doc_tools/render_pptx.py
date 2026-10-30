"""pptx を PowerPoint（COM）で PNG に書き出す。見た目（文字あふれ・重なり）の確認用。
python doc_tools/render_pptx.py "docs/<ファイル名>.pptx" [ページ番号 ...]
出力：doc_tools/render/<ファイル名>/p01.png …（Git には入れない）"""
import os
import sys
from pathlib import Path

import pythoncom
import win32com.client as win32


def render(pptx, pages=(), width=1600, height=900):
    src = Path(pptx).resolve()
    out = Path(__file__).resolve().parent / "render" / src.stem
    out.mkdir(parents=True, exist_ok=True)
    pythoncom.CoInitialize()
    pp = win32.DispatchEx("PowerPoint.Application")
    made = []
    try:
        pr = pp.Presentations.Open(str(src), True, False, False)  # 読み取り専用・ウィンドウなし
        try:
            for i in pages or range(1, pr.Slides.Count + 1):
                f = out / f"p{i:02d}.png"
                pr.Slides(i).Export(str(f), "PNG", width, height)
                made.append(f)
        finally:
            pr.Close()
    finally:
        pp.Quit()
    return made


if __name__ == "__main__":
    files = render(sys.argv[1], [int(x) for x in sys.argv[2:]])
    print(f"{len(files)} ページを書き出した：{os.path.dirname(files[0]) if files else '-'}")
