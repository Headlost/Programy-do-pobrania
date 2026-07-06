# -*- coding: utf-8 -*-
# PUBLIC SOURCE DISCLOSURE NOTE:
# This file is a near-complete public source snapshot for v7.0.7.
# Private signing material, exported certificates and local build-machine paths are not included here.
# Signature/trial compatibility code is left visible for review, but v7.0.7 sets TRIAL_DAYS = 0
# and enforce_trial_status() keeps the program available without a time limit.
#
# YouTube Audio / Video Downloader GUI
# Wersja 7.0.7: darmowa bez limitu czasu, Fix dla yt-dlp i tryby Mini do testów
# Plik .pyw uruchamia się bez czarnego okna konsoli.
#
# Używaj tylko do materiałów, do których masz prawa albo które wolno Ci pobrać zgodnie z regulaminem źródła.
#
# Copyright (C) 2026 Beniamin Żak
#
# Ten program jest wolnym oprogramowaniem: możesz go rozpowszechniać i/lub
# modyfikować zgodnie z warunkami GNU General Public License opublikowanej
# przez Free Software Foundation, w wersji 3 Licencji albo dowolnej późniejszej.
# Szczegóły znajdziesz w pliku LICENSE-GPL-3.0.txt.

import os
import json
import hashlib
import hmac
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def configure_tcl_tk_paths():
    candidates = []

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        bundled_root = Path(sys._MEIPASS)
        candidates.append((bundled_root / "_tcl_data", bundled_root / "_tk_data"))

    python_root = Path(sys.executable).resolve().parent
    candidates.append((python_root / "tcl" / "tcl8.6", python_root / "tcl" / "tk8.6"))

    for tcl_dir, tk_dir in candidates:
        if (tcl_dir / "init.tcl").exists() and tk_dir.exists():
            os.environ["TCL_LIBRARY"] = str(tcl_dir)
            os.environ["TK_LIBRARY"] = str(tk_dir)
            return


configure_tcl_tk_paths()


def add_local_python_libraries():
    if getattr(sys, "frozen", False):
        return

    app_dir = Path(__file__).resolve().parent
    local_dirs = [
        app_dir / ".runtime_deps_v7_0_7",
        app_dir / ".runtime_deps_v6_5_6",
        app_dir / ".runtime_deps_v6_5_5",
        app_dir / ".runtime_deps_v6_0_5",
        app_dir / ".runtime_deps_v6_0_1",
        app_dir / ".runtime_deps_v6_0_0",
        app_dir / ".build_tools_v7_0_7",
        app_dir / ".build_tools_v6_5_6",
        app_dir / ".build_tools_v6_5_5",
        app_dir / ".build_tools_v6_0_5",
        app_dir / ".build_tools_v6_0_1",
        app_dir / ".build_tools_v6_0_0",
    ]
    local_paths = []
    for path in local_dirs:
        try:
            customtkinter_init = path / "customtkinter" / "__init__.py"
            if customtkinter_init.exists():
                with customtkinter_init.open("rb") as handle:
                    handle.read(1)
                local_paths.append(str(path))
        except OSError:
            continue
    for deps_path in reversed(local_paths):
        if deps_path not in sys.path:
            sys.path.insert(0, deps_path)


add_local_python_libraries()

import tkinter as tk
from tkinter import filedialog, messagebox

try:
    import customtkinter as ctk
    if not hasattr(ctk, "CTk"):
        raise ImportError("Niepełna instalacja CustomTkinter - brakuje klasy CTk.")
except (ModuleNotFoundError, ImportError):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Brakuje biblioteki",
        "Ta wersja programu wymaga biblioteki CustomTkinter.\n\n"
        "Najprościej uruchom raz plik Uruchom_GUI_v7-0-7.bat albo zainstaluj:\n"
        "pip install customtkinter\n\n"
        "Jeśli stary folder zależności istnieje, ale program nadal pokazuje ten komunikat, "
        "uruchom Uruchom_GUI_v7-0-7.bat - plik utworzy czysty folder .runtime_deps_v7_0_7.",
    )
    root.destroy()
    raise SystemExit(1)


APP_TITLE = "Video & Sound Downloader Pro"
APP_VERSION = "7.0.7"
APP_AUTHOR = "Beniamin Żak"
APP_LICENSE = "GNU GPL v3.0 lub późniejsza"
SUPPORT_URL = "https://buycoffee.to/beniamin-tv6"
SUPPORT_URL_EN = "https://ko-fi.com/beniaminzak"
PROJECT_REPO_URL = "https://github.com/Headlost/Programy-do-pobrania"
LICENSE_FILE_NAME = "LICENSE-GPL-3.0.txt"
APP_ICON_FILE_NAME = "app_icon.ico"
APP_ICON_PNG_FILE_NAME = "app_icon.png"
LICENSE_URL = "https://www.gnu.org/licenses/gpl-3.0.txt"
YTDLP_ID = "yt-dlp.yt-dlp"
FFMPEG_ID = "Gyan.FFmpeg"
INSTALL_TIMEOUT_SECONDS = 240
TOOLS_DIR_NAME = "tools"
YTDLP_LATEST_RELEASE_API = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"
YTDLP_LATEST_EXE_URL = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
MINI_VIDEO_MAX_BYTES = 20 * 1024 * 1024
MINI_AUDIO_BITRATE = "64k"

TRIAL_DAYS = 0
TRIAL_BUILD_ID = "free-v7-0-7"
TRIAL_BUILD_STARTED_AT = 0
TRIAL_STATE_SECRET = "free-version-no-trial"

# Public disclosure note:
# These constants and helper functions are legacy compatibility code from earlier trial builds.
# In v7.0.7 the effective trial length is zero, so read_trial_state() returns None and the app
# stays available without a time limit. The value above is not a private key.
TRIAL_DEFAULT_DAYS = 30
TRIAL_MAX_DAYS = 365
TRIAL_DAY_SECONDS = 24 * 60 * 60
TRIAL_CLOCK_TOLERANCE_SECONDS = 10 * 60
TRIAL_STATE_SCHEMA = 2
TRIAL_STATE_FILE_NAME = "trial_state_v7_0_7.json"
TRIAL_REGISTRY_KEY = r"Software\VideoAndSoundDownloaderPro"
TRIAL_REGISTRY_VALUE_NAME = "trial_state_v7_0_7"
TRIAL_EXPECTED_SIGNER_MARKERS = ("Beniamin_", "Code_Signing")
SELF_INTEGRITY_BLOCK_STATUSES = {"HashMismatch", "NotSigned"}
SUBTITLE_MODES = {"MP4", "FACEBOOK"}
SUBTITLE_LANGUAGE_PRIORITY_PL = [
    ("pl", "polskim"),
    ("en", "angielskim"),
]
SUBTITLE_LANGUAGE_PRIORITY_EN = [
    ("en", "angielskim"),
    ("pl", "polskim"),
]
SUBTITLE_FILE_EXTENSIONS = {".vtt", ".srt", ".ass", ".lrc"}
BROWSER_RETRY_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36"
)
BROWSER_RETRY_ACCEPT_LANGUAGE = "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"


def get_resource_path(file_name):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / file_name
    return Path(__file__).resolve().parent / file_name

def get_default_save_dir():
    home = Path.home()
    candidates = [
        home / "Downloads",
        home / "Pobrane",
        home / "Desktop",
        home / "Pulpit",
        home,
    ]
    for folder in candidates:
        if folder.exists() and folder.is_dir():
            return str(folder)
    return str(home)

AUDIO_PRESETS = [
    ("MP3   320 kbps", {"kind": "audio", "format": "mp3", "audio_quality": "320k"}),
    ("MP3   192 kbps", {"kind": "audio", "format": "mp3", "audio_quality": "192k"}),
    ("MP3 Mini do testów", {"kind": "audio", "format": "mp3", "audio_quality": MINI_AUDIO_BITRATE, "mini": True}),
    ("M4A   najlepsza", {"kind": "audio", "format": "m4a", "audio_quality": "0"}),
    ("WAV   bez kompresji", {"kind": "audio", "format": "wav", "audio_quality": "0"}),
    ("OPUS  najlepsza", {"kind": "audio", "format": "opus", "audio_quality": "0"}),
]

VIDEO_PRESETS = [
    ("MP4   Najlepsza", {"kind": "video", "format": "mp4", "quality": "Najlepsza"}),
    ("MP4   1080p Full HD", {"kind": "video", "format": "mp4", "quality": "1080p"}),
    ("MP4   720p HD", {"kind": "video", "format": "mp4", "quality": "720p"}),
    ("MP4   480p", {"kind": "video", "format": "mp4", "quality": "480p"}),
    ("MP4 Mini do testów", {"kind": "video", "format": "mp4", "quality": "Mini", "mini": True}),
    ("MKV   Najlepsza", {"kind": "video", "format": "mkv", "quality": "Najlepsza"}),
    ("WEBM  Najlepsza", {"kind": "video", "format": "webm", "quality": "Najlepsza"}),
]

MODE_ONLY_PRESETS = [
    ("Playlista Mini do testów", {"kind": "video", "format": "mp4", "quality": "Mini", "mini": True}),
    ("Facebook Mini do testów", {"kind": "video", "format": "mp4", "quality": "Mini", "mini": True}),
]
QUALITY_PRESETS = dict(AUDIO_PRESETS + VIDEO_PRESETS + MODE_ONLY_PRESETS)
MODE_QUALITY_OPTIONS = {
    "MP3": [label for label, _ in AUDIO_PRESETS],
    "MP4": [label for label, _ in VIDEO_PRESETS],
    "PLAYLISTA": [label for label, _ in AUDIO_PRESETS + VIDEO_PRESETS] + ["Playlista Mini do testów"],
    "FACEBOOK": [label for label, _ in VIDEO_PRESETS] + ["Facebook Mini do testów"],
}
MODE_DEFAULT_QUALITY = {
    "MP3": "MP3   320 kbps",
    "MP4": "MP4   1080p Full HD",
    "PLAYLISTA": "MP3   320 kbps",
    "FACEBOOK": "MP4   1080p Full HD",
}

LANGUAGE_LABELS = {
    "PL": "Polski",
    "EN": "English",
}

QUALITY_LABELS_EN = {
    "MP3   320 kbps": "MP3   320 kbps",
    "MP3   192 kbps": "MP3   192 kbps",
    "MP3 Mini do testów": "MP3 Mini for tests",
    "M4A   najlepsza": "M4A   best",
    "WAV   bez kompresji": "WAV   uncompressed",
    "OPUS  najlepsza": "OPUS  best",
    "MP4   Najlepsza": "MP4   Best",
    "MP4   1080p Full HD": "MP4   1080p Full HD",
    "MP4   720p HD": "MP4   720p HD",
    "MP4   480p": "MP4   480p",
    "MP4 Mini do testów": "MP4 Mini for tests",
    "MKV   Najlepsza": "MKV   Best",
    "WEBM  Najlepsza": "WEBM  Best",
    "Playlista Mini do testów": "Playlist Mini for tests",
    "Facebook Mini do testów": "Facebook Mini for tests",
}
QUALITY_LABELS_PL_BY_EN = {value: key for key, value in QUALITY_LABELS_EN.items()}

UI_TEXT_EN = {
    "Pobieraj audio, wideo i playlisty z jednego panelu": "Download audio, video and playlists from one panel",
    "Wybierz język": "Choose language",
    "Link:": "Link:",
    "Wklej link z YouTube, Facebooka albo innej obsługiwanej strony...": "Paste a link from YouTube, Facebook or another supported site...",
    "Wybierz opcję:": "Choose option:",
    "Napisy do filmu": "Video subtitles",
    "Pobierz dźwięk": "Download audio",
    "Pobierz wideo": "Download video",
    "Pobierz całą listę": "Download full list",
    "PLAYLISTA": "PLAYLIST",
    "Jakość / Format:": "Quality / Format:",
    "Zapisz do:": "Save to:",
    "↓   POBIERZ": "↓   DOWNLOAD",
    "↓   POBIERZ DŹWIĘK": "↓   DOWNLOAD AUDIO",
    "↓   POBIERZ WIDEO": "↓   DOWNLOAD VIDEO",
    "↓   POBIERZ PLAYLISTĘ": "↓   DOWNLOAD PLAYLIST",
    "↓   POBIERZ Z FACEBOOKA": "↓   DOWNLOAD FROM FACEBOOK",
    "Wsparcie": "Support",
    "O mnie": "About",
    "Najpierw polskie, w razie braku angielskie. Napisy będą w filmie.": (
        "Polish first, English if missing. Subtitles will be embedded in the video."
    ),
    "Gotowe.": "Ready.",
    "OK": "OK",
    "TAK": "YES",
    "NIE": "NO",
    "ANULUJ": "CANCEL",
    "TRIAL WYGASŁ": "TRIAL EXPIRED",
}

