; ==========================================================
; SCRIPT DEFINITIVO DE INSTALACIÓN - UNIGYM PRO
; Desarrollador: Erick Moreno
; ==========================================================

[Setup]
; Información general de la aplicación
AppName=UniGym Pro
AppVersion=1.0
AppPublisher=Erick Moreno Developer
AppCopyright=Copyright (C) 2026 Erick Moreno

; Configuración de la instalación
DefaultDirName={autopf}\UniGym Pro
DefaultGroupName=UniGym Pro
PrivilegesRequired=admin
OutputBaseFilename=Instalador_UniGym_Pro
Compression=lzma2
SolidCompression=yes

; Iconos del instalador y desinstalador
SetupIconFile=C:\Users\Erick\Desktop\UniGym\assets\logo.ico
UninstallDisplayIcon={app}\UniGym_Pro.exe

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; 1. Copiamos TODA la carpeta del programa generada por PyInstaller
Source: "C:\Users\Erick\Desktop\UniGym\dist\UniGym_Pro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; 2. Copiamos el icono SUELTO a la carpeta principal para los accesos directos
Source: "C:\Users\Erick\Desktop\UniGym\assets\logo.ico"; DestDir: "{app}"; DestName: "app_icon.ico"; Flags: ignoreversion

[Icons]
; Icono en el Menú Inicio
Name: "{group}\UniGym Pro"; Filename: "{app}\UniGym_Pro.exe"; IconFilename: "{app}\app_icon.ico"
; Icono para desinstalar en el Menú Inicio
Name: "{group}\Desinstalar UniGym Pro"; Filename: "{uninstallexe}"; IconFilename: "{app}\app_icon.ico"

; Icono en el ESCRITORIO
Name: "{autodesktop}\UniGym Pro"; Filename: "{app}\UniGym_Pro.exe"; Tasks: desktopicon; IconFilename: "{app}\app_icon.ico"

[Run]
; Ejecutar el programa automáticamente al terminar de instalar
Filename: "{app}\UniGym_Pro.exe"; Description: "{cm:LaunchProgram,UniGym Pro}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    { Nos aseguramos de crear la carpeta de la base de datos en C:\ para proteger los datos }
    ForceDirectories('C:\UniGym_Datos');
  end;
end;