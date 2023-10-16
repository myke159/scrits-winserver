$Printer = Get-CimInstance -Class Win32_Printer -Filter "Name='NomeDaImpressora'"
Invoke-CimMethod -InputObject $Printer -MethodName SetDefaultPrinter 