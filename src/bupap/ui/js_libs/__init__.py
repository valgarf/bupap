from pathlib import Path

FOLDER = Path(__file__).parent.absolute()

minified = True
if minified:
    PATH_LUXON = FOLDER / "luxon.min.js"
else:
    PATH_LUXON = FOLDER / "luxon.js"
