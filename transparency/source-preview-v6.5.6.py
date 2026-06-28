"""
Fragment rzeczywistego kodu Video And Sound Downloader Pro v6.5.6.

To nie jest pelny kod zrodlowy programu. Ten wycinek pokazuje czesc
odpowiedzialna za odnajdywanie narzedzi yt-dlp/FFmpeg, uruchamianie
procesu pobierania oraz budowanie komend yt-dlp dla audio i wideo.

Czesc metod interfejsu uzytkownika, obslugi trialu, podpisywania i builda
zostala celowo pominieta.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


TOOLS_DIR_NAME = "tools"


def get_tool_executable_name(command: str) -> str:
    if os.name == "nt" and not command.lower().endswith(".exe"):
        return f"{command}.exe"
    return command


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


class VideoDownloaderAppDownloadPreview:
    def run_download_command(self, command):
        output_lines = []
        with self.process_lock:
            self.current_process = subprocess.Popen(
                command,
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
                self.after(
                    0,
                    lambda: self.show_info_dialog(
                        "Blad",
                        "Nie udalo sie pobrac lub przekonwertowac pliku. Sprawdz log.",
                    ),
                )
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