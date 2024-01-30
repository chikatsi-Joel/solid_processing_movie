from setuptools import setup, find_packages

setup(
    name='gradi_app',
    author = "Chikatsi Joel",
    author_email="kappachikatsi@gmail.com",
    packages=find_packages(),
    version="1.4.6",
    url = "https://github.com/chikatsi-Joel/solid_processing_movie.git",
    install_requires=[
        "PyQt5",
        "moviepy",
        "googletrans",
        "qfluentwidgets",
        "pysrt"
    ],
    license="GPLv3",
    project_url = [
        "https://github.com/chikatsi-Joel/solid_processing_movie.git"
    ]
)
