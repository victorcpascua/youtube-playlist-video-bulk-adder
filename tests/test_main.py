import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
from main import main

class TestMain(unittest.TestCase):
    @patch('main.add_video_to_playlist')
    @patch('main.get_youtube_client')
    @patch('builtins.print')
    def test_main_success_args(self, mock_print, mock_get_client, mock_add_video):
        # Setup
        test_args = ['main.py', '--playlist', 'PL123', '--videos', 'vid1,vid2']
        mock_service = MagicMock()
        mock_get_client.return_value = mock_service

        with patch.object(sys, 'argv', test_args):
            # Execute
            main()

        # Verify
        mock_get_client.assert_called_once()
        self.assertEqual(mock_add_video.call_count, 2)
        mock_add_video.assert_any_call(mock_service, 'PL123', 'vid1')
        mock_add_video.assert_any_call(mock_service, 'PL123', 'vid2')

    @patch('main.add_video_to_playlist')
    @patch('main.get_youtube_client')
    @patch('builtins.print')
    def test_main_success_file_arg(self, mock_print, mock_get_client, mock_add_video):
        # Setup
        test_args = ['main.py', '--playlist', 'PL123', '--file', 'my_videos.csv']
        mock_service = MagicMock()
        mock_get_client.return_value = mock_service
        
        csv_content = "vid1,vid2"
        with patch.object(sys, 'argv', test_args):
            with patch('builtins.open', mock_open(read_data=csv_content)):
                # Execute
                main()

        # Verify
        mock_get_client.assert_called_once()
        self.assertEqual(mock_add_video.call_count, 2)
        mock_add_video.assert_any_call(mock_service, 'PL123', 'vid1')
        mock_add_video.assert_any_call(mock_service, 'PL123', 'vid2')

    @patch('main.add_video_to_playlist')
    @patch('main.get_youtube_client')
    @patch('builtins.print')
    @patch('os.path.exists')
    def test_main_success_default_csv(self, mock_exists, mock_print, mock_get_client, mock_add_video):
        # Setup
        test_args = ['main.py', '--playlist', 'PL123']
        mock_service = MagicMock()
        mock_get_client.return_value = mock_service
        mock_exists.side_effect = lambda p: p == 'videos.csv'
        
        csv_content = "vid1\nvid2"
        with patch.object(sys, 'argv', test_args):
            with patch('builtins.open', mock_open(read_data=csv_content)):
                # Execute
                main()

        # Verify
        mock_get_client.assert_called_once()
        self.assertEqual(mock_add_video.call_count, 2)
        mock_add_video.assert_any_call(mock_service, 'PL123', 'vid1')
        mock_add_video.assert_any_call(mock_service, 'PL123', 'vid2')

    @patch('main.add_video_to_playlist')
    @patch('main.get_youtube_client')
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('os.path.exists')
    def test_main_success_interactive(self, mock_exists, mock_print, mock_input, mock_get_client, mock_add_video):
        # Setup
        test_args = ['main.py']
        mock_input.side_effect = ['PL123', 'vid1, vid2']
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
        test_args = ['main.py', '--playlist', 'PL123', '--videos', 'vid1']
        mock_get_client.side_effect = Exception("Auth failed")
        mock_exit.side_effect = SystemExit

        with patch.object(sys, 'argv', test_args):
            # Execute
            with self.assertRaises(SystemExit):
                main()

        # Verify
        mock_exit.assert_called_with(1)
