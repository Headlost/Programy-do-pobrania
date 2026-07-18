# Video & Sound Downloader Pro v8.0.8

Szczegółowa lista zmian od wersji 8.0.0.

Wersja 8.0.8 pozostaje **całkowicie bezpłatna, bez okresu próbnego i bez limitu czasu**. Aplikacja służy do pobierania dźwięku, filmów i playlist z obsługiwanych źródeł oraz wykrywania publicznie osadzonych multimediów na stronach internetowych.

## 1. Angielska wersja językowa

- Uzupełniono angielskie tłumaczenia komunikatów stanu, logów, okien dialogowych, błędów pobierania, wyników wykrywania, kontroli transmisji na żywo, sprawdzania multimediów oraz operacji na folderach.
- Dodano angielskie etykiety i instrukcje w oknie wyboru wykrytych multimediów.
- Dodano angielskie komunikaty diagnostyki dostępności formatów oraz wskazówki dotyczące poszczególnych serwisów.
- Długie informacje techniczne pozostają w logu i oknie błędu, natomiast pasek stanu pokazuje wyłącznie krótką zalecaną czynność.

## 2. Diagnostyka dostępności formatów

- Dodano dodatkowe sprawdzenie metadanych przez yt-dlp, gdy żądany format wideo zostanie zgłoszony jako niedostępny.
- Program może teraz podać wykryte rozdzielczości wideo, najwyższą wykrytą rozdzielczość oraz typy kontenerów źródłowych.
- Poprawiono komunikat wyświetlany, gdy żądana jakość jest widoczna w źródle, ale nie można wybrać kompletnego strumienia obrazu i dźwięku.
- Program nie proponuje ponownie tej samej jakości, jeżeli jest ona już widoczna w źródle.

## 3. Obsługa obrazu, dźwięku i napisów ARTE

- Naprawiono pobieranie z ARTE, w którym prawidłowe ścieżki audio były odrzucane z powodu braku standardowej informacji o kodeku dźwięku.
- Dodano wybór formatów ARTE zależny od polskiego lub angielskiego trybu aplikacji.
- Oddzielono wybór wariantu językowego ARTE od opcjonalnego przełącznika osadzania napisów.
- Naprawiono wybór formatu ARTE w trybie angielskim, w którym wyłączenie osadzania napisów usuwało wcześniej informacje potrzebne do dobrania zgodnej pary obrazu i dźwięku.
- Sprawdzono podaną stronę testową ARTE przy użyciu opcji MP4 720p, MP4 1080p oraz MP4 Najlepsza.

## 4. Wskazówki trybu Wykryj

- Dodano pomocne wyjaśnienie wyświetlane, gdy tryb Wykryj jest używany na ogólnej stronie portalu zawierającej zbyt wiele niepowiązanych linków.
- Program sugeruje teraz otwarcie konkretnego artykułu lub podstrony materiału i ponowne użycie trybu Wykryj.
- Dodano bezpośrednią wskazówkę dla linków YouTube: użytkownik powinien wybrać standardowy tryb pobierania dźwięku, wideo lub playlisty.
- Dodano okno z zaleceniem dla Facebooka. Użytkownik może wybrać:
  - **Tak**, aby mimo wszystko kontynuować wykrywanie,
  - **Nie**, aby zamknąć komunikat i wybrać standardowy kafelek pobierania dźwięku, wideo lub playlisty.
- Pozostałe strony przeznaczone do wykrywania działają bez zmian.

## 5. Tryb Wykryj i układ okien

- Zablokowano rozmiar okna wykrytych multimediów na 780 × 500, aby zmiana rozmiaru nie uszkadzała tabeli ani przycisków.
- Ustawiono minimalny rozmiar obszaru głównego okna na 980 × 760, dzięki czemu wszystkie podstawowe elementy pozostają widoczne.
- Zachowano poziome i pionowe przewijanie tabeli wykrytych multimediów dla długich tytułów i adresów URL.

## 6. Prezentowanie pobierania i błędów

- Pełna diagnostyka formatów jest zapisywana w logu i pozostaje dostępna w oknie błędu.
- Pasek stanu wyświetla teraz krótką wskazówkę zamiast wielowierszowej informacji diagnostycznej.
- Ulepszono rozróżnianie między:
  - rzeczywiście niedostępną rozdzielczością,
  - widoczną rozdzielczością, której nie można połączyć z dźwiękiem,
  - źródłem bez informacji o rozdzielczości,
  - źródłem zawierającym wyłącznie dźwięk.

## 7. Bezpieczeństwo udostępnianych plików

- Usunięto Portable v8.0.0 z publicznego wydania w serwisie GitHub, ponieważ archiwum zawierało elementy, których nie wolno udostępniać.
- Usunięto odwołania do wersji Portable z opisu wydania v8.0.0, listy zmian oraz pliku sum kontrolnych.
- Zastąpiono poprawionymi wersjami listę zmian v8.0.0 oraz plik sum kontrolnych.
- Skrypt kompilacji v8.0.8 nie tworzy katalogu ani archiwum ZIP Portable.
- Skrypt podpisujący v8.0.8 nie eksportuje już certyfikatu podpisującego do pliku `.cer`.
- Prywatne elementy związane z podpisywaniem nigdy nie mogą znaleźć się w publicznych plikach wydania ani w udostępnianych pakietach źródłowych.

## 8. Wersja i pliki kompilacji

- Zaktualizowano numer wersji aplikacji do 8.0.8.
- Dodano pliki v8.0.8 odpowiedzialne za uruchamianie, kompilację, podpisywanie, konfigurację PyInstaller, zależności oraz informacje wersji Windows.
- Zaktualizowano lokalne katalogi zależności uruchomieniowych i kompilacyjnych do v8.0.8, zachowując katalogi v8.0.0 jako zapasowe źródła zgodności w trybie źródłowym.
- Dołączony plik yt-dlp zgłasza obecnie wersję 2026.07.04.

## Ograniczenia prawne i dostępu

Program nie omija DRM, subskrypcji, uwierzytelniania, ograniczeń regionalnych ani innych zabezpieczeń dostępu. Należy go używać wyłącznie do materiałów, które użytkownik ma prawo lub pozwolenie pobrać.
