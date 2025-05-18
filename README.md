# YouTube Subtitles Downloader and Converter

A tool to download YouTube video subtitles and convert them to plain text.

## Requirements

- Python 3
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Install with: `pip install yt-dlp`

## Usage

### Step 1: Download Subtitles from YouTube

Use yt-dlp to download subtitles from a YouTube channel without downloading the videos:

```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format vtt https://www.youtube.com/@healnpd -o "./healNpd/%(title)s.%(ext)s"
```

Options explained:
- `--write-auto-sub`: Download auto-generated subtitles
- `--sub-lang en`: Download English subtitles
- `--skip-download`: Don't download the video, only the subtitles
- `--sub-format vtt`: Download subtitles in VTT format
- `-o "./healNpd/%(title)s.%(ext)s"`: Save files in the healNpd folder with the video title as filename

### Step 2: Convert VTT Files to Plain Text

After downloading the subtitles, use the provided Python script to convert them to plain text:

```bash
python vtt_to_text.py ./healNpd
```

This will:
1. Process all VTT files in the specified folder
2. Create a new output folder (e.g., `output_healNpd`)
3. Save converted text files with the same names as the original VTT files

## Example Workflow

```bash
# Download subtitles from a YouTube channel
yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format vtt https://www.youtube.com/@healnpd -o "./healNpd/%(title)s.%(ext)s"

# Convert the downloaded VTT files to text
python vtt_to_text.py ./healNpd

# Find your converted text files in the output folder
ls output_healNpd
``` 