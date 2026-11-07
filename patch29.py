import re
p = 'Index.html'
t = open(p, encoding='utf-8', errors='ignore').read()
# Tira a saudacao longa, deixa vazio
# Procura o bloco que começa com "Olá! Sou a SKYNET MICHELBDS"
antes = len(t)
# Remove o texto da saudacao, mantem o resto
t2 = re.sub(r"Olá! Sou a SKYNET MICHELBDS.*?(?=Exemplo:)", "", t, flags=re.DOTALL)
# Se nao achou com esse padrao, tenta remover so a primeira frase
if len(t2) == antes:
    t2 = t.replace("Olá! Sou a SKYNET MICHELBDS, sua assistente local no Windows, conectada ao Ollama pela porta 5000. 😊", "")
if len(t2) != antes:
    open(p, 'w', encoding='utf-8', errors='ignore').write(t2)
    print('PATCH TIRA SAUDACAO OK - SAUDACAO REMOVIDA')
else:
    print('NAO ACHOU SAUDACAO')
    for line in t.splitlines():
        if 'Sou a SKYNET' in line or 'assistente local' in line:
            print(repr(line[:300]))
