Set ws = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' 获取当前目录
currentPath = fso.GetParentFolderName(WScript.ScriptFullName)
fullPath = currentPath & "\DeAntiCapture.exe"

ws.Run fullPath, 0, False
