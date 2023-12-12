import requests
from pathlib import Path


class ProxyDownloader:
    def __init__(self):
        self.requests_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        }
        self.output_path_root = Path(__file__).parents[1] / "data"

    def output_path_namer(self, url):
        output_path = (self.output_path_root / url.split("/")[-1]).with_suffix(".html")
        return output_path

    def download(self, url, output_path=None, overwrite=False):
        if output_path is None:
            output_path = self.output_path_namer(url)

        if not output_path.exists() or overwrite:
            res = requests.get(url, headers=self.requests_headers)
            with open(output_path, "wb") as wf:
                wf.write(res.content)
        else:
            print(f"√ Proxies HTML Existed: {output_path}")

        self.url = url
        self.output_path = output_path
        return output_path
