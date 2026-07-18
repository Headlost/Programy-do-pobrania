# 🚀 Video & Sound Downloader Pro v8.0.8

## Free to use — no trial and no time limit

Video & Sound Downloader Pro v8.0.8 is provided **free of charge with no trial period and no time limit**. All download modes remain available without a subscription or an expiration date.

## What the program does

Video & Sound Downloader Pro helps users download audio, video, and playlists from supported links and discover publicly embedded media on web pages. It supports standard sources recognized by yt-dlp as well as direct media files and streams such as HLS, DASH, and Smooth Streaming.

The program must only be used for media the user owns or has permission to download. It does not bypass DRM, subscriptions, authentication, regional restrictions, or other access controls.

## Six key capabilities

### 1. Discover embedded media

**DISCOVER** scans public web pages for embedded audio and video. It can inspect yt-dlp metadata, HTML media elements, page metadata, JavaScript/JSON configuration, direct CDN links, and streaming manifests. Detected items are presented in a selectable list.

### 2. Protection against unfinished live streams

The application detects active, unfinished live streams before downloading. Such streams are blocked so they do not download indefinitely or leave yt-dlp and FFmpeg processes running. After a stream ends and becomes a regular recording, it can be downloaded normally.

### 3. Clear and useful error handling

Instead of displaying only a generic failure, the program distinguishes between DRM, required login, invalid sessions or cookies, private media, regional restrictions, age restrictions, authorization problems, missing formats, incomplete video files, and unavailable sources.

### 4. Video and audio integrity checks

Downloaded video is verified for both picture and sound. FFprobe checks the available streams, and FFmpeg performs a short decoding test so an audio-only, damaged, or undecodable file is not reported as a successful video download.

### 5. Better playlists, formats, and Mini modes

The application supports audio, video, and complete playlist workflows, including improved YouTube and YouTube Music playlist handling. It also provides MP3 Mini and MP4 Mini modes, large-file processing, and output options such as MP4, WEBM, MKV, MP3, M4A, WAV, and OPUS.

### 6. Easier everyday workflow

Facebook links can use the standard audio and video modes, while Discover remains available when needed. The **Downloads** button opens the actual destination folder used in the current session. Clear Polish and English interface modes make the workflow easier to follow.

## What is improved in v8.0.8

Version 8.0.8 is a corrective update that further improves download reliability, English localization, Discover-mode guidance, format diagnostics, ARTE support, window stability, and release safety.

## More consistent English interface

English mode now covers the main interface, status messages, logs, dialogs, discovery results, media validation, format errors, and service-specific guidance.

Long technical messages are no longer displayed in the status area. The status bar presents a concise next step, while the full explanation remains available in the log and error dialog.

## Better format diagnostics

When a requested video option cannot be selected, the application performs an additional metadata check and can report:

- detected video resolutions,
- the highest detected resolution,
- source video containers,
- audio-only sources,
- and sources that do not report resolution metadata.

The application also recognizes when the selected quality is visible but a complete video-and-audio result could not be created, instead of recommending the same quality again.

## ARTE download fix

ARTE uses language-specific HLS variants and may omit a conventional codec value for valid audio tracks. This previously caused false “No media stream” errors for options such as MP4 720p, MP4 1080p, and MP4 Best.

Version 8.0.8 now pairs ARTE video and audio using the appropriate language variant:

- Polish mode selects the Polish ARTE variant.
- English mode selects the English ARTE variant.

ARTE selection now works independently of optional subtitle embedding.

## Clearer Discover workflow

Discover is intended for finding media embedded on pages that do not provide a simple direct media link.

- YouTube links now direct users to the standard audio, video, or playlist modes.
- Facebook links show a recommendation and allow the user to continue with Discover if desired.
- Broad portal pages suggest opening the specific article or media subpage before trying again.
- The discovered-media window has a fixed layout, and the main window cannot be reduced below the size required to show its controls correctly.

## Safer distribution

The previously published Portable v8.0.0 archive was removed because it contained material that must not be publicly distributed. Its release references and checksum entry were also removed.

Version 8.0.8 does not generate a Portable archive, and its signing script does not export a certificate file.

The intended release format is a reviewed standalone EXE plus explicitly approved transparency and documentation assets. Private signing material is never part of the release.

## Included components

The local build configuration uses:

- yt-dlp 2026.07.04,
- FFmpeg,
- FFprobe,
- CustomTkinter,
- and the application resources required by the interface.

## Important

The program does not bypass DRM, paid access, authentication, regional restrictions, or service protections. Use it only for media you are legally allowed to download.

---

This document accompanies the version 8.0.8 release.
