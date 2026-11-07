p = 'Index.html'
t = open(p, encoding='utf-8', errors='ignore').read()
t = t.replace('min-height:320px;max-height:55vh;font-size:13px;', 'min-height:150px;max-height:30vh;font-size:13px;')
t = t.replace('max-height:35vh;min-height:200px;', 'max-height:50vh;min-height:300px;')
open(p, 'w', encoding='utf-8', errors='ignore').write(t)
print('PATCH INVERTEU - MEIO 30vh, BAIXO 50vh')
