"""Interactively download images from a list of URLs then use genai to caption them."""
import click
import download_images
import caption_rename
import pathlib


@click.group()
def cli():
    ...


@cli.command()
@click.option("--input-file", default="images.txt", help="Path to the input file")
@click.option("--output-dir", default="downloads", help="Path to the output directory")
def download(input_file, output_dir):
    download_images.load_then_download(file_path=input_file, target_dir=output_dir)


@cli.command()
@click.option("--input-dir", default="downloads", help="Path to the input directory")
@click.option("--output-dir", default="captions", help="Path to the output directory")
def caption(input_dir, output_dir):
    input_dir = pathlib.Path(input_dir)
    output_dir = pathlib.Path(output_dir)
    caption_rename.caption_and_rename(input_files=input_dir, outputs_dir=output_dir)


@cli.command()
@click.option("--input-file", default="images.txt", help="Path to the input file")
@click.option(
    "--downloads-dir", default="downloads", help="Path to the output directory"
)
@click.option("--output-dir", default="captions", help="Path to the output directory")
def download_and_caption(input_file, downloads_dir, output_dir):
    downloads_dir = pathlib.Path(downloads_dir)
    output_dir = pathlib.Path(output_dir)
    download_images.load_then_download(file_path=input_file, target_dir=downloads_dir)
    caption_rename.caption_and_rename(input_files=downloads_dir, outputs_dir=output_dir)


if __name__ == "__main__":
    cli()
