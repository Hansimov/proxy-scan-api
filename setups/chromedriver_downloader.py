import os
import requests
import zipfile
from DrissionPage.easy_set import set_paths
from pathlib import Path


class ChromedriverDownloader:
    def __init__(self):
        self.url = "https://chromedriver.storage.googleapis.com/114.0.5735.16/chromedriver_linux64.zip"
        self.requests_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        }
        self.output_path = Path(__file__).parents[1] / "chromedriver.zip"
        self.unzip_path = Path(__file__).parents[1]
        self.chromedriver_executable_path = self.unzip_path / "chromedriver"

    def download(self, overwrite=False):
        if self.chromedriver_executable_path.exists() and not overwrite:
            print(f"> chromedriver exists: {self.chromedriver_executable_path}")
            return
        if self.output_path.exists() and not overwrite:
            print(f"> Chromedriver.zip exists: {self.output_path}")
            return
        res = requests.get(self.url, headers=self.requests_headers)
        with open(self.output_path, "wb") as wf:
            wf.write(res.content)
        print(f"> Download chromedriver to: {self.output_path}")

    def unzip(self, overwrite=False):
        if self.chromedriver_executable_path.exists() and not overwrite:
            print(f"> chromedriver exists: {self.chromedriver_executable_path}")
            return
        with zipfile.ZipFile(self.output_path, "r") as rf:
            rf.extractall(self.unzip_path)

    def chmod_executable(self):
        os.chmod(self.chromedriver_executable_path, 666)

    def add_to_path(self):
        set_paths(
            browser_path=self.chromedriver_executable_path,
            local_port=9555,
        )

    def remove_files(self):
        files_to_remove = ["LICENSE.chromedriver"]
        for file in files_to_remove:
            file_fullpath = self.unzip_path / file
            if file_fullpath.exists():
                print(f"> Removing {file}")
                os.remove(file_fullpath)

    def run(self):
        self.download()
        self.unzip()
        self.chmod_executable()
        self.add_to_path()
        self.remove_files()


if __name__ == "__main__":
    downloader = ChromedriverDownloader()
    downloader.run()
