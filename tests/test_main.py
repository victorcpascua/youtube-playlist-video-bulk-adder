import unittest
from unittest.mock import patch, MagicMock
import sys
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
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_success_interactive(self, mock_print, mock_input, mock_get_client, mock_add_video):
        # Setup
        test_args = ['main.py']
        mock_input.side_effect = ['PL123', 'vid1, vid2']
        mock_service = MagicMock()
        mock_get_client.return_value = mock_service

        with patch.object(sys, 'argv', test_args):
            # Execute
            main()

        # Verify
        self.assertEqual(mock_input.call_count, 2)
        mock_get_client.assert_called_once()
        self.assertEqual(mock_add_video.call_count, 2)

    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_args_no_input(self, mock_exit, mock_print):
        # Setup
        test_args = ['main.py']
        with patch.object(sys, 'argv', test_args):
            with patch('builtins.input', return_value=''):
                # Execute
                main()

        # Verify
        mock_exit.assert_called_with(1)

    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_empty_videos(self, mock_exit, mock_print):
        # Setup
        test_args = ['main.py', '--playlist', 'PL123', '--videos', '']
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
