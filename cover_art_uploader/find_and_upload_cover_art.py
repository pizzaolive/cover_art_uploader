from pathlib import Path
import os
import logging
import base64
from io import BytesIO
import requests
from PIL import Image
import pandas as pd
import mutagen
from cover_art_uploader.parameters import (
    INPUT_FOLDER,
    OUTPUT_IMAGE_SIZE,
    IMGBB_API_KEY,
)

from cover_art_uploader.output import write_info_to_csv


def get_image_file_paths(input_folder):
    file_extensions = ["png", "jpeg"]

    image_paths = []
    for ext in file_extensions:
        image_paths.extend(Path(input_folder).glob(f"**/cover.{ext}"))

    if not image_paths:
        raise ValueError(
            "No images were found, check the INPUT_FOLDER value in parameters.py"
        )

    image_paths_df = pd.DataFrame({"path": image_paths})

    return image_paths_df


def get_album_name_from_music_tag(folder_path):
    song_paths = []
    file_extensions = ["mp3", "flac"]
    for ext in file_extensions:
        song_paths.extend(Path(folder_path).glob(f"*.{ext}"))

    example_song = mutagen.File(song_paths[0])

    try:
        album_name = example_song["TALB"][0]
    except:
        album_name = example_song["album"][0]

    return album_name


def filter_out_duplicate_album_versions(image_paths):
    image_paths = image_paths.copy()

    image_paths["album name"] = (
        image_paths["path"].apply(os.path.dirname).apply(get_album_name_from_music_tag)
    )

    unique_image_paths = image_paths.drop_duplicates(subset="album name")

    return unique_image_paths


def get_base64_image_str(image_path, output_image_size):
    output = BytesIO()
    cover_art = Image.open(image_path).convert("RGB")

    if cover_art.size > output_image_size:
        cover_art = cover_art.resize(output_image_size)

    cover_art.save(output, format="JPEG")
    cover_art_str = base64.b64encode(output.getvalue())

    return cover_art_str


def add_base64_column(images_df):
    images_df = images_df.copy()

    images_df["base64 string"] = images_df["path"].apply(
        get_base64_image_str, output_image_size=OUTPUT_IMAGE_SIZE
    )

    return images_df


def add_upload_url_column(images_df):
    images_df = images_df.copy()

    images_df["upload url"] = images_df["base64 string"].apply(
        upload_image, api_key=IMGBB_API_KEY
    )

    return images_df


def upload_image(resized_image, api_key):
    url = "https://api.imgbb.com/1/upload"
    json_params = {"key": api_key, "image": resized_image}

    try:
        response = requests.post(url, json_params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.exception("POST request failed, skipping image: %s", e)
        return f"Post request failed: {response}"

    response_json = response.json()
    uploaded_image_url = response_json["data"]["url"]

    return uploaded_image_url


def select_columns_for_output(images_df):
    images_filtered = images_df[["album name", "upload url"]]

    return images_filtered


def main():
    logging.basicConfig(level=logging.INFO)

    image_file_paths = get_image_file_paths(INPUT_FOLDER)

    image_upload_info = (
        image_file_paths.pipe(filter_out_duplicate_album_versions)
        .pipe(add_base64_column)
        .pipe(add_upload_url_column)
        .pipe(select_columns_for_output)
    )

    write_info_to_csv(image_upload_info)

    logging.info("Script has ended")


if __name__ == "__main__":
    main()
