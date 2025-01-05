# EPUB to Audio Converter

This project converts chapters from an EPUB ebook into audio files using text-to-speech (TTS) functionality.

## Overview

The script processes an EPUB file, extracts chapter text, and then either:

1.  **Prints Chapter Numbers (Mode 1):** Logs the chapter numbers extracted from the EPUB to a `logfile.log`.
2.  **Converts Chapters to Audio (Mode other than 1):** Generates audio files from the text content of the specified chapter range.

The project uses a configuration file (`config.yml`) to control its behavior, and it is driven by a main python script `main.py` which relies on helper functions found in the `util.py` module.

## Files

*   `main.py`: The main script that controls the flow of execution.
*   `util.py`: Contains helper functions for EPUB parsing, audio generation, configuration loading, and subtitle extraction/validation.
*   `config.yml`: YAML configuration file for specifying input, output, and operational parameters.
*   `requirements.txt`: Lists Python package dependencies.
*   `README.md`: This file.
*   `voice_list.csv`: A CSV file containing a comprehensive list of available voices for `edge-tts`.

## Configuration (`config.yml`)

The `config.yml` file contains the following settings:

```yaml
mode: 1 # 1: print chapter numbers, other: get audio
epub:
  file: "in/in.epub"
out:
  chapter:
    start: 56
    end: 100
  path: "out"
  voice: "zh-CN-YunjianNeural"
  watermark: " this is the end of chapter thank you for listening"
```

*   **`mode`**:
    *   `1`: The script will list chapter numbers in a log file.
    *   Other number: The script will generate audio files.
*   **`epub.file`**: The path to the input EPUB file.
*   **`out.chapter.start`**: The starting chapter number to process when generating audio files.
*   **`out.chapter.end`**: The ending chapter number to process when generating audio files.
*   **`out.path`**: The path to the directory where the output files will be saved.
*   **`out.voice`**: The name of the voice to use for text-to-speech. A full list of available voices can be found in `voice_list.csv`.
*   **`out.watermark`**: The watermark text to be appended to each chapter.

## Dependencies

The project relies on the following Python packages:

*   `ebooklib`: For EPUB parsing.
*   `PyYAML`: For reading YAML config files.
*   `beautifulsoup4`: For parsing HTML content from EPUB files.
*   `edge-tts`: For Text-To-Speech.

These dependencies can be installed using `pip` with the command:

```bash
pip install -r requirements.txt
```

## Usage

1.  **Install dependencies:** Run `pip install -r requirements.txt` to install required libraries.
2.  **Prepare EPUB file:** Place your EPUB file in the "in" directory (or adjust `config.yml` accordingly).
3.  **Configure `config.yml`:** Adjust the settings to your liking (e.g., output path, chapter range, mode, voice, watermark).
    *   A full list of available voices can be found in `voice_list.csv`. You can also find voice lists at [azure list](https://speech.azure.cn/portal/voicegallery) or [github list](https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462).
    *   Recommended Voices are:
        ```json
        {"English":['en-US-ChristopherNeural'],"Chinese":["zh-CN-XiaoxiaoNeural", "zh-CN-YunjianNeural", "zh-CN-YunyangNeural", "zh-CN-YunxiNeural", "zh-CN-YunxiaNeural"]}
        ```
4.  **Run the script:** Execute `python main.py` in your terminal or command prompt.
5.  **Check output:** If mode is set to `1` a file named `logfile.log` will be generated. If the mode is not `1` audio files will be generated in the specified output directory, along with subtitle files, in SRT format.

## Example

### Print Chapter Numbers (Mode 1):

1.  Set `mode: 1` in `config.yml`.
2.  Run `python main.py`.
3.  Check log file, named `logfile.log`.

### Convert Chapters to Audio (Mode not equal to 1)

1. Set `mode` to any other integer except for 1 (e.g., 2) in `config.yml`.
2. Adjust the chapter range, voice, and watermark as desired.
3. Run `python main.py`.
4. Audio files and subtitle files (.srt) will be generated in the output directory.

## Code Explanation

### `main.py`

*   Loads the configuration from `config.yml`.
*   Extracts chapter texts from the EPUB file.
*   Conditionally executes based on the `mode`.
*   Handles creation of the output directory.
*   Loads the `voice` and `watermark` from the `config.yml`
*   Calls the functions of `util.py`.

### `util.py`

*   `get_audio(TEXT, OUTPUT_FILE, SRT_FILE, VOICE)`: Converts text to audio using the specified TTS voice and creates an SRT file for subtitles.
*   `extract_chapters(epub_path)`: Extracts chapter content from the EPUB, returning a dictionary of {chapter_number: text}.
*   `load_config(config_path)`: Loads configuration data from a YAML file.
*   `srt_to_text_variable(srt_file_path)`: Extracts only text from a srt file.
*   `process_chapters(chapters, output_dir, VOICE, watermark, chapter_num_start, chapter_num_end)`: Processes a subset of chapters based on numbers and generates audio files.

## Customization

*   Modify the `config.yml` to change the EPUB file path, output location, chapter ranges, operational mode, voice, and watermark.
*   Further extend the `util.py` with more logic and methods to process the book further.

## Notes

*   Ensure that the output directory exists or the script will create it automatically.