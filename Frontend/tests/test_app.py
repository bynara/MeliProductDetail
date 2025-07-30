import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add the parent directory to the path so we can import from the main app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock streamlit before importing the app
mock_st = MagicMock()
sys.modules['streamlit'] = mock_st

# Import after mocking streamlit
import app


class TestApp(unittest.TestCase):
    """Test cases for main app functionality"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Reset streamlit mock
        mock_st.reset_mock()
        
        # Set up session state mock
        mock_st.session_state = {}
        
        # Replace the streamlit import in the app module
        app.st = mock_st

    @patch('app.get_token')
    def test_handle_login_success(self, mock_get_token):
        """Test successful login handling"""
        # Arrange
        mock_get_token.return_value = "test_token_123"
        
        # Act
        result = app.handle_login("testuser", "testpass")
        
        # Assert
        self.assertEqual(result, "test_token_123")
        mock_get_token.assert_called_once_with("testuser", "testpass")
        mock_st.error.assert_not_called()

    @patch('app.get_token')
    def test_handle_login_failure(self, mock_get_token):
        """Test login handling with authentication failure"""
        # Arrange
        mock_get_token.side_effect = Exception("Authentication failed")
        
        # Act
        result = app.handle_login("invalid_user", "invalid_pass")
        
        # Assert
        self.assertIsNone(result)
        mock_st.error.assert_called_once_with("An error occurred: Authentication failed")

    @patch('app.show_product_detail_view')
    def test_process_login_success(self, mock_show_product_detail_view):
        """Test successful login process"""
        # Arrange
        with patch('app.handle_login') as mock_handle_login:
            mock_handle_login.return_value = "test_token"
            
            # Act
            app.process_login()
            
            # Assert
            mock_handle_login.assert_called_once_with("testuser", "testpass")
            self.assertTrue(mock_st.session_state['logged_in'])
            self.assertEqual(mock_st.session_state['token'], "test_token")
            self.assertTrue(mock_st.session_state['show_product_detail'])
            mock_show_product_detail_view.assert_called_once()

    @patch('app.handle_login')
    def test_process_login_failure(self, mock_handle_login):
        """Test login process with authentication failure"""
        # Arrange
        mock_handle_login.return_value = None
        
        # Act
        app.process_login()
        
        # Assert
        mock_handle_login.assert_called_once_with("testuser", "testpass")
        # Session state should not be updated on failure
        self.assertNotIn('logged_in', mock_st.session_state)
        self.assertNotIn('token', mock_st.session_state)

    @patch('app.handle_login')
    def test_process_login_false_result(self, mock_handle_login):
        """Test login process with false result"""
        # Arrange
        mock_handle_login.return_value = False
        
        # Act
        app.process_login()
        
        # Assert
        mock_st.error.assert_called_once_with("Login failed")

    def test_show_product_detail_view(self):
        """Test product detail view display"""
        # Mock the import of pages.product_detail
        with patch('builtins.__import__') as mock_import:
            mock_product_detail = MagicMock()
            mock_import.return_value = mock_product_detail
            mock_product_detail.product_detail.show_product_detail = MagicMock()
            
            # Act
            app.show_product_detail_view()
            
            # The function should attempt to import and call show_product_detail
            # We can't easily test the exact call due to the dynamic import,
            # but we can verify the function runs without error
            # Test passes if no exception is raised

    @patch('app.process_login')
    def test_main_not_logged_in(self, mock_process_login):
        """Test main function when user is not logged in"""
        # Arrange
        mock_st.session_state = {'logged_in': False}
        
        # Act
        app.main()
        
        # Assert
        mock_st.set_page_config.assert_called_once_with(
            page_title="Product Detail MeLi", 
            page_icon="assets/icon.png"
        )
        mock_process_login.assert_called_once()

    @patch('app.show_product_detail_view')
    def test_main_logged_in_show_product_detail(self, mock_show_product_detail_view):
        """Test main function when user is logged in and should show product detail"""
        # Arrange
        mock_st.session_state = {
            'logged_in': True,
            'show_product_detail': True,
            'token': 'test_token'
        }
        
        # Act
        app.main()
        
        # Assert
        mock_show_product_detail_view.assert_called_once()

    @patch('app.show_product_detail_view')
    @patch('app.process_login')
    def test_main_logged_in_no_product_detail(self, mock_process_login, mock_show_product_detail_view):
        """Test main function when user is logged in but shouldn't show product detail"""
        # Arrange
        mock_st.session_state = {
            'logged_in': True,
            'show_product_detail': False,
            'token': 'test_token'
        }
        
        # Act
        app.main()
        
        # Assert
        mock_process_login.assert_not_called()
        mock_show_product_detail_view.assert_not_called()

    def test_main_initializes_session_state(self):
        """Test that main function properly initializes session state"""
        # Arrange
        mock_st.session_state = {}
        
        # Act
        with patch('app.process_login'):
            app.main()
        
        # Assert
        self.assertFalse(mock_st.session_state['logged_in'])
        self.assertIsNone(mock_st.session_state['token'])

    def test_main_preserves_existing_session_state(self):
        """Test that main function preserves existing session state"""
        # Arrange
        mock_st.session_state = {
            'logged_in': True,
            'token': 'existing_token',
            'show_product_detail': True
        }
        
        # Act
        with patch('app.show_product_detail_view'):
            app.main()
        
        # Assert
        self.assertTrue(mock_st.session_state['logged_in'])
        self.assertEqual(mock_st.session_state['token'], 'existing_token')
        self.assertTrue(mock_st.session_state['show_product_detail'])


if __name__ == '__main__':
    unittest.main()
