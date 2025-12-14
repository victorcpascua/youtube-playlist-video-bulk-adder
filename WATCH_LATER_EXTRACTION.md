# How to extract videos from the "Watch Later" playlist

This project was originally born from the need to clean up the YouTube "Watch Later" playlist. Unfortunately, **the YouTube API does not allow programmatic access to this playlist**, so a manual process is required to extract the videos.

> [!NOTE]
> Special thanks to [MichaelCade](https://github.com/MichaelCade/youtube-watch-later-mess), as the original idea for this method came from his repository.

## Extraction Steps

### 1. Get the Video JSON

To start, you need to extract the video information directly from the browser:

1.  Go to your **Watch Later** playlist on YouTube.
2.  Scroll to the bottom of the list to ensure **all videos are loaded**.
3.  Open **Developer Tools** (F12 or Right Click -> Inspect).
4.  Go to the **Console** tab.
5.  Paste and run the following code (this code will extract the necessary data):

```javascript
async function scrollAndExtractVideosWithDebug() {
    let prevVideoCount = 0;

    // Scroll until all videos are loaded
    while (true) {
        window.scrollTo(0, document.documentElement.scrollHeight);
        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for new content to load

        // Count the number of loaded videos
        let videos = document.querySelectorAll('ytd-playlist-video-renderer');
        console.log(`Videos loaded: ${videos.length}`);

        if (videos.length === prevVideoCount) break; // Exit if no new videos loaded
        prevVideoCount = videos.length;
    }

    console.log(`Finished scrolling! Total videos detected: ${prevVideoCount}`);

    // Extract video data
    let videoElements = Array.from(document.querySelectorAll('ytd-playlist-video-renderer'));
    let data = videoElements.map((video, index) => {
        let number = video.querySelector('#index-container')?.textContent.trim() || '#';
        let chanel = video.querySelector('.ytd-channel-name')?.textContent.trim() || '#';
        let title = video.querySelector('#video-title')?.textContent.trim() || 'Unknown Title';
        let link = video.querySelector('#video-title')?.href || '#';
        let ariaLabel = video.querySelector('h3')?.getAttribute('aria-label') || '';
        let videoInfo = video.querySelector('#video-info')?.textContent.trim() || '';
        let progress = video.querySelector('#progress')?.style || '0';
        return { index: number, title, chanel, link, ariaLabel, videoInfo, progress };
    });

    console.log(`Extracted ${data.length} videos.`);
    console.log(data);
    return data;
}

scrollAndExtractVideosWithDebug();
```

### 2. Convert JSON to CSV

Once you have the JSON generated from the previous step:

1.  Copy the JSON result.
2.  Go to the [Konklone JSON to CSV tool](https://konklone.io/json/).
3.  Paste the JSON and download the generated CSV file.

### 3. Filter and Clean in Excel

1.  Open the CSV file in Excel (or Google Sheets).
2.  Filter and clean the list as you wish (e.g., removing videos you've already watched or aren't interested in).
3.  Once you have the final list of videos you want to keep/move:
    *   Extract only the **Video ID** column.
    *   Convert that column into a **comma-separated list**.

Done! Now you have the IDs ready to use with this script and add them to another playlist.
