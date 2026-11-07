import pathlib, re, subprocess

html_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\Index.html")
subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $false"])
html = html_p.read_text(encoding="utf-8")

# 1. Remove a caixa flutuante antiga do canto superior direito
html = re.sub(r'<div id="skynet-robo-widget".*?</script>\s*', '', html, flags=re.S)

# 2. Injeta os botões nativos dentro do painel #pc-manager-actions da interface 66827
barra_nativa = '''<div id="pc-manager-actions"'''
script_nativo = '''
<script>
function skynetExecutarNativo(cmd) {
  const inp = document.getElementById('input');
  const btn = document.getElementById('send');
  if (inp && btn) {
    inp.value = cmd;
    btn.click();
  }
}
window.addEventListener('DOMContentLoaded', () => {
  const alvo = document.getElementById('pc-manager-actions') || document.body;
  const grp = document.createElement('div');
  grp.style.cssText = 'display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;padding-top:8px;border-top:1px solid rgba(0,240,255,0.25);';
  const acoes = [
    ['📊 Raio-X', 'raio-x'], ['💾 SSD', 'saude-ssd'], ['🧹 Limpar RAM', 'limpar-ram'],
    ['🚀 Otimizar', 'otimizar-windows'], ['⚡ Destravar', 'destravar-pc'], ['👁️ Ver Tela', 'ver-tela'],
    ['🛡️ Vigiar', 'vigiar-tela'], ['📋 Ler Ctrl+C', 'ler-area'], ['🧠 Memória', 'consultar-memoria'],
    ['🔑 Senha', 'gerar-senha'], ['📑 Relatório', 'gerar-relatorio'], ['🚨 Sirene', 'sirene'],
    ['☁️ GitHub', 'sincronizar-github'], ['❓ Ajuda', 'ajuda']
  ];
  acoes.forEach(([label, cmd]) => {
    const b = document.createElement('button');
    b.textContent = label;
    b.style.cssText = 'background:#0b192c;color:#00f0ff;border:1px solid #00838f;border-radius:4px;padding:4px 8px;cursor:pointer;font-size:11px;';
    b.onclick = () => skynetExecutarNativo(cmd);
    grp.appendChild(b);
  });
  alvo.appendChild(grp);
});
</script>
</body>'''

if "skynetExecutarNativo" not in html:
    html = re.sub(r'</body>', script_nativo, html, count=1, flags=re.I)
    html_p.write_text(html, encoding="utf-8")
    print("[OK] Botoes fundidos nativamente ao #pc-manager-actions da interface 66827!")

subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $true"])
