p = 'Index.html'
t = open(p, encoding='utf-8', errors='ignore').read()
old = "frRun.addEventListener('click',runFloating);"
new = "frRun.addEventListener('click',runFloating);\nfrQ.addEventListener('keydown',e=>{ if(e.key==='Enter'){ e.preventDefault(); runFloating(); } });"
if old in t and 'frQ.addEventListener' not in t:
    t = t.replace(old, new)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH ENTER HIBRIDA OK')
else:
    print('JA TEM ENTER OU NAO ACHOU')
