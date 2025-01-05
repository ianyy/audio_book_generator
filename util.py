import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import yaml
import edge_tts
import re


def get_audio(TEXT, OUTPUT_FILE, SRT_FILE, VOICE) -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    submaker = edge_tts.SubMaker()
    with open(OUTPUT_FILE, "wb") as file:
        for chunk in communicate.stream_sync():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)

    with open(SRT_FILE, "w", encoding="utf-8") as file:
        file.write(submaker.get_srt())


def extract_chapters(epub_path):
    """
    Extracts text content from chapters in an EPUB file.

    Args:
        epub_path (str): Path to the EPUB file.

    Returns:
        dict: A dictionary where keys are chapter numbers and values are chapter texts.
    """
    book = epub.read_epub(epub_path)
    chapters = {}
    chapter_num = 1

    # Loop through items in the EPUB file
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), "html.parser")
            chapter_text = soup.get_text().strip()
            chapters[chapter_num] = chapter_text
            chapter_num += 1

    return chapters


def load_config(config_path):
    """
    Loads configuration from a YAML file.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        dict: The loaded configuration.
    """
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def srt_to_text_variable(srt_file_path):
    """Converts an SRT file to a text variable, returning only the subtitle text.

    Args:
        srt_file_path (str): The path to the SRT file.

    Returns:
        str: A string containing all extracted subtitle text, or None if an error occurs.
    """
    try:
        with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
            lines = srt_file.readlines()

        subtitle_text = []
        is_subtitle_text = False # Flag to track when we are reading actual text

        for line in lines:
            line = line.strip() # remove whitespace
            if not line:
                is_subtitle_text = False # if line is blank then no longer text
            elif re.match(r'^\d+$', line): # detect the number line
                is_subtitle_text = False 
            elif '-->' in line: # skip time codes
                is_subtitle_text = False
            else:
                is_subtitle_text = True # start of the actual text
                if is_subtitle_text:
                    subtitle_text.append(line)

        return ' '.join(subtitle_text)

    except FileNotFoundError:
        print(f"Error: SRT file not found at '{srt_file_path}'")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def process_chapters(chapters, output_dir, VOICE, watermark, chapter_num_start, chapter_num_end, logging, max_chunk_size=10000):
    """
    Processes a subset of chapters, converts them to speech, and validates the output.

    Args:
        chapters (dict): Dictionary of chapter texts.
        output_dir (str): Directory to save output files.
        VOICE (str): The voice model to use for TTS.
        watermark (str): Watermark text to append to each chapter.
        chapter_num_start (int): Starting chapter number.
        chapter_num_end (int): Ending chapter number.
        logging (logging): Logging object.
        max_chunk_size (int): The maximum size (in characters) of each text chunk.
    """
    # Filter chapters based on the specified range
    chapters_sub = {
        chapter_num: content
        for chapter_num, content in chapters.items()
        if chapter_num_start <= chapter_num <= chapter_num_end
    }

    # Process each chapter
    for chapter_num, content in chapters_sub.items():
      
        lines = content.split('\n') # Split by single new line
        chunk_num = 1
        current_chunk = ""

        for line in lines:
            if len(current_chunk) + len(line) + len(watermark) < max_chunk_size:
                current_chunk += line + "\n"
            else:
                TEXT = current_chunk + watermark
                OUTPUT_FILE = f"{output_dir}/{chapter_num}-{chunk_num}.mp3"
                SRT_FILE = f"{output_dir}/{chapter_num}-{chunk_num}.srt"

                # Log chapter length
                logging.info(f"Chapter {chapter_num} chunk {chunk_num} length: {len(current_chunk)} characters")

                # Convert text to speech
                get_audio(TEXT, OUTPUT_FILE, SRT_FILE, VOICE)

                # Validate the watermark in the subtitles
                srt_text = srt_to_text_variable(SRT_FILE)

                watermark_srt = srt_text[-len(watermark) :]

                if watermark_srt == watermark:
                  print(f"{chapter_num}-{chunk_num}: done")
                else:
                  print(f"{chapter_num}-{chunk_num}: incomplete; actual: {watermark_srt}")

                current_chunk = line + "\n"
                chunk_num +=1

        # Process remaining chunk
        if current_chunk:
            TEXT = current_chunk + watermark
            OUTPUT_FILE = f"{output_dir}/{chapter_num}-{chunk_num}.mp3"
            SRT_FILE = f"{output_dir}/{chapter_num}-{chunk_num}.srt"
            # Log chapter length
            logging.info(f"Chapter {chapter_num} chunk {chunk_num} length: {len(current_chunk)} characters")

            # Convert text to speech
            get_audio(TEXT, OUTPUT_FILE, SRT_FILE, VOICE)

            # Validate the watermark in the subtitles
            srt_text = srt_to_text_variable(SRT_FILE)

            watermark_srt = srt_text[-len(watermark) :]

            if watermark_srt == watermark:
                print(f"{chapter_num}-{chunk_num}: done")
            else:
                print(f"{chapter_num}-{chunk_num}: incomplete; actual: {watermark_srt}")