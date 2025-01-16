from deep_translator import GoogleTranslator
import os
import requests
import pandas as pd
from fpdf import FPDF
from urllib.parse import urlparse
from PIL import Image
from config import TRANSLATION_CONFIG

URL = 'https://api.openverse.engineering/v1/images/?format=json&q='

script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
photos_dir = os.path.join(script_dir, "..", "photos")
extras_dir = os.path.join(script_dir, "..", "extras")
font_dir = os.path.join(script_dir, "..", "font")

# Ensure directories exist
os.makedirs(photos_dir, exist_ok=True)
os.makedirs(extras_dir, exist_ok=True)
os.makedirs(font_dir, exist_ok=True)

def get_file_extension(url):
    """Extracts the file extension from a URL."""
    path = urlparse(url).path
    return os.path.splitext(path)[1]  # Get the extension from the URL path

def check_image(file_path):
    """Checks if the file is a valid image."""
    try:
        with Image.open(file_path) as img:
            img.verify()  # Validate the image
        return True
    except (IOError, SyntaxError) as e:
        print(f"Error with image {file_path}: {e}")
        return False

def convert_to_png(input_path, output_path):
    """Converts an image to PNG format."""
    try:
        with Image.open(input_path) as img:
            img.convert('RGBA').save(output_path, 'PNG')
        print(f"Image {input_path} successfully converted to PNG.")
    except Exception as e:
        print(f"Error converting {input_path}: {e}")

def download_photos(search_term):
    """Downloads photos based on a search term."""
    full_url = f"{URL}{search_term}"
    response = requests.get(full_url)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])

        for i, photo in enumerate(results[:2]):
            photo_url = photo.get('thumbnail')

            if not photo_url:
                print(f"Skipped photo {i+1} for query '{search_term}': URL not found.")
                continue

            try:
                file_extension = get_file_extension(photo_url)
                if not file_extension:
                    file_extension = '.jpg'

                photo_response = requests.get(photo_url, timeout=10)

                if photo_response.status_code == 200:
                    photo_path = os.path.join(photos_dir, f"{search_term}_{i+1}{file_extension}")
                    with open(photo_path, 'wb') as file:
                        file.write(photo_response.content)

                    converted_path = os.path.join(photos_dir, f"{search_term}_{i+1}_converted.png")
                    convert_to_png(photo_path, converted_path)
                    os.remove(photo_path)  # Remove the original image

                    print(f'Photo {i+1} for query "{search_term}" successfully downloaded!')
                else:
                    print(f'Failed to download photo {i+1} for query "{search_term}". Code: {photo_response.status_code}')
            except Exception as e:
                print(f'Error downloading photo {i+1} for query "{search_term}": {e}')
    elif response.status_code == 429:
        print("Rate limit exceeded for Openverse API. Please wait.")
    else:
        print(f'Error fetching data from Openverse API: {response.status_code}')

words = []
translated_words = []

def readWordsFromExcel(filename):
    """Reads words from an Excel file."""
    try:
        data = pd.read_excel(filename)
        global words
        collumn = 'RU'
        words = data[collumn]
        words = words.astype(str).tolist()
        print(words)
    except FileNotFoundError:
        print(f"File {filename} not found. Check the path.")
    except Exception as e:
        print(f"Error reading Excel file: {e}")

def translate(input_text):
    """Translates a word."""
    translated = GoogleTranslator(
            source=TRANSLATION_CONFIG['SOURCE'], 
            target=TRANSLATION_CONFIG['TARGET']
        ).translate(input_text)
    translated_words.append(str(translated))

def makePdf(wrd, trans):
    """Creates a PDF with translations and images."""
    pdf = FPDF()

    for i in range(len(wrd)):
        pdf.add_page('L')
        pdf.add_font(family='FreeSerif', fname=os.path.join(font_dir, 'FreeSerif.ttf'), uni=True)
        pdf.set_font("FreeSerif", size=32)

        pdf.cell(200, 60, txt=wrd[i], ln=True, align='L')
        pdf.set_text_color(80, 80, 80)
        pdf.cell(200, 20, txt=trans[i], ln=True, align='L')

        photo1_path = os.path.join(photos_dir, f"{wrd[i]}_1_converted.png")
        photo2_path = os.path.join(photos_dir, f"{wrd[i]}_2_converted.png")

        if os.path.exists(photo1_path) and check_image(photo1_path):
            pdf.image(photo1_path, x=150, y=20, w=100, h=100)
        else:
            print(f"Photo {photo1_path} not found or invalid.")

        if os.path.exists(photo2_path) and check_image(photo2_path):
            pdf.image(photo2_path, x=150, y=100, w=100, h=100)
        else:
            print(f"Photo {photo2_path} not found or invalid.")

    output_path = os.path.join(script_dir, "output.pdf")
    pdf.output(output_path, 'F').encode('latin1')
    print(f"PDF successfully created: {output_path}")

def clearPhotosDirectory():
    """Clears the photos directory."""
    for filename in os.listdir(photos_dir):
        file_path = os.path.join(photos_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

def main():
    excel_path = os.path.join(extras_dir, 'list.xlsx')
    readWordsFromExcel(excel_path)
    for word in words:
        print(f'Processing word: {word}')
        translate(word)
        download_photos(word)

    makePdf(words, translated_words)
    clearPhotosDirectory()
    print('Photos directory cleaned')
    print(words)
    print(translated_words)

if __name__ == '__main__':
    main()
