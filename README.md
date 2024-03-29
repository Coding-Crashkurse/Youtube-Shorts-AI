# YouTubeShortsAI

## Introduction
YouTubeShortsAI is an innovative project that automates the process of creating and uploading short videos to YouTube. It leverages various APIs to search for images, generate transcripts, resize images, and upload videos.

## Prerequisites
Before running YouTubeShortsAI, ensure you have the following environment variables set in a `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key for transcript generation.
- `PEXELS_API_KEY`: Your Pexels API key for image searching.
- `IMAGEMAGICK_BINARY`: Path to your ImageMagick binary (e.g., `C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe`).

You also need the `client_secret.json` file from YouTube to use the YouTube API.

## Usage
To use YouTubeShortsAI, navigate to the project directory and run the Typer CLI commands.

### Available Commands
- **clean-folder**: Cleans up the working directory. Use this to clear any residual files from previous runs.
```bash
  python main.py clean_folder
```
- **main**:  Main command to generate and upload a video.

```bash
python main.py main --fact "interesting animal fact" --do_cleanup True --upload True --target_width 1080 --target_height 1920
```

- `fact`: Specify the fact or topic for the video.
- `do_cleanup`: Set to True to perform cleanup before running the script. Default is True.
- `upload`: Set to True to upload the video after creation. Default is True.
- `target_width`: Set the target width for image resizing. Default is 1080.
- `target_height`: Set the target height for image resizing. Default is 1920.

- **pick-random-facts**: Chooses a random fact from a specified YAML file and processes it to create and upload a video.

```bash
python main.py pick-random-fact --file-path "./facts.yaml"
```


Have fun :)

