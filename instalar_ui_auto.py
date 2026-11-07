import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8-sig")

if "clicar-texto:" not in code:
    code = code.replace("abrir:", "abrir:|clicar-texto:|digitar-na-tela:|rotina:")
    bloco = '''        "^clicar-texto:\\s*(.+)" {
            $AlvoBtn = $Matches[1].Trim()
            Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes
            $Root = [System.Windows.Automation.AutomationElement]::RootElement
            $Cond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::NameProperty, $AlvoBtn)
            $Elem = $Root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $Cond)
            if ($Elem) {
                try { $Elem.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke(); return "UI Automation: Botao '$AlvoBtn' acionado." }
                catch { $Elem.SetFocus(); return "Elemento '$AlvoBtn' focado na tela." }
            }
            return "Controle '$AlvoBtn' nao encontrado na tela."
        }
        "^digitar-na-tela:\\s*(.+)" {
            Add-Type -AssemblyName System.Windows.Forms
            [System.Windows.Forms.SendKeys]::SendWait($Matches[1].Trim())
            return "Texto digitado na janela ativa."
        }
        "^rotina:\\s*(.+)" {
            $R = $Matches[1].Trim().ToLower()
            if ($R -eq "dev") { powercfg /setactive SCHEME_MIN 2>$null; Start-Process "http://localhost:5000"; return "Rotina DEV ativada." }
            if ($R -eq "encerrar") { [System.GC]::Collect(); return "Rotina ENCERRAR concluida." }
            return "Use 'rotina: dev' ou 'rotina: encerrar'."
        }
        "^abrir:\\s*(.+)" {'''
    code = code.replace('        "^abrir:\\s*(.+)" {', bloco, 1)
    core_p.write_text(code, encoding="utf-8")

py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    p_txt = py_p.read_text(encoding="utf-8")
    if '"clicar-texto:"' not in p_txt:
        py_p.write_text(p_txt.replace('"abrir:",', '"abrir:", "clicar-texto:", "digitar-na-tela:", "rotina:",'), encoding="utf-8")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[OK] UI Automation e Rotinas instaladas com sucesso!")
