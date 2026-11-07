import pathlib
p = pathlib.Path("SKYNET-BACKEND-CORRIGIDO-V2.py")
txt = p.read_text(encoding="utf-8", errors="ignore")
old = 'return jsonify({"ok": True, "models": models, "default_model": models[0]["name"]})'
new = 'default_name = "michelbds:7870" if any(m.get("name")=="michelbds:7870" for m in models) else models[0]["name"]\n        return jsonify({"ok": True, "models": models, "default_model": default_name})'
txt = txt.replace(old, new)
p.write_text(txt, encoding="utf-8")
print("Fix default_model aplicado")
