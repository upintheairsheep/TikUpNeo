TikUp Neo
=====

An updated auto downloader and uploader for TikTok videos.


Note: TikTok-Api is currently broken, meaning that that TikUpNeo will not work until the issues get fixed. tiktok-scraper also broke at the same time.

**Requirements**  
[TikTok-Api](https://github.com/davidteather/TikTok-Api), [internetarchive](https://archive.org/services/docs/api/internetarchive/index.html), [yt-dlp](https://github.com/yt-dlp/yt-dlp), and [playwright](https://github.com/Microsoft/playwright-python) on Python 3.

**How to Install**  
Install with `pip install tikup`.
Update with `pip install -U tikup`.

**How to Use**
```
usage: tikup [-h] [--no-delete] [--hashtag] [--limit LIMIT] [--use-download-archive] [--id] [--liked]
             [--folder FOLDER] [--no-upload]
             user

An auto downloader and uploader for TikTok videos.

positional arguments:
  user

optional arguments:
  -h, --help            show this help message and exit
  --no-delete           don't delete files once uploaded to the Internet Archive
  --hashtag             download this hashtag
  --limit LIMIT         set limit on amount of TikToks to download
  --use-download-archive
                        record the video url to the download archive. This will download only videos not listed in the
                        archive file. Record the IDs of all downloaded videos in it.
  --id                  download this video ID
  --liked               download this user's liked posts
  --folder FOLDER       set download destination (default: ~/.tikup)
  --no-upload           turn off uploading to the Internet Archive
```

**Internet Archive upload**

To interact with the Internet Archive, you will first need to [create an IA account](https://archive.org/account/login.createaccount.php).

Confirm your account and note down your email address and password.

Then run `ia configure` and log in.

**Changes from TikTok-Api**

- Updated TikTok-Api functions to 4.0+ from the dated 3.1.4 version.
- Changed downloader from the now inactive youtube-dl to yt-dlp, which is more active, and supports watermark-free downloads
- Changed tiktok-info json from info to info_full.
- Added IA upload and Changes section

**Credits**

Original TikUp by Coloradohusky. Dear Coloradohusky, I hate you for deleting the original TikUp and InstaUp, then blocking me when I ask why.

Special thanks to osmaelo for forking TikUp's latest version before it's death
