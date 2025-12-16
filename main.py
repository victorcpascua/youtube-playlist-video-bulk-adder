import argparse
import sys
import os
import csv

from src.youtube_client import get_youtube_client, add_video_to_playlist
from src.utils import extract_video_id

def read_videos_from_csv(file_path):
    video_ids = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                for item in row:
                    if item.strip():
                        video_ids.append(extract_video_id(item.strip()))
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)
    return video_ids

def main():
    parser = argparse.ArgumentParser(description='Add videos to a YouTube playlist.')
    parser.add_argument('--playlist', help='The ID of the playlist to add videos to.')
    parser.add_argument('--videos', help='Comma-separated list of video IDs to add.')
    parser.add_argument('--file', help='Path to a CSV file containing video IDs.')
    
    args = parser.parse_args()
    
    playlist_id = args.playlist
    video_ids = []
    
    if args.videos:
        video_ids = [extract_video_id(vid.strip()) for vid in args.videos.split(',') if vid.strip()]
    elif args.file:
        print(f"Reading videos from {args.file}...")
        video_ids = read_videos_from_csv(args.file)
    elif os.path.exists('videos.csv'):
        print("Found videos.csv, reading videos from it...")
        video_ids = read_videos_from_csv('videos.csv')
    
    if not playlist_id:
        playlist_id = input("Enter Playlist ID: ").strip()
        
    if not video_ids:
        video_ids_str = input("Enter Video IDs (comma-separated): ").strip()
        video_ids = [extract_video_id(vid.strip()) for vid in video_ids_str.split(',') if vid.strip()]
        
    if not playlist_id or not video_ids:
        print("Error: Playlist ID and Video IDs are required.")
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
