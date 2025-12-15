import os
import pickle
import unittest
from unittest.mock import patch, MagicMock
from src.auth import get_authenticated_service

class TestAuth(unittest.TestCase):
    @patch('src.auth.InstalledAppFlow')
    @patch('src.auth.Request')
    @patch('src.auth.pickle')
    @patch('src.auth.os.path.exists')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_get_authenticated_service_existing_token(self, mock_open, mock_exists, mock_pickle, mock_request, mock_flow):
        # Setup
        mock_exists.side_effect = lambda p: p.endswith('token.pickle')
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_pickle.load.return_value = mock_creds

        # Execute
        creds = get_authenticated_service()

        # Verify
        self.assertEqual(creds, mock_creds)
        mock_pickle.load.assert_called_once()

    @patch('src.auth.InstalledAppFlow')
    @patch('src.auth.Request')
    @patch('src.auth.pickle')
    @patch('src.auth.os.path.exists')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_get_authenticated_service_expired_token_refresh(self, mock_open, mock_exists, mock_pickle, mock_request, mock_flow):
        # Setup
        mock_exists.side_effect = lambda p: p.endswith('token.pickle')
        mock_creds = MagicMock()
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.refresh_token = True
        mock_pickle.load.return_value = mock_creds

        # Execute
        creds = get_authenticated_service()

        # Verify
        self.assertEqual(creds, mock_creds)
        mock_creds.refresh.assert_called_once()

    @patch('src.auth.InstalledAppFlow')
    @patch('src.auth.Request')
    @patch('src.auth.pickle')
    @patch('src.auth.os.path.exists')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_get_authenticated_service_new_login(self, mock_open, mock_exists, mock_pickle, mock_request, mock_flow):
        # Setup
        # token.pickle does not exist, client_secret.json exists
        mock_exists.side_effect = lambda p: p.endswith('client_secret.json')
        
        mock_flow_instance = MagicMock()
        mock_flow.from_client_secrets_file.return_value = mock_flow_instance
        mock_creds = MagicMock()
        mock_flow_instance.run_local_server.return_value = mock_creds

        # Execute
        creds = get_authenticated_service()

        # Verify
        self.assertEqual(creds, mock_creds)
        mock_flow.from_client_secrets_file.assert_called_once()
        mock_flow_instance.run_local_server.assert_called_once()
        mock_pickle.dump.assert_called_once()

    @patch('src.auth.os.path.exists')
    def test_get_authenticated_service_no_secret(self, mock_exists):
        # Setup
        mock_exists.return_value = False

        # Execute & Verify
        with self.assertRaises(FileNotFoundError):
            get_authenticated_service()
