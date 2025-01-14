import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def try_get_text_from_url(url: str) -> str | None:
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")

            for script in soup(["script, style"]):
                script.extract()
            
            text = soup.get_text()
                # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            return text.encode('utf-8')
    except HTTPError:
        return None