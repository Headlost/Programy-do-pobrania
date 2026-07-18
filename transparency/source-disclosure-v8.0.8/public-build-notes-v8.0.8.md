# Public build notes for v8.0.8

Te notatki nie zawierają prywatnego certyfikatu ani lokalnych ścieżek autora.

## Minimalne wymagania

- Windows,
- Python 3.12 lub zgodny,
- `customtkinter`,
- `pyinstaller`,
- `yt-dlp.exe`,
- `ffmpeg.exe`,
- `ffprobe.exe`.

```powershell
python -m pip install -r requirements_v8-0-8.txt
python -m pip install pyinstaller
```

## Przykładowe budowanie

```powershell
python -m PyInstaller `
  --noconfirm `
  --clean `
  --onefile `
  --windowed `
  --name "Video_And_Sound_Downloader_Pro_v8.0.8" `
  --hidden-import customtkinter `
  --collect-data customtkinter `
  --add-binary ".\tools\yt-dlp.exe;tools" `
  --add-binary ".\tools\ffmpeg.exe;tools" `
  --add-binary ".\tools\ffprobe.exe;tools" `
  ".\source-v8.0.8-public.pyw"
```

Prywatna kompilacja autora dodaje ikony, metadane wersji, dane Tcl/Tk i podpis Authenticode. Nie zmienia to głównej logiki programu.

## Narzędzia użyte przy przygotowaniu wydania

```text
52FE3C26DCF71FBDC85B528589020BB0B8E383155CFA81B64DD447BBE35E24B8  yt-dlp.exe (2026.07.04)
274AB9F3358DAF1376DD237B8C83EB803B53B623A2C6F3ED159CD817063655F3  ffmpeg.exe
5C9EE67EA32F28C018D63BB6835D5D84F5D0EBE52953BA62699E7A2F90BCA5B7  ffprobe.exe
```

FFmpeg i FFprobe pochodzą z wydania `N-124279-g0f6ba39122-20260430`.

## Podpis

Prywatny materiał podpisu kodu nie jest publikowany. Gotowy plik wydania jest podpisany Authenticode i ma znacznik czasu. Jego status oraz sumę SHA-256 należy sprawdzić przed publikacją.
