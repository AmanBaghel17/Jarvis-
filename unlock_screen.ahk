; AutoHotkey script for screen unlocking
; This uses AutoHotkey's reliable typing mechanism
; which works better with Windows lock screens

#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases
#Warn   ; Enable warnings to assist with detecting common errors
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability

; Read the password from file
FileRead, Password, %A_UserProfile%\.jarvis\plain_password.txt
if ErrorLevel
{
    ; If file doesn't exist or can't be read, use the default password
    Password := "asdfghjkl;'"
}

; Display a message
MsgBox, 4, Screen Unlock, This script will attempt to unlock your screen by typing your password.`n`nClick Yes to continue or No to cancel.
IfMsgBox, No
    ExitApp

; Give user time to switch to lock screen
Sleep, 3000

; Wake up the screen with multiple key presses
Send, {Shift}
Sleep, 500
Send, {Space}
Sleep, 2000

; Type the password
SendInput, %Password%
Sleep, 500

; Press Enter
Send, {Enter}

; Clean up - clear variables
Password := ""

ExitApp
