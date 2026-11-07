import pathlib, re, subprocess

html_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\Index.html")
subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $false"])
html = html_p.read_text(encoding="utf-8")

# Remove travas antigas e aplica uma trava sincronizada com o /falando
html = re.sub(r'<script>\s*// Trava anti-eco:.*?</script>\s*', '', html, flags=re.S)

trava_sincronizada = '''
<script>
// Trava Mestre de Voz: impede dupla fala entre Navegador e Robo Windows 8080
(function() {
  window._skynetRoboFalando = false;
  setInterval(async () => {
    try {
      const r = await fetch('http://localhost:8080/falando');
      if (r.ok) {
        const d = await r.json();
        window._skynetRoboFalando = !!d.falando;
        if (window._skynetRoboFalando && 'speechSynthesis' in window) {
          window.speechSynthesis.cancel();
        }
      }
    } catch (e) {}
  }, 250);

  if ('speechSynthesis' in window) {
    const origSpeak = window.speechSynthesis.speak.bind(window.speechSynthesis);
    window.speechSynthesis.speak = function(utterance) {
      if (window._skynetRoboFalando) {
        console.log('[SKYNET VOZ] Navegador silenciado: Robo Windows ja esta falando.');
        return;
      }
      window.speechSynthesis.cancel();
      setTimeout(() => {
        if (!window._skynetRoboFalando) origSpeak(utterance);
      }, 250);
    };
  }
})();
</script>
</body>'''

html = re.sub(r'</body>', trava_sincronizada, html, count=1, flags=re.I)
html_p.write_text(html, encoding="utf-8")
subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $true"])
print("[2/2] Trava Mestre de Voz aplicada no Index.html!")
