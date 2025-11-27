; Script de Inno Setup para Gestión Comercial
; ============================================
;
; INSTRUCCIONES:
; 1. Descarga e instala Inno Setup desde: https://jrsoftware.org/isdl.php
; 2. Ejecuta build.bat para crear GestionComercial.exe
; 3. Abre este archivo con Inno Setup Compiler
; 4. Presiona F9 para compilar el instalador
;
; REQUISITOS:
; - El archivo dist\GestionComercial.exe debe existir
; - Inno Setup 6.0 o superior

#define MyAppName "Gestión Comercial"
#define MyAppVersion "1.0"
#define MyAppPublisher "Tu Nombre o Empresa"
#define MyAppURL "https://www.tuempresa.com"
#define MyAppExeName "GestionComercial.exe"

[Setup]
; Información básica de la aplicación
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Directorio de instalación
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Permisos y configuración
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Archivos de salida
OutputDir=installer_output
OutputBaseFilename=GestionComercial_Setup_v{#MyAppVersion}
SetupIconFile=

; Compresión
Compression=lzma2/max
SolidCompression=yes

; Apariencia del instalador
WizardStyle=modern
WizardSizePercent=100,100

; Licencia y readme (opcional, descomenta si tienes estos archivos)
; LicenseFile=LICENSE.txt
; InfoBeforeFile=README.txt

; Desinstalador
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Archivo ejecutable principal
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Si tienes archivos adicionales, agrégalos aquí
; Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Icono en el menú inicio
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

; Icono en el escritorio (si el usuario lo eligió)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

; Icono de desinstalación
Name: "{group}\Desinstalar {#MyAppName}"; Filename: "{uninstallexe}"

[Run]
; Ejecutar la aplicación después de instalar (opcional)
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Limpiar archivos creados por la aplicación
Type: filesandordirs; Name: "{userappdata}\GestionComercial"

[Code]
var
  IsUpgrade: Boolean;

// Función que se ejecuta al iniciar el instalador
function InitializeSetup(): Boolean;
var
  OldVersion: String;
  UninstallKey: String;
begin
  Result := True;
  IsUpgrade := False;

  // Verificar si ya está instalada una versión anterior
  UninstallKey := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}_is1';

  if RegQueryStringValue(HKEY_LOCAL_MACHINE, UninstallKey, 'DisplayVersion', OldVersion) then
  begin
    IsUpgrade := True;

    // Preguntar si desea actualizar
    if MsgBox('Se detectó una versión anterior (' + OldVersion + ') instalada.' + #13#10 +
              '¿Desea actualizarla a la versión {#MyAppVersion}?',
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;
end;

// Función que se ejecuta después de la instalación
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Aquí puedes agregar lógica adicional después de la instalación
    // Por ejemplo: crear configuraciones, verificar requisitos, etc.
  end;
end;

// Mensaje personalizado al finalizar
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
  begin
    // Mensaje personalizado en la página final
  end;
end;
