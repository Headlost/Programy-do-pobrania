# 🚀 Video & Sound Downloader Pro v8.0.8

## Bezpłatny program — bez wersji próbnej i bez limitu czasu

Video & Sound Downloader Pro v8.0.8 jest udostępniany **całkowicie bezpłatnie, bez okresu próbnego i bez limitu czasu**. Wszystkie tryby pobierania pozostają dostępne bez subskrypcji i bez daty wygaśnięcia.

## Do czego służy program

Video & Sound Downloader Pro umożliwia pobieranie dźwięku, filmów i playlist z obsługiwanych linków oraz wykrywanie publicznie osadzonych multimediów na stronach internetowych. Obsługuje standardowe źródła rozpoznawane przez yt-dlp, bezpośrednie pliki multimedialne, a także strumienie HLS, DASH i Smooth Streaming.

Programu należy używać wyłącznie do materiałów, których użytkownik jest właścicielem lub na których pobranie ma pozwolenie. Program nie omija DRM, subskrypcji, uwierzytelniania, ograniczeń regionalnych ani innych zabezpieczeń dostępu.

## Sześć kluczowych możliwości

### 1. Wykrywanie osadzonych multimediów

Tryb **WYKRYJ** skanuje publiczne strony internetowe w poszukiwaniu osadzonych materiałów audio i wideo. Może analizować metadane yt-dlp, elementy multimedialne HTML, metadane strony, konfigurację JavaScript/JSON, bezpośrednie linki CDN oraz manifesty strumieni. Wykryte elementy są przedstawiane na liście umożliwiającej wybór.

### 2. Ochrona przed pobieraniem niezakończonych transmisji na żywo

Aplikacja wykrywa aktywne, niezakończone transmisje na żywo przed rozpoczęciem pobierania. Takie transmisje są blokowane, aby nie były pobierane bez końca i nie pozostawiały uruchomionych procesów yt-dlp oraz FFmpeg. Po zakończeniu transmisji i przekształceniu jej w zwykłe nagranie materiał można pobrać standardowo.

### 3. Czytelna i użyteczna obsługa błędów

Zamiast wyświetlać wyłącznie ogólny komunikat o niepowodzeniu, program rozróżnia zabezpieczenia DRM, wymagane logowanie, nieprawidłowe sesje lub pliki cookies, materiały prywatne, ograniczenia regionalne i wiekowe, problemy z autoryzacją, brakujące formaty, niekompletne pliki wideo oraz niedostępne źródła.

### 4. Kontrola poprawności obrazu i dźwięku

Pobrany film jest sprawdzany pod kątem obecności obrazu i dźwięku. FFprobe kontroluje dostępne strumienie, a FFmpeg wykonuje krótki test dekodowania. Dzięki temu plik zawierający wyłącznie dźwięk, uszkodzony lub niemożliwy do zdekodowania nie jest zgłaszany jako prawidłowo pobrany film.

### 5. Lepsza obsługa playlist, formatów i trybów Mini

Aplikacja obsługuje pobieranie dźwięku, filmów oraz całych playlist, w tym ulepszoną obsługę playlist YouTube i YouTube Music. Dostępne są również tryby MP3 Mini i MP4 Mini, przetwarzanie dużych plików oraz formaty wyjściowe takie jak MP4, WEBM, MKV, MP3, M4A, WAV i OPUS.

### 6. Wygodniejsza codzienna obsługa

Linki z Facebooka można obsługiwać standardowymi trybami pobierania dźwięku i wideo, a tryb Wykryj pozostaje dostępny w razie potrzeby. Przycisk **Pobrane** otwiera rzeczywisty folder docelowy używany w bieżącej sesji. Czytelne polskie i angielskie wersje interfejsu ułatwiają korzystanie z programu.

## Co poprawiono w wersji 8.0.8

Wersja 8.0.8 jest aktualizacją naprawczą, która zwiększa niezawodność pobierania, uzupełnia angielskie tłumaczenia, poprawia wskazówki trybu Wykryj, diagnostykę formatów, obsługę ARTE, stabilność okien oraz bezpieczeństwo przygotowywania wydania.