MESSAGE_EXACT_EN = {
    "Brakuje biblioteki": "Missing library",
    "Ta wersja programu wymaga biblioteki CustomTkinter.\n\nNajprościej uruchom raz plik Uruchom_GUI_v7-0-7.bat albo zainstaluj:\npip install customtkinter\n\nJeśli stary folder zależności istnieje, ale program nadal pokazuje ten komunikat, uruchom Uruchom_GUI_v7-0-7.bat - plik utworzy czysty folder .runtime_deps_v7_0_7.": "This version of the program requires the CustomTkinter library.\n\nThe easiest way is to run Uruchom_GUI_v7-0-7.bat once or install:\npip install customtkinter\n\nIf the old dependency folder exists but the program still shows this message, run Uruchom_GUI_v7-0-7.bat - it will create a clean .runtime_deps_v7_0_7 folder.",
    "Gotowe.": "Ready.",
    "Schowek jest pusty": "Clipboard is empty",
    "Nie znaleziono tekstu do wklejenia.": "No text was found to paste.",
    "O mnie": "About",
    "Program został zablokowany": "Program blocked",
    "Program został zablokowany. Pobieranie nie jest dostępne.": "The program has been blocked. Downloads are not available.",
    "Program został zablokowany przez kontrolę integralności.": "The program has been blocked by the integrity check.",
    "Program zablokowany: kontrola integralności pliku EXE nie powiodła się.": "Program blocked: EXE integrity check failed.",
    "Czas testów tej wersji programu minął.\n\nPobieranie zostało zablokowane.": "The test period for this program version has expired.\n\nDownloading has been blocked.",
    "Plik programu nie przechodzi kontroli podpisu albo został zmieniony po kompilacji.\n\nPobieranie zostało zablokowane. Uruchom oryginalny, podpisany plik EXE.": "The program file does not pass signature verification or was changed after compilation.\n\nDownloading has been blocked. Run the original signed EXE file.",
    "Program jest dostępny bez limitu czasu.": "The program is available without a time limit.",
    "Na liczne prośby program został udostępniony wszystkim użytkownikom bez limitu czasu. Jeśli doceniasz projekt, możesz przybić wirtualną piątkę, klikając przycisk Wsparcie.": "By popular request, the program is available to all users without a time limit. If you appreciate the project, you can give a virtual high five by clicking Support.",
    "Mini: kończę kompresję...": "Mini: finishing compression...",
    "Błąd: sprawdź szczegóły w logu.": "Error: check the log for details.",
    "Sprawdzam napisy do filmu...": "Checking video subtitles...",
    "Napisy: sprawdzam dostępność PL, potem EN.": "Subtitles: checking PL availability first, then EN.",
    "Napisy: ARTE - wybieram wariant wideo zgodny z językiem napisów.": "Subtitles: ARTE - selecting the video variant that matches the subtitle language.",
    "Napisy: wtapiam napisy w obraz filmu...": "Subtitles: burning subtitles into the video image...",
    "Napisy: kończę wtapianie napisów...": "Subtitles: finishing subtitle burn-in...",
    "Napisy: napisy zostały wtopione w obraz filmu.": "Subtitles: subtitles were burned into the video image.",
    "Napisy: nie udało się wtopić napisów w obraz filmu.": "Subtitles: could not burn subtitles into the video image.",
    "Napisy: nie znaleziono pobranego pliku napisów do wtopienia.": "Subtitles: could not find the downloaded subtitle file to burn in.",
    "Napisy: nie udało się potwierdzić ścieżki pobranego pliku.": "Subtitles: could not confirm the downloaded file path.",
    "Napisy: nie udało się sprawdzić listy napisów dla tego filmu.": "Subtitles: could not check the subtitle list for this video.",
    "Napisy: nie znaleziono zwykłych ani automatycznych napisów po polsku lub angielsku.": "Subtitles: no regular or automatic Polish or English subtitles were found.",
    "Napisy: nie znaleziono zwykłych napisów po polsku lub angielsku.": "Subtitles: no regular Polish or English subtitles were found.",
    "Napisy były wykryte, ale nie udało się ich pobrać lub zintegrować. Film został pobrany bez napisów.": "Subtitles were detected, but could not be downloaded or embedded. The video was downloaded without subtitles.",
    "Napisy były dostępne i zostały zintegrowane z filmem.": "Subtitles were available and embedded in the video.",
    "W tym filmie nie znaleziono napisów po polsku ani po angielsku.": "No Polish or English subtitles were found for this video.",
    "Napisy były dostępne, ale nie zostały scalone z filmem.": "Subtitles were available, but were not embedded into the video.",
    "Napisy scalone:": "Subtitles burned in:",
    "Mini: nie udało się skompresować pliku.": "Mini: could not compress the file.",
    "bez ponownej kompresji": "without recompression",
    "Mini: nie udało się odczytać długości pliku, nie mogę bezpiecznie obliczyć kompresji.": "Mini: could not read the file duration, so compression cannot be calculated safely.",
    "Mini: kompresuję plik do maks. 20 MB...": "Mini: compressing file to max. 20 MB...",
    "Mini: to nie jest aktualizacja programu, tylko kompresja pliku przez FFmpeg.": "Mini: this is not a program update, only file compression with FFmpeg.",
    "Mini: ta próba kompresji nie powiodła się.": "Mini: this compression attempt failed.",
    "Mini: żadna próba kompresji nie zakończyła się poprawnie.": "Mini: no compression attempt finished successfully.",
    "Mini: nie udało się ustalić ścieżki pobranego pliku.": "Mini: could not determine the downloaded file path.",
    "Napisy: w folderze został sam film z osadzonymi napisami.": "Subtitles: only the video with embedded subtitles remains in the folder.",
    "Program nie jest kompletny. Pobierz ponownie pełną paczkę.": "The program is incomplete. Download the full package again.",
    "Gotowe. Wszystko jest gotowe, możesz rozpocząć pobieranie.": "Ready. Everything is prepared, you can start downloading.",
    "OK: wszystko gotowe do pobierania.": "OK: everything is ready for downloading.",
    "Proces trwa": "Process running",
    "Poczekaj na zakończenie obecnej operacji albo użyj STOP.": "Wait for the current operation to finish or use STOP.",
    "Fix: sprawdzam wersję yt-dlp...": "Fix: checking yt-dlp version...",
    "Fix: wersja EXE nie modyfikuje własnych plików programu.": "Fix: the EXE version does not modify its own program files.",
    "Fix: nie znaleziono yt-dlp ani winget do automatycznej instalacji.": "Fix: yt-dlp or winget was not found for automatic installation.",
    "Fix: uruchamiam aktualizację yt-dlp.": "Fix: starting yt-dlp update.",
    "Fix: próbuję aktualizacji yt-dlp przez winget.": "Fix: trying yt-dlp update through winget.",
    "Fix: przygotowano aktualizowalną kopię yt-dlp w folderze danych aplikacji.": "Fix: prepared an updatable yt-dlp copy in the app data folder.",
    "Fix: aktualizacja działa od razu w lokalnym projekcie .pyw.": "Fix: the update works immediately in the local .pyw project.",
    "Fix: przy kolejnym buildzie ta wersja zostanie scalona z EXE przez Kompiluj_EXE_v7-0-7.bat.": "Fix: during the next build this version will be bundled into the EXE by Kompiluj_EXE_v7-0-7.bat.",
    "Fix: wykryto problem. Pobierz nową wersję programu z GitHuba.": "Fix: a problem was detected. Download a new version from GitHub.",
    "Fix: w wersji EXE nie aktualizuję plików programu lokalnie.": "Fix: in the EXE version, program files are not updated locally.",
    "Nie znaleziono komponentu yt-dlp w tej paczce programu.": "The yt-dlp component was not found in this program package.",
    "Ostatni błąd pobierania wygląda na problem po stronie yt-dlp albo zmian w serwisie.": "The last download error looks like an yt-dlp issue or a service-side change.",
    "Wykryto problem z komponentem yt-dlp.": "A problem with the yt-dlp component was detected.",
    "Fix: sprawdzam podstawowe błędy...": "Fix: checking basic errors...",
    "Fix: sprawdzam podstawowe błędy.": "Fix: checking basic errors.",
    "Fix przerwany przez użytkownika.": "Fix stopped by the user.",
    "Fix: przerwany przez użytkownika.": "Fix: stopped by the user.",
    "Sprawdzanie nie wykryło problemów.": "The check did not detect any problems.",
    "Wykryto problem z yt-dlp.": "A problem with yt-dlp was detected.",
    "Wymagana jest aktualizacja bazy/API.": "A database/API update is required.",
    "Po potwierdzeniu zostanie przeprowadzona lokalna aktualizacja projektu przed dystrybucją.": "After confirmation, a local project update will be performed before distribution.",
    "Fix yt-dlp": "Fix yt-dlp",
    "Wykryto problem z yt-dlp.\n\nWymagana jest aktualizacja bazy/API.\nPo potwierdzeniu zostanie przeprowadzona lokalna aktualizacja yt-dlp w projekcie .pyw przed dystrybucją.\n\nCzy rozpocząć aktualizację?": "A problem with yt-dlp was detected.\n\nA database/API update is required.\nAfter confirmation, a local yt-dlp update will be performed in the .pyw project before distribution.\n\nStart the update?",
    "Aktualizacja anulowana.": "Update cancelled.",
    "Fix: użytkownik anulował aktualizację.": "Fix: the user cancelled the update.",
    "Fix: aktualizuję yt-dlp...": "Fix: updating yt-dlp...",
    "Aktualizacja zakończyła się powodzeniem.": "Update completed successfully.",
    "Aktualizacja yt-dlp nie powiodła się.": "yt-dlp update failed.",
    "Fix: aktualizacja yt-dlp nie powiodła się. Szczegóły są powyżej w logu.": "Fix: yt-dlp update failed. Details are above in the log.",
    "Aktualizacja yt-dlp nie powiodła się. Sprawdź log.": "yt-dlp update failed. Check the log.",
    "Program nie jest gotowy": "Program is not ready",
    "Ta kopia programu nie zawiera wszystkich plików potrzebnych do pobierania.\n\nPobierz ponownie pełną paczkę programu od autora.": "This program copy does not contain all files required for downloading.\n\nDownload the full package from the author again.",
    "Brak komponentów": "Missing components",
    "Brakuje yt-dlp lub FFmpeg.\nAutomatyczna instalacja jest przygotowana dla Windows z winget.": "yt-dlp or FFmpeg is missing.\nAutomatic installation is prepared for Windows with winget.",
    "Brak winget": "Missing winget",
    "Nie znaleziono winget. Zainstaluj yt-dlp i FFmpeg ręcznie albo zaktualizuj App Installer.": "winget was not found. Install yt-dlp and FFmpeg manually or update App Installer.",
    "Wymagana instalacja": "Installation required",
    "Instalacja anulowana. Brak wymaganych komponentów.": "Installation cancelled. Required components are missing.",
    "Użytkownik nie wyraził zgody na instalację.": "The user did not agree to installation.",
    "Może pojawić się okno zgody systemu Windows. Nie zamykaj programu.": "A Windows consent window may appear. Do not close the program.",
    "Instalacja trwa zbyt długo": "Installation is taking too long",
    "Komponenty są gotowe.": "Components are ready.",
    "Uruchom ponownie program": "Restart the program",
    "Instalacja została zakończona, ale Windows może odświeżyć ścieżki PATH dopiero po ponownym uruchomieniu programu.\n\nZamknij aplikację i otwórz ją ponownie.": "Installation has finished, but Windows may refresh PATH only after restarting the program.\n\nClose the app and open it again.",
    "Brak linku": "Missing link",
    "Wklej link do filmu lub materiału.": "Paste a link to a video or media item.",
    "Błędny folder": "Invalid folder",
    "Wybierz poprawny folder zapisu.": "Choose a valid save folder.",
    "Tryb playlisty: program pobierze całą listę.": "Playlist mode: the program will download the full list.",
    "Uwaga - wykryto playlistę": "Attention - playlist detected",
    "Pobieranie anulowane.": "Download cancelled.",
    "Anulowano po wykryciu playlisty.": "Cancelled after detecting a playlist.",
    "Użytkownik wybrał pobranie całej playlisty.": "The user chose to download the full playlist.",
    "Użytkownik wybrał pobranie tylko pojedynczego utworu.": "The user chose to download only a single track.",
    "Brak formatu": "Missing format",
    "Wybierz jakość albo format pobierania.": "Choose the download quality or format.",
    "nieznany": "unknown",
    "FFmpeg - przetwarzanie/kompresja pliku": "FFmpeg - file processing/compression",
    "yt-dlp - aktualizacja": "yt-dlp - update",
    "yt-dlp - pobieranie": "yt-dlp - download",
    "winget - instalacja/aktualizacja komponentu": "winget - component installation/update",
    "Pobieranie przerwane.": "Download interrupted.",
    "Pobieranie i konwersja audio...": "Downloading and converting audio...",
    "Start pobierania audio...": "Starting audio download...",
    "Pobieranie przerwane przez użytkownika.": "Download stopped by the user.",
    "Przerwano": "Stopped",
    "Pobieranie zostało zatrzymane.": "Download has been stopped.",
    "Gotowe. Plik audio został zapisany w wybranym folderze.": "Done. The audio file was saved in the selected folder.",
    "Gotowe": "Done",
    "Pobieranie i konwersja zakończone.": "Download and conversion completed.",
    "Wystąpił błąd podczas pobierania audio.": "An error occurred while downloading audio.",
    "Błąd": "Error",
    "Nie udało się pobrać lub przekonwertować pliku. Sprawdź log.": "Could not download or convert the file. Check the log.",
    "Dostęp: ponawiam pobieranie standardowo.": "Access: retrying download with standard settings.",
    "Odczytuję playlistę...": "Reading playlist...",
    "Odczytuję listę elementów playlisty...": "Reading playlist items...",
    "Nie znaleziono elementów playlisty.": "No playlist items were found.",
    "Błąd playlisty": "Playlist error",
    "Nie udało się odczytać elementów playlisty. Sprawdź log.": "Could not read playlist items. Check the log.",
    "Każdy film będzie scalony/konwertowany przed rozpoczęciem kolejnego.": "Each video will be merged/converted before the next one starts.",
    "Pliki tymczasowe po poprawnej konwersji będą usuwane automatycznie.": "Temporary files will be removed automatically after successful conversion.",
    "Pobieranie playlisty wideo zakończone.": "Video playlist download completed.",
    "Zakończono z błędami": "Completed with errors",
    "Pobieranie wideo...": "Downloading video...",
    "Start pobierania wideo...": "Starting video download...",
    "Nie udało się skompresować pliku Mini. Sprawdź log.": "Could not compress the Mini file. Check the log.",
    "Gotowe. Wideo zostało zapisane w wybranym folderze.": "Done. The video was saved in the selected folder.",
    "Pobieranie wideo zakończone.": "Video download completed.",
    "Wystąpił błąd podczas pobierania wideo.": "An error occurred while downloading video.",
    "Nie udało się pobrać wideo. Sprawdź log.": "Could not download the video. Check the log.",
    "Zatrzymywanie pobierania...": "Stopping download...",
    "STOP: użytkownik przerwał pobieranie.": "STOP: the user interrupted the download.",
    "Pobieranie lub instalacja nadal trwa. Czy zatrzymać proces i zamknąć program?": "Download or installation is still running. Stop the process and close the program?",
}

MESSAGE_REPLACEMENTS_EN = [
    ("Autor:", "Author:"),
    ("Wersja programu:", "Program version:"),
    ("Nazwa:", "Name:"),
    ("Disclaimer: Nie ponosimy odpowiedzialności za sposób wykorzystania programu. Pobierając materiały, użytkownik potwierdza, że ma do tego prawo.", "Disclaimer: We are not responsible for how the program is used. By downloading materials, the user confirms that they have the right to do so."),
    ("Dane triala zostały zmienione lub uszkodzone.", "Trial data has been changed or damaged."),
    ("Zegar systemowy jest cofnięty względem daty kompilacji programu.", "The system clock is set before the program build date."),
    ("Wykryto cofnięcie zegara systemowego.", "A system clock rollback was detected."),
    ("Data startu triala jest nieprawidłowa.", "The trial start date is invalid."),
    ("Pobieranie zostało zablokowane. Skontaktuj się z autorem, aby otrzymać nową wersję programu.", "Downloading has been blocked. Contact the author to receive a new program version."),
    ("Czas testów tej wersji programu minął.", "The test period for this program version has expired."),
    ("Plik programu nie przechodzi kontroli podpisu albo został zmieniony po kompilacji.", "The program file does not pass signature verification or was changed after compilation."),
    ("Uruchom oryginalny, podpisany plik EXE.", "Run the original signed EXE file."),
    ("Program zablokowany:", "Program blocked:"),
    ("Mini: trwa kompresja...", "Mini: compression in progress..."),
    ("czas ", "time "),
    ("Napisy: nie udało się odczytać danych napisów:", "Subtitles: could not read subtitle data:"),
    ("Napisy zostały scalone z filmem.", "Subtitles were embedded into the video."),
    ("Napisy zostały wtopione w obraz filmu.", "Subtitles were burned into the video image."),
    ("Napisy były wykryte, ale nie udało się ich scalić z filmem.", "Subtitles were detected, but could not be embedded into the video."),
    ("W tym filmie nie znaleziono napisów po polsku lub angielsku.", "No Polish or English subtitles were found for this video."),
    ("Subtitles: Subtitles were detected, but could not be downloaded or embedded.", "Subtitles: detected, but could not be downloaded or embedded."),
    ("Subtitles: Subtitles were available and embedded in the video.", "Subtitles: available and embedded in the video."),
    ("Subtitles: No regular or automatic Polish or English subtitles were found for this video.", "Subtitles: no regular or automatic Polish or English subtitles were found for this video."),
    ("Napisy: znaleziono język", "Subtitles: found language"),
    ("Napisy: ffprobe:", "Subtitles: ffprobe:"),
    ("polskim", "Polish"),
    ("angielskim", "English"),
    (", źródło:", ", source:"),
    ("napisy automatyczne", "automatic subtitles"),
    ("napisy", "subtitles"),
    ("Zostaną wtopione w obraz filmu.", "They will be burned into the video image."),
    ("Napisy były dostępne i zostały zintegrowane z filmem.", "Subtitles were available and embedded in the video."),
    ("Język:", "Language:"),
    ("Mini: ffprobe:", "Mini: ffprobe:"),
    ("Mini: skompresowano do", "Mini: compressed to"),
    ("Zmniejszenie:", "Reduction:"),
    ("Parametry:", "Parameters:"),
    ("Mini: nie udało się zejść do 20 MB, ale zapisano najmniejszy uzyskany plik:", "Mini: could not get below 20 MB, but saved the smallest generated file:"),
    ("Mini: nie znaleziono pliku do kompresji:", "Mini: compression file not found:"),
    ("Mini: kompresja do maks. 20 MB. Rozmiar wejściowy:", "Mini: compression to max. 20 MB. Input size:"),
    ("Mini: próba kompresji", "Mini: compression attempt"),
    ("wideo", "video"),
    ("audio", "audio"),
    ("obsługa audio i video", "audio and video support"),
    ("Mini: rozmiar po kompresji:", "Mini: size after compression:"),
    ("Napisy: usunięto osobny plik napisów:", "Subtitles: removed separate subtitle file:"),
    ("Napisy: nie udało się usunąć osobnego pliku", "Subtitles: could not remove separate file"),
    ("Bez napisów PL/EN:", "Without PL/EN subtitles:"),
    ("program pobierania", "download engine"),
    ("obsługa audio i wideo", "audio and video support"),
    ("Brakuje plików programu:", "Missing program files:"),
    ("Brakuje komponentów:", "Missing components:"),
    ("Program zapyta o instalację przy pobieraniu.", "The program will ask to install them when downloading."),
    ("Fix: yt-dlp nie uruchamia się poprawnie:", "Fix: yt-dlp does not start correctly:"),
    ("Fix: wykryta wersja yt-dlp:", "Fix: detected yt-dlp version:"),
    ("Fix: najnowsza wersja yt-dlp na GitHubie:", "Fix: latest yt-dlp version on GitHub:"),
    ("Fix: nie udało się sprawdzić najnowszej wersji yt-dlp na GitHubie:", "Fix: could not check the latest yt-dlp version on GitHub:"),
    ("Fix: pobieranie yt-dlp z GitHuba nie powiodło się:", "Fix: downloading yt-dlp from GitHub failed:"),
    ("Fix: aktualizacja yt-dlp przez -U zwróciła kod", "Fix: yt-dlp update through -U returned code"),
    ("Fix: nie udało się przygotować kopii yt-dlp w folderze danych aplikacji:", "Fix: could not prepare a yt-dlp copy in the app data folder:"),
    ("Fix: pobieram yt-dlp", "Fix: downloading yt-dlp"),
    ("pobrany plik yt-dlp.exe jest podejrzanie mały", "downloaded yt-dlp.exe is suspiciously small"),
    ("pobrany yt-dlp.exe nie uruchamia się poprawnie", "downloaded yt-dlp.exe does not start correctly"),
    ("Fix: zainstalowana wersja yt-dlp:", "Fix: installed yt-dlp version:"),
    ("Fix: uwaga, GitHub zgłasza", "Fix: warning, GitHub reports"),
    ("a plik uruchamia się jako", "but the file starts as"),
    ("Fix: po naprawie autora szukaj nowej wersji tutaj:", "Fix: after the author's repair, look for the new version here:"),
    ("Wykryto nieaktualny komponent yt-dlp. Najnowsza znana wersja:", "An outdated yt-dlp component was detected. Latest known version:"),
    ("Ta skompilowana wersja EXE nie naprawia samej siebie, żeby nie naruszać podpisu", "This compiled EXE version does not repair itself, to avoid breaking the signature"),
    ("i nie zostawiać dodatkowych plików przy programie.", "and leaving additional files next to the program."),
    ("Po naprawie przez autora pobierz nową wersję programu z repozytorium:", "After the author's repair, download the new version from the repository:"),
    ("Do poprawnego działania programu trzeba zainstalować:", "For the program to work correctly, install:"),
    ("Program użyje winget. Może pojawić się okno zgody systemu Windows.", "The program will use winget. A Windows consent window may appear."),
    ("Czy wyrażasz zgodę na instalację?", "Do you agree to the installation?"),
    ("Instaluję", "Installing"),
    ("Instalacja:", "Installation:"),
    ("OK: instalator zakończył pracę dla", "OK: installer finished for"),
    ("jest już zainstalowany.", "is already installed."),
    ("UWAGA: winget zwrócił kod", "WARNING: winget returned code"),
    (" przy ", " for "),
    ("TIMEOUT: instalacja", "TIMEOUT: installation of"),
    ("trwała ponad", "took more than"),
    ("sekund. Proces został przerwany, żeby program nie wyglądał na zawieszony.", "seconds. The process was stopped so the program would not appear frozen."),
    ("Instalacja", "Installation"),
    ("Installation zakończona, ale program nadal nie widzi:", "Installation finished, but the program still cannot see:"),
    ("trwała zbyt długo i została zatrzymana.", "took too long and was stopped."),
    ("Możliwe, że winget czekał na zgodę systemu, administratora albo miał problem sieciowy.", "winget may have been waiting for system/admin consent or had a network issue."),
    ("Spróbuj uruchomić program ponownie albo zainstalować komponent ręcznie.", "Try running the program again or install the component manually."),
    ("Błąd instalacji", "Installation error for"),
    ("Instalacja zakończona, ale program nadal nie widzi:", "Installation finished, but the program still cannot see:"),
    ("Wklejony link wygląda jak playlista YouTube.", "The pasted link looks like a YouTube playlist."),
    ("TAK - pobierz wszystkie pliki z playlisty.", "YES - download all files from the playlist."),
    ("NIE - pobierz tylko pojedynczy utwór/film z tego linku.", "NO - download only a single track/video from this link."),
    ("ANULUJ - przerwij operację.", "CANCEL - stop the operation."),
    ("Link oczyszczony z playlisty:", "Link cleaned from playlist parameters:"),
    ("Tryb:", "Mode:"),
    ("cała playlista", "entire playlist"),
    ("tylko pojedynczy utwór", "single track only"),
    ("tylko pojedynczy film", "single video only"),
    ("Format audio:", "Audio format:"),
    ("Format wideo:", "Video format:"),
    (", jakość:", ", quality:"),
    ("Dostęp: ponawiam pobieranie", "Access: retrying download"),
    ("Ponawiam pobieranie", "Retrying download"),
    ("standardowo", "with standard settings"),
    ("z naglowkami przegladarki", "with browser headers"),
    ("Nie udało się odczytać playlisty. Kod błędu:", "Could not read playlist. Error code:"),
    ("Nie udało się odczytać danych playlisty:", "Could not read playlist data:"),
    ("Znaleziono elementów playlisty:", "Playlist items found:"),
    ("Playlista: pobieranie", "Playlist: downloading"),
    ("Element playlisty", "Playlist item"),
    ("Błąd: element", "Error: item"),
    ("nie został poprawnie skompresowany w trybie Mini.", "was not correctly compressed in Mini mode."),
    ("OK: element", "OK: item"),
    ("zakończony i przekonwertowany.", "finished and converted."),
    ("zakończył się kodem", "finished with code"),
    ("Przerwano playlistę. Gotowe pliki:", "Playlist stopped. Completed files:"),
    ("Pobieranie playlisty zostało zatrzymane.", "Playlist download has been stopped."),
    ("Poprawnie zakończone pliki:", "Successfully completed files:"),
    ("Napisy dodane:", "Subtitles added:"),
    ("Bez napisów PL/EN:", "Without PL/EN subtitles:"),
    ("Gotowe. Playlista wideo zakończona:", "Done. Video playlist completed:"),
    ("Gotowe. Playlista video zakończona:", "Done. Video playlist completed:"),
    ("Playlista zakończona z błędami. Gotowe:", "Playlist completed with errors. Done:"),
    ("Poprawnie pobrano:", "Successfully downloaded:"),
    ("Błędy:", "Errors:"),
    ("Szczegóły są w logu.", "Details are in the log."),
    ("Napisy:", "Subtitles:"),
    ("Gotowe. Wideo zapisane.", "Done. Video saved."),
    ("Pobieranie wideo zakończone.", "Video download completed."),
    ("Pobieranie video zakończone.", "Video download completed."),
    ("Nie udało się zatrzymać procesu normalnie:", "Could not stop the process normally:"),
]


