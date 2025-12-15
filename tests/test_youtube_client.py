import unittest
from unittest.mock import patch, MagicMock
from googleapiclient.errors import HttpError
from src.youtube_client import get_youtube_client, add_video_to_playlist

class TestYoutubeClient(unittest.TestCase):
    @patch('src.youtube_client.build')
    @patch('src.youtube_client.get_authenticated_service')
    def test_get_youtube_client(self, mock_get_auth, mock_build):
        # Setup
        mock_creds = MagicMock()
        mock_get_auth.return_value = mock_creds
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        # Execute
        service = get_youtube_client()

        # Verify
        self.assertEqual(service, mock_service)
        mock_get_auth.assert_called_once()
        mock_build.assert_called_once_with('youtube', 'v3', credentials=mock_creds)

    def test_add_video_to_playlist_success(self):
        # Setup
        mock_service = MagicMock()
        mock_request = MagicMock()
        mock_response = {'id': 'playlist_item_id'}
        
        mock_service.playlistItems().insert.return_value = mock_request
        mock_request.execute.return_value = mock_response

        # Execute
        response = add_video_to_playlist(mock_service, 'playlist_id', 'video_id')

        # Verify
        self.assertEqual(response, mock_response)
        mock_service.playlistItems().insert.assert_called_once()

    def test_add_video_to_playlist_error(self):
        # Setup
        mock_service = MagicMock()
        mock_request = MagicMock()
        
        mock_service.playlistItems().insert.return_value = mock_request
        error_response = MagicMock()
        error_response.status = 404
        mock_request.execute.side_effect = HttpError(error_response, b'Error')

        # Execute
        response = add_video_to_playlist(mock_service, 'playlist_id', 'video_id')

        # Verify
        self.assertIsNone(response)
