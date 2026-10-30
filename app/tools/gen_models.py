"""データ定義書から、Django のアプリ（領域ごと）・モデル・管理画面を生成する。
python tools/gen_models.py [定義書.xlsx]   （省略すると docs/ の【データ定義書】を使う。1つだけ置く）

生成したアプリは直接編集しない。データ定義書を直して、tools/rebuild.py で作り直す。"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "doc_tools"))
from definition import check, load  # noqa: E402

CORE = ROOT / "core"
MARK = "# 自動生成（tools/gen_models.py）。直接編集しない。"


def definition_path(argv):
    if argv:
        return Path(argv[0])
    hit = sorted((ROOT.parent / "docs").glob("【データ定義書】*.xlsx"))
    hit = [p for p in hit if not p.name.startswith("~$")]
    assert len(hit) == 1, f"docs/ の【データ定義書】が {len(hit)} 件。1つだけ置くか、ファイルを指定する"
    return hit[0]


def ident(name, used):
    """項目名を Python の識別子にする（日本語は残し、記号だけ _ にする）。"""
    s = "".join(c if ("x" + c).isidentifier() else "_" for c in str(name))
    s = "_".join(p for p in s.split("_") if p) or "f"
    if s[0].isdigit():
        s = "f_" + s
    if s.lower() in ("pk", "id", "objects"):
        s += "_"
    base, n = s, 2
    while s in used:
        s, n = f"{base}{n}", n + 1
    used.add(s)
    return s


def choices(codes, kind):
    """「コード：表示名」→ (コード, 表示名)。DB にはコード、画面には表示名を出す。"""
    return [(v.partition("：")[0].strip()[:50], (v.partition("：")[2] or v).strip()) for v in codes.get(kind, [])]


def main(argv):
    src = definition_path(argv)
    d = load(src)
    err, _ = check(d)
    if err:
        raise SystemExit("データ定義書に誤りがある（python doc_tools/definition.py check で確かめる）：\n" + "\n".join(err))
    areas = {a["name"]: a for a in d["areas"]}
    T = {t["id"]: t for t in d["tables"]}
    app_of = {t["id"]: areas[t["area"]]["app"] for t in d["tables"]}

    # 前回生成したアプリのうち、今回の定義にないものを消す
    old = CORE / "apps.json"
    if old.exists():
        for a in json.loads(old.read_text(encoding="utf-8")):
            p = ROOT / a
            if a not in {x["app"] for x in d["areas"]} and (p / "apps.py").exists() and MARK in (p / "apps.py").read_text(encoding="utf-8"):
                shutil.rmtree(p)

    schema = {}
    for area in d["areas"]:
        app, tables = area["app"], [t for t in d["tables"] if t["area"] == area["name"]]
        p = ROOT / app
        (p / "migrations").mkdir(parents=True, exist_ok=True)
        (p / "migrations" / "__init__.py").touch()
        (p / "__init__.py").touch()
        (p / "apps.py").write_text(
            f"{MARK}\nfrom django.apps import AppConfig\n\n\n"
            f"class Config(AppConfig):\n    name = {app!r}\n    verbose_name = {area['label'] or area['name']!r}\n"
            "    default_auto_field = 'django.db.models.BigAutoField'\n", encoding="utf-8")
        m = [MARK, "from django.db import models", "", ""]
        a = [MARK, "from django.contrib import admin", "", "from core.admin_base import GeneratedAdmin",
             "from .models import *  # noqa", "", ""]
        for t in tables:
            single = sum("PK" in f["key"] for f in t["fields"]) == 1
            used, fdefs, uniq, listd, search, filt, meta = set(), [], [], [], [], [], []
            for f in t["fields"]:
                name, typ, ref = f["name"], f["type"], f["ref"]
                is_pk = "PK" in f["key"]
                fn = ident(name, used)
                opt = [f"verbose_name={name!r}", f"db_column={fn!r}"]
                if f["desc"]:
                    opt.append(f"help_text={str(f['desc']).replace(chr(10), ' ')[:300]!r}")
                null = [] if (f["required"] or is_pk) else ["null=True", "blank=True"]
                pk = ["primary_key=True"] if (is_pk and single) else []
                if ref:
                    target = f"'{app_of[ref]}.T{ref}'"
                    rn = f"related_name='{t['id']}_{fn}'"
                    if pk:
                        fd = f"models.OneToOneField({target}, on_delete=models.PROTECT, primary_key=True, {rn}, {', '.join(opt)})"
                    else:
                        fd = f"models.ForeignKey({target}, on_delete=models.PROTECT, {rn}, {', '.join(null + opt)})"
                    kind = "fk"
                elif typ in ("ID", "コード"):
                    fd, kind = f"models.CharField({', '.join(['max_length=50'] + pk + null + opt)})", "str"
                elif typ == "文字":
                    fd, kind = f"models.CharField({', '.join(['max_length=500'] + pk + null + opt)})", "str"
                elif typ == "区分":
                    chs = choices(d["codes"], f["code"] or name)
                    co = [f"choices={chs!r}"] if chs else []
                    fd, kind = f"models.CharField({', '.join(['max_length=50'] + co + pk + null + opt)})", ("choice" if chs else "cat")
                elif typ == "年月":
                    fd, kind = f"models.CharField({', '.join(['max_length=7'] + pk + null + opt)})", "ym"
                elif typ == "フラグ":
                    fd, kind = f"models.BooleanField({', '.join(['default=False'] + opt)})", "bool"
                else:
                    cls, kind = {"数値": ("FloatField", "num"), "比率": ("FloatField", "ratio"), "金額": ("BigIntegerField", "money"),
                                 "日付": ("DateField", "date"), "日時": ("DateTimeField", "dt")}[typ]
                    fd = f"models.{cls}({', '.join(pk + null + opt)})"
                fdefs.append(f"    {fn} = {fd}")
                if is_pk:
                    uniq.append(fn)
                if kind == "str":
                    search.append(fn)
                if kind in ("choice", "bool"):
                    filt.append(fn)
                if len(listd) < 7:
                    listd.append(fn)
                meta.append(dict(field=fn, name=name, type=typ, key=f["key"], ref=ref or None,
                                 required=bool(f["required"]), source=f["source"], kind=kind))
            pkf = [x for x in meta if "PK" in x["key"]]
            title = next((x["field"] for x in meta if x["type"] == "文字" and "名" in x["name"]), None)
            strexpr = " / ".join("{self.%s%s}" % (x["field"], "_id" if x["ref"] else "") for x in pkf)
            if title:
                strexpr += " {self.%s}" % title
            m += [f"class T{t['id']}(models.Model):",
                  f"    \"\"\"{t['id']} {t['name']}｜1行＝{t['unit']}｜正とする所：{t['home']}\"\"\"",
                  *fdefs, "", "    class Meta:",
                  f"        db_table = '{t['id'].lower()}'",
                  f"        verbose_name = verbose_name_plural = '{t['id']} {t['name']}'"]
            if not single:
                m.append(f"        constraints = [models.UniqueConstraint(fields={uniq!r}, name='uq_{t['id'].lower()}')]")
            m += ["", "    def __str__(self):", f"        return f\"{strexpr}\"", "", ""]
            a += [f"@admin.register(T{t['id']})", f"class T{t['id']}Admin(GeneratedAdmin):",
                  f"    list_display = {listd!r}", f"    search_fields = {search[:6]!r}",
                  f"    list_filter = {filt[:5]!r}", f"    derived = {t['layer'] == '導出'!r}", "", ""]
            schema[t["id"]] = dict(app=app, model=f"T{t['id']}", name=t["name"], layer=t["layer"], area=t["area"],
                                   single_pk=single, fields=meta)
        (p / "models.py").write_text("\n".join(m), encoding="utf-8")
        (p / "admin.py").write_text("\n".join(a), encoding="utf-8")

    (CORE / "schema.json").write_text(json.dumps(schema, ensure_ascii=False, indent=1), encoding="utf-8")
    (CORE / "codes.json").write_text(json.dumps(d["codes"], ensure_ascii=False, indent=1), encoding="utf-8")
    (CORE / "apps.json").write_text(json.dumps([x["app"] for x in d["areas"]], ensure_ascii=False), encoding="utf-8")
    (CORE / "source.txt").write_text(src.name + "\n", encoding="utf-8")
    print(f"{src.name}：{len(d['areas'])} 領域・{len(schema)} テーブル・{sum(len(v['fields']) for v in schema.values())} 項目を生成した")


if __name__ == "__main__":
    main(sys.argv[1:])
