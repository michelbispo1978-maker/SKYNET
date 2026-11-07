import pathlib, re, subprocess

html_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\Index.html")
subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $false"])
html = html_p.read_text(encoding="utf-8")

trava_js = '''
<script>
// Trava anti-eco: impede o navegador de falar enquanto ja existe fala ativa ou comando do robo 8080
(function() {
  if ('speechSynthesis' in window) {
    const origSpeak = window.speechSynthesis.speak.bind(window.speechSynthesis);
    window.speechSynthesis.speak = function(utterance) {
      if (window.speechSynthesis.speaking || window.speechSynthesis.pending) {
        window.speechSynthesis.cancel();
      }
      setTimeout(() => origSpeak(utterance), 150);
    };
  }
})();
</script>
</body>'''

if "Trava anti-eco" not in html:
    html = re.sub(r'</body>', trava_js, html, count=1, flags=re.I)
    html_p.write_text(html, encoding="utf-8")
    print("[OK] Trava anti-eco aplicada no Index.html!")

subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $true"])
