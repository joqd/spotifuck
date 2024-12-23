from pathlib import Path

# Get the base directory of the project (two levels up from the current file)
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the path to the SQLite database file
DB_PATH = (BASE_DIR / 'assets/spotifuck.db').as_posix()

# Define the path to the configuration file
CONFIG_PATH = (BASE_DIR / 'assets/configs/config.yaml').as_posix()

# Define download directory
DOWNLOAD_DIR = BASE_DIR / 'assets/files/'