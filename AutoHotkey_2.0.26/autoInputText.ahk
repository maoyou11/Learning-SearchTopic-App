#SingleInstance Force
#NoTrayIcon

if A_Args.Length >= 1 {
    input_text := A_Args[1]

    if input_text != "" {
        ; 不使用 For char in，改用索引循环读取每个字符
        len := StrLen(input_text)
        Loop len {
            char := SubStr(input_text, A_Index, 1)
            hex_code := Format("{:X}", Ord(char))
            SendInput "{U+" hex_code "}"
            Sleep 8
        }
    }
}
ExitApp