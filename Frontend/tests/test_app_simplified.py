import unittest
from unittest.mock import patch, MagicMock
import sys
import os

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
        result = app.handle_login("testuser", "testpass")
        
        # Assert
        self.assertIsNone(result)
        mock_get_token.assert_called_once_with("testuser", "testpass")
        mock_st.error.assert_called_once()

    @patch('pages.product_detail.show_product_detail')
    def test_show_product_detail_view(self, mock_show_product_detail):
        """Test product detail view display"""
        # Act
        app.show_product_detail_view()
        
        # Assert
        mock_show_product_detail.assert_called_once_with(1)

    @patch('app.show_product_detail_view')
    def test_main_function_calls_product_detail(self, mock_show_product_detail):
        """Test that main function calls product detail view"""
        # Act
        app.main()
        
        # Assert
        mock_show_product_detail.assert_called_once()
        # Check that page config is set
        mock_st.set_page_config.assert_called_once()


if __name__ == '__main__':
    unittest.main()
