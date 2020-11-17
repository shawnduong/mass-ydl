# Open Source Wins!

Due to a recent [victory](https://github.com/github/dmca/blob/e00bfb544e93bfd3066fe1699171964dd2dc29e0/2020/11/2020-11-16-RIAA-reversal-effletter.pdf) for youtube-dl, the script that mass-ytdl is dependent on, this project is up and running again!

# mass-ytdl

A mass youtube-dl script for downloading large quantities of music with metadata. Requires Python, youtube-dl, ffmpeg, and xlrd.

## Usage

1. Copy `TEMPLATE.xlsx` and give the copied file a new name.
2. Fill out the spreadsheet with the appropriate information.
3. Run `./mass-ytdl.py <SPREADSHEET>` to download all the items.
