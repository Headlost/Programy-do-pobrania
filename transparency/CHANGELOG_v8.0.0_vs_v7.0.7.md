Video & Sound Downloader Pro v8.0.0
Pełna lista zmian względem wersji v7.0.7

1. Nowy tryb „WYKRYJ”
- Dodano wykrywanie materiałów audio i wideo osadzonych na publicznych stronach internetowych.
- Program analizuje dane yt-dlp, elementy HTML video/source, metadane strony, konfiguracje JavaScript i JSON oraz bezpośrednie adresy CDN.
- Obsługiwane są zwykłe pliki oraz manifesty HLS, DASH i Smooth Streaming.
- Strony zawierające listy materiałów mogą być analizowane wraz z powiązanymi podstronami w tej samej domenie.
- Usunięto osobny kafelek Facebooka. Materiały z Facebooka pozostają obsługiwane przez standardowe tryby audio i wideo.

2. Lista wykrytych materiałów
- Wyniki są prezentowane w tabeli z kolumnami Format, Materiał i Bezpośredni adres.
- Można pobrać pojedynczy materiał, kilka zaznaczonych pozycji albo wszystkie wyniki.
- Dodano kopiowanie bezpośrednich adresów do schowka.
- Dodano poziomy i pionowy pasek przewijania, ułatwiające odczyt długich nazw oraz adresów.
- Dodano informację o zaznaczaniu wielu pozycji za pomocą lewego Ctrl i lewego przycisku myszy.
- Każdy zaznaczony materiał jest zapisywany jako osobny plik z nazwą pochodzącą z kolumny Materiał.
- Nazwy są oczyszczane ze znaków niedozwolonych w Windows. Duplikaty i istniejące pliki otrzymują kolejne oznaczenia „(2)”, „(3)” itd., zamiast się nadpisywać.

3. Rozszerzona obsługa formatów
- Rozszerzono wykrywanie między innymi formatów MP4, WebM, MKV, MOV, M4V, MP3, M4A, AAC, OGG, OPUS, WAV, FLAC, TS, M2TS, 3GP, AVI, WMV, FLV, M3U8, MPD oraz ISM.
- Tryb WYKRYJ pozwala wybrać docelowy format audio albo wideo przed pobraniem.
- Doprecyzowano opisy formatów: „WEBM Android TV”, „OPUS Komunikacja niskich opóźnień” i „MKV Blu-ray, HEVC”.
- Usunięto zdublowane zbiorcze pozycje Mini w trybach PLAYLISTA i WYKRYJ. Pozostawiono osobne formaty MP3 Mini i MP4 Mini.

4. Pewniejsze pobieranie obrazu i dźwięku
- Selektory wideo wymagają kompletnego wyniku zawierającego obraz i dźwięk.
- Program preferuje wysokiej jakości osobne strumienie obrazu i dźwięku, a gdy serwis ich nie udostępnia, korzysta ze stabilnego bezpośredniego pliku progresywnego.
- Usunięto sortowanie, które w trybie Mini mogło odwrócić wybór jakości i pobrać najwyższy, wadliwy manifest HLS zamiast najmniejszego pliku.
- Po pobraniu FFprobe sprawdza obecność obu strumieni, a FFmpeg wykonuje krótką próbę rzeczywistego dekodowania.
- Uszkodzony, audio-only albo niedekodowalny wynik nie jest już zgłaszany jako poprawny plik wideo.
- Zachowano możliwość pobierania najlepszych oddzielnych strumieni z YouTube bez ograniczania jakości do pliku progresywnego.

5. Poprawki trybu Mini
- Naprawiono pobieranie i kompresję Mini dla serwisów udostępniających jednocześnie pliki progresywne i manifesty HLS.
- Kompresja zachowuje mapowanie obrazu i dźwięku oraz dąży do rozmiaru maksymalnie 20 MB.
- Program zapisuje najmniejszy poprawnie utworzony wariant, jeżeli osiągnięcie 20 MB nie jest możliwe.
- Poprawiono diagnostykę nieudanej kompresji i weryfikację pliku wejściowego.

