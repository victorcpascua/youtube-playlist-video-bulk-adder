from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .auth import get_authenticated_service

def get_youtube_client():
    """Builds and returns the YouTube service."""
    creds = get_authenticated_service()
    service = build('youtube', 'v3', credentials=creds)
    return service

def add_video_to_playlist(service, playlist_id, video_id):
    """Adds a video to a playlist."""
    try:
        request = service.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        response = request.execute()
        print(f"Added video {video_id} to playlist {playlist_id}")
        return response
    except HttpError as e:
        print(f"An error occurred adding video {video_id}: {e}")
        return None
