import subprocess
from pathlib import Path


def start_scrapy(url, classes):
    subprocess.call(
        ['scrapy', 'crawl', 'generic_crawler', "-a", f"url={url}", "-a", f"classes={classes}"],
        cwd=Path(__file__).resolve().parent.parent / "diploma_crawler"
    )