def get_tool_executable_name(command: str) -> str:
    if os.name == "nt" and not command.lower().endswith(".exe"):
        return f"{command}.exe"
    return command


def get_app_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def get_app_data_dir():
    base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
    if base:
        return Path(base) / "VideoAndSoundDownloaderPro"
    return Path.home() / ".VideoAndSoundDownloaderPro"


def get_external_tools_dir():
    if not getattr(sys, "frozen", False):
        return get_app_dir() / TOOLS_DIR_NAME
    return get_app_data_dir() / TOOLS_DIR_NAME


def get_bundled_tool_path(command: str):
    executable_name = get_tool_executable_name(command)
    roots = []
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        roots.append(Path(sys._MEIPASS))
    else:
        roots.append(Path(__file__).resolve().parent)

    for root in roots:
        candidate = root / TOOLS_DIR_NAME / executable_name
        if candidate.exists():
            return candidate
    return None


def get_bundled_tools_dir():
    for command in ("yt-dlp", "ffmpeg", "ffprobe"):
        tool_path = get_bundled_tool_path(command)
        if tool_path:
            return tool_path.parent
    return None


def get_bundled_tool_dirs():
    dirs = []
    seen = set()
    for command in ("yt-dlp", "ffmpeg", "ffprobe"):
        tool_path = get_bundled_tool_path(command)
        if not tool_path:
            continue
        key = str(tool_path.parent).lower()
        if key not in seen:
            seen.add(key)
            dirs.append(tool_path.parent)
    return dirs


def resolve_tool_command(command: str) -> str:
    bundled_path = get_bundled_tool_path(command)
    if bundled_path:
        return str(bundled_path)
    return shutil.which(command) or command


def command_exists(command: str) -> bool:
    return get_bundled_tool_path(command) is not None or shutil.which(command) is not None


def get_process_environment():
    env = os.environ.copy()
    tool_dirs = get_bundled_tool_dirs()
    if tool_dirs:
        env["PATH"] = os.pathsep.join(str(path) for path in tool_dirs) + os.pathsep + env.get("PATH", "")
    return env


def no_window_creation_flags() -> int:
    return subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def is_probably_youtube_playlist(url: str) -> bool:
    try:
        parsed = urlparse(url.strip())
        query = parse_qs(parsed.query)
        return "list" in query and bool(query.get("list", [""])[0])
    except Exception:
        return False


def strip_playlist_params(url: str) -> str:
    try:
        parsed = urlparse(url.strip())
        query = parse_qs(parsed.query)

        if "v" in query and query["v"]:
            new_query = urlencode({"v": query["v"][0]})
            return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", new_query, ""))

        if "youtu.be" in parsed.netloc and parsed.path:
            return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))

        return url
    except Exception:
        return url


class VideoDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.colors = {
            "bg": "#07111f",
            "card": "#0d1726",
            "panel": "#111d2d",
            "panel_hover": "#142b46",
            "border": "#22344b",
            "border_strong": "#2f8cff",
            "text": "#e8f1ff",
            "muted": "#8ca0b8",
            "muted_2": "#64748b",
            "blue": "#1768e8",
            "blue_hover": "#1f7cff",
            "green": "#35e879",
            "red": "#ef4444",
            "red_hover": "#f87171",
        }

        self.title(f"{APP_TITLE} {APP_VERSION}")
        self.apply_window_icon()
        self.geometry("980x760")
        self.minsize(940, 720)
        self.configure(fg_color=self.colors["bg"])

        self.save_dir = tk.StringVar(master=self, value=get_default_save_dir())
        self.url = tk.StringVar(master=self)
        self.language_var = tk.StringVar(master=self, value="PL")
        self.language = "PL"
        self.quality_var = tk.StringVar(master=self, value=MODE_DEFAULT_QUALITY["MP3"])
        self.subtitles_var = tk.BooleanVar(master=self, value=False)
        self.subtitle_status_var = tk.StringVar(
            master=self,
            value="Najpierw polskie, w razie braku angielskie. Napisy będą w filmie.",
        )
        self.last_status_source = "Gotowe."
        self.status = tk.StringVar(master=self, value="Gotowe.")

        self.selected_mode = "MP3"
        self.mode_cards = {}
        self.ui_text_widgets = {}
        self.log_source_lines = []
        self.current_process = None
        self.active_progress_label = ""
        self.last_process_output_lines = []
        self.stop_requested = False
        self.process_lock = threading.Lock()
        self.trial_expired = False
        self.self_integrity_checked = False
        self.self_integrity_failed = False

        self.build_ui()
        self.select_mode("MP3")
        self.after(500, self.check_components_only)
        self.after(700, self.enforce_trial_status)
        self.after(150, self.url_entry.focus_set)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_card = ctk.CTkFrame(
            self,
            corner_radius=24,
            fg_color=self.colors["card"],
            border_width=1,
            border_color="#1f3147",
        )
        main_card.grid(row=0, column=0, padx=20, pady=18, sticky="nsew")
        main_card.grid_columnconfigure(0, weight=1)
        main_card.grid_rowconfigure(8, weight=1, minsize=120)

        header = ctk.CTkFrame(main_card, fg_color="transparent")
        header.grid(row=0, column=0, padx=28, pady=(18, 8), sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        app_icon = ctk.CTkLabel(
            header,
            text="↓",
            width=42,
            height=42,
            corner_radius=21,
            fg_color="#10243a",
            text_color="#8bd8ff",
            font=("Segoe UI", 24, "bold"),
        )
        app_icon.grid(row=0, column=0, rowspan=2, sticky="w", padx=(0, 12))

        title = ctk.CTkLabel(
            header,
            text=APP_TITLE,
            font=("Segoe UI", 22, "bold"),
            text_color=self.colors["text"],
        )
        title.grid(row=0, column=1, sticky="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Pobieraj audio, wideo i playlisty z jednego panelu",
            font=("Segoe UI", 12),
            text_color=self.colors["muted"],
        )
        subtitle.grid(row=1, column=1, sticky="w", pady=(1, 0))
        self.ui_text_widgets["subtitle"] = (subtitle, "Pobieraj audio, wideo i playlisty z jednego panelu")

        right_header = ctk.CTkFrame(header, fg_color="transparent")
        right_header.grid(row=0, column=2, rowspan=2, sticky="e")

        version = ctk.CTkLabel(
            right_header,
            text=f"v{APP_VERSION}",
            width=66,
            height=26,
            corner_radius=13,
            fg_color="#13243a",
            text_color="#9fb5d1",
            font=("Segoe UI", 11, "bold"),
        )
        version.grid(row=0, column=0, sticky="e")

        self.language_label = ctk.CTkLabel(
            right_header,
            text="Wybierz język",
            font=("Segoe UI", 10, "bold"),
            text_color="#9fb5d1",
        )
        self.language_label.grid(row=1, column=0, sticky="e", pady=(4, 2))
        self.ui_text_widgets["language_label"] = (self.language_label, "Wybierz język")

        self.language_switch = ctk.CTkSegmentedButton(
            right_header,
            values=["PL", "EN"],
            variable=self.language_var,
            width=96,
            height=26,
            corner_radius=10,
            fg_color="#13243a",
            selected_color=self.colors["blue"],
            selected_hover_color=self.colors["blue_hover"],
            unselected_color="#13243a",
            unselected_hover_color="#1b3558",
            text_color="#e8f1ff",
            font=("Segoe UI", 10, "bold"),
            command=self.change_language,
        )
        self.language_switch.grid(row=2, column=0, sticky="e")
        self.language_switch.set("PL")

        link_label = ctk.CTkLabel(
            main_card,
            text="Link:",
            font=("Segoe UI", 13, "bold"),
            text_color="#b9c7d9",
        )
        link_label.grid(row=1, column=0, padx=28, pady=(6, 4), sticky="w")
        self.ui_text_widgets["link_label"] = (link_label, "Link:")

        link_row = ctk.CTkFrame(main_card, fg_color="transparent")
        link_row.grid(row=2, column=0, padx=28, pady=(0, 14), sticky="ew")
        link_row.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(
            link_row,
            textvariable=self.url,
            height=42,
            corner_radius=12,
            fg_color=self.colors["panel"],
            border_color=self.colors["border"],
            text_color=self.colors["text"],
            placeholder_text="Wklej link z YouTube, Facebooka albo innej obsługiwanej strony...",
            placeholder_text_color=self.colors["muted_2"],
            font=("Segoe UI", 12),
        )
        self.url_entry.grid(row=0, column=0, sticky="ew")

        self.paste_btn = ctk.CTkButton(
            link_row,
            text="🔗",
            width=46,
            height=42,
            corner_radius=12,
            fg_color="#142236",
            hover_color="#1b3558",
            text_color="#cce6ff",
            font=("Segoe UI", 18),
            command=self.paste_from_clipboard,
        )
        self.paste_btn.grid(row=0, column=1, padx=(10, 0))

        option_header = ctk.CTkFrame(main_card, fg_color="transparent")
        option_header.grid(row=3, column=0, padx=28, pady=(0, 7), sticky="ew")
        option_header.grid_columnconfigure(0, weight=1)

        option_label = ctk.CTkLabel(
            option_header,
            text="Wybierz opcję:",
            font=("Segoe UI", 13, "bold"),
            text_color="#b9c7d9",
        )
        option_label.grid(row=0, column=0, sticky="w")
        self.ui_text_widgets["option_label"] = (option_label, "Wybierz opcję:")

        self.subtitle_option_frame = ctk.CTkFrame(option_header, fg_color="transparent")
        self.subtitle_option_frame.grid(row=0, column=1, sticky="e")

        self.subtitle_switch = ctk.CTkSwitch(
            self.subtitle_option_frame,
            text="Napisy do filmu",
            variable=self.subtitles_var,
            onvalue=True,
            offvalue=False,
            progress_color=self.colors["blue"],
            button_color="#cce6ff",
            button_hover_color="#ffffff",
            fg_color="#25374f",
            text_color="#b9c7d9",
            font=("Segoe UI", 11),
        )
        self.subtitle_switch.grid(row=0, column=0, sticky="e")
        self.ui_text_widgets["subtitle_switch"] = (self.subtitle_switch, "Napisy do filmu")

        cards_row = ctk.CTkFrame(main_card, fg_color="transparent")
        cards_row.grid(row=4, column=0, padx=28, pady=(0, 12), sticky="ew")
        for index in range(4):
            cards_row.grid_columnconfigure(index, weight=1, uniform="modecards")

        self.create_mode_card(cards_row, "MP3", "♫", "MP3", "Pobierz dźwięk", "#d35cff", 0)
        self.create_mode_card(cards_row, "MP4", "■", "MP4", "Pobierz wideo", "#24a8ff", 1)
        self.create_mode_card(cards_row, "PLAYLISTA", "☷", "PLAYLISTA", "Pobierz całą listę", "#35e879", 2)
        self.create_mode_card(cards_row, "FACEBOOK", "f", "FACEBOOK", "Pobierz wideo", "#4b8dff", 3)

        settings = ctk.CTkFrame(main_card, fg_color="transparent")
        settings.grid(row=5, column=0, padx=28, pady=(0, 14), sticky="ew")
        settings.grid_columnconfigure(0, weight=1)
        settings.grid_columnconfigure(1, weight=2)

        quality_group = ctk.CTkFrame(settings, fg_color="transparent")
        quality_group.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        quality_group.grid_columnconfigure(0, weight=1)

        quality_label = ctk.CTkLabel(
            quality_group,
            text="Jakość / Format:",
            font=("Segoe UI", 13, "bold"),
            text_color="#b9c7d9",
        )
        quality_label.grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.ui_text_widgets["quality_label"] = (quality_label, "Jakość / Format:")

        self.quality_box = ctk.CTkComboBox(
            quality_group,
            variable=self.quality_var,
            values=MODE_QUALITY_OPTIONS["MP3"],
            height=40,
            corner_radius=12,
            fg_color=self.colors["panel"],
            border_color=self.colors["border"],
            button_color="#182a42",
            button_hover_color="#22436e",
            dropdown_fg_color=self.colors["panel"],
            dropdown_hover_color="#1c3454",
            text_color=self.colors["text"],
            dropdown_text_color=self.colors["text"],
            font=("Segoe UI", 12),
            state="readonly",
        )
        self.quality_box.grid(row=1, column=0, sticky="ew")

        folder_group = ctk.CTkFrame(settings, fg_color="transparent")
        folder_group.grid(row=0, column=1, sticky="ew")
        folder_group.grid_columnconfigure(0, weight=1)

        folder_label = ctk.CTkLabel(
            folder_group,
            text="Zapisz do:",
            font=("Segoe UI", 13, "bold"),
            text_color="#b9c7d9",
        )
        folder_label.grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.ui_text_widgets["folder_label"] = (folder_label, "Zapisz do:")

        folder_row = ctk.CTkFrame(folder_group, fg_color="transparent")
        folder_row.grid(row=1, column=0, sticky="ew")
        folder_row.grid_columnconfigure(0, weight=1)

        self.path_entry = ctk.CTkEntry(
            folder_row,
            textvariable=self.save_dir,
            height=40,
            corner_radius=12,
            fg_color=self.colors["panel"],
            border_color=self.colors["border"],
            text_color=self.colors["text"],
            font=("Segoe UI", 12),
        )
        self.path_entry.grid(row=0, column=0, sticky="ew")

        self.browse_btn = ctk.CTkButton(
            folder_row,
            text="📁",
            width=46,
            height=40,
            corner_radius=12,
            fg_color="#142236",
            hover_color="#1b3558",
            text_color="#cce6ff",
            font=("Segoe UI", 18),
            command=self.choose_folder,
        )
        self.browse_btn.grid(row=0, column=1, padx=(10, 0))

        action_row = ctk.CTkFrame(main_card, fg_color="transparent")
        action_row.grid(row=6, column=0, padx=28, pady=(0, 12), sticky="ew")
        action_row.grid_columnconfigure(0, weight=1)

        self.download_btn = ctk.CTkButton(
            action_row,
            text="↓   POBIERZ",
            height=48,
            corner_radius=13,
            fg_color=self.colors["blue"],
            hover_color=self.colors["blue_hover"],
            text_color="#eef6ff",
            font=("Segoe UI", 15, "bold"),
            command=self.start_download,
        )
        self.download_btn.grid(row=0, column=0, sticky="ew")

        self.stop_btn = ctk.CTkButton(
            action_row,
            text="STOP",
            width=120,
            height=48,
            corner_radius=13,
            fg_color="#3b1720",
            hover_color=self.colors["red_hover"],
            text_color="#ffd7dd",
            font=("Segoe UI", 14, "bold"),
            command=self.stop_download,
            state="disabled",
        )
        self.stop_btn.grid(row=0, column=1, padx=(12, 0))

        status_row = ctk.CTkFrame(main_card, fg_color="transparent")
        status_row.grid(row=7, column=0, padx=28, pady=(0, 8), sticky="ew")
        status_row.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            status_row,
            textvariable=self.status,
            height=30,
            corner_radius=15,
            fg_color="#101f33",
            text_color="#b9c7d9",
            font=("Segoe UI", 12),
            anchor="w",
            padx=12,
        )
        self.status_label.grid(row=0, column=0, sticky="ew")

        log_frame = ctk.CTkFrame(
            main_card,
            corner_radius=16,
            fg_color="#0a1422",
            border_width=1,
            border_color="#1f3147",
        )
        log_frame.grid(row=8, column=0, padx=28, pady=(0, 12), sticky="nsew")
        log_frame.grid_propagate(False)
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)

        log_header = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_header.grid(row=0, column=0, padx=14, pady=(10, 4), sticky="ew")
        log_header.grid_columnconfigure(2, weight=1)

        log_label = ctk.CTkLabel(
            log_header,
            text="Log",
            font=("Segoe UI", 13, "bold"),
            text_color="#b9c7d9",
        )
        log_label.grid(row=0, column=0, sticky="w")
        self.ui_text_widgets["log_label"] = (log_label, "Log")

        self.spinner_symbols = ["◐", "◓", "◑", "◒"]
        self.spinner_index = 0
        self.spinner_job = None
        self.spinner_label = ctk.CTkLabel(
            log_header,
            text="",
            width=24,
            font=("Segoe UI", 15, "bold"),
            text_color="#2f8cff",
        )
        self.spinner_label.grid(row=0, column=1, padx=(8, 0), sticky="w")

        self.log = ctk.CTkTextbox(
            log_frame,
            height=110,
            corner_radius=12,
            fg_color="#07111f",
            border_width=1,
            border_color="#1f3147",
            text_color="#d8e7fb",
            font=("Consolas", 11),
            wrap="word",
        )
        self.log.grid(row=1, column=0, padx=14, pady=(0, 14), sticky="nsew")
        self.log.configure(state="disabled")

        footer = ctk.CTkFrame(main_card, fg_color="transparent")
        footer.grid(row=9, column=0, padx=28, pady=(0, 10), sticky="ew")
        footer.grid_columnconfigure(1, weight=1)
        footer.grid_columnconfigure(3, weight=1)

        self.support_btn = self.create_footer_button(footer, "Wsparcie", self.open_support_page)
        self.support_btn.grid(row=0, column=0, padx=(0, 8), sticky="w")
        self.ui_text_widgets["support_btn"] = (self.support_btn, "Wsparcie")

        self.fix_btn = self.create_footer_button(footer, "Fix", self.start_fix)
        self.fix_btn.grid(row=0, column=2)
        self.ui_text_widgets["fix_btn"] = (self.fix_btn, "Fix")

        self.about_btn = self.create_footer_button(footer, "O mnie", self.show_about)
        self.about_btn.grid(row=0, column=4, sticky="e")
        self.ui_text_widgets["about_btn"] = (self.about_btn, "O mnie")

        self.apply_language()

    def apply_window_icon(self):
        png_path = get_resource_path(APP_ICON_PNG_FILE_NAME)
        ico_path = get_resource_path(APP_ICON_FILE_NAME)

        if png_path.exists():
            try:
                self.window_icon_image = tk.PhotoImage(file=str(png_path))
                self.iconphoto(True, self.window_icon_image)
                return
            except tk.TclError:
                pass

        if ico_path.exists():
            try:
                self.iconbitmap(str(ico_path))
            except tk.TclError:
                pass

    def tr_ui(self, text):
        if self.language == "EN":
            return UI_TEXT_EN.get(text, text)
        return text

    def translate_message(self, text):
        if self.language != "EN" or not isinstance(text, str):
            return text

        translated = MESSAGE_EXACT_EN.get(text)
        if translated is not None:
            return translated

        translated = UI_TEXT_EN.get(text, text)
        for source, target in sorted(MESSAGE_EXACT_EN.items(), key=lambda item: len(item[0]), reverse=True):
            if len(source) >= 12:
                translated = translated.replace(source, target)
        for source, target in MESSAGE_REPLACEMENTS_EN:
            translated = translated.replace(source, target)
        translated = translated.replace(
            "Subtitles: Subtitles were detected, but could not be downloaded or embedded.",
            "Subtitles: detected, but could not be downloaded or embedded.",
        )
        translated = translated.replace(
            "Subtitles: Subtitles were detected, but the subtitle file could not be downloaded.",
            "Subtitles: detected, but the subtitle file could not be downloaded.",
        )
        translated = translated.replace(
            "Subtitles: Subtitles were available and embedded in the video.",
            "Subtitles: available and embedded in the video.",
        )
        translated = translated.replace(
            "Subtitles: Subtitles were embedded into the video.",
            "Subtitles: embedded into the video.",
        )
        translated = translated.replace(
            "Subtitles: No regular or automatic Polish or English subtitles were found for this video.",
            "Subtitles: no regular or automatic Polish or English subtitles were found for this video.",
        )
        translated = translated.replace(
            "Subtitles: No regular Polish or English subtitles were found for this video.",
            "Subtitles: no regular Polish or English subtitles were found for this video.",
        )
        return translated

    def tr_quality_label(self, label):
        if self.language == "EN":
            return QUALITY_LABELS_EN.get(label, label)
        return label

    def quality_label_to_key(self, label):
        return QUALITY_LABELS_PL_BY_EN.get(label, label)

    def get_quality_options_for_mode(self, mode):
        return [self.tr_quality_label(label) for label in MODE_QUALITY_OPTIONS[mode]]

    def get_default_quality_for_mode(self, mode):
        return self.tr_quality_label(MODE_DEFAULT_QUALITY[mode])

    def change_language(self, selected_language):
        if selected_language not in LANGUAGE_LABELS:
            selected_language = "PL"
        self.language = selected_language
        self.language_var.set(selected_language)
        if self.language == "EN":
            self.subtitles_var.set(False)
        self.apply_language()

    def apply_language(self):
        for widget, source_text in self.ui_text_widgets.values():
            widget.configure(text=self.tr_ui(source_text))

        if hasattr(self, "url_entry"):
            self.url_entry.configure(
                placeholder_text=self.tr_ui("Wklej link z YouTube, Facebooka albo innej obsługiwanej strony...")
            )

        for key, card in self.mode_cards.items():
            card["title"].configure(text=self.tr_ui(card["title_text"]))
            card["subtitle"].configure(text=self.tr_ui(card["subtitle_text"]))

        if hasattr(self, "quality_box"):
            current_key = self.quality_label_to_key(self.quality_var.get())
            choices = self.get_quality_options_for_mode(self.selected_mode)
            self.quality_box.configure(values=choices)
            if current_key in MODE_QUALITY_OPTIONS[self.selected_mode]:
                self.quality_box.set(self.tr_quality_label(current_key))
            else:
                self.quality_box.set(self.get_default_quality_for_mode(self.selected_mode))

        if hasattr(self, "download_btn") and not self.trial_expired:
            self.update_download_button_text()

        if hasattr(self, "subtitle_status_var"):
            self.update_subtitle_option_visibility()

        self.status.set(self.translate_message(self.last_status_source))
        self.render_log()

    def create_footer_button(self, parent, text, command):
        return ctk.CTkButton(
            parent,
            text=text,
            width=112,
            height=32,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#13243a",
            border_width=1,
            border_color="#203a59",
            text_color="#aabbd2",
            font=("Segoe UI", 12),
            command=command,
        )

    def show_dialog(self, title, message, buttons=None, default=None):
        if buttons is None:
            buttons = [("OK", "ok")]

        title = self.translate_message(title)
        message = self.translate_message(message)
        buttons = [(self.tr_ui(label), value) for label, value in buttons]
        result = {"value": default if default is not None else buttons[0][1]}

        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("560x340")
        dialog.resizable(False, False)
        dialog.configure(fg_color=self.colors["card"])
        dialog.transient(self)

        frame = ctk.CTkFrame(
            dialog,
            corner_radius=18,
            fg_color="#0d1726",
            border_width=1,
            border_color="#1f3147",
        )
        frame.pack(fill="both", expand=True, padx=16, pady=16)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 18, "bold"),
            text_color=self.colors["green"],
            anchor="w",
        )
        title_label.grid(row=0, column=0, padx=20, pady=(18, 8), sticky="ew")

        message_label = ctk.CTkLabel(
            frame,
            text=message,
            font=("Segoe UI", 13),
            text_color="#8ff0b5",
            justify="left",
            anchor="nw",
            wraplength=490,
        )
        message_label.grid(row=1, column=0, padx=20, pady=(0, 12), sticky="nsew")

        button_row = ctk.CTkFrame(frame, fg_color="transparent")
        button_row.grid(row=2, column=0, padx=20, pady=(0, 18), sticky="e")

        def close_with(value):
            result["value"] = value
            dialog.grab_release()
            dialog.destroy()

        for index, (label, value) in enumerate(buttons):
            button = ctk.CTkButton(
                button_row,
                text=label,
                width=112,
                height=34,
                corner_radius=10,
                fg_color="transparent",
                hover_color="#13243a",
                border_width=1,
                border_color="#203a59",
                text_color="#24a8ff",
                font=("Segoe UI", 12, "bold"),
                command=lambda selected=value: close_with(selected),
            )
            button.grid(row=0, column=index, padx=(8 if index else 0, 0))

        dialog.protocol("WM_DELETE_WINDOW", lambda: close_with(default))
        dialog.update_idletasks()
        self.update_idletasks()

        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_w = self.winfo_width()
        parent_h = self.winfo_height()
        dialog_w = dialog.winfo_width()
        dialog_h = dialog.winfo_height()
        x = parent_x + max((parent_w - dialog_w) // 2, 0)
        y = parent_y + max((parent_h - dialog_h) // 2, 0)
        dialog.geometry(f"+{x}+{y}")

        dialog.grab_set()
        dialog.focus_force()
        self.wait_window(dialog)
        return result["value"]

    def show_info_dialog(self, title, message):
        self.show_dialog(title, message, buttons=[("OK", "ok")], default="ok")

    def ask_yes_no_dialog(self, title, message):
        return self.show_dialog(
            title,
            message,
            buttons=[("TAK", True), ("NIE", False)],
            default=False,
        )

    def ask_yes_no_cancel_dialog(self, title, message):
        return self.show_dialog(
            title,
            message,
            buttons=[("TAK", True), ("NIE", False), ("ANULUJ", None)],
            default=None,
        )

    def get_effective_trial_days(self):
        try:
            days = int(TRIAL_DAYS)
        except Exception:
            days = TRIAL_DEFAULT_DAYS

        if not getattr(sys, "frozen", False) and days <= 0:
            return 0

        if days < 1 or days > TRIAL_MAX_DAYS:
            return TRIAL_DEFAULT_DAYS
        return days

    def get_trial_build_started_at(self, now):
        try:
            build_started_at = int(TRIAL_BUILD_STARTED_AT)
        except Exception:
            build_started_at = 0
        if build_started_at <= 0:
            return now
        return build_started_at

    def get_trial_state_path(self):
        paths = self.get_trial_state_paths()
        return paths[0]

    def get_trial_state_paths(self):
        candidates = []

        def add_candidate(base_dir):
            if not base_dir:
                return
            try:
                folder = Path(base_dir) / "VideoAndSoundDownloaderPro"
                folder.mkdir(parents=True, exist_ok=True)
                candidates.append(folder / TRIAL_STATE_FILE_NAME)
            except Exception:
                return

        add_candidate(os.environ.get("LOCALAPPDATA"))
        add_candidate(os.environ.get("APPDATA"))
        add_candidate(os.environ.get("PROGRAMDATA"))

        try:
            home_folder = Path.home() / ".VideoAndSoundDownloaderPro"
            home_folder.mkdir(parents=True, exist_ok=True)
            candidates.append(home_folder / TRIAL_STATE_FILE_NAME)
        except Exception:
            pass

        unique = []
        seen = set()
        for path in candidates:
            key = str(path).lower()
            if key not in seen:
                seen.add(key)
                unique.append(path)
        return unique or [Path(TRIAL_STATE_FILE_NAME)]

    def parse_trial_timestamp(self, value):
        try:
            timestamp = int(value)
        except Exception:
            return None
        if timestamp < 946684800 or timestamp > 4102444800:
            return None
        return timestamp

    def get_trial_signature_key(self):
        material = "|".join(
            [
                str(TRIAL_STATE_SECRET),
                str(TRIAL_BUILD_ID),
                str(TRIAL_BUILD_STARTED_AT),
                str(APP_VERSION),
            ]
        )
        return hashlib.sha256(material.encode("utf-8", errors="replace")).digest()

    def sign_trial_payload(self, payload):
        encoded = json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hmac.new(self.get_trial_signature_key(), encoded, hashlib.sha256).hexdigest()

    def create_trial_record(self, payload):
        return {
            "schema": TRIAL_STATE_SCHEMA,
            "payload": payload,
            "signature": self.sign_trial_payload(payload),
        }

    def create_trial_payload(self, first_started_at, last_seen_at, trial_days, build_started_at):
        return {
            "first_started_at": int(first_started_at),
            "last_seen_at": int(last_seen_at),
            "trial_days": int(trial_days),
            "trial_build_id": str(TRIAL_BUILD_ID),
            "trial_build_started_at": int(build_started_at),
            "app_version": APP_VERSION,
        }

    def decode_trial_state_record(self, data, trial_days, build_started_at):
        if not isinstance(data, dict):
            return None, "stale"

        if int(data.get("schema") or 0) == TRIAL_STATE_SCHEMA:
            payload = data.get("payload")
            signature = str(data.get("signature") or "")
            if not isinstance(payload, dict) or not signature:
                return None, "tampered"
            expected_signature = self.sign_trial_payload(payload)
            if not hmac.compare_digest(signature, expected_signature):
                return None, "tampered"
            if payload.get("trial_build_id") != TRIAL_BUILD_ID:
                return None, "stale"
            if int(payload.get("trial_days") or 0) != int(trial_days):
                return None, "stale"
            if int(payload.get("trial_build_started_at") or 0) != int(build_started_at):
                return None, "stale"

            first_started_at = self.parse_trial_timestamp(payload.get("first_started_at"))
            last_seen_at = self.parse_trial_timestamp(payload.get("last_seen_at"))
            if first_started_at is None or last_seen_at is None:
                return None, "tampered"
            return payload, None

        if "signature" in data or "payload" in data:
            return None, "tampered"

        if data.get("trial_build_id") != TRIAL_BUILD_ID:
            return None, "stale"
        if int(data.get("trial_days") or 0) != int(trial_days):
            return None, "stale"

        first_started_at = self.parse_trial_timestamp(data.get("first_started_at"))
        if first_started_at is None:
            return None, "stale"
        last_seen_at = self.parse_trial_timestamp(data.get("last_seen_at")) or first_started_at
        return self.create_trial_payload(first_started_at, last_seen_at, trial_days, build_started_at), None

    def read_trial_file_state(self, path):
        try:
            if not path.exists():
                return None
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None

    def write_trial_file_state(self, path, record):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def read_trial_registry_state(self):
        if os.name != "nt":
            return None
        try:
            import winreg

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, TRIAL_REGISTRY_KEY) as key:
                value, _ = winreg.QueryValueEx(key, TRIAL_REGISTRY_VALUE_NAME)
            if not isinstance(value, str) or not value.strip():
                return None
            return json.loads(value)
        except Exception:
            return None

    def write_trial_registry_state(self, record):
        if os.name != "nt":
            return
        try:
            import winreg

            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, TRIAL_REGISTRY_KEY, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(
                    key,
                    TRIAL_REGISTRY_VALUE_NAME,
                    0,
                    winreg.REG_SZ,
                    json.dumps(record, ensure_ascii=False, separators=(",", ":")),
                )
        except Exception:
            pass

    def read_trial_state_candidates(self):
        candidates = []
        for path in self.get_trial_state_paths():
            data = self.read_trial_file_state(path)
            if data is not None:
                candidates.append((str(path), data))

        registry_data = self.read_trial_registry_state()
        if registry_data is not None:
            candidates.append(("HKCU:" + TRIAL_REGISTRY_KEY, registry_data))
        return candidates

    def write_trial_state_everywhere(self, record):
        for path in self.get_trial_state_paths():
            self.write_trial_file_state(path, record)
        self.write_trial_registry_state(record)

    def verify_self_integrity(self):
        # Public disclosure note:
        # The public package does not include private signing keys or certificates.
        # This check only inspects the Authenticode signature of a frozen Windows EXE.
        # In v7.0.7 enforce_trial_status() no longer blocks the app on trial expiry.
        if getattr(self, "self_integrity_checked", False):
            return not getattr(self, "self_integrity_failed", False)

        self.self_integrity_checked = True
        self.self_integrity_failed = False

        if not getattr(sys, "frozen", False) or os.name != "nt":
            return True

        try:
            powershell_path = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe"
            powershell = str(powershell_path) if powershell_path.exists() else "powershell.exe"
            script = (
                "$s=Get-AuthenticodeSignature -LiteralPath $args[0];"
                "[pscustomobject]@{Status=[string]$s.Status;Subject=[string]$s.SignerCertificate.Subject}"
                "|ConvertTo-Json -Compress"
            )
            result = subprocess.run(
                [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script, str(Path(sys.executable).resolve())],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                errors="replace",
                timeout=8,
                creationflags=no_window_creation_flags(),
            )
            if result.returncode != 0 or not result.stdout.strip():
                return True
            info = json.loads(result.stdout)
            status = str(info.get("Status") or "")
            subject = str(info.get("Subject") or "")
            signer_matches = all(marker in subject for marker in TRIAL_EXPECTED_SIGNER_MARKERS)
            if status in SELF_INTEGRITY_BLOCK_STATUSES or not signer_matches:
                self.self_integrity_failed = True
                return False
        except Exception:
            return True

        return True

    def read_trial_state(self):
        trial_days = self.get_effective_trial_days()
        if trial_days <= 0:
            return None

        now = int(time.time())
        build_started_at = self.get_trial_build_started_at(now)
        valid_payloads = []
        tampered = False

        for _, data in self.read_trial_state_candidates():
            payload, reason = self.decode_trial_state_record(data, trial_days, build_started_at)
            if payload:
                valid_payloads.append(payload)
            elif reason == "tampered":
                tampered = True

        if valid_payloads:
            first_started_at = min(int(payload["first_started_at"]) for payload in valid_payloads)
            last_seen_at = max(int(payload["last_seen_at"]) for payload in valid_payloads)
        else:
            first_started_at = now
            last_seen_at = now

        reason = ""
        if tampered:
            reason = "Dane triala zostały zmienione lub uszkodzone."
        elif now + TRIAL_CLOCK_TOLERANCE_SECONDS < build_started_at:
            reason = "Zegar systemowy jest cofnięty względem daty kompilacji programu."
        elif last_seen_at > now + TRIAL_CLOCK_TOLERANCE_SECONDS:
            reason = "Wykryto cofnięcie zegara systemowego."
        elif first_started_at > now + TRIAL_CLOCK_TOLERANCE_SECONDS:
            reason = "Data startu triala jest nieprawidłowa."

        last_seen_at = max(last_seen_at, now)
        payload = self.create_trial_payload(first_started_at, last_seen_at, trial_days, build_started_at)
        record = self.create_trial_record(payload)
        self.write_trial_state_everywhere(record)

        user_expires_at = first_started_at + int(trial_days) * TRIAL_DAY_SECONDS
        build_expires_at = build_started_at + int(trial_days) * TRIAL_DAY_SECONDS
        expires_at = min(user_expires_at, build_expires_at)
        seconds_left = expires_at - now
        days_left = max(0, (seconds_left + TRIAL_DAY_SECONDS - 1) // TRIAL_DAY_SECONDS)
        expired = bool(reason) or seconds_left <= 0

        return {
            "expired": expired,
            "days_left": int(days_left),
            "expires_at": expires_at,
            "state_path": self.get_trial_state_path(),
            "reason": reason,
        }

    def format_trial_date(self, timestamp):
        return time.strftime("%Y-%m-%d", time.localtime(timestamp))

    def disable_app_for_expired_trial(self):
        self.trial_expired = True
        self.download_btn.configure(state="disabled", text=self.tr_ui("TRIAL WYGASŁ"))
        self.stop_btn.configure(state="disabled")
        self.url_entry.configure(state="disabled")
        self.path_entry.configure(state="disabled")
        self.quality_box.configure(state="disabled")
        if hasattr(self, "subtitle_switch"):
            self.subtitle_switch.configure(state="disabled")
        self.paste_btn.configure(state="disabled")
        self.browse_btn.configure(state="disabled")

    def get_trial_block_message(self, state=None):
        reason = ""
        if isinstance(state, dict):
            reason = str(state.get("reason") or "").strip()
        if reason:
            return reason + "\n\nPobieranie zostało zablokowane. Skontaktuj się z autorem, aby otrzymać nową wersję programu."
        return "Czas testów tej wersji programu minął.\n\nPobieranie zostało zablokowane."

    def block_app_for_trial(self, state=None):
        self.disable_app_for_expired_trial()
        message = self.get_trial_block_message(state)
        self.set_status("Program został zablokowany. Pobieranie nie jest dostępne.")
        self.log_line("Program zablokowany: " + message.replace("\n", " "))
        self.show_info_dialog("Program zablokowany", message)

    def block_app_for_integrity_failure(self):
        self.disable_app_for_expired_trial()
        message = (
            "Plik programu nie przechodzi kontroli podpisu albo został zmieniony po kompilacji.\n\n"
            "Pobieranie zostało zablokowane. Uruchom oryginalny, podpisany plik EXE."
        )
        self.set_status("Program został zablokowany przez kontrolę integralności.")
        self.log_line("Program zablokowany: kontrola integralności pliku EXE nie powiodła się.")
        self.show_info_dialog("Program zablokowany", message)

    def enforce_trial_status(self):
        self.trial_expired = False
        self.set_status("Program jest dostępny bez limitu czasu.")
        self.log_line(
            "Na liczne prośby program został udostępniony wszystkim użytkownikom bez limitu czasu. "
            "Jeśli doceniasz projekt, możesz przybić wirtualną piątkę, klikając przycisk Wsparcie."
        )

    def create_mode_card(self, parent, key, icon, title, subtitle, accent, column):
        frame = ctk.CTkFrame(
            parent,
            height=98,
            corner_radius=16,
            fg_color=self.colors["panel"],
            border_width=1,
            border_color="#25374f",
        )
        frame.grid(row=0, column=column, padx=(0 if column == 0 else 8, 0), sticky="ew")
        frame.grid_propagate(False)
        frame.grid_columnconfigure(0, weight=1)

        icon_label = ctk.CTkLabel(
            frame,
            text=icon,
            font=("Segoe UI", 28, "bold"),
            text_color=accent,
        )
        icon_label.grid(row=0, column=0, pady=(10, 0))

        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 14, "bold"),
            text_color=accent,
        )
        title_label.grid(row=1, column=0)

        subtitle_label = ctk.CTkLabel(
            frame,
            text=subtitle,
            font=("Segoe UI", 10),
            text_color=self.colors["muted"],
        )
        subtitle_label.grid(row=2, column=0, pady=(0, 8))

        for widget in (frame, icon_label, title_label, subtitle_label):
            widget.bind("<Button-1>", lambda _event, mode=key: self.select_mode(mode))

        self.mode_cards[key] = {
            "frame": frame,
            "accent": accent,
            "title": title_label,
            "title_text": title,
            "subtitle": subtitle_label,
            "subtitle_text": subtitle,
        }

    def update_download_button_text(self):
        button_text = {
            "MP3": "↓   POBIERZ DŹWIĘK",
            "MP4": "↓   POBIERZ WIDEO",
            "PLAYLISTA": "↓   POBIERZ PLAYLISTĘ",
            "FACEBOOK": "↓   POBIERZ Z FACEBOOKA",
        }.get(self.selected_mode, "↓   POBIERZ")
        self.download_btn.configure(text=self.tr_ui(button_text))

    def select_mode(self, mode):
        self.selected_mode = mode

        for key, card in self.mode_cards.items():
            if key == mode:
                card["frame"].configure(border_color=self.colors["border_strong"], fg_color=self.colors["panel_hover"])
                card["subtitle"].configure(text_color="#cfe2ff")
            else:
                card["frame"].configure(border_color="#25374f", fg_color=self.colors["panel"])
                card["subtitle"].configure(text_color=self.colors["muted"])

        if hasattr(self, "quality_box"):
            current_key = self.quality_label_to_key(self.quality_var.get())
            choices = self.get_quality_options_for_mode(mode)
            self.quality_box.configure(values=choices)
            if current_key not in MODE_QUALITY_OPTIONS[mode]:
                self.quality_box.set(self.get_default_quality_for_mode(mode))
            else:
                self.quality_box.set(self.tr_quality_label(current_key))

        if hasattr(self, "download_btn") and not self.trial_expired:
            self.update_download_button_text()

        if hasattr(self, "subtitle_option_frame"):
            self.update_subtitle_option_visibility()

    def update_subtitle_option_visibility(self):
        if self.language == "EN":
            self.subtitles_var.set(False)
            self.subtitle_option_frame.grid_remove()
            self.subtitle_switch.configure(state="disabled")
        elif self.selected_mode in SUBTITLE_MODES:
            self.subtitle_option_frame.grid()
            self.subtitle_switch.configure(state="normal")
            self.subtitle_status_var.set(
                self.tr_ui("Najpierw polskie, w razie braku angielskie. Napisy będą w filmie.")
            )
        else:
            self.subtitle_option_frame.grid_remove()
            self.subtitle_switch.configure(state="disabled")

    def paste_from_clipboard(self):
        try:
            text = self.clipboard_get().strip()
        except tk.TclError:
            self.show_info_dialog("Schowek jest pusty", "Nie znaleziono tekstu do wklejenia.")
            return

        if text:
            self.url.set(text)
            self.url_entry.icursor("end")

    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.save_dir.get())
        if folder:
            self.save_dir.set(folder)

    def show_about(self):
        self.show_info_dialog(
            "O mnie",
            f"Autor: {APP_AUTHOR}\n"
            f"Wersja programu: {APP_VERSION}\n"
            f"Nazwa: {APP_TITLE}\n\n"
            "Disclaimer: Nie ponosimy odpowiedzialności za sposób wykorzystania programu. "
            "Pobierając materiały, użytkownik potwierdza, że ma do tego prawo.",
        )

    def open_support_page(self):
        webbrowser.open(SUPPORT_URL_EN if self.language == "EN" else SUPPORT_URL)

    def open_project_repo_page(self):
        webbrowser.open(PROJECT_REPO_URL)

    def open_license(self):
        if getattr(sys, "frozen", False):
            app_dir = Path(sys.executable).resolve().parent
        else:
            app_dir = Path(__file__).resolve().parent

        license_path = app_dir / LICENSE_FILE_NAME
        if license_path.exists():
            webbrowser.open(license_path.as_uri())
        else:
            webbrowser.open(LICENSE_URL)

    def log_line(self, text):
        self.after(0, self._log_line_ui, text)

    def _log_line_ui(self, text):
        self.log_source_lines.append(text)
        self.log.configure(state="normal")
        self.log.insert("end", self.translate_message(text) + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def render_log(self):
        if not hasattr(self, "log"):
            return
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        for source_text in self.log_source_lines:
            self.log.insert("end", self.translate_message(source_text) + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def update_status_from_process_line(self, text):
        clean_text = text.strip()
        if not clean_text:
            return

        progress_label = getattr(self, "active_progress_label", "") or "Mini: trwa kompresja..."
        if clean_text.startswith("out_time="):
            self.set_status(progress_label + " " + clean_text.replace("out_time=", "czas "))
        elif clean_text.startswith("speed="):
            self.set_status(progress_label + " " + clean_text)
        elif clean_text.startswith("progress=end"):
            if progress_label.startswith("Napisy:"):
                self.set_status("Napisy: kończę wtapianie napisów...")
            else:
                self.set_status("Mini: kończę kompresję...")
        elif clean_text.startswith("progress=continue"):
            return
        if clean_text.startswith("[download]") or clean_text.startswith("[ExtractAudio]"):
            self.set_status(clean_text)
        elif clean_text.startswith(
            (
                "[Merger]",
                "[VideoConvertor]",
                "[VideoRemuxer]",
                "[EmbedSubtitle]",
                "[SubtitlesConvertor]",
                "[Fixup]",
                "[MoveFiles]",
                "[Metadata]",
                "[ExtractAudio]",
            )
        ):
            self.set_status(clean_text)
        elif "ERROR:" in clean_text:
            self.set_status("Błąd: sprawdź szczegóły w logu.")

    def language_code_matches(self, code, base_language):
        code = str(code or "").lower()
        base_language = base_language.lower()
        return code == base_language or code.startswith(base_language + "-") or code.startswith(base_language + "_")

    def get_subtitle_language_priority(self):
        if self.language == "EN":
            return SUBTITLE_LANGUAGE_PRIORITY_EN
        return SUBTITLE_LANGUAGE_PRIORITY_PL

    def get_arte_subtitle_format_prefix(self, subtitle_code):
        code = str(subtitle_code or "").lower()
        if self.language_code_matches(code, "en"):
            return "VO-STE_ANG_"
        if self.language_code_matches(code, "pl"):
            return "VO-STE_POL_"
        return ""

    def choose_subtitle_language(self, video_info):
        sources = [
            ("subtitles", "napisy"),
            ("automatic_captions", "napisy automatyczne"),
        ]
        for source_key, source_label in sources:
            tracks = video_info.get(source_key) or {}
            if not isinstance(tracks, dict):
                continue
            available_codes = [code for code, items in tracks.items() if items]
            for base_code, language_label in self.get_subtitle_language_priority():
                for code in available_codes:
                    if self.language_code_matches(code, base_code):
                        return {
                            "enabled": True,
                            "found": True,
                            "embedded": True,
                            "burn_in": True,
                            "code": code,
                            "language_label": language_label,
                            "source_label": source_label,
                            "source_key": source_key,
                        }
        return {"enabled": True, "found": False}

    def prepare_subtitles_for_video(self, link, enabled):
        if not enabled or self.language == "EN":
            return {"enabled": False, "found": False}

        self.set_status("Sprawdzam napisy do filmu...")
        self.log_line("Napisy: sprawdzam dostępność PL, potem EN.")
        command = [
            resolve_tool_command("yt-dlp"),
            "--dump-single-json",
            "--skip-download",
            "--no-warnings",
            "--no-playlist",
            link,
        ]
        code, stdout, stderr = self.run_capture_command(command)

        for line in stderr.splitlines()[-8:]:
            clean_line = line.strip()
            if clean_line:
                self.log_line(clean_line)

        if self.stop_requested:
            return {"enabled": True, "found": False}

        if code != 0 or not stdout.strip():
            self.log_line("Napisy: nie udało się sprawdzić listy napisów dla tego filmu.")
            return {"enabled": True, "found": False}

        try:
            video_info = json.loads(stdout)
        except json.JSONDecodeError as exc:
            self.log_line(f"Napisy: nie udało się odczytać danych napisów: {exc}")
            return {"enabled": True, "found": False}

        subtitle_info = self.choose_subtitle_language(video_info)
        if subtitle_info.get("found"):
            self.log_line(
                "Napisy: znaleziono język "
                f"{subtitle_info['language_label']} ({subtitle_info['code']}), źródło: "
                f"{subtitle_info['source_label']}. Zostaną zintegrowane z filmem."
            )
        else:
            self.log_line("Napisy: nie znaleziono napisów po polsku ani po angielsku.")
        return subtitle_info

    def append_subtitle_options(self, command, subtitle_info):
        if not subtitle_info or not subtitle_info.get("found"):
            return

        command.extend(
            [
                "--write-subs",
                "--write-auto-subs",
                "--sub-langs",
                subtitle_info["code"],
                "--embed-subs",
                "--convert-subs",
                "srt",
            ]
        )

    def format_subtitle_result(self, subtitle_info):
        if not subtitle_info or not subtitle_info.get("enabled"):
            return ""
        if subtitle_info.get("subtitle_download_failed"):
            return (
                "Napisy były wykryte, ale nie udało się ich pobrać lub zintegrować. "
                "Film został pobrany bez napisów."
            )
        if subtitle_info.get("found"):
            return (
                "Napisy były dostępne i zostały zintegrowane z filmem. "
                f"Język: {subtitle_info['language_label']} ({subtitle_info['code']})."
            )
        return "W tym filmie nie znaleziono napisów po polsku ani po angielsku."

    def extract_subtitle_paths_from_output(self, output_lines):
        paths = []
        marker = "Writing video subtitles to:"
        for line in output_lines or []:
            if marker not in line:
                continue
            raw_path = line.split(marker, 1)[1].strip().strip('"')
            if raw_path:
                paths.append(Path(raw_path))
        return paths

    def extract_downloaded_video_paths_from_output(self, output_lines):
        paths = []
        marker = "__VSDP_FILE__:"
        for line in output_lines or []:
            if marker not in line:
                continue
            raw_path = line.split(marker, 1)[1].strip().strip('"')
            if raw_path:
                paths.append(Path(raw_path))
        return paths

    def build_burn_subtitles_command(self, video_path, subtitle_path, output_path, video_format):
        subtitle_filter = (
            "subtitles=subtitles"
            f"{subtitle_path.suffix.lower()}:force_style='"
            "FontName=Arial,FontSize=22,"
            "PrimaryColour=&H00FFFFFF&,OutlineColour=&H00000000&,"
            "BorderStyle=1,Outline=2,Shadow=1,MarginV=28'"
        )
        command = [
            resolve_tool_command("ffmpeg"),
            "-y",
            "-nostdin",
            "-hide_banner",
            "-loglevel",
            "warning",
            "-i",
            str(video_path),
            "-vf",
            subtitle_filter,
            "-map",
            "0:v:0",
            "-map",
            "0:a?",
            "-sn",
            "-progress",
            "pipe:1",
        ]

        if video_format == "webm" or output_path.suffix.lower() == ".webm":
            command.extend(["-c:v", "libvpx-vp9", "-crf", "32", "-b:v", "0", "-c:a", "libopus", "-b:a", "128k"])
        else:
            command.extend(["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k"])
            if output_path.suffix.lower() == ".mp4":
                command.extend(["-movflags", "+faststart"])

        command.append(str(output_path))
        return command

    def burn_subtitles_into_recent_video(self, subtitle_info, video_format):
        if (
            not subtitle_info
            or not subtitle_info.get("found")
            or subtitle_info.get("subtitle_download_failed")
        ):
            return subtitle_info

        download_output_lines = list(self.last_process_output_lines)
        video_paths = [
            file_path
            for file_path in self.extract_downloaded_video_paths_from_output(download_output_lines)
            if file_path.exists()
        ]
        subtitle_paths = [
            file_path
            for file_path in self.extract_subtitle_paths_from_output(download_output_lines)
            if file_path.exists()
        ]

        if not video_paths:
            subtitle_info["subtitle_download_failed"] = True
            self.log_line("Napisy: nie udało się potwierdzić ścieżki pobranego pliku.")
            return subtitle_info
        if not subtitle_paths:
            subtitle_info["subtitle_download_failed"] = True
            self.log_line("Napisy: nie znaleziono pobranego pliku napisów do wtopienia.")
            return subtitle_info

        video_path = video_paths[-1]
        subtitle_path = subtitle_paths[-1]
        output_path = video_path.with_name(video_path.stem + ".vsdp_subtitled_tmp" + video_path.suffix)
        if output_path.exists():
            try:
                output_path.unlink()
            except OSError:
                pass

        self.set_status("Napisy: wtapiam napisy w obraz filmu...")
        self.log_line("Napisy: wtapiam napisy w obraz filmu...")

        burn_output_lines = []
        try:
            with tempfile.TemporaryDirectory(prefix="vsdp_subtitles_") as temp_dir:
                temp_dir_path = Path(temp_dir)
                safe_subtitle_path = temp_dir_path / ("subtitles" + subtitle_path.suffix.lower())
                shutil.copy2(subtitle_path, safe_subtitle_path)
                command = self.build_burn_subtitles_command(video_path, safe_subtitle_path, output_path, video_format)
                code = self.run_download_command(
                    command,
                    cwd=str(temp_dir_path),
                    progress_label="Napisy: wtapiam napisy w obraz filmu...",
                )
                burn_output_lines = list(self.last_process_output_lines)
        except OSError as exc:
            subtitle_info["subtitle_download_failed"] = True
            self.log_line(f"Napisy: nie udało się wtopić napisów w obraz filmu. {exc}")
            self.last_process_output_lines = download_output_lines + burn_output_lines
            return subtitle_info

        self.last_process_output_lines = download_output_lines + burn_output_lines
        if code != 0 or not output_path.exists():
            subtitle_info["subtitle_download_failed"] = True
            self.log_line("Napisy: nie udało się wtopić napisów w obraz filmu.")
            if output_path.exists():
                try:
                    output_path.unlink()
                except OSError:
                    pass
            return subtitle_info

        try:
            video_path.unlink()
            output_path.replace(video_path)
        except OSError as exc:
            subtitle_info["subtitle_download_failed"] = True
            self.log_line(f"Napisy: nie udało się wtopić napisów w obraz filmu. {exc}")
            return subtitle_info

        subtitle_info["subtitle_burned_in"] = True
        subtitle_info["subtitle_embed_verified"] = True
        self.log_line("Napisy: napisy zostały wtopione w obraz filmu.")
        return subtitle_info

    def probe_media_duration_seconds(self, file_path):
        command = [
            resolve_tool_command("ffprobe"),
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(file_path),
        ]
        code, stdout, stderr = self.run_capture_command(command)
        if code != 0:
            clean_error = (stderr or stdout).strip()
            if clean_error:
                self.log_line("Mini: ffprobe: " + clean_error.splitlines()[-1])
            return None
        try:
            duration = float(stdout.strip())
        except ValueError:
            return None
        if duration <= 0:
            return None
        return duration

    def build_mini_compression_attempts(self, duration):
        attempts = [
            {"width": 426, "fps": 15, "audio_kbps": 32, "safety": 0.88},
            {"width": 320, "fps": 12, "audio_kbps": 24, "safety": 0.78},
            {"width": 256, "fps": 10, "audio_kbps": 16, "safety": 0.68},
        ]
        for attempt in attempts:
            total_kbps = max(12, int((MINI_VIDEO_MAX_BYTES * 8 * attempt["safety"]) / duration / 1000))
            audio_kbps = min(attempt["audio_kbps"], max(6, total_kbps // 3))
            video_kbps = max(6, total_kbps - audio_kbps)
            yield {
                "width": attempt["width"],
                "fps": attempt["fps"],
                "audio_kbps": audio_kbps,
                "video_kbps": video_kbps,
            }

    def format_size_mb(self, size_bytes):
        return f"{size_bytes / 1024 / 1024:.1f} MB"

    def format_mini_result_message(self, result):
        if not result or not result.get("success"):
            return "Mini: nie udało się skompresować pliku."

        size_text = self.format_size_mb(result["size"])
        original_text = self.format_size_mb(result["original_size"])
        reduction = result.get("reduction_percent", 0)
        width = result.get("width")
        fps = result.get("fps")
        video_kbps = result.get("video_kbps")
        audio_kbps = result.get("audio_kbps")
        if isinstance(width, str):
            params = "bez ponownej kompresji"
        else:
            params = f"{width}px/{fps} fps, wideo {video_kbps}k, audio {audio_kbps}k"
        if result.get("within_limit"):
            return (
                f"Mini: skompresowano do {size_text} z {original_text}. "
                f"Zmniejszenie: {reduction:.1f}%. Parametry: {params}."
            )
        return (
            f"Mini: nie udało się zejść do 20 MB, ale zapisano najmniejszy uzyskany plik: {size_text} "
            f"z {original_text}. Zmniejszenie: {reduction:.1f}%. Parametry: {params}."
        )

    def compress_video_file_to_mini(self, file_path):
        file_path = Path(file_path)
        if not file_path.exists():
            self.log_line(f"Mini: nie znaleziono pliku do kompresji: {file_path}")
            return {"success": False, "reason": "missing_file"}

        current_size = file_path.stat().st_size
        if current_size <= MINI_VIDEO_MAX_BYTES:
            result = {
                "success": True,
                "within_limit": True,
                "size": current_size,
                "original_size": current_size,
                "reduction_percent": 0,
                "width": "bez zmian",
                "fps": "bez zmian",
                "video_kbps": "bez zmian",
                "audio_kbps": "bez zmian",
            }
            self.log_line(self.format_mini_result_message(result))
            return result

        duration = self.probe_media_duration_seconds(file_path)
        if not duration:
            self.log_line("Mini: nie udało się odczytać długości pliku, nie mogę bezpiecznie obliczyć kompresji.")
            return {"success": False, "reason": "unknown_duration"}

        self.set_status("Mini: kompresuję plik do maks. 20 MB...")
        self.log_line(
            f"Mini: kompresja do maks. 20 MB. Rozmiar wejściowy: {self.format_size_mb(current_size)}."
        )

        temp_path = file_path.with_name(file_path.stem + ".mini_tmp" + file_path.suffix)
        best_path = file_path.with_name(file_path.stem + ".mini_best" + file_path.suffix)
        best_result = None
        for attempt in self.build_mini_compression_attempts(duration):
            if temp_path.exists():
                temp_path.unlink()

            scale_filter = f"scale='min({attempt['width']},iw)':-2,fps={attempt['fps']}"
            command = [
                resolve_tool_command("ffmpeg"),
                "-y",
                "-nostats",
                "-i",
                str(file_path),
                "-map",
                "0:v:0",
                "-map",
                "0:a?",
                "-map",
                "0:s?",
                "-vf",
                scale_filter,
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-b:v",
                f"{attempt['video_kbps']}k",
                "-maxrate",
                f"{attempt['video_kbps']}k",
                "-bufsize",
                f"{attempt['video_kbps'] * 2}k",
                "-c:a",
                "aac",
                "-b:a",
                f"{attempt['audio_kbps']}k",
                "-ac",
                "1",
                "-c:s",
                "mov_text",
                "-movflags",
                "+faststart",
                "-progress",
                "pipe:1",
                str(temp_path),
            ]
            self.log_line(
                "Mini: próba kompresji "
                f"{attempt['width']}px/{attempt['fps']} fps, "
                f"wideo {attempt['video_kbps']}k, audio {attempt['audio_kbps']}k."
            )
            self.log_line("Mini: to nie jest aktualizacja programu, tylko kompresja pliku przez FFmpeg.")
            code = self.run_download_command(command, progress_label="Mini: trwa kompresja...")
            if code != 0 or not temp_path.exists():
                self.log_line("Mini: ta próba kompresji nie powiodła się.")
                continue

            output_size = temp_path.stat().st_size
            reduction = max(0, (1 - (output_size / current_size)) * 100)
            result = {
                "success": True,
                "within_limit": output_size <= MINI_VIDEO_MAX_BYTES,
                "size": output_size,
                "original_size": current_size,
                "reduction_percent": reduction,
                "width": attempt["width"],
                "fps": attempt["fps"],
                "video_kbps": attempt["video_kbps"],
                "audio_kbps": attempt["audio_kbps"],
            }
            self.log_line(f"Mini: rozmiar po kompresji: {self.format_size_mb(output_size)}.")

            if best_result is None or output_size < best_result["size"]:
                if best_path.exists():
                    best_path.unlink()
                temp_path.replace(best_path)
                best_result = result
            else:
                temp_path.unlink()

            if result["within_limit"]:
                break

        if temp_path.exists():
            temp_path.unlink()
        if best_result and best_path.exists():
            file_path.unlink()
            best_path.replace(file_path)
            message = self.format_mini_result_message(best_result)
            self.log_line(message)
            self.set_status(message)
            return best_result

        if best_path.exists():
            best_path.unlink()
        self.log_line("Mini: żadna próba kompresji nie zakończyła się poprawnie.")
        return {"success": False, "reason": "compression_failed"}

    def compress_recent_video_download_to_mini(self):
        download_output_lines = list(self.last_process_output_lines)
        paths = self.extract_downloaded_video_paths_from_output(download_output_lines)
        if not paths:
            self.log_line("Mini: nie udało się ustalić ścieżki pobranego pliku.")
            return {"success": False, "reason": "missing_output_path"}

        final_result = {"success": True, "within_limit": True, "results": []}
        compression_output = []
        for file_path in paths[-1:]:
            result = self.compress_video_file_to_mini(file_path)
            compression_output.extend(self.last_process_output_lines)
            final_result["results"].append(result)
            final_result["success"] = final_result["success"] and bool(result.get("success"))
            final_result["within_limit"] = final_result["within_limit"] and bool(result.get("within_limit"))

        self.last_process_output_lines = download_output_lines + compression_output
        if final_result["results"]:
            final_result.update(final_result["results"][-1])
        return final_result

    def cleanup_embedded_subtitle_files(self, subtitle_info):
        if (
            not subtitle_info
            or not subtitle_info.get("found")
            or not subtitle_info.get("embedded")
            or subtitle_info.get("subtitle_download_failed")
        ):
            return

        candidates = set()
        for subtitle_path in self.extract_subtitle_paths_from_output(self.last_process_output_lines):
            candidates.add(subtitle_path)
            for extension in SUBTITLE_FILE_EXTENSIONS:
                candidates.add(subtitle_path.with_suffix(extension))

        removed = 0
        for subtitle_path in candidates:
            try:
                if subtitle_path.suffix.lower() in SUBTITLE_FILE_EXTENSIONS and subtitle_path.exists():
                    subtitle_path.unlink()
                    removed += 1
                    self.log_line(f"Napisy: usunięto osobny plik napisów: {subtitle_path.name}")
            except OSError as exc:
                self.log_line(f"Napisy: nie udało się usunąć osobnego pliku {subtitle_path.name}: {exc}")

        if removed:
            self.log_line("Napisy: w folderze został sam film z osadzonymi napisami.")

    def set_status(self, text):
        self.last_status_source = text
        self.after(0, self.status.set, self.translate_message(text))

    def set_busy(self, busy):
        self.after(0, self._set_busy_ui, busy)

    def _set_busy_ui(self, busy):
        if busy:
            self.download_btn.configure(state="disabled")
            if hasattr(self, "fix_btn"):
                self.fix_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            if hasattr(self, "subtitle_switch"):
                self.subtitle_switch.configure(state="disabled")
            self.start_spinner()
        else:
            if self.trial_expired:
                self.download_btn.configure(state="disabled")
                if hasattr(self, "fix_btn"):
                    self.fix_btn.configure(state="normal")
                self.stop_btn.configure(state="disabled")
                if hasattr(self, "subtitle_switch"):
                    self.subtitle_switch.configure(state="disabled")
                self.stop_spinner()
                return

            self.download_btn.configure(state="normal")
            if hasattr(self, "fix_btn"):
                self.fix_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            if hasattr(self, "subtitle_switch"):
                self.update_subtitle_option_visibility()
            self.stop_spinner()

    def start_spinner(self):
        if self.spinner_job is None:
            self.spinner_index = 0
            self._animate_spinner()

    def _animate_spinner(self):
        self.spinner_label.configure(text=self.spinner_symbols[self.spinner_index])
        self.spinner_index = (self.spinner_index + 1) % len(self.spinner_symbols)
        self.spinner_job = self.after(120, self._animate_spinner)

    def stop_spinner(self):
        if self.spinner_job is not None:
            self.after_cancel(self.spinner_job)
            self.spinner_job = None
        self.spinner_label.configure(text="")

    def get_missing_components(self):
        missing = []
        if not command_exists("yt-dlp"):
            missing.append(("program pobierania", YTDLP_ID))
        if not command_exists("ffmpeg") or not command_exists("ffprobe"):
            missing.append(("obsługa audio i wideo", FFMPEG_ID))
        return missing

    def check_components_only(self):
        missing = self.get_missing_components()
        if missing:
            names = ", ".join(name for name, _ in missing)
            if getattr(sys, "frozen", False):
                self.set_status("Program nie jest kompletny. Pobierz ponownie pełną paczkę.")
                self.log_line(f"Brakuje plików programu: {names}")
            else:
                self.set_status(f"Brakuje komponentów: {names}. Program zapyta o instalację przy pobieraniu.")
                self.log_line(f"Brakuje komponentów: {names}")
        else:
            self.set_status("Gotowe. Wszystko jest gotowe, możesz rozpocząć pobieranie.")
            self.log_line("OK: wszystko gotowe do pobierania.")

    def start_fix(self):
        with self.process_lock:
            process_running = self.current_process and self.current_process.poll() is None

        if process_running:
            self.show_info_dialog("Proces trwa", "Poczekaj na zakończenie obecnej operacji albo użyj STOP.")
            return

        self.stop_requested = False
        self.set_busy(True)
        threading.Thread(target=self.run_fix_checks, daemon=True).start()

    def ask_yes_no_from_worker(self, title, message):
        result = {"value": False}
        completed = threading.Event()

        def ask_on_ui():
            try:
                result["value"] = self.ask_yes_no_dialog(title, message)
            finally:
                completed.set()

        self.after(0, ask_on_ui)
        completed.wait()
        return result["value"]

    def show_info_from_worker(self, title, message):
        self.after(0, lambda: self.show_info_dialog(title, message))

    def show_repo_fix_dialog(self, message):
        self.show_info_dialog("Fix", message)
        self.open_project_repo_page()

    def show_repo_fix_dialog_from_worker(self, message):
        self.after(0, lambda: self.show_repo_fix_dialog(message))

    def fetch_latest_ytdlp_release_info(self):
        request = urllib.request.Request(
            YTDLP_LATEST_RELEASE_API,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": f"{APP_TITLE}/{APP_VERSION}",
            },
        )
        with urllib.request.urlopen(request, timeout=25) as response:
            data = json.loads(response.read().decode("utf-8", errors="replace"))

        tag = str(data.get("tag_name") or "").strip()
        exe_url = ""
        for asset in data.get("assets") or []:
            if str(asset.get("name") or "").lower() == "yt-dlp.exe":
                exe_url = str(asset.get("browser_download_url") or "").strip()
                break

        return {
            "tag": tag,
            "exe_url": exe_url or YTDLP_LATEST_EXE_URL,
            "html_url": str(data.get("html_url") or "").strip(),
        }

    def detect_ytdlp_problem(self):
        if not command_exists("yt-dlp"):
            return "missing"

        self.set_status("Fix: sprawdzam wersję yt-dlp...")
        command = [resolve_tool_command("yt-dlp"), "--version"]
        try:
            code, stdout, stderr = self.run_capture_command(command)
        except Exception as exc:
            self.log_line(f"Fix: yt-dlp nie uruchamia się poprawnie: {exc}")
            return "broken"

        output = (stdout or stderr).strip()
        if output:
            self.log_line("Fix: wykryta wersja yt-dlp: " + output.splitlines()[0])
        if code != 0:
            return "broken"

        self.latest_ytdlp_release = None
        try:
            latest = self.fetch_latest_ytdlp_release_info()
            self.latest_ytdlp_release = latest
            latest_tag = latest.get("tag") or ""
            if latest_tag:
                self.log_line("Fix: najnowsza wersja yt-dlp na GitHubie: " + latest_tag)
                current_version = output.splitlines()[0].strip()
                if current_version and current_version != latest_tag:
                    return "outdated"
        except Exception as exc:
            self.log_line(f"Fix: nie udało się sprawdzić najnowszej wersji yt-dlp na GitHubie: {exc}")

        recent_output = "\n".join(self.last_process_output_lines[-80:]).lower()
        ytdlp_markers = [
            "unable to extract",
            "signature extraction failed",
            "nsig extraction failed",
            "player response",
            "unable to download webpage",
            "youtube said",
            "this video is unavailable",
            "requested format is not available",
            "http error 403",
            "forbidden",
        ]
        if any(marker in recent_output for marker in ytdlp_markers):
            return "last_error"

        return None

    def update_ytdlp(self, problem):
        if getattr(sys, "frozen", False):
            self.log_line("Fix: wersja EXE nie modyfikuje własnych plików programu.")
            return False

        try:
            return self.download_latest_ytdlp_from_github()
        except Exception as exc:
            self.log_line(f"Fix: pobieranie yt-dlp z GitHuba nie powiodło się: {exc}")

        if problem == "missing":
            if command_exists("winget"):
                return self.install_one_package("yt-dlp", YTDLP_ID)
            self.log_line("Fix: nie znaleziono yt-dlp ani winget do automatycznej instalacji.")
            return False

        ytdlp_command = self.prepare_writable_ytdlp_for_update()
        command = [ytdlp_command, "-U"]
        self.log_line("Fix: uruchamiam aktualizację yt-dlp.")
        code = self.run_download_command(command)
        if code == 0:
            return True

        self.log_line(f"Fix: aktualizacja yt-dlp przez -U zwróciła kod {code}.")
        if os.name == "nt" and command_exists("winget"):
            self.log_line("Fix: próbuję aktualizacji yt-dlp przez winget.")
            command = [
                "winget",
                "upgrade",
                "--id",
                YTDLP_ID,
                "-e",
                "--accept-package-agreements",
                "--accept-source-agreements",
            ]
            code = self.run_download_command(command)
            return code == 0

        return False

    def prepare_writable_ytdlp_for_update(self):
        current = Path(resolve_tool_command("yt-dlp"))
        target = get_external_tools_dir() / get_tool_executable_name("yt-dlp")

        if current == target:
            return str(target)

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            if current.exists():
                shutil.copy2(current, target)
                self.log_line("Fix: przygotowano aktualizowalną kopię yt-dlp w folderze danych aplikacji.")
                return str(target)
        except Exception as exc:
            self.log_line(f"Fix: nie udało się przygotować kopii yt-dlp w folderze danych aplikacji: {exc}")

        return str(current)

    def download_latest_ytdlp_from_github(self):
        latest = getattr(self, "latest_ytdlp_release", None) or self.fetch_latest_ytdlp_release_info()
        tag = latest.get("tag") or "latest"
        exe_url = latest.get("exe_url") or YTDLP_LATEST_EXE_URL
        target = get_external_tools_dir() / get_tool_executable_name("yt-dlp")
        temp_target = target.with_suffix(target.suffix + ".download")

        target.parent.mkdir(parents=True, exist_ok=True)
        self.log_line(f"Fix: pobieram yt-dlp {tag} z oficjalnego GitHuba.")

        request = urllib.request.Request(
            exe_url,
            headers={"User-Agent": f"{APP_TITLE}/{APP_VERSION}"},
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                with temp_target.open("wb") as handle:
                    shutil.copyfileobj(response, handle)

            if temp_target.stat().st_size < 1024 * 1024:
                raise RuntimeError("pobrany plik yt-dlp.exe jest podejrzanie mały")

            if target.exists():
                target.unlink()
            temp_target.replace(target)

            code, stdout, stderr = self.run_capture_command([str(target), "--version"])
            version = (stdout or stderr).strip().splitlines()[0] if (stdout or stderr).strip() else ""
            if code != 0 or not version:
                raise RuntimeError("pobrany yt-dlp.exe nie uruchamia się poprawnie")
        finally:
            temp_target.unlink(missing_ok=True)

        self.log_line("Fix: zainstalowana wersja yt-dlp: " + version)
        self.log_line("Fix: aktualizacja działa od razu w lokalnym projekcie .pyw.")
        self.log_line("Fix: przy kolejnym buildzie ta wersja zostanie scalona z EXE przez Kompiluj_EXE_v7-0-7.bat.")
        if tag != "latest" and version != tag:
            self.log_line(f"Fix: uwaga, GitHub zgłasza {tag}, a plik uruchamia się jako {version}.")
        return True

    def handle_frozen_fix_problem(self, problem):
        latest = getattr(self, "latest_ytdlp_release", None) or {}
        latest_tag = latest.get("tag") or "najnowsza"
        self.set_status("Fix: wykryto problem. Pobierz nową wersję programu z GitHuba.")
        self.log_line("Fix: w wersji EXE nie aktualizuję plików programu lokalnie.")
        self.log_line(f"Fix: po naprawie autora szukaj nowej wersji tutaj: {PROJECT_REPO_URL}")

        if problem == "outdated":
            reason = f"Wykryto nieaktualny komponent yt-dlp. Najnowsza znana wersja: {latest_tag}."
        elif problem == "missing":
            reason = "Nie znaleziono komponentu yt-dlp w tej paczce programu."
        elif problem == "last_error":
            reason = "Ostatni błąd pobierania wygląda na problem po stronie yt-dlp albo zmian w serwisie."
        else:
            reason = "Wykryto problem z komponentem yt-dlp."

        message = (
            reason
            + "\n\nTa skompilowana wersja EXE nie naprawia samej siebie, żeby nie naruszać podpisu "
            + "i nie zostawiać dodatkowych plików przy programie.\n\n"
            + "Po naprawie przez autora pobierz nową wersję programu z repozytorium:\n"
            + PROJECT_REPO_URL
        )
        self.show_repo_fix_dialog_from_worker(message)

    def run_fix_checks(self):
        try:
            self.set_status("Fix: sprawdzam podstawowe błędy...")
            self.log_line("Fix: sprawdzam podstawowe błędy.")
            problem = self.detect_ytdlp_problem()

            if self.stop_requested:
                self.set_status("Fix przerwany przez użytkownika.")
                self.log_line("Fix: przerwany przez użytkownika.")
                return

            if not problem:
                self.set_status("Sprawdzanie nie wykryło problemów.")
                self.log_line("Sprawdzanie nie wykryło problemów.")
                return

            if getattr(sys, "frozen", False):
                self.handle_frozen_fix_problem(problem)
                return

            self.set_status("Wykryto problem z yt-dlp.")
            self.log_line("Wykryto problem z yt-dlp.")
            self.log_line("Wymagana jest aktualizacja bazy/API.")
            self.log_line("Po potwierdzeniu zostanie przeprowadzona lokalna aktualizacja projektu przed dystrybucją.")

            consent = self.ask_yes_no_from_worker(
                "Fix yt-dlp",
                "Wykryto problem z yt-dlp.\n\n"
                "Wymagana jest aktualizacja bazy/API.\n"
                "Po potwierdzeniu zostanie przeprowadzona lokalna aktualizacja yt-dlp "
                "w projekcie .pyw przed dystrybucją.\n\n"
                "Czy rozpocząć aktualizację?",
            )
            if not consent:
                self.set_status("Aktualizacja anulowana.")
                self.log_line("Fix: użytkownik anulował aktualizację.")
                return

            self.set_status("Fix: aktualizuję yt-dlp...")
            ok = self.update_ytdlp(problem)
            if ok and not self.stop_requested:
                self.set_status("Aktualizacja zakończyła się powodzeniem.")
                self.log_line("Aktualizacja zakończyła się powodzeniem.")
                self.show_info_from_worker("Fix", "Aktualizacja zakończyła się powodzeniem.")
            elif self.stop_requested:
                self.set_status("Fix przerwany przez użytkownika.")
                self.log_line("Fix: przerwany przez użytkownika.")
            else:
                self.set_status("Aktualizacja yt-dlp nie powiodła się.")
                self.log_line("Fix: aktualizacja yt-dlp nie powiodła się. Szczegóły są powyżej w logu.")
                self.show_info_from_worker("Fix", "Aktualizacja yt-dlp nie powiodła się. Sprawdź log.")
        finally:
            self.set_busy(False)

    def confirm_missing_components(self):
        missing = self.get_missing_components()
        if not missing:
            self.log_line("OK: wszystko gotowe do pobierania.")
            return []

        names = ", ".join(name for name, _ in missing)

        if getattr(sys, "frozen", False):
            self.set_status("Program nie jest kompletny. Pobierz ponownie pełną paczkę.")
            self.show_info_dialog(
                "Program nie jest gotowy",
                "Ta kopia programu nie zawiera wszystkich plików potrzebnych do pobierania.\n\n"
                "Pobierz ponownie pełną paczkę programu od autora.",
            )
            return None

        if os.name != "nt":
            self.show_info_dialog(
                "Brak komponentów",
                "Brakuje yt-dlp lub FFmpeg.\n"
                "Automatyczna instalacja jest przygotowana dla Windows z winget.",
            )
            return None

        if not command_exists("winget"):
            self.show_info_dialog(
                "Brak winget",
                "Nie znaleziono winget. Zainstaluj yt-dlp i FFmpeg ręcznie albo zaktualizuj App Installer.",
            )
            return None

        consent = self.ask_yes_no_dialog(
            "Wymagana instalacja",
            "Do poprawnego działania programu trzeba zainstalować:\n\n"
            f"- {names}\n\n"
            "Program użyje winget. Może pojawić się okno zgody systemu Windows.\n\n"
            "Czy wyrażasz zgodę na instalację?",
        )

        if not consent:
            self.set_status("Instalacja anulowana. Brak wymaganych komponentów.")
            self.log_line("Użytkownik nie wyraził zgody na instalację.")
            return None

        return missing

    def install_one_package(self, name, package_id):
        self.set_status(f"Instaluję {name}...")
        self.log_line(f"Instalacja: {name} ({package_id})")
        self.log_line("Może pojawić się okno zgody systemu Windows. Nie zamykaj programu.")

        command = [
            "winget",
            "install",
            "--id",
            package_id,
            "-e",
            "--accept-package-agreements",
            "--accept-source-agreements",
        ]

        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                errors="replace",
                timeout=INSTALL_TIMEOUT_SECONDS,
                creationflags=no_window_creation_flags(),
            )

            output = (completed.stdout or "") + "\n" + (completed.stderr or "")
            clean_lines = []
            for line in output.splitlines():
                line = line.strip()
                if not line or line in {"-", "\\", "|", "/"}:
                    continue
                clean_lines.append(line)

            if clean_lines:
                self.log_line("\n".join(clean_lines[-20:]))

            if completed.returncode == 0:
                self.log_line(f"OK: instalator zakończył pracę dla {name}.")
                return True

            output_lower = output.lower()
            if "already installed" in output_lower or "is already installed" in output_lower:
                self.log_line(f"OK: {name} jest już zainstalowany.")
                return True

            self.log_line(f"UWAGA: winget zwrócił kod {completed.returncode} przy {name}.")
            return False

        except subprocess.TimeoutExpired:
            self.log_line(
                f"TIMEOUT: instalacja {name} trwała ponad {INSTALL_TIMEOUT_SECONDS} sekund. "
                "Proces został przerwany, żeby program nie wyglądał na zawieszony."
            )
            self.after(
                0,
                lambda: self.show_info_dialog(
                    "Instalacja trwa zbyt długo",
                    f"Instalacja {name} trwała zbyt długo i została zatrzymana.\n\n"
                    "Możliwe, że winget czekał na zgodę systemu, administratora albo miał problem sieciowy.\n"
                    "Spróbuj uruchomić program ponownie albo zainstalować komponent ręcznie.",
                ),
            )
            return False
        except Exception as exc:
            self.log_line(f"Błąd instalacji {name}: {exc}")
            return False

    def ensure_components_installed(self, missing):
        if not missing:
            return True

        all_ok = True
        for name, package_id in missing:
            if self.stop_requested:
                return False
            ok = self.install_one_package(name, package_id)
            all_ok = all_ok and ok

        missing_after = self.get_missing_components()
        if not missing_after:
            self.set_status("Komponenty są gotowe.")
            return True

        names_after = ", ".join(name for name, _ in missing_after)
        self.set_status(f"Instalacja zakończona, ale program nadal nie widzi: {names_after}.")
        self.after(
            0,
            lambda: self.show_info_dialog(
                "Uruchom ponownie program",
                "Instalacja została zakończona, ale Windows może odświeżyć ścieżki PATH dopiero "
                "po ponownym uruchomieniu programu.\n\n"
                "Zamknij aplikację i otwórz ją ponownie.",
            ),
        )
        return False

    def prepare_download_request(self, force_playlist=False):
        link = self.url.get().strip()
        folder = self.save_dir.get().strip()

        if not link:
            self.show_info_dialog("Brak linku", "Wklej link do filmu lub materiału.")
            return None

        if not folder or not os.path.isdir(folder):
            self.show_info_dialog("Błędny folder", "Wybierz poprawny folder zapisu.")
            return None

        download_playlist = force_playlist

        if force_playlist:
            self.log_line("Tryb playlisty: program pobierze całą listę.")
        elif is_probably_youtube_playlist(link):
            answer = self.ask_yes_no_cancel_dialog(
                "Uwaga - wykryto playlistę",
                "Wklejony link wygląda jak playlista YouTube.\n\n"
                "TAK - pobierz wszystkie pliki z playlisty.\n"
                "NIE - pobierz tylko pojedynczy utwór/film z tego linku.\n"
                "ANULUJ - przerwij operację.",
            )

            if answer is None:
                self.set_status("Pobieranie anulowane.")
                self.log_line("Anulowano po wykryciu playlisty.")
                return None

            if answer is True:
                download_playlist = True
                self.log_line("Użytkownik wybrał pobranie całej playlisty.")
            else:
                old_link = link
                link = strip_playlist_params(link)
                download_playlist = False
                self.log_line("Użytkownik wybrał pobranie tylko pojedynczego utworu.")
                self.log_line(f"Link oczyszczony z playlisty: {link}")
                if old_link != link:
                    self.url.set(link)

        return link, folder, download_playlist

    def start_download(self):
        self.trial_expired = False

        preset_label = self.quality_label_to_key(self.quality_box.get())
        preset = QUALITY_PRESETS.get(preset_label)
        if not preset:
            self.show_info_dialog("Brak formatu", "Wybierz jakość albo format pobierania.")
            return

        request = self.prepare_download_request(force_playlist=self.selected_mode == "PLAYLISTA")
        if not request:
            return

        missing = self.confirm_missing_components()
        if missing is None:
            return

        link, folder, download_playlist = request
        self.stop_requested = False
        self.set_busy(True)
        embed_subtitles = (
            preset["kind"] == "video"
            and self.selected_mode in SUBTITLE_MODES
            and self.language != "EN"
            and bool(self.subtitles_var.get())
        )

        if preset["kind"] == "audio":
            target = self.download_audio
            args = (
                link,
                folder,
                preset["format"],
                preset["audio_quality"],
                download_playlist,
                missing,
            )
        elif download_playlist:
            target = self.download_video_playlist
            args = (
                link,
                folder,
                preset["format"],
                preset["quality"],
                missing,
                embed_subtitles,
            )
        else:
            target = self.download_video
            args = (
                link,
                folder,
                preset["format"],
                preset["quality"],
                download_playlist,
                missing,
                embed_subtitles,
            )

        threading.Thread(target=target, args=args, daemon=True).start()

    def run_download_command(self, command, cwd=None, progress_label=None):
        output_lines = []
        self.log_line("Proces: " + self.describe_command_for_log(command))
        previous_progress_label = getattr(self, "active_progress_label", "")
        self.active_progress_label = progress_label or ""
        with self.process_lock:
            self.current_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors="replace",
                shell=False,
                cwd=cwd,
                env=get_process_environment(),
                creationflags=no_window_creation_flags(),
            )

        try:
            if self.current_process.stdout:
                for line in self.current_process.stdout:
                    clean_line = line.replace(chr(13), "").rstrip()
                    if clean_line:
                        output_lines.append(clean_line)
                        if not clean_line.startswith("__VSDP_FILE__:"):
                            self.update_status_from_process_line(clean_line)
                            self.log_line(clean_line)
                    if self.stop_requested:
                        break

            if self.stop_requested:
                self.terminate_current_process()

            self.current_process.wait()
            return self.current_process.returncode
        finally:
            self.last_process_output_lines = output_lines
            self.active_progress_label = previous_progress_label
            with self.process_lock:
                self.current_process = None

    def describe_command_for_log(self, command):
        if not command:
            return "nieznany"
        executable = Path(str(command[0])).name.lower()
        if "ffmpeg" in executable:
            return "FFmpeg - przetwarzanie/kompresja pliku"
        if "yt-dlp" in executable:
            if any(arg in {"-U", "--update", "--update-to"} for arg in command):
                return "yt-dlp - aktualizacja"
            return "yt-dlp - pobieranie"
        if "winget" in executable:
            return "winget - instalacja/aktualizacja komponentu"
        return Path(str(command[0])).name

    def run_capture_command(self, command):
        with self.process_lock:
            self.current_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                errors="replace",
                shell=False,
                env=get_process_environment(),
                creationflags=no_window_creation_flags(),
            )

        try:
            stdout, stderr = self.current_process.communicate()
            return self.current_process.returncode, stdout or "", stderr or ""
        finally:
            with self.process_lock:
                self.current_process = None

    def download_audio(self, link, folder, fmt, audio_quality, download_playlist, missing):
        try:
            if not self.ensure_components_installed(missing):
                return

            if self.stop_requested:
                self.set_status("Pobieranie przerwane.")
                return

            self.set_status("Pobieranie i konwersja audio...")
            self.log_line("Start pobierania audio...")

            output_template = os.path.join(folder, "%(title).200B.%(ext)s")
            command = [
                resolve_tool_command("yt-dlp"),
                "--newline",
                "--no-keep-video",
                "-x",
                "--audio-format",
                fmt,
                "--audio-quality",
                audio_quality,
                "-o",
                output_template,
            ]

            if not download_playlist:
                command.append("--no-playlist")

            command.append(link)

            self.log_line("Tryb: " + ("cała playlista" if download_playlist else "tylko pojedynczy utwór"))
            self.log_line(f"Format audio: {fmt}, jakość: {audio_quality}")
            code = self.run_download_command(command)

            if self.stop_requested:
                self.set_status("Pobieranie przerwane przez użytkownika.")
                self.after(0, lambda: self.show_info_dialog("Przerwano", "Pobieranie zostało zatrzymane."))
                return

            if code == 0:
                self.set_status("Gotowe. Plik audio został zapisany w wybranym folderze.")
                self.after(0, lambda: self.show_info_dialog("Gotowe", "Pobieranie i konwersja zakończone."))
            else:
                self.set_status("Wystąpił błąd podczas pobierania audio.")
                self.after(
                    0,
                    lambda: self.show_info_dialog(
                        "Błąd",
                        "Nie udało się pobrać lub przekonwertować pliku. Sprawdź log.",
                    ),
                )
        finally:
            self.set_busy(False)

    def get_retry_referer(self, link):
        try:
            parsed = urlparse(link)
        except Exception:
            return ""
        if not parsed.scheme or not parsed.netloc:
            return ""
        return f"{parsed.scheme}://{parsed.netloc}/"

    def get_browser_retry_variants(self, link):
        referer = self.get_retry_referer(link)
        browser_options = [
            "--user-agent",
            BROWSER_RETRY_USER_AGENT,
            "--add-header",
            f"Accept-Language: {BROWSER_RETRY_ACCEPT_LANGUAGE}",
            "--geo-bypass",
        ]
        if referer:
            browser_options.extend(["--referer", referer])
        return [
            ("standardowo", []),
            ("z naglowkami przegladarki", browser_options),
        ]

    def output_suggests_access_retry(self, output_lines):
        output_text = chr(10).join(output_lines or []).lower()
        retry_markers = [
            "http error 410",
            "http error 403",
            "http error 429",
            "unable to download webpage",
            "forbidden",
            "gone",
            "not available in your country",
            "geo",
        ]
        return any(marker in output_text for marker in retry_markers)

    def build_arte_format_selector(self, arte_prefix, video_quality):
        quality_to_height = {
            "4K": 2160,
            "1440p": 1440,
            "1080p": 1080,
            "720p": 720,
            "480p": 480,
            "360p": 360,
        }
        height = quality_to_height.get(video_quality)
        height_limit = f"[height<={height}]" if height else ""
        prefix_filter = f"[format_id^={arte_prefix}]"

        if video_quality == "Mini":
            return (
                f"worstvideo{prefix_filter}[ext=mp4]+worstaudio{prefix_filter}/"
                f"worst{prefix_filter}/worst"
            )

        return (
            f"bestvideo{prefix_filter}{height_limit}[ext=mp4]+bestaudio{prefix_filter}/"
            f"best{prefix_filter}{height_limit}[ext=mp4]/"
            f"bestvideo{prefix_filter}{height_limit}+bestaudio{prefix_filter}/"
            f"best{prefix_filter}{height_limit}"
        )

    def build_video_format_selector(self, video_format, video_quality, subtitle_info=None):
        arte_prefix = ""
        if subtitle_info and subtitle_info.get("found"):
            arte_prefix = str(subtitle_info.get("arte_format_prefix") or "")
        if arte_prefix:
            return self.build_arte_format_selector(arte_prefix, video_quality)

        quality_to_height = {
            "4K": 2160,
            "1440p": 1440,
            "1080p": 1080,
            "720p": 720,
            "480p": 480,
            "360p": 360,
        }
        if video_quality == "Mini":
            if video_format == "mp4":
                return "worst[ext=mp4]/worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst"
            if video_format == "webm":
                return "worst[ext=webm]/worstvideo[ext=webm]+worstaudio[ext=webm]/worst"
            return "worst"

        height = quality_to_height.get(video_quality)
        height_limit = f"[height<={height}]" if height else ""

        if video_format == "mp4":
            return (
                f"bestvideo{height_limit}[ext=mp4]+bestaudio[ext=m4a]/"
                f"best{height_limit}[ext=mp4]/"
                f"bestvideo{height_limit}+bestaudio/"
                f"best{height_limit}/best"
            )

        if video_format == "webm":
            return (
                f"bestvideo{height_limit}[ext=webm]+bestaudio[ext=webm]/"
                f"best{height_limit}[ext=webm]/"
                f"bestvideo{height_limit}+bestaudio/"
                f"best{height_limit}/best"
            )

        return f"bestvideo{height_limit}+bestaudio/best{height_limit}/best"

    def build_video_command(
        self, link, folder, video_format, video_quality, download_playlist, subtitle_info=None, access_options=None
    ):
        output_template = os.path.join(folder, "%(title).200B.%(ext)s")
        format_selector = self.build_video_format_selector(video_format, video_quality, subtitle_info)

        command = [
            resolve_tool_command("yt-dlp"),
            "--newline",
            "--progress",
            "--no-keep-video",
            "--print",
            "after_move:__VSDP_FILE__:%(filepath)s",
            "--no-quiet",
            "--no-simulate",
        ]

        if video_quality == "Mini":
            command.extend(
                [
                    "--format-sort",
                    "+size,+br,+res,+fps",
                ]
            )

        command.extend(
            [
                "-f",
                format_selector,
                "--merge-output-format",
                video_format,
                "-o",
                output_template,
            ]
        )

        if video_format in {"mp4", "webm"}:
            command.extend(["--recode-video", video_format])

        self.append_subtitle_options(command, subtitle_info)

        if access_options:
            command.extend(access_options)

        if not download_playlist:
            command.append("--no-playlist")

        command.append(link)
        return command

    def run_single_video_download(
        self, link, folder, video_format, video_quality, download_playlist, subtitle_info=None, access_options=None
    ):
        command = self.build_video_command(
            link, folder, video_format, video_quality, download_playlist, subtitle_info, access_options
        )
        return self.run_download_command(command)

    def run_video_download_with_access_retries(
        self, link, folder, video_format, video_quality, download_playlist, subtitle_info=None
    ):
        variants = self.get_browser_retry_variants(link)
        last_code = 1
        for index, (label, access_options) in enumerate(variants):
            if self.stop_requested:
                return last_code
            if index > 0:
                self.log_line(f"Dostęp: ponawiam pobieranie {label}.")
                self.set_status(f"Ponawiam pobieranie {label}...")
            last_code = self.run_single_video_download(
                link,
                folder,
                video_format,
                video_quality,
                download_playlist,
                subtitle_info=subtitle_info,
                access_options=access_options,
            )
            if last_code == 0:
                return 0
            if not self.output_suggests_access_retry(self.last_process_output_lines):
                return last_code
        return last_code

    def run_video_download_with_subtitle_fallback(
        self, link, folder, video_format, video_quality, download_playlist, subtitle_info
    ):
        code = self.run_video_download_with_access_retries(
            link, folder, video_format, video_quality, download_playlist, subtitle_info=subtitle_info
        )

        if (
            code == 0
            or self.stop_requested
            or not subtitle_info
            or not subtitle_info.get("found")
        ):
            return code, subtitle_info

        self.log_line(
            "Napisy: nie udało się pobrać lub zintegrować napisów. "
            "Ponawiam pobieranie filmu bez napisów."
        )
        self.set_status("Napisy nie zadziałały. Pobieram film bez napisów...")

        fallback_info = dict(subtitle_info)
        fallback_info["subtitle_download_failed"] = True
        fallback_code = self.run_video_download_with_access_retries(
            link, folder, video_format, video_quality, download_playlist, subtitle_info=None
        )

        if fallback_code == 0:
            return fallback_code, fallback_info

        return code, subtitle_info

    def resolve_playlist_entry_url(self, entry):
        if not isinstance(entry, dict):
            return None

        for key in ("webpage_url", "original_url", "url"):
            value = str(entry.get(key) or "").strip()
            if value.startswith("http://") or value.startswith("https://"):
                return value

        entry_id = str(entry.get("id") or entry.get("url") or "").strip()
        extractor = f"{entry.get('ie_key') or ''} {entry.get('extractor') or ''}".lower()
        if not entry_id:
            return None

        if "youtube" in extractor or (len(entry_id) == 11 and " " not in entry_id):
            return f"https://www.youtube.com/watch?v={entry_id}"

        return entry_id

    def read_playlist_entries(self, link):
        self.set_status("Odczytuję playlistę...")
        self.log_line("Odczytuję listę elementów playlisty...")

        command = [
            resolve_tool_command("yt-dlp"),
            "--flat-playlist",
            "--ignore-errors",
            "--dump-single-json",
            link,
        ]
        code, stdout, stderr = self.run_capture_command(command)

        for line in stderr.splitlines()[-12:]:
            clean_line = line.strip()
            if clean_line:
                self.log_line(clean_line)

        if self.stop_requested:
            return []

        if code != 0:
            self.log_line(f"Nie udało się odczytać playlisty. Kod błędu: {code}")
            return []

        try:
            playlist_data = json.loads(stdout)
        except json.JSONDecodeError as exc:
            self.log_line(f"Nie udało się odczytać danych playlisty: {exc}")
            return []

        entries = []
        for entry in playlist_data.get("entries") or []:
            entry_url = self.resolve_playlist_entry_url(entry)
            if entry_url:
                entries.append(entry_url)

        return entries

    def download_video_playlist(self, link, folder, video_format, video_quality, missing, embed_subtitles):
        completed = 0
        failures = 0
        subtitles_added = 0
        subtitles_missing = 0

        try:
            if not self.ensure_components_installed(missing):
                return

            if self.stop_requested:
                self.set_status("Pobieranie przerwane.")
                return

            entries = self.read_playlist_entries(link)
            total = len(entries)

            if self.stop_requested:
                self.set_status("Pobieranie przerwane przez użytkownika.")
                return

            if total == 0:
                self.set_status("Nie znaleziono elementów playlisty.")
                self.after(
                    0,
                    lambda: self.show_info_dialog(
                        "Błąd playlisty",
                        "Nie udało się odczytać elementów playlisty. Sprawdź log.",
                    ),
                )
                return

            self.log_line(f"Znaleziono elementów playlisty: {total}")
            self.log_line("Każdy film będzie scalony/konwertowany przed rozpoczęciem kolejnego.")
            self.log_line("Pliki tymczasowe po poprawnej konwersji będą usuwane automatycznie.")

            for index, entry_url in enumerate(entries, start=1):
                if self.stop_requested:
                    break

                self.set_status(f"Playlista: pobieranie {index}/{total}...")
                self.log_line("")
                self.log_line(f"--- Element playlisty {index}/{total} ---")
                self.log_line(f"Format wideo: {video_format}, jakość: {video_quality}")

                subtitle_info = self.prepare_subtitles_for_video(entry_url, embed_subtitles)
                code, subtitle_info = self.run_video_download_with_subtitle_fallback(
                    entry_url,
                    folder,
                    video_format,
                    video_quality,
                    download_playlist=False,
                    subtitle_info=subtitle_info,
                )

                if self.stop_requested:
                    break

                if code == 0:
                    mini_result = None
                    if video_quality == "Mini":
                        mini_result = self.compress_recent_video_download_to_mini()
                    if mini_result is not None and not mini_result.get("success"):
                        failures += 1
                        self.log_line(f"Błąd: element {index}/{total} nie został poprawnie skompresowany w trybie Mini.")
                        continue

                    completed += 1
                    if subtitle_info.get("found") and not subtitle_info.get("subtitle_download_failed"):
                        subtitles_added += 1
                    elif subtitle_info.get("enabled"):
                        subtitles_missing += 1
                    self.cleanup_embedded_subtitle_files(subtitle_info)
                    subtitle_message = self.format_subtitle_result(subtitle_info)
                    if subtitle_message:
                        self.log_line("Napisy: " + subtitle_message)
                    self.log_line(f"OK: element {index}/{total} zakończony i przekonwertowany.")
                else:
                    failures += 1
                    self.log_line(f"Błąd: element {index}/{total} zakończył się kodem {code}.")

            if self.stop_requested:
                self.set_status(f"Przerwano playlistę. Gotowe pliki: {completed}/{total}.")
                self.after(
                    0,
                    lambda: self.show_info_dialog(
                        "Przerwano",
                        f"Pobieranie playlisty zostało zatrzymane.\n\n"
                        f"Poprawnie zakończone pliki: {completed}/{total}.",
                    ),
                )
                return

            if failures == 0:
                if embed_subtitles:
                    self.log_line(
                        f"Napisy scalone: {subtitles_added}. Bez napisów PL/EN: {subtitles_missing}."
                    )
                self.set_status(f"Gotowe. Playlista wideo zakończona: {completed}/{total}.")
                self.after(0, lambda: self.show_info_dialog("Gotowe", "Pobieranie playlisty wideo zakończone."))
            else:
                self.set_status(f"Playlista zakończona z błędami. Gotowe: {completed}/{total}.")
                self.after(
                    0,
                    lambda: self.show_info_dialog(
                        "Zakończono z błędami",
                        f"Poprawnie pobrano: {completed}/{total}.\n"
                        f"Błędy: {failures}. Szczegóły są w logu.",
                    ),
                )
        finally:
            self.set_busy(False)

    def download_video(self, link, folder, video_format, video_quality, download_playlist, missing, embed_subtitles):
        try:
            if not self.ensure_components_installed(missing):
                return

            if self.stop_requested:
                self.set_status("Pobieranie przerwane.")
                return

            self.set_status("Pobieranie wideo...")
            self.log_line("Start pobierania wideo...")

            self.log_line("Tryb: " + ("cała playlista" if download_playlist else "tylko pojedynczy film"))
            self.log_line(f"Format wideo: {video_format}, jakość: {video_quality}")
            subtitle_info = self.prepare_subtitles_for_video(link, embed_subtitles)
            if self.stop_requested:
                self.set_status("Pobieranie przerwane przez użytkownika.")
                return
            code, subtitle_info = self.run_video_download_with_subtitle_fallback(
                link, folder, video_format, video_quality, download_playlist, subtitle_info
            )

            if self.stop_requested:
                self.set_status("Pobieranie przerwane przez użytkownika.")
                self.after(0, lambda: self.show_info_dialog("Przerwano", "Pobieranie zostało zatrzymane."))
                return

            if code == 0:
                mini_result = None
                if video_quality == "Mini":
                    mini_result = self.compress_recent_video_download_to_mini()
                if mini_result is not None and not mini_result.get("success"):
                    self.set_status("Mini: nie udało się skompresować pliku.")
                    self.after(
                        0,
                        lambda: self.show_info_dialog(
                            "Mini",
                            "Nie udało się skompresować pliku Mini. Sprawdź log.",
                        ),
                    )
                    return

                self.cleanup_embedded_subtitle_files(subtitle_info)
                subtitle_message = self.format_subtitle_result(subtitle_info)
                mini_message = self.format_mini_result_message(mini_result) if mini_result else ""
                if subtitle_message:
                    self.log_line("Napisy: " + subtitle_message)
                    status_message = "Gotowe. Wideo zapisane. " + subtitle_message
                    dialog_message = "Pobieranie wideo zakończone.\n\n" + subtitle_message
                else:
                    status_message = "Gotowe. Wideo zostało zapisane w wybranym folderze."
                    dialog_message = "Pobieranie wideo zakończone."
                if mini_message:
                    status_message = mini_message
                    dialog_message += "\n\n" + mini_message
                self.set_status(status_message)
                self.after(0, lambda: self.show_info_dialog("Gotowe", dialog_message))
            else:
                self.set_status("Wystąpił błąd podczas pobierania wideo.")
                self.after(
                    0,
                    lambda: self.show_info_dialog("Błąd", "Nie udało się pobrać wideo. Sprawdź log."),
                )
        finally:
            self.set_busy(False)

    def terminate_current_process(self):
        with self.process_lock:
            process = self.current_process

        if process and process.poll() is None:
            try:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
            except Exception as exc:
                self.log_line(f"Nie udało się zatrzymać procesu normalnie: {exc}")

    def stop_download(self):
        self.stop_requested = True
        self.set_status("Zatrzymywanie pobierania...")
        self.log_line("STOP: użytkownik przerwał pobieranie.")
        self.stop_btn.configure(state="disabled")
        threading.Thread(target=self.terminate_current_process, daemon=True).start()

    def on_close(self):
        if self.current_process and self.current_process.poll() is None:
            answer = self.ask_yes_no_dialog(
                "Proces trwa",
                "Pobieranie lub instalacja nadal trwa. Czy zatrzymać proces i zamknąć program?",
            )
            if not answer:
                return
            self.stop_requested = True
            self.terminate_current_process()

        self.destroy()


if __name__ == "__main__":
    app = VideoDownloaderApp()
    app.mainloop()
