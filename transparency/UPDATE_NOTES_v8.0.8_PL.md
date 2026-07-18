# Video & Sound Downloader Pro v8.0.8 — opis aktualizacji

## Licencja i dostępność

Wersja 8.0.8 jest **bezpłatna, bez okresu próbnego i bez limitu czasu**. Program umożliwia pobieranie dźwięku, filmów i playlist z obsługiwanych źródeł oraz wykrywanie publicznie osadzonych multimediów na stronach internetowych.

## Podsumowanie aktualizacji

Wersja 8.0.8 jest aktualizacją naprawczą skoncentrowaną na tłumaczeniach, wskazówkach trybu Wykryj, diagnostyce formatów, zgodności z ARTE, stabilności okien oraz bezpieczniejszym przygotowywaniu plików wydania.

Aktualizacja została przygotowana i sprawdzona jako wydanie wersji 8.0.8.

## Zmiany widoczne dla użytkownika

- Angielski tryb programu zawiera teraz spójne tłumaczenia interfejsu, okien dialogowych, logów i komunikatów stanu.
- Długie informacje o dostępności formatów nie rozszerzają obszaru stanu. Pasek pokazuje krótką zalecaną czynność, a wszystkie szczegóły pozostają w logu i oknie błędu.
- Gdy nie można pobrać wybranego formatu, program ponownie sprawdza źródło i podaje wykryte rozdzielczości oraz kontenery.
- Linki YouTube wprowadzone w trybie Wykryj kierują do standardowego pobierania dźwięku, wideo lub playlisty.
- Linki Facebooka wprowadzone w trybie Wykryj wyświetlają zalecenie z wyborem **Tak/Nie**.
- Ogólne strony portali zawierające zbyt wiele niepowiązanych treści sugerują otwarcie konkretnego artykułu lub podstrony materiału.
- Okna wykrytych multimediów nie można już zmniejszyć w sposób powodujący uszkodzenie układu.

## Poprawka ARTE

ARTE może udostępniać prawidłowe strumienie HLS zawierające wyłącznie dźwięk bez standardowej informacji o kodeku. Wcześniejsze selektory odrzucały takie strumienie, powodując błędny komunikat „Żądany format jest niedostępny”, nawet gdy wybrana rozdzielczość znajdowała się na liście.

Wersja 8.0.8 wybiera obraz i dźwięk ARTE przy użyciu pasującego identyfikatora wariantu językowego:

- polski tryb aplikacji preferuje polski wariant ARTE,
- angielski tryb aplikacji preferuje angielski wariant ARTE,
- wybór działa niezależnie od opcjonalnego osadzania napisów.

Podana strona testowa ARTE została sprawdzona w trybie symulacji dla opcji 720p, 1080p i Najlepsza.

## Zmiana dotycząca bezpieczeństwa udostępnianych plików

Publiczne archiwum Portable v8.0.0 zostało usunięte, ponieważ zawierało plik certyfikatu podpisującego. Powiązane odwołania i sumy kontrolne zostały usunięte lub poprawione.

Wersja 8.0.8 korzysta z następujących zasad przygotowywania plików:

- archiwum Portable nie jest tworzone,
- certyfikat podpisujący nie jest eksportowany obok kompilacji,
- pliki certyfikatów nie są kopiowane do materiałów wydania,
- można przesyłać wyłącznie celowo wybrane pliki wydania,
- sumy kontrolne należy wygenerować po utworzeniu ostatecznych plików,
- zawartość udostępnianego pakietu źródłowego musi zostać sprawdzona przed publikacją.

## Lokalne pliki wersji 8.0.8

- `YouTube_Audio_Downloader_Zak v8-0-8.pyw`
- `Uruchom_GUI_v8-0-8.bat`
- `Kompiluj_EXE_v8-0-8.bat`
- `Podpisz_EXE_v8-0-8.ps1`
- `Video_And_Sound_Downloader_Pro_v8.0.8.spec`
- `version_info_v8_0_8.txt`
- `requirements_v8-0-8.txt`
- `GITHUB_RELEASE_v8.0.8_PL.md`
- `GITHUB_RELEASE_v8.0.8_EN.md`
- `CHANGELOG_v8.0.8_PL.md`
- `CHANGELOG_v8.0.8_EN.md`
- `UPDATE_NOTES_v8.0.8_PL.md`
- `UPDATE_NOTES_v8.0.8_EN.md`
- `RELEASE_NOTES_v8.0.8_PL.md`
- `RELEASE_NOTES_v8.0.8_EN.md`

## Lista kontroli wydania

1. Uruchomić wersję źródłową i sprawdzić polski oraz angielski tryb programu.
2. Przetestować pobieranie MP3, MP4, playlist oraz działanie trybu Wykryj.
3. Ponownie sprawdzić ARTE w polskim i angielskim trybie programu.
4. Lokalnie skompilować i podpisać ostateczny plik EXE.
5. Zweryfikować podpis Authenticode oraz znacznik czasu.
6. Przeskanować cały katalog przygotowanego wydania pod kątem plików `.cer`, `.pfx`, `.p12`, kluczy prywatnych, danych uwierzytelniających i plików przeznaczonych wyłącznie do użytku lokalnego.
7. Wygenerować sumy SHA-256 dla ostatecznie zatwierdzonych plików.
8. Oddzielnie sprawdzić pakiet udostępnianych źródeł.
9. Opublikować wersję dopiero po wyraźnym zatwierdzeniu wydania.
