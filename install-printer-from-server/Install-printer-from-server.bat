@echo off

echo RESET PRINTER ZEBRA

wmic printer get name /value | findstr /I /E "zd230-ext-03" && (
	Rundll32 printui.dll,PrintUIEntry /dn /n "\\168.17.20.2\zd230-ext-03" && Rundll32 printui.dll,PrintUIEntry /in /n "\\168.17.20.2\zd230-ext-03") || (
	Rundll32 printui.dll,PrintUIEntry /in /n "\\168.17.20.2\zd230-ext-03")