# Cover art uploader

# What does this script do?
This script is intended to be used on a directory containing music albums, each containing a cover art image.
It searches through the given directory and sub-directories, and finds any jpeg or png images named "cover". It then resizes these images to a smaller format if they are larger than the specified output size (default is 750x750), and uploads them to https://imgbb.com/. 

The script then outputs a csv file with a table of albums and asscociated direct image URLs.

If there are multiple albums with different file versions, or multiple *Disk* folders within an album, only one cover art image will be uploaded, **assuming that the songs are correctly tagged**.

## Prerequisites
* You must have Python installed: https://www.python.org/downloads/windows/
* You must have an account with https://imgbb.com/ in order to get an API key and upload images

## Setting up the script

1. Git clone the script, or download the repository to wherever you like.
2. Update the values in [parameters.py](cover_art_uploader\parameters.py). 
    * IMGBB_API_KEY: Your API key from https://imgbb.com/
        * Log in to your account, click *About* in the top left, then *API*.
        * If there is no key, click *Add API key*, then copy this.
    * INPUT_FOLDER: the parent directory that contains albums.
    * OUTPUT_FOLDER: the directory in which the output csv file containing the upload URLs should be saved.
    * OUTPUT_IMAGE_SIZE: optional, as the default is already set to 750x750

## Running the script
1. Navigate into the folder: either use a terminal to CD into the folder, or open the folder in Windows explorer -> select the address bar -> type cmd
2. Type `pip install .` - this should use setup and install the modules required (pandas, Pillow and mutagen)
2. Type `python -m cover_art_uploader.find_and_upload_cover_art`