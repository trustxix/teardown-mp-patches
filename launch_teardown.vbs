' Silent pre-launch: activate all local mods before Teardown starts
' No visible window — runs Python script hidden, then launches the game

Set WshShell = CreateObject("WScript.Shell")

' Run mod activator silently (hidden window, wait for it to finish)
WshShell.Run "python ""C:\Users\trust\teardown-mp-patches\activate_all_local_mods.py"" --silent", 0, True

' Launch the game — pass through whatever Steam gave us
Dim args
args = ""
Dim i
For i = 0 To WScript.Arguments.Count - 1
    args = args & " """ & WScript.Arguments(i) & """"
Next
If Len(args) > 0 Then
    WshShell.Run args, 1, False
End If
