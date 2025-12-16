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

from unittest.mock import patch, mock_open
from src.utils import read_videos_from_csv
import sys

class TestReadVideosFromCsv(unittest.TestCase):
    @patch('builtins.print')
    @patch('sys.exit')
    def test_read_csv_success(self, mock_exit, mock_print):
        # Setup
        csv_content = "vid1,https://youtu.be/vid2\nvid3"
        with patch('builtins.open', mock_open(read_data=csv_content)):
            # Execute
            ids = read_videos_from_csv('dummy.csv')
            
        # Verify
        self.assertEqual(ids, ['vid1', 'vid2', 'vid3'])
        mock_exit.assert_not_called()

    @patch('builtins.print')
    @patch('sys.exit')
    def test_read_csv_empty(self, mock_exit, mock_print):
        # Setup
        with patch('builtins.open', mock_open(read_data="")):
            # Execute
            ids = read_videos_from_csv('dummy.csv')
            
        # Verify
        self.assertEqual(ids, [])
        mock_exit.assert_not_called()

    @patch('builtins.print')
    @patch('sys.exit')
    def test_read_csv_error(self, mock_exit, mock_print):
        # Setup
        mock_exit.side_effect = SystemExit
        with patch('builtins.open', side_effect=Exception("Read error")):
            # Execute
            with self.assertRaises(SystemExit):
                read_videos_from_csv('dummy.csv')
                
        # Verify
        mock_exit.assert_called_with(1)
