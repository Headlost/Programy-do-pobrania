# Source disclosure for Video And Sound Downloader Pro v7.0.7

Ten folder zawiera prawie pelny publiczny snapshot kodu zrodlowego wersji v7.0.7.

## Co jest w srodku

- `source-v7.0.7-public.pyw` - glowny plik programu v7.0.7 z dodanymi komentarzami przy miejscach zwiazanych z podpisem i starym kodem triala.
- `requirements_v7-0-7.txt` - minimalna lista zaleznosci Pythona.
- `public-build-notes-v7.0.7.md` - opis sposobu budowania i elementow zewnetrznych.
- `public-pyinstaller-v7.0.7.spec` - przykladowy, odpersonalizowany plik PyInstaller.
- `LICENSE-GPL-3.0.txt` - licencja programu.

## Co zostalo celowo pominiete

- prywatny material podpisu kodu,
- lokalny certyfikat `.cer`,
- lokalny skrypt podpisywania EXE,
- absolutne sciezki z komputera autora,
- katalogi budowania, cache, gotowy plik EXE i tymczasowe pliki narzedzi,
- zewnetrzne binaria `yt-dlp.exe`, `ffmpeg.exe` i `ffprobe.exe`.

## Uwagi o podpisie i trialu

W kodzie pozostaly funkcje historycznie zwiazane z trialem i sprawdzaniem podpisu. Sa pokazane publicznie, z komentarzem, poniewaz ich ukrywanie pogorszyloby transparentnosc.

W wersji v7.0.7 program jest darmowy i bez limitu czasu:

- `TRIAL_DAYS = 0`,
- `TRIAL_STATE_SECRET = "free-version-no-trial"` nie jest prywatnym kluczem,
- `enforce_trial_status()` ustawia status programu jako dostepny bez limitu czasu.

## Jak to czytac

Ten folder ma pokazac realna logike programu: GUI, tryby pobierania, tryby Mini, obsluge playlist, obsluge `yt-dlp`, obsluge FFmpeg, logi, Fix dla `yt-dlp` oraz zapis plikow w folderze wybranym przez uzytkownika.

Nie jest to paczka z prywatnym procesem podpisywania autora. Podpis EXE sluzy identyfikacji wydania, a nie ukrywaniu dzialania programu.
