from ..abstract_logic.abstract_download import abstract_download
from pytube import YouTube


class download_on_youtube(abstract_download) :
    def __init__(
        self,
        url_video : str,
        url_destination : str | None,
        file_name  : str
    ) :
        self.url_video = url_video
        self.url_destination = url_destination
        self.file_name = file_name

    def download_file(self) -> str:
        youtube = YouTube(url = self.url_video)
        youtube = youtube.streams.get_lowest_resolution()
        path = youtube.download(
            self.url_destination,
            self.file_name + '.mp4'
        )

        return path
    