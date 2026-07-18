# Video & Sound Downloader Pro v8.0.8

Detailed changelog since v8.0.0.

Version 8.0.8 remains **free of charge with no trial period and no time limit**. The application is designed to download audio, video, and playlists from supported sources and to discover publicly embedded media on web pages.

## 1. English localization

- Completed English translations for status messages, logs, dialogs, download errors, discovery results, live-stream checks, media validation, and folder operations.
- Added English labels and instructions to the discovered-media selection window.
- Added English messages for format availability diagnostics and service-specific guidance.
- Kept long technical diagnostics in the log and error dialog while showing only a concise action in the status bar.

## 2. Format availability diagnostics

- Added an additional yt-dlp metadata check when a requested video format is reported as unavailable.
- The program can now report detected video resolutions, the highest detected resolution, and source container types.
- Improved the message shown when the requested quality is visible in the source but a complete video-and-audio result cannot be selected.
- Prevented the program from recommending the same quality again when that quality is already present in the source.

## 3. ARTE video, audio, and subtitle handling

- Fixed ARTE downloads where valid audio tracks were rejected because ARTE did not expose a conventional audio codec value.
- Added language-aware ARTE format selection based on the Polish or English application mode.
- Separated ARTE language-variant selection from the optional subtitle embedding switch.
- Fixed ARTE selection in English mode, where disabling subtitle embedding previously removed information required to select a compatible video and audio pair.
- Verified the ARTE test page with MP4 720p, MP4 1080p, and MP4 Best selectors.

## 4. Discover mode guidance

- Added a helpful explanation when Discover is used on a broad portal page containing too many unrelated links.
- The program now suggests opening the specific article or media subpage and running Discover again.
- Added direct guidance for YouTube links: users are instructed to select the standard audio, video, or playlist mode.
- Added a Facebook recommendation dialog. Users can select:
  - **Yes** to continue with Discover anyway.
  - **No** to close the message and choose the standard audio, video, or playlist tile.
- Standard pages intended for discovery remain unaffected.

## 5. Discover and window layout

- Locked the discovered-media window to 780 × 500 so resizing cannot break its table or buttons.
- Set the minimum main-window client size to 980 × 760 so all primary controls remain visible.
- Kept horizontal and vertical scrolling in the discovered-media table for long titles and URLs.

## 6. Download and error presentation

- Full format diagnostics are written to the log and remain available in the error dialog.
- The status bar now displays a short action instead of a multi-line diagnostic.
- Improved distinction between:
  - a genuinely unavailable resolution,
  - a visible resolution that cannot be combined with audio,
  - a source that does not report resolution metadata,
  - and an audio-only source.

## 7. Distribution safety

- Removed Portable v8.0.0 from the public GitHub release because the archive contained material that must not be distributed.
- Removed Portable references from the v8.0.0 release description, changelog, and checksum list.
- Replaced the corrected v8.0.0 changelog and checksum assets.
- The v8.0.8 build script does not create a Portable directory or Portable ZIP archive.
- The v8.0.8 signing script no longer exports the signing certificate to a `.cer` file.
- Private signing material must never be included in public release assets or source-disclosure packages.

## 8. Version and build files

- Updated the application version to 8.0.8.
- Added v8.0.8 launch, build, signing, PyInstaller, requirements, and Windows version-information files.
- Updated local runtime and build dependency directories to v8.0.8 while retaining v8.0.0 directories as compatibility fallbacks in source mode.
- The bundled yt-dlp file currently reports version 2026.07.04.

## Legal and access limitations

The program does not bypass DRM, subscriptions, authentication, regional restrictions, or other access controls. It must only be used for media the user has the legal right or permission to download.
