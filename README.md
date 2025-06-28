![Python](https://img.shields.io/badge/Python-3.12-blue) ![License](https://img.shields.io/badge/License-MIT-green)

# Spotifuck

A Python-based Telegram bot built with Aiogram that allows users to download songs from Spotify, SoundCloud, and YouTube. The bot leverages powerful libraries like yt-dlp for YouTube downloads and spotDL for Spotify track fetching, ensuring fast and accurate results.


## Requirements
You need to install ffmpeg tool.
```
$ sudo apt update && apt install -y ffmpeg
```

## Installation
1. Clone the repository.
```
$ git clone https://github.com/joqd/spotifuck.git && cd spotifuck
```
2. Install dependencies:
```
$ pip install -r requirements.txt
```
3. Update the configuration file with your bot token and other required settings:
```bash
$ cp config-example.yaml config.yaml
$ nano config.yaml
```
4. Run the bot
```
$ python3 -m app
# or
$ make run
```

## Contributions
Feel free to contribute by submitting pull requests or reporting issues.

## License
This project is licensed under the MIT License.
