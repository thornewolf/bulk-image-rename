import json
import os
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
import functools
from pathlib import Path

import google.generativeai as genai
from PIL import Image
from retry import retry
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ.get("GENAI_API_KEY"))
_DOWNLOADS_DIR = Path("./downloads")
_OUTPUTS_DIR = Path("./output")


def generate_filename(img: Image):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content(
        [
            """select a descriptive filename for this .jpg
output in json format like
{"filename":"person-holding-a-medal.jpg"}
only respond with json. do not provide any additional content.
a valid FULL response is on the next few examples
{"filename":"person-standing-with-an-apple-in-hand.jpg"}
{"filename":"woman-smiling-wearing-red-dress.jpg"}
{"filename":"unknown.jpg"}""",
            img,
        ],
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0,
            "top_p": 1,
            "top_k": 32,
        },
        stream=True,
    )
    response.resolve()
    result = json.loads(response.text)
    filename = result["filename"]
    return filename


def save_image_to_output_directory(outputs_dir, img, name):
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
        print(f"Created directory {outputs_dir}")
    output_path = outputs_dir / name
    img.save(output_path)


@retry(tries=3, delay=2, backoff=2, max_delay=10, logger=logging.getLogger(__name__))
def process_file_raw(outputs_dir: Path, file_path: Path):
    img = Image.open(file_path)
    name = generate_filename(img).replace(".jpg", "-") + uuid.uuid4().hex[:3] + ".jpg"
    print(f"New name for {file_path} is {name}")
    save_image_to_output_directory(outputs_dir, img, name)


def get_processor_for_dir(outputs_dir):
    return functools.partial(process_file_raw, outputs_dir)


def caption_and_rename(*, input_files: Path, outputs_dir: Path):
    processor = get_processor_for_dir(outputs_dir)
    files = [file for file in input_files.iterdir() if file.is_file()]
    print(files)
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(processor, files)


def main():
    caption_and_rename(input_files=_DOWNLOADS_DIR, outputs_dir=_OUTPUTS_DIR)


if __name__ == "__main__":
    main()
