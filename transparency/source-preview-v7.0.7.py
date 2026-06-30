"""
Fragment rzeczywistego kodu Video And Sound Downloader Pro v7.0.7.

To nie jest pelny kod zrodlowy programu. Ten wycinek pokazuje czesc
odpowiedzialna za odnajdywanie narzedzi yt-dlp/FFmpeg, uruchamianie
procesu pobierania oraz budowanie komend yt-dlp dla audio, wideo,
Facebooka i playlist.

Czesc metod interfejsu uzytkownika, obslugi przycisku Fix, podpisywania
i builda zostala celowo pominieta.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


APP_VERSION = "7.0.7"
TOOLS_DIR_NAME = "tools"
SUBTITLE_MODES = {"MP4", "FACEBOOK"}


def get_tool_executable_name(command: str) -> str:
    if os.name == "nt" and not command.lower().endswith(".exe"):
        return f"{command}.exe"
    return command


def get_external_tools_dir() -> Path:
    base_dir = Path(os.environ.get("LOCALAPPDATA") or Path.home())
    return base_dir / "VideoAndSoundDownloaderPro" / "tools"


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

    external_candidate = get_external_tools_dir() / executable_name
    if external_candidate.exists():
        return external_candidate

    return None


def get_bundled_tools_dir():
    for command in ("yt-dlp", "ffmpeg", "ffprobe"):
        tool_path = get_bundled_tool_path(command)
        if tool_path:
            return tool_path.parent
    return None


def resolve_tool_command(command: str) -> str:
    bundled_path = get_bundled_tool_path(command)
    if bundled_path:
        return str(bundled_path)
    return shutil.which(command) or command


def command_exists(command: str) -> bool:
    return get_bundled_tool_path(command) is not None or shutil.which(command) is not None


def get_process_environment():
    env = os.environ.copy()
    tools_dir = get_bundled_tools_dir()
    if tools_dir:
        env["PATH"] = str(tools_dir) + os.pathsep + env.get("PATH", "")
    return env


def no_window_creation_flags() -> int:
    if os.name == "nt":
        return getattr(subprocess, "CREATE_NO_WINDOW", 0)
    return 0


def is_probably_youtube_playlist(url: str) -> bool:
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    return "list" in params and "youtube" in parsed.netloc.lower()


def strip_playlist_params(url: str) -> str:
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    params.pop("list", None)
    params.pop("start_radio", None)
    clean_query = urlencode(params, doseq=True)
    return urlunparse(parsed._replace(query=clean_query))


class VideoDownloaderAppDownloadPreview:
    def run_download_command(self, command, cwd=None, progress_label=None):
        output_lines = []
        with self.process_lock:
            self.current_process = subprocess.Popen(
                command,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors="replace",
                shell=False,
                env=get_process_environment(),
                creationflags=no_window_creation_flags(),
            )

        try:
            if self.current_process.stdout:
                for line in self.current_process.stdout:
                    clean_line = line.replace(chr(13), "").rstrip()
                    if clean_line:
                        output_lines.append(clean_line)
                        self.update_status_from_process_line(clean_line, progress_label=progress_label)
                        self.log_line(clean_line)
                    if self.stop_requested:
                        break

            if self.stop_requested:
                self.terminate_current_process()

            self.current_process.wait()
            return self.current_process.returncode
        finally:
            self.last_process_output_lines = output_lines
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

            self.log_line("Tryb: " + ("cala playlista" if download_playlist else "tylko pojedynczy utwor"))
            self.log_line(f"Format audio: {fmt}, jakosc: {audio_quality}")
            code = self.run_download_command(command)

            if self.stop_requested:
                self.set_status("Pobieranie przerwane przez uzytkownika.")
                self.after(0, lambda: self.show_info_dialog("Przerwano", "Pobieranie zostalo zatrzymane."))
                return

            if code == 0:
                self.set_status("Gotowe. Plik audio zostal zapisany w wybranym folderze.")
                self.after(0, lambda: self.show_info_dialog("Gotowe", "Pobieranie i konwersja zakonczone."))
            else:
                self.set_status("Wystapil blad podczas pobierania audio.")
                self.after(0, lambda: self.show_info_dialog("Blad", "Nie udalo sie pobrac pliku. Sprawdz log."))
        finally:
            self.set_busy(False)

    def build_video_command(
        self, link, folder, video_format, video_quality, download_playlist, subtitle_info=None, access_options=None
    ):
        output_template = os.path.join(folder, "%(title).200B.%(ext)s")
        format_selector = self.build_video_format_selector(video_format, video_quality)

        command = [
            resolve_tool_command("yt-dlp"),
            "--newline",
            "--no-keep-video",
            "-f",
            format_selector,
            "--merge-output-format",
            video_format,
            "-o",
            output_template,
        ]

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

    def read_playlist_entries(self, link):
        self.set_status("Odczytuje playliste...")
        self.log_line("Odczytuje liste elementow playlisty...")
        command = [
            resolve_tool_command("yt-dlp"),
            "--flat-playlist",
            "--dump-single-json",
            "--no-warnings",
            link,
        ]
        code, stdout = self.run_capture_command(command)
        if code != 0:
            self.log_line(f"Nie udalo sie odczytac playlisty. Kod bledu: {code}")
            return []

        try:
            playlist_data = json.loads(stdout)
        except json.JSONDecodeError as exc:
            self.log_line(f"Nie udalo sie odczytac danych playlisty: {exc}")
            return []

        entries = []
        for entry in playlist_data.get("entries") or []:
            entry_url = self.resolve_playlist_entry_url(entry)
            if entry_url:
                entries.append(entry_url)
        return entries

    def download_video_playlist(self, link, folder, video_format, video_quality, missing, embed_subtitles):
        try:
            if not self.ensure_components_installed(missing):
                return

            entries = self.read_playlist_entries(link)
            if not entries:
                self.set_status("Nie znaleziono elementow playlisty.")
                self.after(
                    0,
                    lambda: self.show_info_dialog(
                        "Blad playlisty",
                        "Nie udalo sie odczytac elementow playlisty. Sprawdz log.",
                    ),
                )
                return

            total = len(entries)
            completed = 0
            self.log_line(f"Znaleziono elementow playlisty: {total}")

            for index, entry_link in enumerate(entries, start=1):
                if self.stop_requested:
                    break
                self.log_line(f"--- Element playlisty {index}/{total} ---")
                subtitle_info = self.get_subtitle_info(entry_link, video_format, embed_subtitles)
                code = self.run_single_video_download(
                    entry_link,
                    folder,
                    video_format,
                    video_quality,
                    download_playlist=False,
                    subtitle_info=subtitle_info,
                )
                if code == 0:
                    completed += 1

            if self.stop_requested:
                self.set_status(f"Przerwano playliste. Gotowe pliki: {completed}/{total}.")
            else:
                self.set_status(f"Gotowe. Playlista wideo zakonczona: {completed}/{total}.")
        finally:
            self.set_busy(False)
