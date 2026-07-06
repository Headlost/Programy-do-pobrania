# Public build notes for v7.0.7

To sa publiczne notatki budowania. Nie zawieraja prywatnego certyfikatu ani lokalnych sciezek autora.

## Minimalne wymagania

- Windows
- Python 3
- `customtkinter`
- `pyinstaller`
- `yt-dlp.exe`
- `ffmpeg.exe`
- `ffprobe.exe`

Zaleznosc Pythona z pliku:

```powershell
python -m pip install -r requirements_v7-0-7.txt
python -m pip install pyinstaller
```

## Przykladowe budowanie

```powershell
python -m PyInstaller `
  --noconfirm `
  --clean `
  --onefile `
  --windowed `
  --name "Video_And_Sound_Downloader_Pro_v7.0.7" `
  --hidden-import customtkinter `
  --collect-data customtkinter `
  --add-binary ".\tools\yt-dlp.exe;tools" `
  --add-binary ".\tools\ffmpeg.exe;tools" `
  --add-binary ".\tools\ffprobe.exe;tools" `
  ".\source-v7.0.7-public.pyw"
```

W prywatnym buildzie autora dochodza ikony, metadane wersji, dane Tcl/Tk oraz podpis Authenticode. Te elementy nie zmieniaja glownej logiki programu.

## Zewnetrzne narzedzia

Program uruchamia lokalnie `yt-dlp` i korzysta z FFmpeg do konwersji, scalania audio/wideo i obslugi trybow Mini.

Hash narzedzia `yt-dlp.exe` uzytego lokalnie przy przygotowaniu v7.0.7:

```text
3A48CB955D55C8821B60CCBDBBC6F61BC958F2F3D3B7AD5EAF3D83A543293A27  yt-dlp.exe
```

Hash lokalnie wykrytych narzedzi FFmpeg:

```text
274AB9F3358DAF1376DD237B8C83EB803B53B623A2C6F3ED159CD817063655F3  ffmpeg.exe
5C9EE67EA32F28C018D63BB6835D5D84F5D0EBE52953BA62699E7A2F90BCA5B7  ffprobe.exe
```

## Podpis

Prywatny material podpisu kodu nie jest publikowany. Publiczny kod zawiera komentarze przy miejscach, gdzie program odnosi sie do podpisu lub starych mechanizmow triala.

Wersja v7.0.7 jest bez limitu czasu.
