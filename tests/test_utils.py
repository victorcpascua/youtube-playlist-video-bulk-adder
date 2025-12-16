import unittest
from src.utils import extract_video_id

class TestExtractVideoId(unittest.TestCase):
    def test_extract_standard_url(self):
        url = "https://www.youtube.com/watch?v=VIDEO_ID123"
        self.assertEqual(extract_video_id(url), "VIDEO_ID123")
        
    def test_extract_standard_url_with_params(self):
        url = "https://www.youtube.com/watch?v=VIDEO_ID123&list=PL123&index=1"
        self.assertEqual(extract_video_id(url), "VIDEO_ID123")
        
    def test_extract_short_url(self):
        url = "https://youtu.be/VIDEO_ID123"
        self.assertEqual(extract_video_id(url), "VIDEO_ID123")
        
    def test_extract_plain_id(self):
        vid = "VIDEO_ID123"
        self.assertEqual(extract_video_id(vid), "VIDEO_ID123")
        
    def test_extract_empty(self):
        self.assertEqual(extract_video_id(""), "")
        self.assertEqual(extract_video_id(None), "")

    def test_extract_non_youtube_url(self):
        # Should return as is if implementation assumes it's an ID, 
        # or maybe we want to be strict?
        # Current implementation: "Assume it's a raw video ID if no URL pattern matches"
        url = "https://example.com/foo"
        self.assertEqual(extract_video_id(url), "https://example.com/foo")
