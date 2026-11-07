p = 'Index.html'
t = open(p, encoding='utf-8', errors='ignore').read()
old = '#floating-research-panel{position:fixed;bottom:105px;right:28px;width:440px;max-width:calc(100vw - 20px);max-height:78vh;'
new = '#floating-research-panel{position:fixed;bottom:20px;right:20px;width:620px;max-width:calc(100vw - 20px);max-height:92vh;'
if old in t:
    t = t.replace(old, new)
    print('PATCH HIBRIDA TAMANHO OK')
else:
    print('NAO ACHOU CSS - ME MANDA LINHA 33')
open(p, 'w', encoding='utf-8', errors='ignore').write(t)
