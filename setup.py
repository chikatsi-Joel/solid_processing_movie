from setuptools import setup, find_packages

setup(
    name='gradi_app',
    version='1.0.0',
    author = "Chikatsi Joel",
    packages=find_packages(),
    install_requires=[
        "PyQt5",
        "moviepy",
        "googletrans",
        "whisper_timestamped",
        "qfluentwidgets",
        "pysrt"
    ],
    license = "MIT"
)
