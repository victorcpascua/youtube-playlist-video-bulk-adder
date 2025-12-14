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
