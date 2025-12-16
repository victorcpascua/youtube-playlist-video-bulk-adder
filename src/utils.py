from urllib.parse import urlparse, parse_qs

import csv
import sys

def extract_video_id(input_str: str) -> str:
    """
    Extracts the video ID from a YouTube URL or returns the input if it's already an ID.
    
    Args:
        input_str (str): The input string which could be a URL or a video ID.
        
    Returns:
        str: The extracted video ID.
    """
    if not input_str:
        return ""
        
    parsed_url = urlparse(input_str)
    
    # Handle standard URLs: https://www.youtube.com/watch?v=VIDEO_ID
    if "youtube.com" in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        if "v" in query_params:
            return query_params["v"][0]
            
    # Handle short URLs: https://youtu.be/VIDEO_ID
    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/")
        
    # Assume it's a raw video ID if no URL pattern matches
    return input_str

def read_videos_from_csv(file_path: str) -> list[str]:
    """
    Reads video IDs/URLs from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        list[str]: List of extracted video IDs.
    """
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
