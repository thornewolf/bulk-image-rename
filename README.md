# Bulk Image Rename

Bulk Image Rename is a simple, yet powerful command-line utility that allows you to rename and caption multiple images in bulk. This tool is designed to be easy to use and efficient for handling large collections of images. It leverages Google's Gemini LLM to provide accurate and contextually relevant captions for images.

## Features

- Download images from URLs.
- Automatically caption images using Google's Gemini LLM.
- Rename images in bulk using these captions.
- Supports various image formats.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/thornewolf/bulk-image-rename.git
cd bulk-image-rename
```

Before using the tool, install the necessary dependencies with Poetry:

```bash
poetry install
```

## Setup

Before using Bulk Image Rename, create a `.env` file in the root directory of this project with the following variable:

```
GENAI_API_KEY=... # Obtain your key from https://makersuite.google.com/app/apikey
```

This repo Google's Gemini API for image captioning.

## Usage

Prepare an `images.txt` file listing the URLs of the images you wish to process. The file should be formatted similarly to the following example:

```
https://placekitten.com/200/300
https://placekitten.com/200/287
https://placekitten.com/200/284
```

### Downloading Images

To download images:

```bash
poetry run python bulk_image_rename/cli.py download --input-file images.txt --output-dir downloads
```

Where:
- `--input-file` specifies the input file containing the image URLs.
- `--output-dir` defines the directory where the images will be saved.

### Captioning Images

To caption images in a directory:

```bash
poetry run python bulk_image_rename/cli.py caption --input-dir downloads
```

Where:
- `--input-dir` specifies the directory containing the images to be captioned.

### Downloading and Captioning Images

To download images from a URL list and then automatically caption them:

```bash
poetry run python bulk_image_rename/cli.py download-and-caption --input-file images.txt --downloads-dir temp_downloads --output-dir final_output
```

Where:
- `--input-file` specifies the input file containing the image URLs.
- `--downloads-dir` defines the temporary directory where images will be downloaded.
- `--output-dir` defines the final directory where captioned and renamed images will be saved.

## Example

Given the following `images.txt`:

```
https://placekitten.com/200/300
https://placekitten.com/200/287
https://placekitten.com/200/284
```

And running the command:

```bash
poetry run python bulk_image_rename/cli.py download-and-caption --input-file images.txt --downloads-dir temp_downloads --output-dir captioned_kittens
```

The images will be downloaded to the `temp_downloads` directory, captioned, and then saved in the `captioned_kittens` directory with their new names and captions.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.