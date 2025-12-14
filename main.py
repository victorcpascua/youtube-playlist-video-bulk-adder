import argparse
import sys
from youtube_client import get_youtube_client, add_video_to_playlist

def main():
    parser = argparse.ArgumentParser(description='Add videos to a YouTube playlist.')
    parser.add_argument('--playlist', help='The ID of the playlist to add videos to.')
    parser.add_argument('--videos', help='Comma-separated list of video IDs to add.')
    
    args = parser.parse_args()
    
    playlist_id = args.playlist
    video_ids_str = args.videos
    
    if not playlist_id:
        playlist_id = input("Enter Playlist ID: ").strip()
        
    if not video_ids_str:
        video_ids_str = input("Enter Video IDs (comma-separated): ").strip()
        
    if not playlist_id or not video_ids_str:
        print("Error: Playlist ID and Video IDs are required.")
        sys.exit(1)
        
    video_ids = [vid.strip() for vid in video_ids_str.split(',') if vid.strip()]
    
    if not video_ids:
        print("Error: No valid video IDs provided.")
        sys.exit(1)
        
    print("Authenticating...")
    try:
        service = get_youtube_client()
    except Exception as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)
        
    print(f"Adding {len(video_ids)} videos to playlist {playlist_id}...")
    
    for video_id in video_ids:
        add_video_to_playlist(service, playlist_id, video_id)
        
    print("Done.")

if __name__ == '__main__':
    main()
