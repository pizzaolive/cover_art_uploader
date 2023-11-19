import pandas as pd
from cover_art_uploader.parameters import OUTPUT_FOLDER
import logging


def write_info_to_csv(output_df):
    if not output_df.empty:
        output_file_path = OUTPUT_FOLDER + "\Cover art upload urls.csv"
        logging.info(f"Writing list of cover art upload URLs to {output_file_path} ...")
        output_df.to_csv(output_file_path, index=False, encoding="utf-8-sig")
    else:
        logging.warning("The table of uploaded URLs is empty, no csv has been saved.")
