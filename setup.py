from setuptools import setup

setup(
   name='cover_art_uploader',
   version='1.0',
   description='Upload "cover" images found within directory to imgbb',
   author='pizzaolive',
   packages=['cover_art_uploader'], 
   install_requires=["pandas","Pillow","mutagen"],
)