"""
Wybrane fragmenty rzeczywistej logiki Video And Sound Downloader Pro v8.0.8.

Pełniejszy snapshot znajduje się w folderze source-disclosure-v8.0.8.
Ten plik pokazuje najważniejsze mechanizmy obecne w v8.0.8:
wykrywanie multimediów, bezpieczne nazwy, wybór kompletnego wideo oraz
walidację obrazu i dźwięku.
"""

import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urljoin, urlparse


APP_VERSION = "8.0.8"
DIRECT_MEDIA_EXTENSIONS = (
    ".mp4", ".webm", ".mkv", ".mov", ".m4v", ".mp3", ".m4a",
    ".aac", ".ogg", ".opus", ".wav", ".flac", ".m3u8", ".mpd",
)


class VideoDownloaderV8Preview:
    def is_direct_media_url(self, url):
        if not str(url).startswith(("http://", "https://")):
            return False
        parsed = urlparse(str(url))
        path = parsed.path.lower()
        lowered = str(url).lower()
        return (
            path.endswith(DIRECT_MEDIA_EXTENSIONS)
            or any(marker in lowered for marker in (".m3u8?", ".mpd?", "format=mp4"))
            or any(marker in path for marker in ("/manifest/", "/playlist/", "/video-stream/", "/audio-stream/"))
        )

    def extract_media_urls_from_document(self, document, page_url):
        decoded = str(document or "")
        for escaped, plain in ((r"\/", "/"), (r"\u002f", "/"), (r"\u002F", "/")):
            decoded = decoded.replace(escaped, plain)

        extensions = "|".join(re.escape(ext.lstrip(".")) for ext in DIRECT_MEDIA_EXTENSIONS)
        patterns = [
            rf"https?://[^\s\"'<>\\]+?\.(?:{extensions})(?:\?[^\s\"'<>\\]*)?",
            rf"(?P<url>//[^\s\"'<>\\]+?\.(?:{extensions})(?:\?[^\s\"'<>\\]*)?)",
        ]
        found = []
        for pattern in patterns:
            for match in re.finditer(pattern, decoded, flags=re.IGNORECASE):
                value = match.groupdict().get("url") or match.group(0)
                absolute = urljoin(page_url, value.rstrip("),;]"))
                if self.is_direct_media_url(absolute):
                    found.append(absolute)
        return list(dict.fromkeys(found))

    def safe_detected_filename_stem(self, title):
        stem = re.sub(r'[<>:"/\\|?*%\x00-\x1f]', "_", str(title or "Wykryty materiał"))
        stem = re.sub(r"\s+", " ", stem).strip(" .") or "Wykryty materiał"
        return stem[:180].rstrip(" .") or "Wykryty materiał"

    def unique_detected_filename_stem(self, title, folder, extension, reserved_stems):
        base = self.safe_detected_filename_stem(title)
        candidate = base
        number = 2
        extension = str(extension or "").lstrip(".")
        while candidate.casefold() in reserved_stems or os.path.exists(
            os.path.join(folder, f"{candidate}.{extension}")
        ):
            suffix = f" ({number})"
            candidate = base[: 180 - len(suffix)].rstrip(" .") + suffix
            number += 1
        reserved_stems.add(candidate.casefold())
        return candidate

    def build_video_format_selector(self, video_format, video_quality):
        quality_to_height = {"1080p": 1080, "720p": 720, "480p": 480}
        height = quality_to_height.get(video_quality)
        height_limit = f"[height<={height}]" if height else ""

        if video_quality == "Mini":
            return (
                "worst[ext=mp4][height>0][protocol^=http]/"
                "worstvideo[vcodec!=none][ext=mp4]+worstaudio[acodec!=none][ext=m4a]/"
                "worst[vcodec!=none][acodec!=none][ext=mp4]/"
                "worstvideo[vcodec!=none]+worstaudio[acodec!=none]/"
                "worst[vcodec!=none][acodec!=none]"
            )

        if video_format == "mp4":
            return (
                f"bestvideo{height_limit}[vcodec!=none][ext=mp4]+bestaudio[acodec!=none][ext=m4a]/"
                f"best{height_limit}[ext=mp4][height>0][protocol^=http]/"
                f"best{height_limit}[vcodec!=none][acodec!=none][ext=mp4]/"
                f"bestvideo{height_limit}[vcodec!=none]+bestaudio[acodec!=none]/"
                f"best{height_limit}[vcodec!=none][acodec!=none]"
            )
        return (
            f"bestvideo{height_limit}[vcodec!=none]+bestaudio[acodec!=none]/"
            f"best{height_limit}[height>0][protocol^=http]/"
            f"best{height_limit}[vcodec!=none][acodec!=none]"
        )

    def extract_downloaded_video_paths_from_output(self, output_lines):
        paths = []
        json_marker = "__VSDP_FILE_JSON__:"
        legacy_marker = "__VSDP_FILE__:"
        for line in output_lines or []:
            raw_path = ""
            if json_marker in line:
                payload = line.split(json_marker, 1)[1].strip()
                try:
                    decoded = json.loads(payload)
                    raw_path = decoded if isinstance(decoded, str) else ""
                except json.JSONDecodeError:
                    pass
            elif legacy_marker in line:
                raw_path = line.split(legacy_marker, 1)[1].strip().strip('"')
            if raw_path:
                paths.append(Path(raw_path))
        return paths

    def probe_media_stream_types(self, file_path):
        command = [
            "ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
            "-of", "json", str(file_path),
        ]
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            return set()
        data = json.loads(completed.stdout)
        return {
            str(stream.get("codec_type") or "").lower()
            for stream in data.get("streams") or []
        }

    def media_streams_are_decodable(self, file_path):
        command = [
            "ffmpeg", "-v", "error", "-xerror", "-i", str(file_path),
            "-map", "0:v:0", "-map", "0:a:0", "-t", "2", "-f", "null", "-",
        ]
        completed = subprocess.run(command, capture_output=True, timeout=20, check=False)
        return completed.returncode == 0

    def validate_video_file(self, file_path):
        stream_types = self.probe_media_stream_types(file_path)
        return {"video", "audio"}.issubset(stream_types) and self.media_streams_are_decodable(file_path)
