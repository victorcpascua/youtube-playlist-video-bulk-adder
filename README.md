# Youtube Playlist Video Bulk Adder

A simple Python console application to batch add videos to a YouTube playlist using the YouTube Data API v3.

## Features

-   Add multiple videos to a playlist at once.
-   Simple command-line interface.
-   OAuth 2.0 authentication.

## Prerequisites

1.  **Python 3.6+**
2.  **Google Cloud Project** with **YouTube Data API v3** enabled.
3.  **OAuth 2.0 Credentials** (`client_secret.json`) for a Desktop Application.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/youtube-playlist-video-bulk-adder.git
    cd youtube-playlist-video-bulk-adder
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Place your `client_secret.json` file in the project root directory.

## Preparation

Before running the script, you need two things:

1.  **Playlist ID**:
    *   Create a new playlist on YouTube (or use an existing one).
    *   Open the playlist in your browser.
    *   The URL will look like `https://www.youtube.com/playlist?list=PLxxxxx...`
    *   The **Playlist ID** is the part after `list=`. For example, if the URL is `https://www.youtube.com/playlist?list=PL12345ABCDE_ASF5614SDF`, the ID is `PL12345ABCDE_ASF5614SDF`.

2.  **Video IDs**:
    *   You need a list of video IDs you want to add.
    *   A video ID is the part of the YouTube URL after `v=`.
    *   For example, in `https://www.youtube.com/watch?v=dQw4w9WgXcQ`, the ID is `dQw4w9WgXcQ`.
    *   Prepare your list as comma-separated values (e.g., `dQw4w9WgXcQ,as2a4w9Wgd54,9WgXcQasd94a`).

## Extracting Videos from "Watch Later"

If you are looking to move videos from your **Watch Later** playlist (which is not accessible via the YouTube API), we have prepared a specific guide for that.

Check out [WATCH_LATER_EXTRACTION.md](WATCH_LATER_EXTRACTION.md) to learn how to:
1.  Extract video IDs using a browser script.
2.  Convert the data to CSV.
3.  Filter and prepare the IDs for this tool.

## Usage

```bash
python3 main.py --playlist <PLAYLIST_ID> --videos <VIDEO_ID_1>,<VIDEO_ID_2>,...
```

Or run interactively:
```bash
python3 main.py
```

## Quota Warning

> [!WARNING]
> **YouTube Data API v3 Quota Limit**
>
> The free tier of the YouTube Data API has a daily quota limit of **10,000 units**.
> Each video addition (`playlistItems.insert`) costs **50 units**.
>
> This means you can add a maximum of **200 videos per day** with the free quota.
> If you exceed this limit, you will receive a `quotaExceeded` error and will have to wait until the next day (Pacific Time) for the quota to reset.

## Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) (if applicable) and check the issue templates before submitting a pull request.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
