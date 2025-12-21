import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
from main import main

class TestMain(unittest.TestCase):
    @patch('main.add_video_to_playlist')
    @patch('main.get_youtube_client')
    @patch('builtins.print')
    def test_main_success_args(self, mock_print, mock_get_client, mock_add_video):
        # Setup
        test_args = ['main.py', '--playlist', 'dQw4w9WgXcQ', '--videos', '97w4w9WgXcQ,dQw4w9WgXcQ']
        mock_service = MagicMock()
        mock_get_client.return_value = mock_service

        with patch.object(sys, 'argv', test_args):
            # Execute
            main()

        # Verify
        mock_get_client.assert_called_once()
        self.assertEqual(mock_add_video.call_count, 2)
        mock_add_video.assert_any_call(mock_service, 'dQw4w9WgXcQ', '97w4w9WgXcQ')
        mock_add_video.assert_any_call(mock_service, 'dQw4w9WgXcQ', 'dQw4w9WgXcQ')

    @patch('main.add_video_to_playlist')
    @patch('main.get_youtube_client')
    @patch('builtins.print')
    @patch('main.read_videos_from_csv')
    def test_main_success_file_arg(self, mock_read_csv, mock_print, mock_get_client, mock_add_video):
        # Setup
        test_args = ['main.py', '--playlist', 'dQw4w9WgXcQ', '--file', 'my_videos.csv']
        mock_service = MagicMock()
        mock_get_client.return_value = mock_service
        
        mock_read_csv.return_value = ['97w4w9WgXcQ', 'dQw4w9WgXcQ']
        
        with patch.object(sys, 'argv', test_args):
            # Execute
            main()

        # Verify
        mock_get_client.assert_called_once()
        mock_read_csv.assert_called_with('my_videos.csv')
        self.assertEqual(mock_add_video.call_count, 2)
        mock_add_video.assert_any_call(mock_service, 'dQw4w9WgXcQ', '97w4w9WgXcQ')
        mock_add_video.assert_any_call(mock_service, 'dQw4w9WgXcQ', 'dQw4w9WgXcQ')

    @patch('main.add_video_to_playlist')
    @patch('main.get_youtube_client')
    @patch('builtins.print')
    @patch('os.path.exists')
    @patch('main.read_videos_from_csv')
    def test_main_success_default_csv(self, mock_read_csv, mock_exists, mock_print, mock_get_client, mock_add_video):
        # Setup
        test_args = ['main.py', '--playlist', 'dQw4w9WgXcQ']
        mock_service = MagicMock()
        mock_get_client.return_value = mock_service
        mock_exists.side_effect = lambda p: p == 'videos.csv'
        
        mock_read_csv.return_value = ['97w4w9WgXcQ', 'dQw4w9WgXcQ']
        
        with patch.object(sys, 'argv', test_args):
            # Execute
            main()

        # Verify
        mock_get_client.assert_called_once()
        mock_read_csv.assert_called_with('videos.csv')
        self.assertEqual(mock_add_video.call_count, 2)
        mock_add_video.assert_any_call(mock_service, 'dQw4w9WgXcQ', '97w4w9WgXcQ')
        mock_add_video.assert_any_call(mock_service, 'dQw4w9WgXcQ', 'dQw4w9WgXcQ')

    @patch('main.add_video_to_playlist')
    @patch('main.get_youtube_client')
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('os.path.exists')
    def test_main_success_interactive(self, mock_exists, mock_print, mock_input, mock_get_client, mock_add_video):
        # Setup
        test_args = ['main.py']
        mock_input.side_effect = ['dQw4w9WgXcQ', '97w4w9WgXcQ, dQw4w9WgXcQ']
        mock_service = MagicMock()
        mock_get_client.return_value = mock_service
        mock_exists.return_value = False

        with patch.object(sys, 'argv', test_args):
            # Execute
            main()

        # Verify
        self.assertEqual(mock_input.call_count, 2)
        mock_get_client.assert_called_once()
        self.assertEqual(mock_add_video.call_count, 2)

    @patch('builtins.print')
    @patch('sys.exit')
    @patch('os.path.exists')
    def test_main_no_args_no_input(self, mock_exists, mock_exit, mock_print):
        # Setup
        test_args = ['main.py']
        mock_exists.return_value = False
        with patch.object(sys, 'argv', test_args):
            with patch('builtins.input', return_value=''):
                # Execute
                main()

        # Verify
        mock_exit.assert_called_with(1)
        
    @patch('main.get_youtube_client')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_auth_failure(self, mock_exit, mock_print, mock_get_client):
        # Setup
        test_args = ['main.py', '--playlist', 'dQw4w9WgXcQ', '--videos', '97w4w9WgXcQ']
        mock_get_client.side_effect = Exception("Auth failed")
        mock_exit.side_effect = SystemExit

        with patch.object(sys, 'argv', test_args):
            # Execute
            with self.assertRaises(SystemExit):
                main()

        # Verify
        mock_exit.assert_called_with(1)

    @patch('main.add_video_to_playlist')
    @patch('main.get_youtube_client')
    @patch('builtins.print')
    def test_main_success_url_args(self, mock_print, mock_get_client, mock_add_video):
        # Setup
        # Use full URL and a short URL
        test_args = ['main.py', '--playlist', 'dQw4w9WgXcQ', '--videos', 'https://www.youtube.com/watch?v=97w4w9WgXcQ, https://youtu.be/dQw4w9WgXcQ']
        mock_service = MagicMock()
        mock_get_client.return_value = mock_service

        with patch.object(sys, 'argv', test_args):
            # Execute
            main()

        # Verify
        mock_get_client.assert_called_once()
        self.assertEqual(mock_add_video.call_count, 2)
        mock_add_video.assert_any_call(mock_service, 'dQw4w9WgXcQ', '97w4w9WgXcQ')
        mock_add_video.assert_any_call(mock_service, 'dQw4w9WgXcQ', 'dQw4w9WgXcQ')

