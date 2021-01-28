# Installation

```pip install -r requirements.txt```

# Build Instructions

```pyinstaller --onefile -w .\mscrape.py```

# Running

```python mscrape.py```

--- or ---

double-click the exe you made in ```.\dist\mscrape\

# Created Files

Two files are created by default:

- scraper.ini
  - This will contain the saved path (default is the path of the exe or .py file)
- archive.txt
  - this will save the ids of videos you've previously downloaded, so they cannot be downloaded again
