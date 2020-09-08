from pathlib import Path

from bs4 import BeautifulSoup
from src.scraper import scrap_course


import pytest

BASE_DIR = Path(__file__).resolve(strict=True).parent

def test_scrap_course():
    with open(Path(BASE_DIR, "../css.html")) as f:
        soup = BeautifulSoup(f, 'html.parser')
        courses = soup.find_all("table")
        for c in courses:
            scrap_course(c, f"a[name^=\"css\"]", "AUT", "2019", None)
            break

