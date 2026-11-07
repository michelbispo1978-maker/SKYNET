p = 'Index.html'
t = open(p, encoding='utf-8', errors='ignore').read()
t = t.replace('min-height:200px;max-height:38vh;', 'min-height:320px;max-height:55vh;font-size:13px;')
t = t.replace('.fr-sources{max-height:20vh;', '.fr-sources{max-height:35vh;min-height:200px;')
open(p, 'w', encoding='utf-8', errors='ignore').write(t)
print('PATCH LISTA HIBRIDA OK - FR-RESULTS 55vh, FR-SOURCES 35vh')
