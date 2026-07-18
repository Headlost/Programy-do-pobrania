# Video & Sound Downloader Pro v8.0.8 — Update Notes

## License and availability

Version 8.0.8 is **free to use with no trial period and no time limit**. The program downloads audio, video, and playlists from supported sources and can discover publicly embedded media on web pages.

## Update summary

Version 8.0.8 is a corrective update focused on localization, Discover-mode guidance, format diagnostics, ARTE compatibility, window stability, and safer release packaging.

The update has been prepared and validated as the version 8.0.8 release.

## What users will notice

- English mode now provides consistent English text across the interface, dialogs, logs, and status messages.
- Long format diagnostics no longer expand the status area. The status bar shows a short recommended action, while complete details remain in the log and error dialog.
- When a selected format cannot be downloaded, the program checks the source again and reports the detected resolutions and source containers.
- YouTube links entered in Discover are redirected to the standard audio, video, or playlist workflow.
- Facebook links entered in Discover show a recommendation with a **Yes/No** choice.
- Broad portal pages that expose too much unrelated content now include a suggestion to open the specific article or media subpage.
- The discovered-media window can no longer be resized into a broken layout.

## ARTE fix

ARTE may expose valid audio-only HLS tracks without a conventional codec value. Earlier selectors rejected those tracks, causing false “Requested format is not available” errors even when the selected resolution was listed.

Version 8.0.8 selects ARTE video and audio using the matching language-variant identifier:

- Polish application mode prefers the Polish ARTE variant.
- English application mode prefers the English ARTE variant.
- The selection works independently of optional subtitle embedding.

The supplied ARTE test page was validated in simulation mode for 720p, 1080p, and Best.

## Distribution and security change

The public Portable v8.0.0 archive was removed because it contained a signing-certificate file. Related references and checksums were removed or corrected.

Version 8.0.8 follows these packaging rules:

- no Portable archive is generated,
- no signing certificate is exported beside the build,
- no certificate file is copied into release materials,
- only intentional release assets may be uploaded,
- checksums must be generated after final files are built,
- source-disclosure content must be reviewed before publication.

## Local v8.0.8 files

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

## Release validation checklist

1. Run the source version and verify both Polish and English modes.
2. Test MP3, MP4, playlist, and Discover workflows.
3. Recheck ARTE in Polish and English modes.
4. Build and sign the final EXE locally.
5. Verify the Authenticode signature and timestamp.
6. Scan the complete release staging directory for `.cer`, `.pfx`, `.p12`, private keys, credentials, and local-only files.
7. Generate SHA-256 checksums from the final approved assets.
8. Review the source-disclosure package separately.
9. Publish only after an explicit release approval.
