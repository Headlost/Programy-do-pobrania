# Source disclosure for Video And Sound Downloader Pro v8.0.0

Ten folder zawiera prawie pełny publiczny snapshot kodu źródłowego wersji v8.0.0.

## Zawartość

- `source-v8.0.0-public.pyw` — główny plik programu v8.0.0,
- `requirements_v8-0-0.txt` — minimalna lista zależności Pythona,
- `public-build-notes-v8.0.0.md` — opis budowania i narzędzi zewnętrznych,
- `public-pyinstaller-v8.0.0.spec` — odpersonalizowany przykład konfiguracji PyInstaller,
- `LICENSE-GPL-3.0.txt` — licencja programu.

## Celowo pominięte elementy

- prywatny materiał podpisu kodu,
- lokalny certyfikat i prywatny skrypt podpisywania EXE,
- absolutne ścieżki z komputera autora,
- katalogi budowania, cache, gotowy EXE i pliki tymczasowe,
- zewnętrzne binaria `yt-dlp.exe`, `ffmpeg.exe` i `ffprobe.exe`.

## Zakres ujawnionego kodu

Snapshot pokazuje rzeczywistą logikę GUI, tryb WYKRYJ, obsługę playlist, tryby Mini, wybór i walidację strumieni obrazu oraz dźwięku, obsługę yt-dlp/FFmpeg, napisy, logi, przycisk Fix i zatrzymywanie procesów.

Wersja v8.0.0 jest darmowa i bez limitu czasu. Historyczne funkcje związane z trialem pozostały w kodzie dla transparentności, ale `TRIAL_DAYS = 0`, a `enforce_trial_status()` udostępnia pełną wersję wszystkim użytkownikom.

Program nie omija DRM ani zabezpieczeń dostępu. Należy go używać wyłącznie do materiałów, do których użytkownik ma prawa lub zgodę na pobranie.
