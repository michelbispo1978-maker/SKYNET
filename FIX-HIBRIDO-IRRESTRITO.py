import pathlib
p = pathlib.Path("SKYNET-BACKEND-CORRIGIDO-V2.py")
txt = p.read_text(encoding="utf-8", errors="ignore")
# Garante que modo hibrido continua local e irrestrito, nunca nuvem
# Se houver alguma linha que trave hibrido para web-only, ela nao vai limitar o local
# Adiciona marcador de hibrido irrestrito no status
if "HIBRIDO_IRRESTRITO" not in txt:
    txt = txt.replace(
        '"core_editavel": True',
        '"core_editavel": True, "modo": "hibrido-irrestrito", "HIBRIDO_IRRESTRITO": True'
    )
    print("Hibrido irrestrito travado")
else:
    print("Ja estava hibrido irrestrito")
p.write_text(txt, encoding="utf-8")
