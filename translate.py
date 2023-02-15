# Import required libraries and modules.
import os
import json
from dotenv import load_dotenv

from bs4 import BeautifulSoup
from bs4.element import NavigableString
import boto3

# Load environment variables from .env file.
load_dotenv()

# Set base directory and directories for html and translated html files.
base_dir = "./"
html_dir = os.path.join(base_dir, "web/html")
translated_html_dir = os.path.join(base_dir, "web/translated_html")

# Create translated_html_dir directory if it does not exist.
if not os.path.exists(translated_html_dir):
    os.makedirs(translated_html_dir)

# Set path for translation history file.
translation_history_path = os.path.join(base_dir, "translations.json")

# Check if translation history file exists
# If not, create an empty file with "{}" as contents
# If yes, load contents of the file into translation_history dict.
translation_history = dict()
if not os.path.exists(translation_history_path):
    with open(translation_history_path, "w") as f:
        f.write("{}")
else:
    with open(translation_history_path, "r") as f:
        translation_history = json.load(f)

# Set source language and target language codes.
source_language = "en"
target_language = "hi"

# Create an Amazon Translate client.
translate_api = boto3.client(
    service_name="translate",
    region_name=os.environ.get("REGION_NAME", ""),
    use_ssl=True,
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", ""),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
)


def translate_texts(texts):
    """
    Translates the input texts and replaces the original text content in HTML
    with the translated text.
    The function also updates the translation history dict
    with the newly translated text.
    """
    for original, cleaned_up in texts:
        if cleaned_up in translation_history:
            translated_text = translation_history[cleaned_up]
        else:
            res = translate_api.translate_text(
                Text=cleaned_up,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language,
            )
            translated_text = res.get("TranslatedText")
            translation_history[cleaned_up] = translated_text
        print(cleaned_up, "-->", translated_text)
        original.replace_with(translated_text)


def clean_up(text):
    """
    Removes any unnecessary spaces and next lines from a given text.
    """
    return " ".join(text.strip().replace("\n", " ").split())


def remove_empty_texts(texts):
    """
    Remove empty texts from a list of texts.
    """
    return [
        (original, cleaned_up)
        for original, cleaned_up in texts
        if cleaned_up != ""
    ]


def translate_html(html_file):
    """
    Opens an HTML file and iterates through each tag within it.
    For each tag, the text content is extracted
    and the `translate_texts` function is applied to it.
    The updated content is then saved in a new HTML file.
    After processing all the tags,
    the translation history file is also updated.
    """
    try:
        with open(os.path.join(html_dir, html_file), "r") as f:
            html_content = f.read()
            soup = BeautifulSoup(html_content, "html.parser")
            for i in soup.find_all():
                texts = remove_empty_texts(
                    [
                        (content, clean_up(content))
                        for content in i.contents
                        if type(content) == NavigableString
                    ]
                )
                if texts:
                    translate_texts(texts)
            with open(os.path.join(translated_html_dir, html_file), "w") as f:
                f.write(soup.prettify())
                print(f"[ HTML file {html_file} ---> Done. ]")
    except Exception as e:
        print("ERROR :", str(e))
    finally:
        with open(translation_history_path, "w") as f:
            json.dump(translation_history, f)
            print(
                f"[ translation history at size: {len(translation_history)} ]"
            )


# Loops through each file in the directory specified by html_dir
# Applies the translate_html function to it, which translates the text content
# Saves the modified HTML file with the translated text."
for html_file in os.listdir(os.path.join(html_dir)):
    translate_html(html_file)