6. Poprawki nazw Unicode i identyfikacji pliku
- Ścieżka pliku zwracana przez yt-dlp jest teraz przekazywana w formacie JSON z bezpiecznym kodowaniem Unicode.
- Naprawiono fałszywy komunikat „Niepełny plik wideo” dla tytułów zawierających znaki spoza strony kodowej konsoli, na przykład pełnoszeroką pionową kreskę „｜”.
- Zachowano zgodność z wcześniejszym formatem wpisów ścieżki w logu.

7. Playlisty i duże pliki
- Usprawniono wykrywanie playlist YouTube i YouTube Music dla adresów watch, shorts, youtu.be oraz bezpośrednich adresów playlist.
- Wybór pojedynczego materiału zachowuje pełny adres i ogranicza pobieranie do jednego elementu.
- Elementy playlisty wideo są pobierane i finalizowane kolejno, co ogranicza liczbę plików tymczasowych.
- Ograniczono częstotliwość komunikatów postępu, aby duże pliki nie blokowały interfejsu podczas ekstrakcji, konwersji i sprzątania.

8. Ochrona przed aktywnymi transmisjami
- Przed pobieraniem program sprawdza, czy materiał jest trwającą, niezakończoną transmisją na żywo.
- Aktywne transmisje są blokowane z czytelnym komunikatem i można je pobrać po zakończeniu jako zwykłe nagranie.
- Tryb WYKRYJ oznacza aktywne transmisje jako niedostępne i nie uruchamia dla nich FFmpeg.
- Przycisk STOP kończy w Windows całe drzewo procesów yt-dlp i FFmpeg.

9. Diagnostyka dostępu i błędów
- Dodano dokładniejsze komunikaty dla DRM, logowania, sesji/cookies, ograniczeń regionalnych, brakujących strumieni, materiałów prywatnych, ograniczeń wiekowych i problemów autoryzacyjnych.
- Dodano osobny komunikat dla niepełnego lub niedekodowalnego pliku wideo.
- Usunięto lokalną listę blokowanych domen. Bezwzględną blokadą programu pozostaje wykryte DRM.
- Zachowano legalne warianty ponawiania dostępu z nagłówkami przeglądarki i refererem.

10. Interfejs i wygoda obsługi
- Dodano kafelek WYKRYJ z funkcją „Wykryj audio lub wideo”.
- Zaktualizowano ikony kafelków WYKRYJ i PLAYLISTA oraz wyrównano elementy wszystkich kafelków.
- Dodano przycisk „Pobrane”, otwierający bieżący folder zapisu po udanym pobraniu w danej sesji.
- Zachowano polską i angielską wersję interfejsu.

11. Bezpieczeństwo i transparentność
- Program nadal nie omija DRM ani zabezpieczeń dostępu.
- Gotowy EXE jest podpisany Authenticode i ma dołączoną sumę SHA-256.
- Przygotowano publiczny snapshot kodu v8.0.0, skrócony podgląd najważniejszej logiki oraz odpersonalizowane notatki budowania.
- Prywatny materiał podpisu, lokalny certyfikat i lokalne ścieżki autora nie są częścią source-disclosure.

12. Wydanie i pakowanie
- Zaktualizowano numer programu oraz metadane pliku do 8.0.0.
- Zaktualizowano skrypty uruchamiania, budowania i podpisywania oraz konfigurację PyInstaller.
- Dołączono nowe zasoby graficzne oraz wymagane narzędzia yt-dlp, FFmpeg i FFprobe.
- Wydanie korzysta z yt-dlp 2026.07.04.

Program należy wykorzystywać wyłącznie do materiałów, do których użytkownik posiada prawa lub zgodę na pobranie.
