# Bezpieczenstwo i transparentnosc

Ten dokument opisuje, co wiadomo o publicznych wydaniach programu Video And Sound Downloader Pro publikowanych w tym repozytorium. Najnowsze wydanie opisane w plikach weryfikacyjnych to v8.0.8.

## Co robi program

Video And Sound Downloader Pro jest aplikacja desktopowa do pobierania materialow audio, wideo, napisow oraz playlist. Program korzysta z narzedzi yt-dlp i FFmpeg.

Program:

- uruchamia yt-dlp lokalnie na komputerze uzytkownika,
- zapisuje pobrane pliki w folderze wybranym przez uzytkownika,
- uzywa FFmpeg do konwersji oraz scalania audio i wideo,
- pokazuje logi pobierania w oknie programu,
- w wersji v8.0.8 jest dostępny bezpłatnie i bez limitu czasu,
- w wersji v8.0.8 udostępnia przełącznik języka PL/EN, tryby Mini, tryb WYKRYJ oraz przycisk Fix do lokalnej naprawy lub aktualizacji yt-dlp,
- nie wymaga logowania do programu,
- nie prosi o hasla do kont uzytkownika,
- nie publikuje prywatnych plikow uzytkownika.

## Co zawiera publiczne repozytorium

To repozytorium publikacyjne zawiera materiały pomocnicze do weryfikacji publicznych wydań. Dla v8.0.8 dodano rozszerzony snapshot kodu źródłowego, aby ograniczyć ryzyko traktowania programu jako black box:

- pliki EXE w sekcji Releases,
- sumy kontrolne SHA-256 plików EXE i obrazów GUI,
- rozszerzony kod źródłowy v8.0.8 w `source-disclosure-v8.0.8`,
- paczkę ZIP z rozszerzonym kodem: `source-disclosure-v8.0.8.zip`,
- skrócone fragmenty rzeczywistego kodu programu,
- obrazy pokazujące wygląd aplikacji dla danego wydania.

## Co nie jest publikowane

Publiczny snapshot v8.0.8 nie zawiera prywatnego materiału podpisu kodu, lokalnego certyfikatu `.cer`, lokalnych ścieżek autora, gotowych plików EXE ani katalogów budowania/cache. Miejsca związane z podpisem i historycznym kodem triala są w publicznym pliku oznaczone komentarzami.

## Jak sprawdzic pobrany plik

Po pobraniu pliku EXE mozna porownac jego sume SHA256 z plikiem `SHA256SUMS.txt`.

W PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 .\Video_And_Sound_Downloader_Pro_v8.0.8.exe
```

Otrzymany hash powinien byc taki sam jak w `transparency/SHA256SUMS.txt`.

## Ciaglosc wydan

Poprzednie wydania pozostaja dostepne w sekcji Releases. Plik `SHA256SUMS.txt` zachowuje wpisy dla starszych wersji i dopisuje kolejne sumy dla nowych wydan, aby mozna bylo sprawdzic zarowno aktualna, jak i poprzednia paczke programu.

## Uwaga

Rozszerzony kod zrodlowy i sumy SHA256 zwiekszaja transparentnosc wydania, ale nie sa pelna gwarancja bezpieczenstwa. Windows moze nadal pokazac ostrzezenie, szczegolnie gdy program jest podpisany certyfikatem lokalnym albo pobrany z internetu po raz pierwszy.
