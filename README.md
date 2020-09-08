

# Usage

`poetry shell`

`python3 src/main.py`

Modify the variables in `src/main.py` to change which department, what years, what campus, etc is scraped.

```python
# Default values 
SEASONS = ["AUTUMN", "WINTER", "SPRING"]
YEARS = ["2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
DEPARTMENT = "CSS"
CAMPUS = "Bothell"
OUTPUT_FILE = "courses.json"
```

# Setup

Install [poetry](https://python-poetry.org/).

Install [pyenv](https://github.com/pyenv/pyenv).

Install `Python 3.8.4` using `pyenv`.


Run the following commands:

```
pyenv local 3.8.4
poetry install
```

