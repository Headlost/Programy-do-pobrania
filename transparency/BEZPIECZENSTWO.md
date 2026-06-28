# Bezpieczenstwo i transparentnosc

Ten dokument opisuje, co wiadomo o publicznym wydaniu programu Video And Sound Downloader Pro v6.5.6.

## Co robi program

Video And Sound Downloader Pro jest aplikacja desktopowa do pobierania materialow audio, wideo, napisow oraz playlist. Program korzysta z narzedzi yt-dlp i FFmpeg.

Program:

- uruchamia yt-dlp lokalnie na komputerze uzytkownika,
- zapisuje pobrane pliki w folderze wybranym przez uzytkownika,
- uzywa FFmpeg do konwersji oraz scalania audio i wideo,
- pokazuje logi pobierania w oknie programu,
- nie wymaga logowania do programu,
- nie prosi o hasla do kont uzytkownika,
- nie publikuje prywatnych plikow uzytkownika.

## Co zawiera publiczne repozytorium

To repozytorium publikacyjne nie zawiera pelnego kodu zrodlowego aplikacji. Zawiera tylko materialy pomocnicze do weryfikacji publicznego wydania:

- plik EXE w sekcji Releases,
- sume kontrolna SHA256 pliku EXE,
- fragment rzeczywistego kodu programu pokazujacy sposob uruchamiania yt-dlp,
- obraz pokazujacy aktualny wyglad aplikacji.

## Jak sprawdzic pobrany plik

Po pobraniu pliku EXE mozna porownac jego sume SHA256 z plikiem `SHA256SUMS.txt`.

W PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 .\Video_And_Sound_Downloader_Pro_v6.5.6.exe
```

Otrzymany hash powinien byc taki sam jak w `transparency/SHA256SUMS.txt`.

## Uwaga

Fragment kodu i suma SHA256 zwiekszaja transparentnosc wydania, ale nie sa pelna gwarancja bezpieczenstwa. Windows moze nadal pokazac ostrzezenie, szczegolnie gdy program jest podpisany certyfikatem lokalnym albo pobrany z internetu po raz pierwszy.