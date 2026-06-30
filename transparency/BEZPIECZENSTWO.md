# Bezpieczenstwo i transparentnosc

Ten dokument opisuje, co wiadomo o publicznych wydaniach programu Video And Sound Downloader Pro publikowanych w tym repozytorium. Najnowsze wydanie opisane w plikach weryfikacyjnych to v7.0.7.

## Co robi program

Video And Sound Downloader Pro jest aplikacja desktopowa do pobierania materialow audio, wideo, napisow oraz playlist. Program korzysta z narzedzi yt-dlp i FFmpeg.

Program:

- uruchamia yt-dlp lokalnie na komputerze uzytkownika,
- zapisuje pobrane pliki w folderze wybranym przez uzytkownika,
- uzywa FFmpeg do konwersji oraz scalania audio i wideo,
- pokazuje logi pobierania w oknie programu,
- w wersji v7.0.7 udostepnia nowy panel GUI, przelacznik jezyka PL/EN, tryb pobierania z Facebooka oraz przycisk Fix do lokalnej naprawy lub aktualizacji yt-dlp,
- nie wymaga logowania do programu,
- nie prosi o hasla do kont uzytkownika,
- nie publikuje prywatnych plikow uzytkownika.

## Co zawiera publiczne repozytorium

To repozytorium publikacyjne nie zawiera pelnego kodu zrodlowego aplikacji. Zawiera tylko materialy pomocnicze do weryfikacji publicznych wydan:

- pliki EXE w sekcji Releases,
- sumy kontrolne SHA256 plikow EXE i obrazow GUI,
- fragmenty rzeczywistego kodu programu pokazujace sposob uruchamiania yt-dlp,
- obrazy pokazujace wyglad aplikacji dla danego wydania.

## Jak sprawdzic pobrany plik

Po pobraniu pliku EXE mozna porownac jego sume SHA256 z plikiem `SHA256SUMS.txt`.

W PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 .\Video_And_Sound_Downloader_Pro_v7.0.7.exe
```

Otrzymany hash powinien byc taki sam jak w `transparency/SHA256SUMS.txt`.

## Ciaglosc wydan

Poprzednie wydania pozostaja dostepne w sekcji Releases. Plik `SHA256SUMS.txt` zachowuje wpisy dla starszych wersji i dopisuje kolejne sumy dla nowych wydan, aby mozna bylo sprawdzic zarowno aktualna, jak i poprzednia paczke programu.

## Uwaga

Fragment kodu i suma SHA256 zwiekszaja transparentnosc wydania, ale nie sa pelna gwarancja bezpieczenstwa. Windows moze nadal pokazac ostrzezenie, szczegolnie gdy program jest podpisany certyfikatem lokalnym albo pobrany z internetu po raz pierwszy.
