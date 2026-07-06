# Bezpieczenstwo i transparentnosc

Ten dokument opisuje, co wiadomo o publicznych wydaniach programu Video And Sound Downloader Pro publikowanych w tym repozytorium. Najnowsze wydanie opisane w plikach weryfikacyjnych to v7.0.7.

## Co robi program

Video And Sound Downloader Pro jest aplikacja desktopowa do pobierania materialow audio, wideo, napisow oraz playlist. Program korzysta z narzedzi yt-dlp i FFmpeg.

Program:

- uruchamia yt-dlp lokalnie na komputerze uzytkownika,
- zapisuje pobrane pliki w folderze wybranym przez uzytkownika,
- uzywa FFmpeg do konwersji oraz scalania audio i wideo,
- pokazuje logi pobierania w oknie programu,
- w wersji v7.0.7 jest dostepny bez limitu czasu,
- w wersji v7.0.7 udostepnia przelacznik jezyka PL/EN, tryby Mini oraz przycisk Fix do lokalnej naprawy lub aktualizacji yt-dlp,
- nie wymaga logowania do programu,
- nie prosi o hasla do kont uzytkownika,
- nie publikuje prywatnych plikow uzytkownika.

## Co zawiera publiczne repozytorium

To repozytorium publikacyjne zawiera materialy pomocnicze do weryfikacji publicznych wydan. Dla v7.0.7 dodano rozszerzony snapshot kodu zrodlowego, aby ograniczyc ryzyko traktowania programu jako black box:

- pliki EXE w sekcji Releases,
- sumy kontrolne SHA256 plikow EXE i obrazow GUI,
- rozszerzony kod zrodlowy v7.0.7 w `source-disclosure-v7.0.7`,
- paczke ZIP z rozszerzonym kodem: `source-disclosure-v7.0.7.zip`,
- starsze fragmenty rzeczywistego kodu programu pokazujace sposob uruchamiania yt-dlp,
- obrazy pokazujace wyglad aplikacji dla danego wydania.

## Co nie jest publikowane

Publiczny snapshot v7.0.7 nie zawiera prywatnego materialu podpisu kodu, lokalnego certyfikatu `.cer`, lokalnych sciezek autora, gotowych plikow EXE ani katalogow budowania/cache. Miejsca zwiazane z podpisem i historycznym kodem triala sa w publicznym pliku oznaczone komentarzami.

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

Rozszerzony kod zrodlowy i sumy SHA256 zwiekszaja transparentnosc wydania, ale nie sa pelna gwarancja bezpieczenstwa. Windows moze nadal pokazac ostrzezenie, szczegolnie gdy program jest podpisany certyfikatem lokalnym albo pobrany z internetu po raz pierwszy.
