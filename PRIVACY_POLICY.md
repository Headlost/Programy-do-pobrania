# Polityka prywatności / Privacy Policy

**Video And Sound Downloader Pro (Video & Sound Downloader Pro)**  
**Data wejścia w życie i ostatniej aktualizacji / Effective and last updated: 21 października 2026 / 21 October 2026**

[Polski](#polski) · [English](#english)

---

## Polski

### 1. Wydawca i zakres polityki

Wydawcą aplikacji jest **Beniamin Żak**, prowadzący projekt na GitHubie pod nazwą **Headlost**. Ta polityka opisuje działanie aplikacji Video And Sound Downloader Pro dla systemu Windows na podstawie wersji **8.0.8**.

Program służy do pobierania materiałów audio, wideo, playlist i napisów z podanych przez użytkownika adresów oraz do wykrywania multimediów osadzonych na stronach. Korzysta z uruchamianych lokalnie narzędzi **yt-dlp, FFmpeg i FFprobe**.

Kontakt w sprawach prywatności: [zgłoszenia w repozytorium projektu](https://github.com/Headlost/Programy-do-pobrania/issues). Zgłoszenia są publiczne. Nie zamieszczaj w nich prywatnych linków, haseł, plików cookies, tokenów dostępu ani nieocenzurowanych logów.

### 2. Brak konta i własnego zbierania danych o użytkowaniu

Aplikacja nie wymaga zakładania konta, rejestracji ani logowania do usługi wydawcy. Nie ma serwera wydawcy obsługującego pobieranie ani chmurowego magazynu historii użytkownika.

Standardowa wersja aplikacji:

- nie wysyła autorowi wprowadzanych linków, historii pobierania, pobranych plików ani logów;
- nie zawiera własnej analityki, reklam, profilowania ani automatycznego przesyłania raportów awarii;
- nie wysyła materiałów do usług AI, LLM ani ChatGPT — tryby Mini jedynie lokalnie zmniejszają pliki;
- nie sprzedaje danych użytkownika ani nie przekazuje ich do celów reklamowych;
- nie wymaga podawania imienia, adresu e-mail, numeru telefonu ani danych płatniczych.

Ustawienia bieżącej sesji, wprowadzony adres i informacje o wykonywanym zadaniu są używane do realizacji czynności wybranej przez użytkownika.

### 3. Co dzieje się z wprowadzonym linkiem

Wprowadzony link jest przetwarzany na komputerze użytkownika. Po uruchomieniu pobierania, sprawdzania materiału lub trybu WYKRYJ program i yt-dlp nawiązują połączenia z odpowiednim serwisem oraz serwerami udostępniającymi materiał.

**Link nie jest przesyłany do autora w celu prowadzenia historii czy analizy. Nie jest jednak niewidoczny dla serwisu, z którego pobierasz materiał.** Serwis źródłowy, jego API, serwery CDN lub inne serwery wymagane do udostępnienia materiału otrzymują odpowiednie żądania sieciowe. Mogą one obejmować adres URL i parametry zapytania, adres IP, czas połączenia, nagłówki techniczne, język oraz dane wymagane przez dany serwis do dostarczenia treści.

Adres URL może sam zawierać dane identyfikujące użytkownika albo token dostępu. Używaj tylko linków, które chcesz przekazać serwisowi w celu realizacji wybranego zadania.

Tryb WYKRYJ może dodatkowo pobierać wskazaną stronę, powiązane podstrony materiałów oraz źródła multimediów wykryte w jej treści. Szczegółowy zestaw adresów zależy od strony i obsługi danego źródła przez yt-dlp.

**yt-dlp jest narzędziem działającym lokalnie, a nie usługą chmurową, do której autor aplikacji wysyła wszystkie linki.** FFmpeg i FFprobe wykonują konwersję, scalanie, kompresję oraz sprawdzanie pobranych plików lokalnie.

### 4. Inne połączenia z internetem

Poza połączeniami potrzebnymi do obsługi wskazanego materiału aplikacja może nawiązywać następujące połączenia:

- **Fix:** po uruchomieniu tej funkcji sprawdzana jest wersja yt-dlp, w tym przez API GitHuba. Po potwierdzeniu aktualizacji program może pobrać yt-dlp z oficjalnego repozytorium. Do żądań aktualizacji aplikacja nie dołącza wprowadzonych linków ani zawartości logów.
- **Instalacja brakujących komponentów:** po zgodzie użytkownika program może uruchomić Windows Package Manager (winget), który łączy się ze swoimi źródłami i dostawcami pakietów.
- **Przyciski otwierające strony:** repozytorium projektu, strona licencji oraz dobrowolne strony wsparcia BuyCoffee lub Ko-fi mogą zostać otwarte w przeglądarce po odpowiedniej czynności użytkownika.

Dostawcy tych serwisów otrzymują zwykłe dane połączenia, np. adres IP i nagłówki żądania. Po otwarciu strony w przeglądarce mogą obowiązywać jej własne pliki cookies i zasady prywatności. Dobrowolna wpłata może przekazać operatorowi płatności i odbiorcy wsparcia informacje związane z transakcją, zgodnie z zasadami danej platformy. Aplikacja nie zbiera numerów kart ani danych logowania do płatności.

Samo odwiedzenie tej polityki na GitHubie również podlega zasadom GitHuba. Windows i Microsoft Store mogą niezależnie przetwarzać dane dotyczące instalacji, bezpieczeństwa, diagnostyki lub działania sklepu zgodnie z ustawieniami użytkownika i zasadami Microsoftu.

### 5. Dane i pliki na komputerze

Aplikacja i używane narzędzia przetwarzają lokalnie adresy URL, tytuły i metadane materiałów, informacje o formatach, napisy, ścieżki zapisu oraz wyniki i komunikaty błędów. Dane te służą do pobierania, konwersji, wykrywania mediów i prezentowania postępu.

Pobrane pliki są zapisywane w folderze wybranym przez użytkownika. Mogą powstawać również pliki częściowe i tymczasowe, osobne ścieżki obrazu lub dźwięku, napisy oraz lokalna pamięć podręczna yt-dlp. Po przerwaniu zadania część takich plików może pozostać na dysku.

Log widoczny w oknie programu jest przechowywany w pamięci bieżącej sesji i nie jest automatycznie wysyłany autorowi. Może zawierać linki, tytuły, ścieżki z nazwą konta Windows oraz techniczne komunikaty. System operacyjny i uruchamiane narzędzia mogą niezależnie tworzyć własne pliki diagnostyczne.

Zaktualizowany komponent yt-dlp może być zapisany w lokalnym folderze danych aplikacji, zazwyczaj `%LOCALAPPDATA%\VideoAndSoundDownloaderPro\tools`. Wersja źródłowa może używać folderu `tools` obok programu.

Przycisk wklejania odczytuje tekst ze schowka po jego użyciu, a przycisk kopiowania zapisuje wybrane linki do schowka. Aplikacja nie monitoruje schowka w tle.

### 6. Hasła, logowanie i konfiguracja yt-dlp

Interfejs aplikacji nie prosi o hasła do serwisów i standardowo nie importuje automatycznie plików cookies z przeglądarki. Nie jest to równoznaczne z uzyskaniem dostępu do materiałów wymagających logowania.

Jeśli użytkownik samodzielnie skonfiguruje yt-dlp, np. za pomocą zewnętrznego pliku konfiguracyjnego, może to zmienić sposób korzystania z cookies, uwierzytelniania, pamięci podręcznej, logów, proxy lub sieci. Takie ustawienia i ich konsekwencje pozostają pod kontrolą użytkownika. Nigdy nie publikuj plików cookies ani danych uwierzytelniających.

### 7. Przechowywanie, usuwanie i bezpieczeństwo

Wydawca nie prowadzi na swoim serwerze bazy linków ani kopii pobrań użytkownika. Nie może więc udostępnić ani usunąć kopii, której nie otrzymał.

Log i adres widoczne w aplikacji nie stanowią trwałej historii prowadzonej przez program; zamknięcie aplikacji kończy tę sesję. Pobrane pliki, lokalne kopie komponentów oraz ewentualna pamięć podręczna lub pozostałości zadań pozostają do czasu usunięcia ich przez użytkownika albo odpowiednie narzędzie. Odinstalowanie programu nie musi usuwać plików zapisanych w wybranym folderze.

Program nie zapewnia własnego szyfrowania plików na dysku. Dostęp do nich zależy od uprawnień konta, zabezpieczeń Windows, innych programów oraz ewentualnej synchronizacji folderów, np. przez OneDrive. Połączenia używają HTTPS, gdy dany adres i usługa to obsługują; adresy HTTP nie zapewniają takiej samej ochrony transmisji.

Aby ograniczyć przetwarzanie, możesz przerwać zadanie, nie uruchamiać funkcji sieciowych, usunąć lokalne pliki i pamięć podręczną albo zamknąć aplikację. Samo przerwanie zadania nie usuwa danych połączenia, które serwis otrzymał wcześniej.

### 8. Dobrowolny kontakt i prawa użytkownika

Jeżeli samodzielnie przekażesz autorowi zgłoszenie lub log, otrzyma on informacje, które zdecydujesz się udostępnić. Wydawca wykorzystuje je do odpowiedzi, wyjaśnienia problemu i utrzymania projektu, a nie do reklamy czy sprzedaży danych. Takie informacje są przechowywane przez czas potrzebny do obsługi sprawy oraz ewentualnych obowiązków prawnych; widoczność i przechowywanie zgłoszeń na GitHubie zależą również od tej platformy.

W zakresie, w jakim wydawca otrzyma dane osobowe, odpowiada za ich przetwarzanie przy obsłudze zgłoszenia. Podstawą może być realizacja prośby użytkownika lub prawnie uzasadniony interes polegający na udzielaniu pomocy i utrzymaniu bezpieczeństwa projektu, zależnie od charakteru kontaktu.

W granicach obowiązującego prawa możesz wystąpić o dostęp do takich danych, ich poprawienie, usunięcie lub ograniczenie przetwarzania, wnieść sprzeciw oraz skargę do właściwego organu nadzorczego, w Polsce do Prezesa UODO. Kontakt z wydawcą jest wskazany w punkcie 1. Nie podawaj publicznie dodatkowych danych osobowych; w pierwszym zgłoszeniu wystarczy ogólnie opisać sprawę.

Pytania o dane przechowywane przez serwis źródłowy, GitHub, Microsoft lub operatora wsparcia należy kierować także do odpowiedniego podmiotu. Aplikacja nie kontroluje ich okresów przechowywania i zasad.

### 9. Zmiany polityki

Polityka będzie aktualizowana, jeżeli zmieni się sposób przetwarzania danych przez aplikację. Data aktualizacji jest podana na początku. Aktualna wersja jest dostępna pod stałym adresem:

[https://github.com/Headlost/Programy-do-pobrania/blob/main/PRIVACY_POLICY.md](https://github.com/Headlost/Programy-do-pobrania/blob/main/PRIVACY_POLICY.md)

---

## English

### 1. Publisher and scope

The application is published by **Beniamin Żak**, who maintains the project on GitHub as **Headlost**. This policy describes the Windows application Video And Sound Downloader Pro based on version **8.0.8**.

The application downloads audio, video, playlists and subtitles from URLs supplied by the user and discovers embedded media on web pages. It uses **yt-dlp, FFmpeg and FFprobe**, which run locally on the user's computer.

Privacy contact: [the project's GitHub issues](https://github.com/Headlost/Programy-do-pobrania/issues). Issues are public. Do not include private links, passwords, cookies, access tokens or unredacted logs.

### 2. No application account or usage-data collection by the publisher

The application does not require an account, registration or sign-in to a service operated by the publisher. There is no publisher-operated download server or cloud store of user history.

The standard application:

- does not send entered URLs, download history, downloaded files or logs to the author;
- does not include its own analytics, advertising, profiling or automatic crash-report uploads;
- does not send content to AI services, LLMs or ChatGPT — Mini modes only reduce file sizes locally;
- does not sell user data or disclose it for advertising purposes;
- does not require a name, email address, phone number or payment details.

Current-session options, the entered URL and task information are used to carry out the action selected by the user.

### 3. What happens to an entered URL

An entered URL is processed on the user's computer. Starting a download, a media check or DISCOVER causes the application and yt-dlp to connect to the relevant service and the servers delivering the content.

**The URL is not sent to the author to maintain a history or perform analytics. It is not, however, hidden from the service from which you request content.** The source service, its APIs, CDNs or other servers needed to deliver the content receive the relevant network requests. These may include URLs and query parameters, the IP address, connection time, technical headers, language and information required by that service to deliver the content.

A URL itself may contain identifying information or an access token. Only use URLs that you intend to send to the service to perform the selected task.

DISCOVER may also retrieve the supplied web page, related media subpages and media sources found within the page. The exact destinations depend on the website and yt-dlp's support for that source.

**yt-dlp is a local tool, not a cloud service to which the application author sends all URLs.** FFmpeg and FFprobe perform conversion, merging, compression and checks of downloaded files locally.

### 4. Other internet connections

In addition to connections needed to process the selected content, the application may make the following connections:

- **Fix:** when this feature is started, the application checks the yt-dlp version, including through the GitHub API. After the user confirms an update, it may download yt-dlp from the official repository. The application does not attach entered media URLs or log contents to its update requests.
- **Missing components:** with the user's agreement, the application may run Windows Package Manager (winget), which contacts its package sources and providers.
- **Buttons that open websites:** the project repository, license page and optional BuyCoffee or Ko-fi support pages may open in the browser following the corresponding user action.

These providers receive ordinary connection data, such as IP addresses and request headers. Websites opened in a browser may use their own cookies and privacy practices. An optional contribution may disclose transaction-related information to the payment platform and support recipient under that platform's rules. The application does not collect card numbers or payment sign-in details.

Visiting this policy on GitHub is also subject to GitHub's practices. Windows and Microsoft Store may independently process installation, security, diagnostic or Store information under the user's settings and Microsoft's policies.

### 5. Information and files on the computer

The application and its tools locally process URLs, media titles and metadata, format information, subtitles, destination paths, results and error messages. They use this information for downloading, conversion, media discovery and progress reporting.

Downloaded files are saved in the folder selected by the user. Partial and temporary files, separate audio or video tracks, subtitles and yt-dlp cache files may also be created. Some files may remain after an interrupted task.

The log displayed in the application is held in memory for the current session and is not automatically sent to the author. It may contain URLs, titles, paths including the Windows account name and technical messages. The operating system and invoked tools may independently create their own diagnostic files.

An updated yt-dlp component may be stored in the application's local data folder, usually `%LOCALAPPDATA%\VideoAndSoundDownloaderPro\tools`. The source version may use a `tools` folder next to the program.

The paste button reads clipboard text when used, and the copy button places selected links on the clipboard. The application does not monitor the clipboard in the background.

### 6. Passwords, sign-in and yt-dlp configuration

The application interface does not ask for service passwords and does not automatically import browser cookies in its standard configuration. This does not grant access to content requiring authentication.

If the user independently configures yt-dlp, for example through an external configuration file, this may change cookie handling, authentication, caching, logging, proxy use or network behavior. These settings and their consequences remain under the user's control. Never publish cookie files or credentials.

### 7. Retention, deletion and security

The publisher does not maintain a server-side database of user URLs or copies of downloads. The publisher therefore cannot provide or delete a copy it has never received.

The displayed URL and log are not a persistent history maintained by the application; closing the application ends that session. Downloads, local component copies, caches and task remnants may remain until the user or the relevant tool deletes them. Uninstalling the application may not remove files from the selected destination folder.

The application does not provide its own encryption of files on disk. Access depends on account permissions, Windows security, other software and any folder-sync service, such as OneDrive. Connections use HTTPS where supported by the URL and service; HTTP URLs do not provide the same protection in transit.

You can limit processing by stopping a task, not starting network features, deleting local files and caches, or closing the application. Stopping a task does not delete connection information already received by a service.

### 8. Voluntary contact and user rights

If you voluntarily send the author an issue report or log, the author receives the information you choose to provide. The publisher uses it to respond, investigate the problem and maintain the project, rather than for advertising or data sales. Such information is kept as long as needed to handle the matter and meet any applicable legal obligations; GitHub also controls aspects of issue visibility and retention.

Where the publisher receives personal data, the publisher is responsible for processing it when handling the request. Depending on the contact, processing may be based on responding to the user's request or the legitimate interest in providing support and maintaining project security.

Subject to applicable law, you may request access, correction, deletion or restriction of such data, object to processing and complain to the relevant supervisory authority, including the President of the Personal Data Protection Office in Poland. The publisher's contact is in section 1. Do not publicly disclose additional personal data; a general description of the matter is sufficient for an initial issue.

Questions about information retained by source services, GitHub, Microsoft or support platforms should also be directed to the relevant provider. The application does not control their retention periods or policies.

### 9. Changes to this policy

This policy will be updated if the application's data practices change. The update date appears at the top. The current version remains available at:

[https://github.com/Headlost/Programy-do-pobrania/blob/main/PRIVACY_POLICY.md](https://github.com/Headlost/Programy-do-pobrania/blob/main/PRIVACY_POLICY.md)
