import pathlib, re, subprocess

html_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\Index.html")
subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $false"])
html = html_p.read_text(encoding="utf-8")

escudo_mic = '''
<script>
// Escudo Anti-Auto-Escuta: ignora o microfone enquanto a Skynet (Web ou Windows) estiver falando
(function() {
  window._skynetRoboFalando = false;
  setInterval(async () => {
    try {
      const r = await fetch('http://localhost:8080/falando');
      const d = await r.json();
      window._skynetRoboFalando = !!d.falando;
    } catch (e) {
      window._skynetRoboFalando = false;
    }
  }, 400);

  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SR) {
    const origStart = SR.prototype.start;
    SR.prototype.start = function() {
      const rec = this;
      const origResult = rec.onresult;
      rec.onresult = function(ev) {
        if (window.speechSynthesis.speaking || window._skynetRoboFalando) {
          console.log('[SKYNET MIC] Ignorado: Skynet esta falando.');
          return;
        }
        if (origResult) origResult.apply(this, arguments);
      };
      return origStart.apply(this, arguments);
    };
  }
})();
</script>
</body>'''

if "Escudo Anti-Auto-Escuta" not in html:
    html = re.sub(r'</body>', escudo_mic, html, count=1, flags=re.I)
    html_p.write_text(html, encoding="utf-8")
    print("[OK] Escudo anti-auto-escuta aplicado ao microfone no Index.html!")

subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $true"])
