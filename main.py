from util import load_config, extract_chapters, process_chapters
import os
import logging


def main():
    """Main function to orchestrate the script."""
    # Load configuration
    config = load_config("config.yml")
    epub_path = config["epub"]["file"]
    mode=config["mode"]

    # Extract chapters from the EPUB file   
    chapters = extract_chapters(epub_path)

    if mode==1:
        # Set up logging to a file
        logging.basicConfig(filename='logfile.log', level=logging.INFO)

        logging.info("Extracted chapters: %s", list(chapters.keys()))
    
    else:
        # Load configuration
        output_dir = config["out"]["path"]
        chapter_num_start = config["out"]['chapter']["start"]
        chapter_num_end = config["out"]['chapter']["end"]
        voice = config["out"]["voice"] # Load voice
        watermark = config["out"]["watermark"] # Load watermark

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Process a subset of chapters
        process_chapters(chapters, output_dir, voice, watermark, chapter_num_start, chapter_num_end) # Pass voice and watermark


if __name__ == "__main__":
    main()