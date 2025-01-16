# Translation and Image Integration Project

This project automates the process of translating words, retrieving related images, and creating a visually rich PDF document. It is ideal for language learners, educators, or anyone looking to create compelling multilingual materials with images.

## Features

1. **Word Translation**: 🌐
   - Reads words from an Excel file.
   - Automatically translates words using the [Deep Translator](https://github.com/nidhaloff/deep-translator) library.

2. **Image Retrieval**: 🖼️
   - Searches for related images on the Openverse API.
   - Downloads and converts images to PNG format.

3. **PDF Generation**: 📄
   - Combines words, translations, and images into a well-formatted PDF.
   - Uses custom fonts for multilingual support.

4. **Directory Management**: 📁
   - Ensures the proper structure of directories for photos, fonts, and additional resources.
   - Automatically clears the photo directory after PDF creation.

## Requirements

- Python 3.7 or higher 🐍
- Required Python libraries:
  ```
  deep-translator
  requests
  pandas
  fpdf
  pillow
  ```
- Font file (`FreeSerif.ttf`) for Unicode character support.

## Directory Structure

```
project-root/
|
├── photos/         # Directory for downloaded and converted images
├── extras/         # Directory for the Excel file
├── font/           # Directory for custom fonts
├── config.py       # Configuration file for source and target languages
└── main.py         # Main script
```

## Configuration

Update `config.py` to set the source and target languages: 🌍
```python
TRANSLATION_CONFIG = {
    'source': 'auto',  # Source language (use 'auto' for auto-detection)
    'target': 'no'     # Target language (e.g., 'no' for Norwegian)
}
```

## Usage

1. Ensure all directories (`photos`, `extras`, `font`) are properly set up. ✅
2. Place your word list in `list.xlsx` under the `extras` directory.
3. Run the script: ▶️
   ```bash
   python main.py
   ```
4. Find the generated PDF (`output.pdf`) in the project root.

## Error Handling

- If the Excel file is missing or has incorrect formatting, the script will notify you. ⚠️
- The script handles rate limits from the Openverse API and informs you when to retry.
- Invalid or missing images are skipped, and appropriate messages are displayed.

## Future Improvements

- Add support for multiple source/target languages in one run. 🔄
- Integrate additional image sources for broader coverage. 🌟
- Improve error handling and logging. 🛡️

## License

This project is licensed under the MIT License. 📜

## Acknowledgments

- [Deep Translator](https://github.com/nidhaloff/deep-translator) for seamless translation. 🌐
- [Openverse API](https://api.openverse.engineering/) for image resources. 🖼️
- [FPDF](http://www.fpdf.org/) for PDF generation. 📄