## Spójniejszy interfejs w języku angielskim

Tryb angielski obejmuje teraz główny interfejs, komunikaty stanu, logi, okna dialogowe, wyniki wykrywania, sprawdzanie multimediów, błędy formatów oraz wskazówki dotyczące poszczególnych serwisów.

Długie komunikaty techniczne nie są już wyświetlane w obszarze stanu. Pasek stanu przedstawia krótką informację o następnym kroku, a pełne wyjaśnienie pozostaje dostępne w logu i oknie błędu.

## Lepsza diagnostyka dostępnych formatów

Jeżeli nie można pobrać wybranej opcji wideo, aplikacja dodatkowo sprawdza metadane i może podać:

- wykryte rozdzielczości wideo,
- najwyższą wykrytą rozdzielczość,
- kontenery źródłowych strumieni wideo,
- źródła zawierające wyłącznie dźwięk,
- źródła bez informacji o rozdzielczości.

Aplikacja rozpoznaje również sytuację, w której wybrana jakość jest widoczna w źródle, ale nie można utworzyć kompletnego pliku z obrazem i dźwiękiem. Dzięki temu nie proponuje ponownie tej samej jakości.

## Poprawka pobierania z ARTE

ARTE używa wariantów HLS przypisanych do języka i może nie podawać standardowej wartości kodeka dla prawidłowych ścieżek audio. Powodowało to wcześniej błędne komunikaty „Brak strumienia multimedialnego” dla opcji takich jak MP4 720p, MP4 1080p i MP4 Najlepsza.

Wersja 8.0.8 łączy obraz i dźwięk ARTE przy użyciu odpowiedniego wariantu językowego:

- polski tryb programu wybiera polski wariant ARTE,
- angielski tryb programu wybiera angielski wariant ARTE.

Wybór strumienia ARTE działa teraz niezależnie od opcjonalnego osadzania napisów.

## Czytelniejsza obsługa trybu Wykryj

Tryb Wykryj służy do znajdowania multimediów osadzonych na stronach, które nie udostępniają prostego, bezpośredniego linku do materiału.

- Linki YouTube kierują użytkownika do standardowego trybu pobierania dźwięku, wideo lub playlisty.
- Linki Facebooka wyświetlają zalecenie i pozwalają mimo wszystko kontynuować wykrywanie.
- Ogólne strony portali sugerują otwarcie konkretnego artykułu lub podstrony materiału przed ponowną próbą.
- Okno wykrytych multimediów ma zablokowany rozmiar, a głównego okna nie można zmniejszyć poniżej rozmiaru potrzebnego do prawidłowego wyświetlenia wszystkich elementów.

## Bezpieczniejsze udostępnianie programu

Opublikowane wcześniej archiwum Portable v8.0.0 zostało usunięte, ponieważ zawierało elementy, które nie powinny być publicznie udostępniane. Usunięto również odwołania do niego w opisie wydania i wpis w pliku sum kontrolnych.

Wersja 8.0.8 nie tworzy archiwum Portable, a jej skrypt podpisujący nie eksportuje pliku certyfikatu.

Planowany format wydania obejmuje sprawdzony samodzielny plik EXE oraz wyłącznie zatwierdzone materiały informacyjne i dokumentacyjne. Prywatne elementy związane z podpisywaniem nigdy nie są częścią wydania.

## Dołączone komponenty

Lokalna konfiguracja kompilacji korzysta z:

- yt-dlp 2026.07.04,
- FFmpeg,
- FFprobe,
- CustomTkinter,
- zasobów aplikacji wymaganych przez interfejs.

## Ważne

Program nie omija DRM, płatnego dostępu, uwierzytelniania, ograniczeń regionalnych ani zabezpieczeń serwisów. Należy go używać wyłącznie do materiałów, które można legalnie pobrać.

---

Ten dokument towarzyszy wydaniu wersji 8.0.8.
