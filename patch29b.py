import re
p = 'Index.html'
t = open(p, encoding='utf-8', errors='ignore').read()
antes = len(t)
# Tira o bloco div msg-assistant com a saudacao
t = re.sub(r'<div class="msg-assistant">Olá! Sou a <strong>SKYNET MICHELBDS</strong>.*?</div>', '', t, flags=re.DOTALL)
# Tira a outra variacao sem div
t = t.replace('Sou a SKYNET, sua assistente local integrada ao Ollama e às ferramentas autorizadas do Windows.<br><br>', '')
if len(t) != antes:
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH TIRA SAUDACAO 2 OK - 2 SAUDACOES REMOVIDAS')
else:
    print('NAO ACHOU SAUDACAO 2')
