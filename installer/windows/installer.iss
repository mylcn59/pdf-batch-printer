; Inno Setup Script for PDF Batch Printer
; Generates Windows installer with desktop shortcut and uninstaller
; Developer: BK Bilgi Teknolojileri

#define MyAppName "PDF Batch Printer"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "BK Bilgi Teknolojileri"
#define MyAppURL "https://github.com/mylcn59/pdf-batch-printer"
#define MyAppExeName "PDFBatchPrinter.exe"

[Setup]
; Unique application identifier
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation directory
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

; Output settings
OutputDir=..\..\dist\installer
OutputBaseFilename=PDFBatchPrinter_Setup_{#MyAppVersion}
; SetupIconFile=..\..\assets\icon.ico

; Compression
Compression=lzma2/ultra64
SolidCompression=yes

; Installer appearance
WizardStyle=modern
DisableProgramGroupPage=yes

; Privileges (install for current user by default)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Version info
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
VersionInfoCopyright=Copyright (c) 2024 BK Bilgi Teknolojileri

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
; Main executable (PyInstaller bundle - includes Python and all dependencies)
Source: "..\..\dist\PDFBatchPrinter.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start menu shortcut
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

; Desktop shortcut (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Option to run application after install
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up any created files
Type: filesandordirs; Name: "{app}"

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Post-installation tasks
  end;
end;
